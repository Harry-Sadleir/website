# woof_site/github_activity.py
import os, json, time, urllib.request, urllib.error

GITHUB_USER = "woofdog7"
GITHUB_TOKEN = None
CACHE_TTL = 600  # seconds (10 minutes)
_cache = {"ts": 0, "items": []}

API_URL = f"https://api.github.com/users/{GITHUB_USER}/events/public"

def _request(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "woof-site",
        "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {})
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def _summarize(ev):
    t = ev.get("type", "")
    repo = (ev.get("repo") or {}).get("name", "")
    url = f"https://github.com/{repo}"
    when = ev.get("created_at", "")
    # Friendly text per type
    if t == "PushEvent":
        commits = ev.get("payload", {}).get("commits", []) or []
        msg = commits[-1].get("message", "(push)") if commits else "pushed commits"
        return {"when": when, "text": f"Pushed to {repo}: {msg}", "url": url}
    if t == "PullRequestEvent":
        pr = ev.get("payload", {}).get("pull_request", {}) or {}
        action = ev.get("payload", {}).get("action", "updated")
        return {"when": when, "text": f"{action.title()} PR #{pr.get('number')} in {repo}", "url": pr.get("html_url", url)}
    if t == "IssuesEvent":
        issue = ev.get("payload", {}).get("issue", {}) or {}
        action = ev.get("payload", {}).get("action", "updated")
        return {"when": when, "text": f"{action.title()} issue #{issue.get('number')} in {repo}", "url": issue.get("html_url", url)}
    if t == "CreateEvent":
        ref_type = ev.get("payload", {}).get("ref_type", "ref")
        ref = ev.get("payload", {}).get("ref", "")
        what = f"{ref_type} {ref}" if ref else ref_type
        return {"when": when, "text": f"Created {what} in {repo}", "url": url}
    if t == "ReleaseEvent":
        rel = ev.get("payload", {}).get("release", {}) or {}
        return {"when": when, "text": f"Published release {rel.get('tag_name','')} in {repo}", "url": rel.get("html_url", url)}
    if t == "WatchEvent":
        return {"when": when, "text": f"⭐ Starred {repo}", "url": url}
    if t == "ForkEvent":
        forkee = ev.get("payload", {}).get("forkee", {}) or {}
        return {"when": when, "text": f"Forked {repo}", "url": forkee.get("html_url", url)}
    # Fallback
    return {"when": when, "text": f"{t} in {repo}", "url": url}

def get_github_activity(limit=5):
    now = time.time()
    if now - _cache["ts"] < CACHE_TTL and _cache["items"]:
        return _cache["items"][:limit]
    try:
        raw = _request(API_URL)
        items = []
        for ev in raw:
            s = _summarize(ev)
            if s: items.append(s)
            if len(items) >= 20:  # gather more than we display after filtering
                break
        _cache["ts"] = now
        _cache["items"] = items
        return items[:limit]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        # on error, return whatever we last had
        return _cache["items"][:limit]