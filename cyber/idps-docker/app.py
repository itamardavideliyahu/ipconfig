"""
IDPS Simulation — Web Interface (Flask)
Students open the browser, build a packet, and see which rules fire.
"""

import re
import struct
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ═══════════════════════════════════════════════════════════════
# IDPS ENGINE  (same logic as idps_simulation.py)
# ═══════════════════════════════════════════════════════════════

def build_ipv4_header(src_ip, dst_ip, protocol=6):
    version_ihl = 0x45
    tos = 0
    total_len = 40
    ident = flags_frag = checksum = 0
    ttl = 64
    header = struct.pack('!BBHHHBBH',
                         version_ihl, tos, total_len,
                         ident, flags_frag, ttl, protocol, checksum)
    src = bytes(int(x) for x in src_ip.split('.'))
    dst = bytes(int(x) for x in dst_ip.split('.'))
    return header + src + dst


def build_tcp_header(src_port, dst_port, flags=0x02):
    return struct.pack('!HHIIBBHHH',
                       src_port, dst_port, 0, 0,
                       0x50, flags, 65535, 0, 0)


def build_udp_header(src_port, dst_port):
    return struct.pack('!HHHH', src_port, dst_port, 8, 0)


def make_packet(src_ip, dst_ip, proto, src_port, dst_port,
                tcp_flags=0x02, payload=""):
    ipv4 = build_ipv4_header(src_ip, dst_ip,
                              protocol=6 if proto == "tcp" else 17)
    layers = {"IPv4 Header": ipv4}
    if proto == "tcp":
        layers["TCP Header"] = build_tcp_header(src_port, dst_port, tcp_flags)
    elif proto == "udp":
        layers["UDP Header"] = build_udp_header(src_port, dst_port)
    if payload:
        layers["HTTP Payload"] = payload.encode()
    return layers


def bytes_to_bin(data):
    return ''.join(format(b, '08b') for b in data)


def bytes_to_ip(data):
    return '.'.join(str(b) for b in data)


def match_pattern(data, pattern, location):
    if pattern.startswith('/') and pattern.endswith('/'):
        regex = pattern[1:-1]
        if "IPv4" in location and len(data) == 4:
            text = bytes_to_ip(data)
        else:
            text = data.decode('utf-8', errors='replace')
        m = re.search(regex, text)
        if m:
            return True, f"Regex matched '{m.group()}' in '{text}'"
        return False, f"Regex '{regex}' did not match '{text}'"
    else:
        data_bin = bytes_to_bin(data)
        if data_bin == pattern:
            return True, f"{data_bin} == {pattern}"
        return False, f"{data_bin} != {pattern}"


def check_condition(layers, cond):
    layer = layers.get(cond["location"])
    if layer is None:
        return False, f"Layer '{cond['location']}' not in packet"
    scope = cond["scope"]
    data = layer[cond["offset"]:] if scope == "all" \
           else layer[cond["offset"]: cond["offset"] + scope]
    if not data:
        return False, "No data at that offset/scope"
    return match_pattern(data, cond["pattern"], cond["location"])


def run_idps(layers, rules):
    fired = []
    for rule in rules:
        results = []
        all_match = True
        for cond in rule["conditions"]:
            matched, explanation = check_condition(layers, cond)
            results.append({**cond, "matched": matched,
                             "explanation": explanation})
            if not matched:
                all_match = False
        if all_match:
            fired.append({"rule": rule, "details": results})
    return fired


# ═══════════════════════════════════════════════════════════════
# RULES
# ═══════════════════════════════════════════════════════════════

RULES = [
    {
        "id": 1,
        "name": "TCP Destination Port 52,000",
        "desc": "Catches TCP packets aimed at port 52,000",
        "tag": "Port Scan",
        "conditions": [{
            "location": "TCP Header", "offset": 2, "scope": 2,
            "pattern": "1100101100100000",
        }],
    },
    {
        "id": 2,
        "name": "TCP Flags: SYN + PSH",
        "desc": "SYN (bit1) and PSH (bit3) both active",
        "tag": "Suspicious Flags",
        "conditions": [{
            "location": "TCP Header", "offset": 13, "scope": 1,
            "pattern": "00001010",
        }],
    },
    {
        "id": 3,
        "name": "Source IP range 1.1.1.1 - 1.1.1.25",
        "desc": "IP range regex match on source address",
        "tag": "IP Filter",
        "conditions": [{
            "location": "IPv4 Header", "offset": 12, "scope": 4,
            "pattern": r"/^1\.1\.1\.([1-9]|1[0-9]|2[0-5])$/",
        }],
    },
    {
        "id": 4,
        "name": "HTTP Payload XirusY + Server 192.168.1.100",
        "desc": "[a-z]irus[2-8] in payload AND destination = 192.168.1.100",
        "tag": "Malware Signature",
        "conditions": [
            {
                "location": "HTTP Payload", "offset": 0, "scope": "all",
                "pattern": "/[a-z]irus[2-8]/",
            },
            {
                "location": "IPv4 Header", "offset": 16, "scope": 4,
                "pattern": r"/^192\.168\.1\.100$/",
            },
        ],
    },
    {
        "id": 5,
        "name": "Source IP 192.168.127.5 - 192.168.127.155",
        "desc": "Catches packets from that subnet range",
        "tag": "IP Filter",
        "conditions": [{
            "location": "IPv4 Header", "offset": 12, "scope": 4,
            "pattern": (r"/^192\.168\.127\."
                        r"([5-9]|[1-9][0-9]|1[0-4][0-9]|15[0-5])$/"),
        }],
    },
    {
        "id": 6,
        "name": "TCP Source Port 80 AND SYN flag",
        "desc": "From port 80 with SYN - possible reverse connection",
        "tag": "Port Scan",
        "conditions": [
            {
                "location": "TCP Header", "offset": 0, "scope": 2,
                "pattern": "0000000001010000",
            },
            {
                "location": "TCP Header", "offset": 13, "scope": 1,
                "pattern": "00000010",
            },
        ],
    },
]

TCP_FLAGS = {
    "SYN":         0x02,
    "ACK":         0x10,
    "PSH":         0x08,
    "FIN":         0x01,
    "RST":         0x04,
    "SYN+ACK":     0x12,
    "SYN+PSH":     0x0A,
    "ACK+PSH":     0x18,
}

# ═══════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════════════════════════════

HTML = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IDPS Simulation</title>
<style>
  :root {
    --bg:      #0d1117;
    --surface: #161b22;
    --border:  #30363d;
    --text:    #e6edf3;
    --muted:   #8b949e;
    --green:   #3fb950;
    --red:     #f85149;
    --yellow:  #d29922;
    --blue:    #58a6ff;
    --purple:  #bc8cff;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text);
         font-family: 'Courier New', monospace; min-height: 100vh; }

  header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 1rem 2rem;
    display: flex; align-items: center; gap: 1rem;
  }
  header h1 { font-size: 1.4rem; color: var(--blue); }
  header span { color: var(--muted); font-size: .85rem; }

  .layout { display: grid; grid-template-columns: 340px 1fr;
             gap: 0; min-height: calc(100vh - 60px); }

  /* ── Left panel ── */
  .panel {
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 1.5rem;
    overflow-y: auto;
  }
  .panel h2 { color: var(--blue); margin-bottom: 1rem;
               font-size: 1rem; text-transform: uppercase;
               letter-spacing: .05em; }

  label { display: block; margin-bottom: .25rem;
          color: var(--muted); font-size: .8rem; }
  input, select, textarea {
    width: 100%; padding: .45rem .6rem;
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 6px; color: var(--text);
    font-family: inherit; font-size: .85rem; margin-bottom: .9rem;
  }
  input:focus, select:focus, textarea:focus {
    outline: none; border-color: var(--blue);
  }
  textarea { resize: vertical; min-height: 70px; }

  .flag-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: .4rem; margin-bottom: .9rem;
  }
  .flag-grid label {
    display: flex; align-items: center; gap: .4rem;
    color: var(--text); font-size: .82rem; cursor: pointer; margin: 0;
  }
  .flag-grid input[type=checkbox] { width: auto; margin: 0; }

  .btn {
    width: 100%; padding: .7rem;
    background: var(--blue); color: #000;
    border: none; border-radius: 6px;
    font-family: inherit; font-weight: bold; font-size: .95rem;
    cursor: pointer; transition: opacity .2s;
  }
  .btn:hover { opacity: .85; }
  .btn-secondary {
    background: transparent; color: var(--muted);
    border: 1px solid var(--border); margin-top: .5rem;
  }

  /* ── Right panel ── */
  .main { padding: 1.5rem; overflow-y: auto; }

  .rules-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr));
    gap: .75rem; margin-bottom: 1.5rem;
  }
  .rule-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1rem;
    transition: border-color .2s;
  }
  .rule-card.fired  { border-color: var(--red);   background: #1c0f0f; }
  .rule-card.tested { border-color: var(--border); }

  .rule-header { display: flex; justify-content: space-between;
                  align-items: flex-start; margin-bottom: .5rem; }
  .rule-id { color: var(--muted); font-size: .75rem; }
  .tag {
    font-size: .7rem; padding: .15rem .5rem; border-radius: 20px;
    background: #1f2937; color: var(--yellow); border: 1px solid var(--yellow);
  }
  .rule-name { color: var(--text); font-size: .9rem;
                font-weight: bold; margin-bottom: .3rem; }
  .rule-desc { color: var(--muted); font-size: .78rem;
                margin-bottom: .7rem; }

  .conditions { display: flex; flex-direction: column; gap: .4rem; }
  .cond {
    background: var(--bg); border-radius: 5px; padding: .5rem .7rem;
    font-size: .75rem; border-left: 3px solid var(--border);
  }
  .cond.pass { border-color: var(--green); }
  .cond.fail { border-color: var(--red); }

  .cond-row { display: flex; gap: .5rem; flex-wrap: wrap; }
  .cond-field { color: var(--muted); }
  .cond-val   { color: var(--blue); }
  .cond-result { margin-top: .3rem; }
  .cond-result.pass { color: var(--green); }
  .cond-result.fail { color: var(--red); }

  .alert-banner {
    padding: .9rem 1.2rem; border-radius: 8px; margin-bottom: 1rem;
    font-weight: bold; font-size: 1rem;
  }
  .alert-banner.alert { background: #2d1010; color: var(--red);
                         border: 1px solid var(--red); }
  .alert-banner.clean { background: #0f2010; color: var(--green);
                         border: 1px solid var(--green); }
  .alert-banner.idle  { background: var(--surface); color: var(--muted);
                         border: 1px solid var(--border); }

  .packet-info {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem;
    font-size: .82rem;
  }
  .packet-info h3 { color: var(--blue); margin-bottom: .6rem; font-size: .9rem; }
  .pi-row { display: flex; gap: 1.5rem; flex-wrap: wrap; }
  .pi-item { color: var(--muted); }
  .pi-item span { color: var(--text); }

  .section-title {
    color: var(--muted); font-size: .8rem; text-transform: uppercase;
    letter-spacing: .06em; margin-bottom: .75rem;
  }

  .spinner { display: none; text-align: center; color: var(--muted);
              padding: 2rem; }
  .spinner.active { display: block; }

  .and-badge {
    text-align: center; font-size: .7rem; color: var(--yellow);
    padding: .15rem 0;
  }

  @media (max-width: 700px) {
    .layout { grid-template-columns: 1fr; }
    .panel { border-right: none; border-bottom: 1px solid var(--border); }
  }
</style>
</head>
<body>

<header>
  <h1>&#x1F6E1; IDPS Simulation</h1>
  <span>Build a packet &rarr; check against {{ rules|length }} rules</span>
</header>

<div class="layout">

  <!-- ── Left: Packet Builder ── -->
  <div class="panel">
    <h2>&#x1F4E6; Packet Builder</h2>

    <label>Protocol</label>
    <select id="proto">
      <option value="tcp">TCP</option>
      <option value="udp">UDP</option>
    </select>

    <label>Source IP</label>
    <input id="src_ip" value="192.168.1.10" placeholder="e.g. 1.1.1.17">

    <label>Destination IP</label>
    <input id="dst_ip" value="8.8.8.8" placeholder="e.g. 192.168.1.100">

    <label>Source Port</label>
    <input id="src_port" type="number" value="54321" min="1" max="65535">

    <label>Destination Port</label>
    <input id="dst_port" type="number" value="80" min="1" max="65535">

    <label>TCP Flags</label>
    <div class="flag-grid" id="flags-section">
      <label><input type="checkbox" id="flag_syn" checked> SYN (2)</label>
      <label><input type="checkbox" id="flag_ack"> ACK (16)</label>
      <label><input type="checkbox" id="flag_psh"> PSH (8)</label>
      <label><input type="checkbox" id="flag_fin"> FIN (1)</label>
      <label><input type="checkbox" id="flag_rst"> RST (4)</label>
      <label><input type="checkbox" id="flag_urg"> URG (32)</label>
    </div>

    <label>HTTP Payload (optional)</label>
    <textarea id="payload" placeholder="e.g. HTTP/1.1 200 OK&#10;Content: virus3 detected"></textarea>

    <button class="btn" onclick="check()">&#x25B6; Inspect Packet</button>
    <button class="btn btn-secondary" onclick="loadPreset()">Load Example Packet</button>

    <div style="margin-top:1.5rem; font-size:.75rem; color:var(--muted)">
      <div style="margin-bottom:.4rem; color:var(--text)">Quick presets:</div>
      {% for p in presets %}
      <div style="cursor:pointer; padding:.3rem 0; border-bottom:1px solid var(--border);
                  color:var(--blue)" onclick="loadPreset({{ loop.index0 }})">
        {{ loop.index }}. {{ p.label }}
      </div>
      {% endfor %}
    </div>
  </div>

  <!-- ── Right: Results ── -->
  <div class="main">
    <div id="banner" class="alert-banner idle">
      &#x2139;&#xFE0F; Build a packet on the left and click <strong>Inspect Packet</strong>
    </div>

    <div id="packet-info" style="display:none" class="packet-info">
      <h3>Inspected Packet</h3>
      <div class="pi-row" id="pi-content"></div>
    </div>

    <div class="spinner" id="spinner">Inspecting... &#x23F3;</div>

    <div class="section-title">Rules ({{ rules|length }} loaded)</div>
    <div class="rules-grid" id="rules-grid">
      {% for rule in rules %}
      <div class="rule-card" id="card-{{ rule.id }}">
        <div class="rule-header">
          <span class="rule-id">Rule #{{ rule.id }}</span>
          <span class="tag">{{ rule.tag }}</span>
        </div>
        <div class="rule-name">{{ rule.name }}</div>
        <div class="rule-desc">{{ rule.desc }}</div>
        <div class="conditions" id="conds-{{ rule.id }}">
          {% for c in rule.conditions %}
          <div class="cond">
            <div class="cond-row">
              <span class="cond-field">Location:</span>
              <span class="cond-val">{{ c.location }}</span>
              <span class="cond-field">offset:</span>
              <span class="cond-val">{{ c.offset }}</span>
              <span class="cond-field">scope:</span>
              <span class="cond-val">{{ c.scope }}</span>
            </div>
            <div class="cond-row" style="margin-top:.3rem">
              <span class="cond-field">Pattern:</span>
              <span class="cond-val" style="word-break:break-all">{{ c.pattern }}</span>
            </div>
          </div>
          {% if not loop.last %}
          <div class="and-badge">&amp;&amp; AND</div>
          {% endif %}
          {% endfor %}
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>

<script>
const PRESETS = {{ presets_json|safe }};

function loadPreset(idx) {
  const p = PRESETS[idx || 0];
  document.getElementById('src_ip').value    = p.src_ip;
  document.getElementById('dst_ip').value    = p.dst_ip;
  document.getElementById('proto').value     = p.proto;
  document.getElementById('src_port').value  = p.src_port;
  document.getElementById('dst_port').value  = p.dst_port;
  document.getElementById('payload').value   = p.payload || '';
  const flags = p.flags || 0x02;
  document.getElementById('flag_syn').checked = !!(flags & 0x02);
  document.getElementById('flag_ack').checked = !!(flags & 0x10);
  document.getElementById('flag_psh').checked = !!(flags & 0x08);
  document.getElementById('flag_fin').checked = !!(flags & 0x01);
  document.getElementById('flag_rst').checked = !!(flags & 0x04);
  document.getElementById('flag_urg').checked = !!(flags & 0x20);
}

function getFlags() {
  let f = 0;
  if (document.getElementById('flag_syn').checked) f |= 0x02;
  if (document.getElementById('flag_ack').checked) f |= 0x10;
  if (document.getElementById('flag_psh').checked) f |= 0x08;
  if (document.getElementById('flag_fin').checked) f |= 0x01;
  if (document.getElementById('flag_rst').checked) f |= 0x04;
  if (document.getElementById('flag_urg').checked) f |= 0x20;
  return f;
}

async function check() {
  document.getElementById('spinner').classList.add('active');
  document.getElementById('banner').className = 'alert-banner idle';
  document.getElementById('banner').innerHTML = 'Inspecting...';

  const body = {
    src_ip:    document.getElementById('src_ip').value,
    dst_ip:    document.getElementById('dst_ip').value,
    proto:     document.getElementById('proto').value,
    src_port:  parseInt(document.getElementById('src_port').value),
    dst_port:  parseInt(document.getElementById('dst_port').value),
    tcp_flags: getFlags(),
    payload:   document.getElementById('payload').value,
  };

  const res  = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  });
  const data = await res.json();

  document.getElementById('spinner').classList.remove('active');

  // Packet info
  const pi = document.getElementById('packet-info');
  pi.style.display = 'block';
  const flagNames = [];
  if (body.tcp_flags & 0x02) flagNames.push('SYN');
  if (body.tcp_flags & 0x10) flagNames.push('ACK');
  if (body.tcp_flags & 0x08) flagNames.push('PSH');
  if (body.tcp_flags & 0x01) flagNames.push('FIN');
  if (body.tcp_flags & 0x04) flagNames.push('RST');
  if (body.tcp_flags & 0x20) flagNames.push('URG');
  document.getElementById('pi-content').innerHTML = `
    <div class="pi-item">Proto: <span>${body.proto.toUpperCase()}</span></div>
    <div class="pi-item">Src: <span>${body.src_ip}:${body.src_port}</span></div>
    <div class="pi-item">Dst: <span>${body.dst_ip}:${body.dst_port}</span></div>
    <div class="pi-item">Flags: <span>${flagNames.join('+') || 'none'}</span></div>
    ${body.payload ? `<div class="pi-item" style="width:100%">Payload: <span>"${body.payload.substring(0,60)}${body.payload.length>60?'...':''}"</span></div>` : ''}
  `;

  // Banner
  const banner = document.getElementById('banner');
  if (data.fired.length > 0) {
    banner.className = 'alert-banner alert';
    banner.innerHTML = `&#x1F6A8; ALERT — ${data.fired.length} rule(s) fired!`;
  } else {
    banner.className = 'alert-banner clean';
    banner.innerHTML = '&#x2705; CLEAN — No rules matched this packet';
  }

  // Update rule cards
  const firedIds = new Set(data.fired.map(f => f.rule_id));
  const detailMap = {};
  data.fired.forEach(f => { detailMap[f.rule_id] = f.details; });

  document.querySelectorAll('.rule-card').forEach(card => {
    const id = parseInt(card.id.replace('card-', ''));
    card.className = firedIds.has(id) ? 'rule-card fired' : 'rule-card tested';

    if (firedIds.has(id)) {
      const details = detailMap[id];
      const condsEl = document.getElementById('conds-' + id);
      const condEls = condsEl.querySelectorAll('.cond');
      condEls.forEach((el, i) => {
        const d = details[i];
        el.classList.toggle('pass', d.matched);
        el.classList.toggle('fail', !d.matched);
        let resultEl = el.querySelector('.cond-result');
        if (!resultEl) {
          resultEl = document.createElement('div');
          resultEl.className = 'cond-result';
          el.appendChild(resultEl);
        }
        resultEl.className = 'cond-result ' + (d.matched ? 'pass' : 'fail');
        resultEl.textContent = (d.matched ? '✔ ' : '✘ ') + d.explanation;
      });
    } else {
      // Reset any previous results
      card.querySelectorAll('.cond-result').forEach(r => r.remove());
      card.querySelectorAll('.cond').forEach(c => {
        c.classList.remove('pass', 'fail');
      });
    }
  });
}
</script>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════
# PRESET PACKETS (for students to load quickly)
# ═══════════════════════════════════════════════════════════════

import json

PRESETS = [
    {"label": "TCP to port 52,000  (fires Rule 1)",
     "src_ip": "192.168.1.10", "dst_ip": "8.8.8.8",
     "proto": "tcp", "src_port": 54321, "dst_port": 52000, "flags": 0x02},

    {"label": "SYN + PSH flags  (fires Rule 2)",
     "src_ip": "10.0.0.5", "dst_ip": "10.0.0.1",
     "proto": "tcp", "src_port": 5000, "dst_port": 80, "flags": 0x0A},

    {"label": "Source IP 1.1.1.17  (fires Rule 3)",
     "src_ip": "1.1.1.17", "dst_ip": "192.168.1.1",
     "proto": "tcp", "src_port": 12345, "dst_port": 443, "flags": 0x02},

    {"label": "HTTP payload 'virus3' to .100  (fires Rule 4)",
     "src_ip": "10.10.10.10", "dst_ip": "192.168.1.100",
     "proto": "tcp", "src_port": 44444, "dst_port": 8080, "flags": 0x18,
     "payload": "HTTP/1.1 200 OK\r\nContent: virus3 detected in file"},

    {"label": "Same payload but wrong server  (CLEAN)",
     "src_ip": "10.10.10.10", "dst_ip": "192.168.1.200",
     "proto": "tcp", "src_port": 44444, "dst_port": 8080, "flags": 0x18,
     "payload": "HTTP/1.1 200 OK\r\nContent: virus3 detected"},

    {"label": "Source IP 192.168.127.99  (fires Rule 5)",
     "src_ip": "192.168.127.99", "dst_ip": "10.0.0.1",
     "proto": "tcp", "src_port": 9999, "dst_port": 22, "flags": 0x02},

    {"label": "Port 80 + SYN  (fires Rule 6)",
     "src_ip": "93.184.216.34", "dst_ip": "192.168.1.5",
     "proto": "tcp", "src_port": 80, "dst_port": 54000, "flags": 0x02},

    {"label": "Normal HTTPS traffic  (CLEAN)",
     "src_ip": "172.16.0.1", "dst_ip": "8.8.8.8",
     "proto": "tcp", "src_port": 9999, "dst_port": 443, "flags": 0x18},
]


# ═══════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template_string(
        HTML,
        rules=RULES,
        presets=PRESETS,
        presets_json=json.dumps(PRESETS),
    )


@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    try:
        layers = make_packet(
            src_ip    = data['src_ip'],
            dst_ip    = data['dst_ip'],
            proto     = data['proto'],
            src_port  = int(data['src_port']),
            dst_port  = int(data['dst_port']),
            tcp_flags = int(data.get('tcp_flags', 0x02)),
            payload   = data.get('payload', ''),
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    fired_raw = run_idps(layers, RULES)
    fired = [
        {
            "rule_id": item["rule"]["id"],
            "name":    item["rule"]["name"],
            "details": [
                {
                    "location":    d["location"],
                    "offset":      d["offset"],
                    "scope":       d["scope"],
                    "pattern":     d["pattern"],
                    "matched":     d["matched"],
                    "explanation": d["explanation"],
                }
                for d in item["details"]
            ],
        }
        for item in fired_raw
    ]
    return jsonify({"fired": fired})


@app.route('/health')
def health():
    return jsonify({"status": "ok", "rules": len(RULES)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
