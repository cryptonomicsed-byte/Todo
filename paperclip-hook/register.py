#!/usr/bin/env python3
"""PATCH this agent's Paperclip record to the http adapter.

usage: register.py <public-base-url>
env:   PAPERCLIP_URL, PAPERCLIP_AGENT_ID, PAPERCLIP_API_KEY (the agent's own claimed key)
"""
import json, os, sys, urllib.request

STATE = os.environ.get("PAPERCLIP_HOOK_STATE", os.path.expanduser("~/.paperclip-hook"))
TOKEN_FILE = os.environ.get("PAPERCLIP_HOOK_TOKEN_FILE", os.path.join(STATE, "token"))
PATH = os.environ.get("PAPERCLIP_HOOK_PATH", "/paperclip-hook")


def register(base_url):
    api, agent, key = (os.environ[k] for k in ("PAPERCLIP_URL", "PAPERCLIP_AGENT_ID", "PAPERCLIP_API_KEY"))
    with open(TOKEN_FILE) as f:
        token = f.read().strip()
    body = {
        "adapterType": "http",
        "adapterConfig": {
            "url": base_url.rstrip("/") + PATH,
            "method": "POST",
            "headers": {"Authorization": f"Bearer {token}"},
        },
    }
    req = urllib.request.Request(
        f"{api.rstrip('/')}/api/agents/{agent}", data=json.dumps(body).encode(), method="PATCH",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        out = json.load(r)
    if out.get("adapterType") != "http":
        raise SystemExit(f"PATCH returned but adapterType is {out.get('adapterType')!r}")
    print(f"registered http adapter -> {body['adapterConfig']['url']}")


if __name__ == "__main__":
    register(sys.argv[1])
