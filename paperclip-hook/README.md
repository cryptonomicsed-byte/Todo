# paperclip-hook — HTTP-adapter receiver for Paperclip

Makes this agent push-reachable from Paperclip (`adapterType: "http"`).
Stdlib Python + POSIX sh; no dependencies.

| File | Role |
|---|---|
| `init_token.sh` | generate the bearer token once → `$STATE/token` (chmod 600) |
| `receiver.py` | `POST /paperclip-hook` (Bearer auth, 401 otherwise) → files payload to `$STATE/inbox/*.json`; `GET /health` → 200 |
| `register.py <base-url>` | `PATCH /api/agents/$PAPERCLIP_AGENT_ID` to `adapterType: http` with the URL + token header |
| `watchdog.sh` | for rotating tunnels: re-runs `register.py` whenever the public URL changes |
| `process.py` | the ~15 min check: drain inbox + poll `/api/agents/me/inbox-lite`, write report, archive |

`$STATE` defaults to `~/.paperclip-hook` (`PAPERCLIP_HOOK_STATE`).

## Run on a persistent host

```sh
./init_token.sh
PAPERCLIP_HOOK_HOST=0.0.0.0 ./receiver.py &                   # or behind a TLS reverse proxy
cloudflared tunnel --url http://127.0.0.1:8787 2> ~/.paperclip-hook/tunnel.log &   # if no stable URL
export PAPERCLIP_URL=https://paperclip.2-25-70-156.sslip.io PAPERCLIP_AGENT_ID=... PAPERCLIP_API_KEY=...
./watchdog.sh &                                               # or: ./register.py https://<stable-host>
# crontab: */15 * * * * cd /path/paperclip-hook && ./process.py
```

## Write rule

Paperclip only accepts issue comments, checkouts and status changes inside a run it
created. Send the wake's `runId` (stored as `run_id` in each inbox envelope) as the
`X-Paperclip-Run-Id` header. Writes without a run are rejected by design.

## Limit

Queueing is 24/7 while the receiver runs; the agent acts on payloads only when
`process.py` runs (every ~15 min).
