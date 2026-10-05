# awesome-linux-for-ai

> Curated tier list of Linux distros, ranked specifically for **running local AI on your own hardware in 2026** — NVIDIA driver currency, CUDA / ROCm ergonomics, kernel cadence, btrfs / snapshot safety. Not a general-purpose desktop list.

Maintained by [Brethof AI](https://brethof.ai). Companion to Nova's
episode 2 — **[Best OS for Local AI in 2026](https://brethof.ai/nova/ep-002-best-os-local-ai/)** —
which is the long-form video version of this list. Watch the episode
for the editorial argument; use this list as the at-a-glance reference.

## Why this list exists

Every "best Linux for AI" article in 2026 still says "Ubuntu, because
that's what the tutorials assume." That was true in 2022. In 2026 the
tutorials are written by AI agents, and three things decide an AI
workstation.

**The newest drivers and kernel, fast.** In September 2026 CachyOS ran
kernel 7.2 and packaged NVIDIA's new 615 driver the day after it was
released; Ubuntu 26.04 LTS sat on kernel 7.0 and the older 595 driver
line.

**One command, not a guide.** `pacman -S docker`.
`pacman -S nvidia-container-toolkit`. `pacman -S cuda python-pytorch-cuda
ollama-cuda`. On Ubuntu, Docker's own guide tells you to remove Ubuntu's
Docker packages first, then runs eight commands to add Docker's key and
repository; NVIDIA's container toolkit isn't in Ubuntu 26.04 LTS's
repositories at all — five more commands to add NVIDIA's. And
`apt install firefox` hands you a snap.

**Snapshots of everything, automatically.** Every update on CachyOS takes
a btrfs snapshot first, and the Limine boot menu lists them: if a driver
update breaks something, reboot into yesterday's system. Ubuntu installs
onto ext4 with GRUB — there is nothing to go back to.

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
the operational vs editorial split: Ubuntu IS still the path every CUDA
tutorial assumes today. Nova's episode is the
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
- **🟡 Tier A — Runner-up.** Excellent for AI work, with one trade-off
  you accept up front: a setup ritual (Arch) or an older base (Pop!_OS).
- **🟡 Tier B — With caveats.** Will run AI workloads, but with known
  friction — driver lag or packaging quirks.
- **🔴 Tier C — Not for an AI desktop.** Either positioned for a
  different use case (server / fleet), or actively deprecated for AI.
- **🚫 Snub Round.** Distros Nova called out by name in the episode
  for being beside-the-point: pretty, themed, or basically Arch
  again. Listed for completeness.

The per-entry tag pills carry the specific reasons (e.g. *NVIDIA ~2
releases behind*, *btrfs default*, *DKMS dance*, *Snap forced*).
