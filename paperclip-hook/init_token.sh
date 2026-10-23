#!/usr/bin/env sh
# Generate the webhook bearer token once, readable only by its owner.
set -eu
STATE="${PAPERCLIP_HOOK_STATE:-$HOME/.paperclip-hook}"
TOKEN_FILE="${PAPERCLIP_HOOK_TOKEN_FILE:-$STATE/token}"
mkdir -p "$STATE" && chmod 700 "$STATE"
if [ -s "$TOKEN_FILE" ]; then echo "token already exists: $TOKEN_FILE"; exit 0; fi
umask 077
python3 -c 'import secrets; print(secrets.token_urlsafe(48))' > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"
echo "token written: $TOKEN_FILE"
