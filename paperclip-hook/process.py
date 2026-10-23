#!/usr/bin/env python3
"""Recurring check (~15 min): drain queued wakes + poll inbox-lite, write a report, archive.

The report is printed and appended to $STATE/reports/<date>.md; deliver it to bino1985
via whatever channel the agent's runtime has (Paperclip comment inside a run, mail, etc.).
"""
import glob, json, os, sys, time, urllib.request

STATE = os.environ.get("PAPERCLIP_HOOK_STATE", os.path.expanduser("~/.paperclip-hook"))
INBOX, ARCHIVE, REPORTS = (os.path.join(STATE, d) for d in ("inbox", "archive", "reports"))
SEEN = os.path.join(STATE, "inbox_lite_seen.json")


def queued_wakes():
    out = []
    for p in sorted(glob.glob(os.path.join(INBOX, "*.json"))):
        with open(p) as f:
            out.append((p, json.load(f)))
    return out


def inbox_lite():
    api, key = os.environ.get("PAPERCLIP_URL"), os.environ.get("PAPERCLIP_API_KEY")
    if not (api and key):
        return None, "PAPERCLIP_URL/PAPERCLIP_API_KEY not set; inbox-lite not polled"
    req = urllib.request.Request(f"{api.rstrip('/')}/api/agents/me/inbox-lite",
                                 headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            items = json.load(r)
    except Exception as e:  # report, don't crash the cron
        return None, f"inbox-lite poll failed: {e}"
    items = items.get("items", items) if isinstance(items, dict) else items
    seen = set(json.load(open(SEEN))) if os.path.exists(SEEN) else set()
    new = [i for i in items if str(i.get("id")) not in seen]
    with open(SEEN, "w") as f:
        json.dump(sorted(seen | {str(i.get("id")) for i in items}), f)
    return new, None


def main():
    wakes = queued_wakes()
    lite, err = inbox_lite()
    if not wakes and not lite and not err:
        return
    lines = [f"## Paperclip check {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}"]
    for _, w in wakes:
        p = w["payload"] if isinstance(w["payload"], dict) else {}
        issue = p.get("issueId") or (p.get("issue") or {}).get("id")
        lines.append(f"- wake {w['id']} runId={w.get('run_id')} issue={issue} "
                     f"reason={p.get('reason') or p.get('wakeReason')}")
    for i in lite or []:
        lines.append(f"- inbox-lite {i.get('id')}: {i.get('title') or i.get('identifier') or ''} [{i.get('status')}]")
    if err:
        lines.append(f"- note: {err}")
    report = "\n".join(lines) + "\n"
    print(report)
    os.makedirs(REPORTS, mode=0o700, exist_ok=True)
    with open(os.path.join(REPORTS, time.strftime("%Y-%m-%d.md", time.gmtime())), "a") as f:
        f.write(report + "\n")
    os.makedirs(ARCHIVE, mode=0o700, exist_ok=True)
    for path, _ in wakes:  # archive only after the report is safely written
        os.rename(path, os.path.join(ARCHIVE, os.path.basename(path)))


if __name__ == "__main__":
    sys.exit(main())
