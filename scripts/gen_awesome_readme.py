#!/usr/bin/env python3
"""Generate this repo's README.md from entries/*.yaml.

Single source of truth = entries/. The hand-written prose lives in two files:
README.head.md (title, why, legend) and README.foot.md (discovery hubs,
related work, contributing, license). This script stitches:

    README.head.md  +  generated Contents TOC  +  generated category sections
                    +  README.foot.md

Optional README.categories.yaml maps a category slug -> intro paragraph,
emitted under that category's heading.

    python scripts/gen_awesome_readme.py

Edit the YAML (or the head/foot .md) — never hand-edit the generated middle.
Idempotent: the same entries produce the same README every time.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing PyYAML. Install it: pip install pyyaml")

REPO_ROOT = Path(__file__).resolve().parents[1]

# tag -> badge rendering for this list (empty = render the tag verbatim)
BADGES: dict[str, str] = {}

NOTE = ("<!-- The list below is generated from entries/*.yaml by "
        "scripts/gen_awesome_readme.py. Edit the YAML, not this section. -->")


def load_entries(repo_dir: Path) -> list[dict]:
    out = []
    for p in sorted((repo_dir / "entries").glob("*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            out.append(d)
    # skip placeholders (no tagline yet, or repo "[stub]" markers)
    return [e for e in out if e.get("tagline") and "[stub]" not in str(e.get("name", ""))]


def anchor(label: str) -> str:
    s = label.lower()
    for ch in "/()&·,.":
        s = s.replace(ch, "")
    return s.replace(" ", "-")


def badges(tags, mapping) -> str:
    if not tags:
        return ""
    # emoji-badge lists join tight (" "); raw phrase-tag lists (ratings,
    # licence verdicts) get a separator so they don't run together.
    sep = " " if mapping else " · "
    return sep.join(mapping.get(t, t) for t in tags)


def render() -> str:
    d = REPO_ROOT
    entries = load_entries(d)

    cat_intros: dict = {}
    ci = d / "README.categories.yaml"
    if ci.is_file():
        cat_intros = yaml.safe_load(ci.read_text(encoding="utf-8")) or {}

    cats: dict[str, dict] = {}
    for e in entries:
        c = e.get("category", "uncategorized")
        cats.setdefault(c, {"slug": c, "label": e.get("category_label") or c,
                            "order": e.get("category_order", 999), "items": []})["items"].append(e)
    ordered = sorted(cats.values(), key=lambda c: (c["order"], c["label"]))

    out: list[str] = []
    head = d / "README.head.md"
    if head.is_file():
        out.append(head.read_text(encoding="utf-8").rstrip() + "\n")

    # LIST:START/END wrap the generated listing. brethof.ai builds this list's
    # page from README.md: the text outside the markers verbatim, the entries
    # inside them as a searchable catalog (brethof-website awesome_catalog.py).
    out.append("<!-- LIST:START -->")
    out.append("## Contents\n")
    for c in ordered:
        out.append(f"- [{c['label']}](#{anchor(c['label'])}) ({len(c['items'])})")
    out.append("")
    out.append(NOTE + "\n")

    for c in ordered:
        out.append(f"## {c['label']}\n")
        intro = (cat_intros.get(c["slug"]) or "").strip()
        if intro:
            out.append(intro + "\n")
        for e in sorted(c["items"], key=lambda e: str(e.get("name", "")).lower()):
            name, url = e.get("name", "?"), (e.get("url") or "")
            tag = badges(e.get("tags"), BADGES)
            tagline = (e.get("tagline") or "").strip()
            line = f"- **[{name}]({url})**" if url else f"- **{name}**"
            if tag:
                line += f" — {tag}"
            if tagline:
                line += f"  \n  {tagline}"
            out.append(line)
        out.append("")

    out.append("<!-- LIST:END -->\n")

    foot = d / "README.foot.md"
    if foot.is_file():
        out.append(foot.read_text(encoding="utf-8").strip() + "\n")
    return "\n".join(out)


def main() -> int:
    if not (REPO_ROOT / "entries").is_dir():
        sys.exit(f"ERROR: no entries/ dir at {REPO_ROOT}")
    text = render()
    (REPO_ROOT / "README.md").write_text(text, encoding="utf-8")
    print(f"wrote README.md ({len(text)} bytes, {len(load_entries(REPO_ROOT))} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
