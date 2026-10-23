#!/usr/bin/env python3
"""Paperclip HTTP-adapter webhook receiver.

POST /paperclip-hook  -> Bearer-auth'd; every accepted payload is filed as JSON in $STATE/inbox
GET  /health          -> public 200

Receive-and-queue only: it never acts on a payload. process.py drains the inbox.
Stdlib only, so it runs on any box with python3.
"""
import hmac, json, os, sys, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STATE = os.path.abspath(os.environ.get("PAPERCLIP_HOOK_STATE", os.path.expanduser("~/.paperclip-hook")))
INBOX = os.path.join(STATE, "inbox")
TOKEN_FILE = os.environ.get("PAPERCLIP_HOOK_TOKEN_FILE", os.path.join(STATE, "token"))
PATH = os.environ.get("PAPERCLIP_HOOK_PATH", "/paperclip-hook")
MAX_BODY = 1 << 20  # 1 MiB


def load_token():
    st = os.stat(TOKEN_FILE)
    if st.st_mode & 0o077:
        sys.exit(f"refusing to start: {TOKEN_FILE} must be chmod 600")
    with open(TOKEN_FILE) as f:
        tok = f.read().strip()
    if len(tok) < 32:
        sys.exit("refusing to start: token shorter than 32 chars")
    return tok


def file_payload(body, headers):
    """Atomically write one envelope to the inbox; returns its id."""
    os.makedirs(INBOX, mode=0o700, exist_ok=True)
    wid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:12]
    try:
        payload = json.loads(body)
    except ValueError:
        payload = {"_raw": body.decode("utf-8", "replace")}
    run_id = headers.get("X-Paperclip-Run-Id") or (payload.get("runId") if isinstance(payload, dict) else None)
    env = {"id": wid, "received_at": time.time(), "run_id": run_id, "payload": payload}
    tmp = os.path.join(INBOX, f".{wid}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(env, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.rename(tmp, os.path.join(INBOX, f"{wid}.json"))
    return wid


class Handler(BaseHTTPRequestHandler):
    server_version = "paperclip-hook/1"

    def _send(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.split("?")[0] == "/health":
            return self._send(200, {"ok": True})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path.split("?")[0] != PATH:
            return self._send(404, {"error": "not found"})
        auth = self.headers.get("Authorization", "")
        expected = "Bearer " + self.server.token
        if not hmac.compare_digest(auth.encode(), expected.encode()):
            return self._send(401, {"error": "unauthorized"})
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            return self._send(413, {"error": "payload too large"})
        wid = file_payload(self.rfile.read(n), self.headers)
        self._send(200, {"ok": True, "queued": wid})

    def log_message(self, fmt, *args):  # never log headers (token)
        sys.stderr.write("%s %s\n" % (self.log_date_time_string(), fmt % args))


def main():
    host = os.environ.get("PAPERCLIP_HOOK_HOST", "127.0.0.1")
    port = int(os.environ.get("PAPERCLIP_HOOK_PORT", "8787"))
    srv = ThreadingHTTPServer((host, port), Handler)
    srv.token = load_token()
    print(f"paperclip-hook listening on http://{host}:{port}{PATH} inbox={INBOX}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
