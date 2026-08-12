"""
=================================================================
  IDPS Simulation -- Presentation Format
  Rules: Location | Offset | Scope | Pattern (binary / regex)
  Supports && (AND) between multiple conditions per rule
=================================================================

How it works:
  1. Each packet is split into layers: IPv4 Header, TCP Header, HTTP Payload, etc.
  2. Each rule has one or more CONDITIONS connected by AND (&&).
  3. Each condition specifies:
       Location → which layer to look in
       Offset   → how many bytes to skip from the start
       Scope    → how many bytes to read (or "all")
       Pattern  → binary string OR /regex/ to match against
  4. The engine checks every rule against every packet and reports matches.
"""

import re
import struct

# ─────────────────────────────────────────────────────────────────
# ANSI colors for nice terminal output
# ─────────────────────────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


# ═════════════════════════════════════════════════════════════════
# SECTION 1 — PACKET BUILDER
# ═════════════════════════════════════════════════════════════════

def build_ipv4_header(src_ip: str, dst_ip: str, protocol: int = 6) -> bytes:
    """
    Build a minimal 20-byte IPv4 header.

    IPv4 Header layout (bytes):
      0-1  : version + IHL + TOS + total length (4 bytes)
      4-7  : ID + flags + fragment offset (4 bytes)
      8-11 : TTL + protocol + checksum (4 bytes)
      12-15: Source IP  ← Offset 12
      16-19: Destination IP ← Offset 16
    """
    version_ihl = 0x45          # version=4, header length=5×4=20 bytes
    tos         = 0
    total_len   = 40
    ident       = 0
    flags_frag  = 0
    ttl         = 64
    checksum    = 0

    header = struct.pack('!BBHHHBBH',
                         version_ihl, tos, total_len,
                         ident, flags_frag,
                         ttl, protocol, checksum)

    src_bytes = bytes(int(x) for x in src_ip.split('.'))
    dst_bytes = bytes(int(x) for x in dst_ip.split('.'))
    return header + src_bytes + dst_bytes


def build_tcp_header(src_port: int, dst_port: int, flags: int = 0x02) -> bytes:
    """
    Build a minimal 20-byte TCP header.

    TCP Header layout (bytes):
      0-1  : Source Port  ← Offset 0
      2-3  : Destination Port ← Offset 2
      4-7  : Sequence Number
      8-11 : Acknowledgment Number
      12   : Data Offset + Reserved
      13   : FLAGS byte ← Offset 13
               bit 0 = FIN, bit 1 = SYN, bit 2 = RST,
               bit 3 = PSH, bit 4 = ACK, bit 5 = URG
      14-15: Window Size
      16-17: Checksum
      18-19: Urgent Pointer
    """
    data_offset = 0x50          # 5 (no options) → 5×4=20 bytes
    window      = 65535
    checksum    = 0
    urgent      = 0
    seq         = 0
    ack_num     = 0

    return struct.pack('!HHIIBBHHH',
                       src_port, dst_port,
                       seq, ack_num,
                       data_offset, flags,
                       window, checksum, urgent)


def build_udp_header(src_port: int, dst_port: int) -> bytes:
    """
    Build an 8-byte UDP header.

    UDP Header layout (bytes):
      0-1: Source Port ← Offset 0
      2-3: Destination Port ← Offset 2
      4-5: Length
      6-7: Checksum
    """
    length   = 8
    checksum = 0
    return struct.pack('!HHHH', src_port, dst_port, length, checksum)


def make_packet(src_ip: str    = "192.168.1.10",
                dst_ip: str    = "8.8.8.8",
                proto: str     = "tcp",
                src_port: int  = 54321,
                dst_port: int  = 80,
                tcp_flags: int = 0x02,
                payload: str   = "") -> dict:
    """
    Assemble a packet as a dictionary of layers.
    Each layer maps to its raw bytes — ready for rule inspection.
    """
    ipv4 = build_ipv4_header(src_ip, dst_ip,
                              protocol=6 if proto == "tcp" else 17)
    layers = {"IPv4 Header": ipv4}

    if proto == "tcp":
        layers["TCP Header"] = build_tcp_header(src_port, dst_port, tcp_flags)
    elif proto == "udp":
        layers["UDP Header"] = build_udp_header(src_port, dst_port)

    if payload:
        layers["HTTP Payload"] = payload.encode()

    return {
        "meta": {
            "src_ip":   src_ip,
            "dst_ip":   dst_ip,
            "proto":    proto.upper(),
            "src_port": src_port,
            "dst_port": dst_port,
            "flags":    bin(tcp_flags) if proto == "tcp" else "N/A",
            "payload":  payload[:40] + "..." if len(payload) > 40 else payload,
        },
        "layers": layers,
    }


# ═════════════════════════════════════════════════════════════════
# SECTION 2 — PATTERN MATCHING ENGINE
# ═════════════════════════════════════════════════════════════════

def bytes_to_bin(data: bytes) -> str:
    """Convert bytes to a binary string: b'\xcb\x20' → '1100101100100000'"""
    return ''.join(format(b, '08b') for b in data)


def bytes_to_ip(data: bytes) -> str:
    """Convert 4 bytes to dotted IP string: b'\x01\x01\x01\x05' → '1.1.1.5'"""
    return '.'.join(str(b) for b in data)


def match_pattern(data: bytes, pattern: str, location: str) -> tuple:
    """
    Returns (matched: bool, explanation: str)

    Pattern types:
      Binary string  → "1100101100100000"   exact bit comparison
      Regex string   → "/[a-z]irus[2-8]/"   applied to decoded content
    """
    if pattern.startswith('/') and pattern.endswith('/'):
        # ── Regex pattern ──────────────────────────────────────────
        regex = pattern[1:-1]

        # For IP addresses → convert bytes to "x.x.x.x" string
        if "IPv4" in location and len(data) == 4:
            text = bytes_to_ip(data)
        else:
            # Try UTF-8 decode for payloads
            try:
                text = data.decode('utf-8', errors='replace')
            except Exception:
                text = data.hex()

        match = re.search(regex, text)
        if match:
            return True, f"regex '{regex}' -> matched '{match.group()}' in '{text}'"
        return False, f"regex '{regex}' -> no match in '{text}'"

    else:
        # ── Binary pattern ─────────────────────────────────────────
        data_bin = bytes_to_bin(data)
        if data_bin == pattern:
            return True, f"binary {data_bin} == {pattern}"
        return False, f"binary {data_bin} != {pattern}"


def check_condition(packet_layers: dict, condition: dict) -> tuple:
    """
    Extract the relevant bytes from the packet using:
      location, offset, scope
    Then match against the pattern.
    """
    location = condition["location"]
    offset   = condition["offset"]
    scope    = condition["scope"]
    pattern  = condition["pattern"]

    layer = packet_layers.get(location)
    if layer is None:
        return False, f"layer '{location}' not present in packet"

    # Extract bytes
    if scope == "all":
        data = layer[offset:]
    else:
        data = layer[offset: offset + scope]

    if not data:
        return False, f"no data at offset={offset}, scope={scope} in '{location}'"

    matched, explanation = match_pattern(data, pattern, location)
    return matched, explanation


# ═════════════════════════════════════════════════════════════════
# SECTION 3 — RULES (Presentation examples + extras)
# ═════════════════════════════════════════════════════════════════

RULES = [

    # ──────────────────────────────────────────────────────────────
    # Rule 1 — TCP Destination Port 52,000  (presentation example 1)
    # ──────────────────────────────────────────────────────────────
    {
        "id":   1,
        "name": "TCP Destination Port 52,000",
        "desc": "Catches any TCP packet aimed at port 52,000",
        "conditions": [
            {
                "location": "TCP Header",
                "offset":   2,          # bytes 2-3 = destination port
                "scope":    2,
                "pattern":  "1100101100100000",  # 52000 in binary
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # Rule 2 — TCP SYN + PSH flags  (presentation example 2)
    # ──────────────────────────────────────────────────────────────
    {
        "id":   2,
        "name": "TCP Flags: SYN + PSH active",
        "desc": "Catches TCP packets where both SYN (bit1) and PSH (bit3) are set",
        "conditions": [
            {
                "location": "TCP Header",
                "offset":   13,         # byte 13 = flags byte
                "scope":    1,
                "pattern":  "00001010", # SYN=2 + PSH=8 = 10 = 00001010
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # Rule 3 — Source IP range 1.1.1.1–1.1.1.25  (presentation example 3)
    # ──────────────────────────────────────────────────────────────
    {
        "id":   3,
        "name": "Source IP 1.1.1.1 – 1.1.1.25",
        "desc": "Catches packets coming from the IP range 1.1.1.1 to 1.1.1.25",
        "conditions": [
            {
                "location": "IPv4 Header",
                "offset":   12,         # bytes 12-15 = source IP
                "scope":    4,
                "pattern":  "/^1\\.1\\.1\\.([1-9]|1[0-9]|2[0-5])$/",
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # Rule 4 — HTTP Payload with XirusY  (presentation example 4, improved)
    # Two conditions connected by && :
    #   condition 1 → payload contains [a-z]irus[2-8]
    #   condition 2 → destination IP is 192.168.1.100 (target server)
    # ──────────────────────────────────────────────────────────────
    {
        "id":   4,
        "name": "HTTP Payload XirusY -> target server 192.168.1.100",
        "desc": ("Catches HTTP packets to 192.168.1.100 whose payload "
                 "matches [a-z]irus[2-8]  (example: virus3, xirus7)"),
        "conditions": [
            {
                # condition 1 — search payload
                "location": "HTTP Payload",
                "offset":   0,
                "scope":    "all",
                "pattern":  "/[a-z]irus[2-8]/",
            },
            {
                # condition 2 — destination IP must be 192.168.1.100
                "location": "IPv4 Header",
                "offset":   16,         # bytes 16-19 = destination IP
                "scope":    4,
                "pattern":  "/^192\\.168\\.1\\.100$/",
            },
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # Bonus Rule 5 — Exercise 2: Source IP 192.168.127.5–155
    # ──────────────────────────────────────────────────────────────
    {
        "id":   5,
        "name": "Source IP 192.168.127.5 – 192.168.127.155",
        "desc": "Catches packets from IP range 192.168.127.5 to 192.168.127.155",
        "conditions": [
            {
                "location": "IPv4 Header",
                "offset":   12,
                "scope":    4,
                "pattern":  "/^192\\.168\\.127\\.([5-9]|[1-9][0-9]|1[0-4][0-9]|15[0-5])$/",
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # Bonus Rule 6 — Exercise 3: TCP from port 80 with SYN flag
    # Two conditions: source port == 80  &&  SYN flag set
    # ──────────────────────────────────────────────────────────────
    {
        "id":   6,
        "name": "TCP Source Port 80 AND SYN flag",
        "desc": "Catches TCP packets from port 80 that have SYN set",
        "conditions": [
            {
                "location": "TCP Header",
                "offset":   0,          # bytes 0-1 = source port
                "scope":    2,
                "pattern":  "0000000001010000",  # 80 in binary
            },
            {
                "location": "TCP Header",
                "offset":   13,
                "scope":    1,
                "pattern":  "00000010",  # SYN only = 2 = 00000010
            },
        ]
    },

]


# ═════════════════════════════════════════════════════════════════
# SECTION 4 — IDPS ENGINE
# ═════════════════════════════════════════════════════════════════

def run_idps(packet: dict, rules: list) -> list:
    """
    Check a packet against all rules.
    A rule fires only when ALL its conditions match (AND / &&).
    Returns list of fired rule dicts (with match details).
    """
    fired = []
    layers = packet["layers"]

    for rule in rules:
        results   = []
        all_match = True

        for cond in rule["conditions"]:
            matched, explanation = check_condition(layers, cond)
            results.append({
                "location":    cond["location"],
                "offset":      cond["offset"],
                "scope":       cond["scope"],
                "pattern":     cond["pattern"],
                "matched":     matched,
                "explanation": explanation,
            })
            if not matched:
                all_match = False

        if all_match:
            fired.append({"rule": rule, "details": results})

    return fired


# ═════════════════════════════════════════════════════════════════
# SECTION 5 — DISPLAY HELPERS
# ═════════════════════════════════════════════════════════════════

def print_packet(idx: int, packet: dict):
    m = packet["meta"]
    flags_val = m.get("flags", "N/A")
    print(f"\n{BOLD}{CYAN}{'-'*60}{RESET}")
    print(f"{BOLD}[Packet #{idx}]{RESET}")
    print(f"{'-'*60}")
    print(f"  Protocol : {m['proto']}")
    print(f"  Src      : {m['src_ip']}:{m['src_port']}")
    print(f"  Dst      : {m['dst_ip']}:{m['dst_port']}")
    if m["proto"] == "TCP":
        print(f"  TCP Flags: {flags_val}")
    if m.get("payload"):
        print(f"  Payload  : \"{m['payload']}\"")


def print_rule_result(fired_rules: list, total_rules: int):
    if not fired_rules:
        print(f"  {GREEN}[OK] No rules matched -- packet is CLEAN{RESET}")
        return

    print(f"  {RED}[ALERT] {len(fired_rules)}/{total_rules} rule(s) fired!{RESET}")
    for item in fired_rules:
        rule = item["rule"]
        print(f"\n  {BOLD}{RED}  >> Rule #{rule['id']}: {rule['name']}{RESET}")
        print(f"     {rule['desc']}")
        print(f"     Conditions ({len(item['details'])} total -- all must match):")
        for i, d in enumerate(item["details"], 1):
            icon = "PASS" if d["matched"] else "FAIL"
            color = GREEN if d["matched"] else RED
            print(f"       {color}[{icon}] Condition {i}{RESET}")
            print(f"            Location : {d['location']}")
            print(f"            Offset   : {d['offset']}  |  "
                  f"Scope : {d['scope']}")
            print(f"            Pattern  : {d['pattern']}")
            print(f"            Result   : {d['explanation']}")


# ═════════════════════════════════════════════════════════════════
# SECTION 6 — TEST PACKETS
# ═════════════════════════════════════════════════════════════════

TEST_PACKETS = [

    # ── Packet 1 ─────────────────────────────────────────────────
    # Expected: Rule 1 fires (dest port 52000)
    make_packet(
        src_ip="192.168.1.10", dst_ip="8.8.8.8",
        proto="tcp", src_port=54321, dst_port=52000,
        tcp_flags=0x02,   # SYN
    ),

    # ── Packet 2 ─────────────────────────────────────────────────
    # Expected: Rule 2 fires (SYN + PSH = flags 0x0A)
    make_packet(
        src_ip="10.0.0.5", dst_ip="10.0.0.1",
        proto="tcp", src_port=5000, dst_port=80,
        tcp_flags=0x0A,   # SYN=2 + PSH=8 = 10 = 0x0A
    ),

    # ── Packet 3 ─────────────────────────────────────────────────
    # Expected: Rule 3 fires (source IP 1.1.1.17 → in range 1.1.1.1–25)
    make_packet(
        src_ip="1.1.1.17", dst_ip="192.168.1.1",
        proto="tcp", src_port=12345, dst_port=443,
    ),

    # ── Packet 4 ─────────────────────────────────────────────────
    # Expected: Rule 4 fires (payload has "virus3", dst IP = 192.168.1.100)
    make_packet(
        src_ip="10.10.10.10", dst_ip="192.168.1.100",
        proto="tcp", src_port=44444, dst_port=8080,
        payload="HTTP/1.1 200 OK\r\nContent: virus3 detected in file",
    ),

    # ── Packet 5 ─────────────────────────────────────────────────
    # Expected: Rule 4 does NOT fire (payload matches but dst IP is wrong)
    make_packet(
        src_ip="10.10.10.10", dst_ip="192.168.1.200",   # wrong server!
        proto="tcp", src_port=44444, dst_port=8080,
        payload="HTTP/1.1 200 OK\r\nContent: virus3 detected",
    ),

    # ── Packet 6 ─────────────────────────────────────────────────
    # Expected: Rule 5 fires (source IP 192.168.127.99 in range 5–155)
    make_packet(
        src_ip="192.168.127.99", dst_ip="10.0.0.1",
        proto="tcp", src_port=9999, dst_port=22,
    ),

    # ── Packet 7 ─────────────────────────────────────────────────
    # Expected: Rule 6 fires (source port 80, SYN flag)
    make_packet(
        src_ip="93.184.216.34", dst_ip="192.168.1.5",
        proto="tcp", src_port=80, dst_port=54000,
        tcp_flags=0x02,   # SYN
    ),

    # ── Packet 8 ─────────────────────────────────────────────────
    # Expected: CLEAN — nothing matches
    make_packet(
        src_ip="172.16.0.1", dst_ip="8.8.8.8",
        proto="tcp", src_port=9999, dst_port=443,
        tcp_flags=0x18,   # ACK + PSH
    ),

]


# ═════════════════════════════════════════════════════════════════
# SECTION 7 — MAIN
# ═════════════════════════════════════════════════════════════════

def main():
    print(f"\n{BOLD}{'='*60}")
    print("  IDPS Simulation -- Presentation Format")
    print(f"{'='*60}{RESET}")
    print(f"  Rules loaded    : {len(RULES)}")
    print(f"  Packets to check: {len(TEST_PACKETS)}")
    print()

    # Print rule summary
    print(f"{BOLD}{YELLOW}[Active Rules]{RESET}")
    for rule in RULES:
        cond_count = len(rule["conditions"])
        print(f"  Rule #{rule['id']}: {rule['name']}  "
              f"[{cond_count} condition{'s' if cond_count > 1 else ''} / "
              f"{'&&' if cond_count > 1 else 'single'}]")

    # Process each packet
    total_alerts = 0
    for idx, packet in enumerate(TEST_PACKETS, 1):
        print_packet(idx, packet)
        fired = run_idps(packet, RULES)
        print_rule_result(fired, len(RULES))
        if fired:
            total_alerts += 1

    # Summary
    print(f"\n{BOLD}{'='*60}")
    print("  SIMULATION COMPLETE")
    print(f"{'='*60}{RESET}")
    print(f"  Packets checked : {len(TEST_PACKETS)}")
    print(f"  {RED}Alerts fired    : {total_alerts}{RESET}")
    print(f"  {GREEN}Clean packets   : {len(TEST_PACKETS) - total_alerts}{RESET}")
    print()


if __name__ == "__main__":
    main()
