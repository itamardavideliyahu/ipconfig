#!/usr/bin/env python3
"""
Intentionally vulnerable "ping" web app - FOR SECURITY-TRAINING LAB USE ONLY.

This app contains a deliberate OS Command Injection vulnerability
(the classic "ping tool" bug) so it can be used to demonstrate how an
attacker turns a web-app flaw into a reverse shell.

DO NOT deploy this on any network you don't fully control, and never
expose it to the internet. Run it only inside an isolated lab VM.
"""

import subprocess

from flask import Flask, request

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>Lab Ping Tool (VULNERABLE - training only)</title>
<h1>Lab Ping Tool</h1>
<p>Enter a host to ping. (This tool is intentionally vulnerable to
command injection for lab/training purposes.)</p>
<form method="get" action="/ping">
  <input name="host" placeholder="e.g. 127.0.0.1">
  <button type="submit">Ping</button>
</form>
{output}
"""


@app.route("/")
def index():
    return PAGE.format(output="")


@app.route("/ping")
def ping():
    host = request.args.get("host", "")

    # VULNERABLE ON PURPOSE: user input is concatenated straight into a
    # shell command. A real-world fix would use subprocess with a list
    # of args (no shell=True) plus strict input validation, e.g.:
    #   if not re.fullmatch(r"[a-zA-Z0-9.\-]+", host): reject
    command = f"ping -c 1 {host}"

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )
        output = result.stdout + result.stderr
    except Exception as exc:  # noqa: BLE001 - demo only
        output = str(exc)

    return PAGE.format(output=f"<pre>{output}</pre>")


if __name__ == "__main__":
    # 0.0.0.0 so it's reachable from the attacker VM on the lab network.
    app.run(host="0.0.0.0", port=5000)
