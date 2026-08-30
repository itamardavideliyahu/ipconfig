#!/usr/bin/env bash
# Attacker-side listener for the reverse-shell lab demo.
# FOR USE IN AN ISOLATED LAB / AUTHORIZED PENTEST ONLY.
#
# Usage: ./listener.sh [port]
set -euo pipefail

PORT="${1:-4444}"

if ! command -v nc >/dev/null 2>&1; then
  echo "netcat (nc) not found. Install it with: sudo apt install -y netcat-traditional" >&2
  exit 1
fi

echo "[*] Starting listener on 0.0.0.0:${PORT}"
echo "[*] Waiting for an incoming reverse shell connection..."
echo "[*] Press Ctrl+C to stop."
echo

nc -lvnp "${PORT}"
