# awesome-linux-for-ai

> Curated tier list of Linux distros, ranked specifically for **running local AI on your own hardware in 2026** — NVIDIA driver currency, CUDA / ROCm ergonomics, kernel cadence, btrfs / snapshot safety. Not a general-purpose desktop list.

Maintained by [Brethof AI](https://brethof.ai). Companion to Nova's
episode 2 — **[Best OS for Local AI in 2026](https://brethof.ai/nova/ep-002-best-os-local-ai/)** —
which is the long-form video version of this list. Watch the episode
for the editorial argument; use this list as the at-a-glance reference.

## Why this list exists

Every "best Linux for AI" article in 2026 still says "Ubuntu, because
that's what the tutorials assume." That was true in 2022. In 2026 the
tutorials are written by AI agents, NVIDIA driver releases happen
weekly, and the OS that ships kernel updates in hours wins. Ubuntu
ships them two releases later.

This list ranks distros by **the things that actually matter for
running models on your own GPU**:

- How fast does the NVIDIA driver land after a release?
- What's the kernel currency, and does it match the cards on the market?
- Does CUDA install in one command, or does it install in a weekend?
- Are containers + the NVIDIA Container Toolkit a first-class path?
- Is there btrfs + snapshots to roll back a broken driver update?
- Is the desktop usable for the other 90% of your time at the machine?

Editorial alignment: where this list and Nova's ep_002 verdicts agree,
they agree. Where the list places Ubuntu B and Nova says 🔴 — that's
the operational vs editorial split: Ubuntu IS still the most workable
non-CachyOS path for plug-and-play CUDA today. Nova's episode is the
opinionated argument for moving off it. Both are true at once.

## Inclusion rules

To be on the list:

- A distro a real person could install on a real AI workstation in 2026.
- Active maintenance — a release, point release, or kernel rebase in
  the last 12 months.
- A real artefact (not a "coming soon" landing page).
- Covered in Nova's ep_002 — either in the main verdict block or the
  Snub Round.

## Tier legend

- **🟢 Tier S — Winner.** The one to install. Single entry: CachyOS.
- **🟡 Tier A — Setup ritual.** Excellent if you accept that initial
  configuration is a project, not a wizard.
- **🟡 Tier B — With caveats.** Will run AI workloads, but with known
  friction — driver lag, packaging quirks, or pre-production desktops.
- **🔴 Tier C — Not for an AI desktop.** Either positioned for a
  different use case (server / fleet), or actively deprecated for AI.
- **🚫 Snub Round.** Distros Nova called out by name in the episode
  for being beside-the-point: pretty, themed, or basically Arch
  again. Listed for completeness.

The per-entry tag pills carry the specific reasons (e.g. *NVIDIA ~2
releases behind*, *btrfs default*, *DKMS dance*, *Snap forced*).
