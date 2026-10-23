#!/usr/bin/env sh
# For rotating tunnels: re-register with Paperclip whenever the public URL changes.
# Reads the current URL from the cloudflared quick-tunnel log (override with URL_CMD).
set -eu
DIR="$(cd "$(dirname "$0")" && pwd)"
STATE="${PAPERCLIP_HOOK_STATE:-$HOME/.paperclip-hook}"
LOG="${TUNNEL_LOG:-$STATE/tunnel.log}"
URL_CMD="${URL_CMD:-grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' \"$LOG\" | tail -1}"
LAST="$STATE/registered_url"
while :; do
  url="$(sh -c "$URL_CMD" 2>/dev/null || true)"
  if [ -n "$url" ] && [ "$url" != "$(cat "$LAST" 2>/dev/null || true)" ]; then
    if curl -fsS -m 10 "$url/health" >/dev/null && python3 "$DIR/register.py" "$url"; then
      echo "$url" > "$LAST"
    fi
  fi
  sleep "${WATCH_INTERVAL:-60}"
done
