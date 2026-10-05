#!/usr/bin/env python3
"""Read the live facts of every entry in this list, and what changed since last week.

Runs in each list's GitHub Actions every week (.github/workflows/facts.yml),
on GitHub's machines — whether or not anyone's computer is on. Writes nothing
to main: the workflow stores the result on the `facts` branch.

  Founder, 2026-10-05: "This market is changing so fast. The things are
  disappearing, renaming, being abandoned… we will have thousands of these
  records… the system really have to check the things one times a week and
  see what's really changed. Probably we will need to update the versions."

FACTS (no judgement — a script reads only what a source states)
  GitHub project  name as GitHub now has it, archived, last push, latest
                  release + date, licence (SPDX), stars, description
                  — one GraphQL request per 50 projects, so thousands of
                  entries cost a few dozen requests
  any other link  status, where it redirects to now, page title

CHANGES (week over week, from the previous facts.json)
  gone · renamed · archived · release · licence · dormant (crossed 180 days)
  · dead (the link stopped answering) · redirect (the homepage now lands on
  another site) · title (the entry's own name left its homepage title — a
  rename or an acquisition)

The weekly routine reads the changes and a research agent judges each one;
the release, licence and star facts are shown on the README and the page.

THE MASTER COPY lives in /mnt/AI/Programming/Playbooks/awesome-weekly/facts.py;
publish.py copies it into every list's scripts/ before it publishes.

  GH_TOKEN=… python3 scripts/facts.py --prev prev.json --out facts.json \\
      --changes changes.json --summary summary.md
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml

try:                # the README generators import fact_line from here, and in
    import requests  # CI they run with pyyaml only — reading needs requests,
except ImportError:  # rendering does not
    requests = None

UA = "Mozilla/5.0 (X11; Linux x86_64) brethof-awesome-facts/1.0"
GH_REPO = re.compile(r"^https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?(?:[#?].*)?$")
GH_NOT_REPOS = {"features", "orgs", "topics", "sponsors", "marketplace", "apps", "settings", "enterprise"}
DORMANT_DAYS = 180
BATCH = 50

session = requests.Session() if requests else None
if session:
    session.headers["User-Agent"] = UA


def load_entries(root: Path) -> list[dict]:
    out = []
    for p in sorted((root / "entries").glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            d.setdefault("slug", p.stem)
            out.append(d)
    return out


def gh_repo_of(e: dict) -> str | None:
    for f in ("repository", "url"):
        m = GH_REPO.match(str(e.get(f) or ""))
        if m and m.group(1).lower() not in GH_NOT_REPOS:
            return f"{m.group(1)}/{m.group(2)}"
    return None


# ── GitHub, in batches ─────────────────────────────────────────────────────
FIELDS = """nameWithOwner isArchived pushedAt stargazerCount description
  licenseInfo { spdxId }
  latestRelease { tagName publishedAt }"""


def github(repos: list[str], token: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    h = {"Authorization": f"Bearer {token}"} if token else {}
    for i in range(0, len(repos), BATCH):
        chunk = repos[i:i + BATCH]
        q = "query {" + " ".join(
            f'r{j}: repository(owner: {json.dumps(r.split("/")[0])}, name: {json.dumps(r.split("/")[1])}) {{ {FIELDS} }}'
            for j, r in enumerate(chunk)) + "}"
        r = session.post("https://api.github.com/graphql", json={"query": q}, headers=h, timeout=60)
        if r.status_code != 200:
            sys.exit(f"GitHub GraphQL {r.status_code}: {r.text[:300]}")
        body = r.json()
        data = body.get("data") or {}
        for j, full in enumerate(chunk):
            d = data.get(f"r{j}")
            if d is None:
                out[full] = {"gone": True}
                continue
            out[full] = {
                "repo": d["nameWithOwner"],
                "archived": d["isArchived"],
                "pushed": (d["pushedAt"] or "")[:10],
                "stars": d["stargazerCount"],
                "licence": (d.get("licenseInfo") or {}).get("spdxId"),
                "release": (d.get("latestRelease") or {}).get("tagName"),
                "released": ((d.get("latestRelease") or {}).get("publishedAt") or "")[:10] or None,
                "description": d.get("description"),
            }
    return out


# ── any other link ─────────────────────────────────────────────────────────
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)


def _ipv4_only():
    """A site whose IPv6 address is broken still answers over IPv4 (measured
    2026-10-05: exodus-privacy.eu.org). One retry over IPv4 before calling a
    link dead."""
    import socket
    import urllib3.util.connection as c
    c.allowed_gai_family = lambda: socket.AF_INET


def web(url: str, retry: bool = True) -> dict:
    try:
        r = session.get(url, timeout=25, allow_redirects=True, stream=True)
        body = r.raw.read(65536, decode_content=True).decode(r.encoding or "utf-8", "replace")
        r.close()
        t = TITLE.search(body)
        return {"status": r.status_code, "final": r.url,
                "title": " ".join(html.unescape(t.group(1)).split())[:160] if t else None}
    except Exception as e:      # requests' errors; any failure is a fact too
        if retry and type(e).__name__ == "ConnectionError":
            _ipv4_only()
            return web(url, retry=False)
        return {"status": None, "error": type(e).__name__}


def host(u: str | None) -> str:
    h = (urlparse(u or "").hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def site(h: str) -> str:
    """docs.ollama.com and ollama.com are one site; ollama.com and ollama.ai are not."""
    parts = h.split(".")
    return ".".join(parts[-3:]) if len(parts) >= 3 and parts[-2] in ("co", "com", "org", "ac") else ".".join(parts[-2:])


def norm(s: str) -> str:
    return re.sub(r"[\W_]+", "", (s or "").lower())


# ── what the README and the page show ─────────────────────────────────────
def load_facts(root: Path) -> dict:
    """facts.json on main (publish.py merges it from the facts branch)."""
    f = Path(root) / "facts.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")).get("entries", {})
    except (OSError, ValueError):
        return {}


def stars(n: int) -> str:
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def fact_line(f: dict | None) -> str:
    """One line of facts for an entry: ★ 12.5k · v0.20.0 (2026-09-30), or the
    last push when there are no releases. Empty when nothing is known. The
    README generators and the page both use it, so they say the same."""
    g = (f or {}).get("github") or {}
    if not g or g.get("gone"):
        return ""
    bits = [f"★ {stars(g.get('stars') or 0)}"]
    if g.get("archived"):
        bits.append(f"archived, last push {g.get('pushed')}")
    elif g.get("release"):
        bits.append(f"{g['release']} ({g.get('released')})")
    elif g.get("pushed"):
        bits.append(f"last push {g['pushed']}")
    return " · ".join(bits)


# ── changes ────────────────────────────────────────────────────────────────
def changes(prev: dict, cur: dict, entries: dict[str, dict], today: dt.date) -> list[dict]:
    ev = []

    def add(slug, kind, detail):
        ev.append({"slug": slug, "name": entries[slug].get("name"), "kind": kind, "detail": detail})

    for slug, c in cur.items():
        p = prev.get(slug) or {}
        g, pg = c.get("github") or {}, p.get("github") or {}
        if g:
            if g.get("gone") and not pg.get("gone"):
                add(slug, "gone", f"GitHub no longer has {c['github_ref']}")
            if g.get("repo") and pg.get("repo") and g["repo"].lower() != pg["repo"].lower():
                add(slug, "renamed", f"{pg['repo']} → {g['repo']}")
            elif g.get("repo") and not pg and g["repo"].lower() != c["github_ref"].lower():
                add(slug, "renamed", f"listed as {c['github_ref']}, GitHub says {g['repo']}")
            if g.get("archived") and not pg.get("archived"):
                add(slug, "archived", f"archived (last push {g.get('pushed')})")
            if pg and g.get("release") and g.get("release") != pg.get("release"):
                add(slug, "release", f"{pg.get('release') or 'no release'} → {g['release']} ({g.get('released')})")
            if pg and g.get("licence") != pg.get("licence") and not g.get("gone"):
                add(slug, "licence", f"{pg.get('licence')} → {g.get('licence')}")
            if g.get("pushed"):
                age = (today - dt.date.fromisoformat(g["pushed"])).days
                was = pg.get("pushed") and (today - dt.date.fromisoformat(pg["pushed"])).days > DORMANT_DAYS
                if age > DORMANT_DAYS and not was:
                    add(slug, "dormant", f"no push for {age} days (since {g['pushed']})")
        w, pw = c.get("web") or {}, p.get("web") or {}
        if w:
            dead = w.get("status") in (404, 410) or w.get("error") == "ConnectionError"
            pdead = pw.get("status") in (404, 410) or pw.get("error") == "ConnectionError"
            if dead and not pdead:
                add(slug, "dead", f"{c['url']} → {w.get('status') or w.get('error')}")
            if (w.get("final") and site(host(w["final"])) != site(host(c["url"]))
                    and (not pw or site(host(pw.get("final"))) != site(host(w["final"])))):
                add(slug, "redirect", f"{c['url']} now lands on {w['final']}")
            name = norm(entries[slug].get("name", "").split("(")[0])
            if (pw.get("title") and w.get("title") and name and len(name) >= 3
                    and name in norm(pw["title"]) and name not in norm(w["title"])):
                add(slug, "title", f"homepage title was «{pw['title']}», now «{w['title']}»")
    return ev


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--prev", help="last week's facts.json (missing = first run)")
    ap.add_argument("--out", default="facts.json")
    ap.add_argument("--changes", default="changes.json")
    ap.add_argument("--summary", default="summary.md")
    a = ap.parse_args()
    root = Path(a.root)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    today = dt.date.today()

    entries = {e["slug"]: e for e in load_entries(root)}
    refs = {s: gh_repo_of(e) for s, e in entries.items()}
    gh = github(sorted({r for r in refs.values() if r}), token)
    urls = {s: e["url"] for s, e in entries.items()
            if str(e.get("url", "")).startswith("http") and not GH_REPO.match(str(e["url"]))}
    with cf.ThreadPoolExecutor(16) as ex:
        webs = dict(zip(urls, ex.map(web, urls.values())))

    cur = {}
    for s, e in sorted(entries.items()):
        c = {"name": e.get("name"), "url": e.get("url"), "checked": today.isoformat()}
        if refs[s]:
            c["github_ref"] = refs[s]
            c["github"] = gh.get(refs[s], {"gone": True})
        if s in webs:
            c["web"] = webs[s]
        cur[s] = c

    prev = {}
    if a.prev and Path(a.prev).is_file():
        try:
            prev = json.loads(Path(a.prev).read_text(encoding="utf-8")).get("entries", {})
        except ValueError:
            prev = {}
    ev = changes(prev, cur, entries, today)

    Path(a.out).write_text(json.dumps({"checked": today.isoformat(), "entries": cur},
                                      ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    Path(a.changes).write_text(json.dumps({"checked": today.isoformat(), "since": bool(prev), "changes": ev},
                                          ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = [f"## Facts {today} — {len(cur)} entries, {len(ev)} change(s)"
             + ("" if prev else " (first run: baseline only)"), ""]
    lines += [f"- **{x['kind']}** {x['name']}: {x['detail']}" for x in ev] or ["No changes."]
    Path(a.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
