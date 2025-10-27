# collect.py
import json
import hashlib
import requests
from datetime import datetime, timezone

DATA_FILE = "data.json"
MAX_ITEMS = 1000

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

def make_id(source, url):
    return hashlib.sha1(f"{source}:{url}".encode("utf-8")).hexdigest()

def fetch_github_events(auth_token=None, limit=50):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if auth_token:
        headers["Authorization"] = f"token {auth_token}"
    url = "https://api.github.com/events"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    events = resp.json()[:limit]
    out = []
    for e in events:
        repo = e.get("repo", {}).get("name")
        if not repo:
            continue
        # Build a simple record
        item_url = f"https://github.com/{repo}"
        created_at = e.get("created_at") or datetime.now(timezone.utc).isoformat()
        title = f"{e.get('type')} — {repo}"
        item = {
            "id": make_id("github", item_url + (e.get("id") or "")),
            "source": "github",
            "title": title,
            "url": item_url,
            "canonical_url": item_url,
            "created_at": created_at,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "summary": None,
            "author": {"name": e.get("actor", {}).get("display_login") or e.get("actor", {}).get("login"), "url": None},
            "tags": [],
            "meta": {"raw_type": e.get("type")}
        }
        out.append(item)
    return out

def dedupe_and_merge(existing, new_items):
    existing_ids = {it["id"] for it in existing}
    added = []
    for it in new_items:
        if it["id"] not in existing_ids:
            added.append(it)
            existing_ids.add(it["id"])
    # newest first: new items appear at top
    merged = added + existing
    return merged[:MAX_ITEMS], added

def main():
    print("Loading existing data...")
    current = load_data()
    print(f"Existing items: {len(current)}")

    # Optionally set GITHUB_TOKEN env var if you have one for higher rate limits.
    import os
    token = os.getenv("GITHUB_TOKEN")

    print("Fetching GitHub events...")
    try:
        gh_items = fetch_github_events(auth_token=token, limit=50)
    except Exception as e:
        print("Error fetching GitHub:", e)
        gh_items = []

    print(f"Fetched {len(gh_items)} items from GitHub.")
    merged, added = dedupe_and_merge(current, gh_items)

    if added:
        save_data(merged)
        print(f"Added {len(added)} new items. Total stored: {len(merged)}")
    else:
        print("No new items to add.")

if __name__ == "__main__":
    main()
