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

<!-- LIST:START -->
## Contents

- [Tier S](#tier-s) (1)
- [Tier A](#tier-a) (2)
- [Tier B](#tier-b) (2)
- [Tier C](#tier-c) (3)
- [Snub Round](#snub-round) (6)

<!-- The list below is generated from entries/*.yaml by scripts/gen_awesome_readme.py. Edit the YAML, not this section. -->

## Tier S

The single distro built around the actual demands of a 2026 AI workstation. NVIDIA driver updates land within about a day, the kernel is tuned and rolling, packages are compiled for modern x86, and btrfs + snapshots give you a 30-second rollback when something goes sideways. If you only read one tier of this list, read this one.

- **[CachyOS](https://cachyos.org)** — 🟢 Winner · AutoFDO + Propeller kernel · x86-64-v3 · LTO/PGO/BOLT · NVIDIA hot updates · btrfs default · pacman + paru · KDE polish  
  Nova's pick for best OS for local AI in 2026. linux-cachyos kernel (EEVDF + Clang LTO + AutoFDO/Propeller by default; BORE one package away in linux-cachyos-bore), x86-64-v3 compiled packages, LTO + PGO + BOLT optimisations, Limine bootloader, NVIDIA driver updates within about a day (615.71.09: NVIDIA release 2026-09-09, CachyOS package 2026-09-10, in the repos 2026-09-11), btrfs with snapshots on by default (30-second rollback). Same Arch wiki applies; pacman + paru is the friendliest install experience in this list. Gaming and AI both first-class.

## Tier A

No "Winner" status, but the best choices outside of Tier S. Arch gives you the best long-term ergonomics if you are happy to spend a weekend configuring the machine — current packages, the best wiki in Linux, and AUR recipes for every CUDA / NVIDIA / ROCm release. Pop!_OS is the opposite trade: it works out of the box, with a current kernel and NVIDIA driver on an older Ubuntu base.

- **[Arch Linux](https://archlinux.org)** — 🟡 Setup ritual · Rolling · AUR · Maximum transparency · Best wiki in Linux · pacman  
  Vanilla Arch. The 2020-era "breaks every Tuesday" reputation is outdated in 2026. Setup is a project, not an install — but configure everything yourself and you get maximum transparency, current packages, and the best wiki in Linux. AUR has a recipe for every CUDA / NVIDIA / ROCm release.
- **[Pop!_OS (COSMIC)](https://system76.com/pop)** — 🟡 Older base · COSMIC desktop · Rust DE · No snap (Flatpak) · NVIDIA ISO · Own kernel + driver · Ubuntu 24.04 base  
  System76's Pop!_OS with the COSMIC desktop — Rust-based, the only fully from-scratch desktop project in this category. COSMIC went stable with Pop!_OS 24.04 LTS on 2025-12-11. System76 strips snap (Flatpak is the default), ships a dedicated NVIDIA ISO with the proprietary driver preinstalled, and carries its own kernel and driver on top of the base (kernel 7.1.5 and NVIDIA 595.84 on 2026-10-05 — a newer kernel than Ubuntu 26.04 itself, though a slightly older 595 driver than Ubuntu's 595.91.07). The one trade-off is the base: still Ubuntu 24.04 — the 26.04 rebase was promised ~2 weeks after Ubuntu 26.04 (April 2026) and on 2026-10-05 there is still no 26.04 ISO (the package repo is being built).

## Tier B

These distros will run AI workloads, but each has a known friction point you will hit within the first week: SELinux + container permissions, or a snap-and-Pro upsell pipeline that ships with the system. Workable, with eyes open.

- **[Fedora Workstation 44](https://fedoraproject.org/workstation)** — 🟡 With caveats · Fedora 44 · Wayland / PipeWire / HDR · SELinux friction · NVIDIA via RPMFusion · 6mo release breaks  
  Best preview of where the Linux desktop is going — Wayland, PipeWire, HDR first. But SELinux fights AI tooling (containers blocked, mounts denied), NVIDIA needs RPMFusion + signed kernel modules + reboot dance, and 6-month release upgrades break things. Great desktop, not a great AI workstation. Cutting edge has a cost.
- **[Ubuntu 26.04 LTS](https://ubuntu.com)** — 🟡 Deprecate (still workable) · Ubuntu 26.04 LTS · Largest CUDA ecosystem · ubuntu-drivers autoinstall · Snap forced · NVIDIA branch behind · Pro motd upsell  
  Industry default — every CUDA guide on the internet assumes Ubuntu; `ubuntu-drivers autoinstall` works on day one. But: Lambda Stack still stops at 24.04 (its installer refuses 26.04), `apt install firefox` gives you a snap, NVIDIA stays on the 595 production branch (595.91.07 in updates on 2026-10-05, while NVIDIA itself is at 595.104.02) and the 615 branch, out since 2026-09-09, has only reached -proposed (2026-09-29), Pro tier upsell printed in the terminal motd, desktop team skeleton crew. The path every CUDA guide assumes — and that is the entire argument for it. Nova's editorial verdict: switch away.

## Tier C

Positioned for a different use case — set-and-forget servers, identical-fleet reproducibility, or Windows-refugee onboarding — and wrong for an AI workstation in 2026 specifically. Each one is still a great Linux distro for its actual job; just not this one.

- **[Debian 13 (Trixie)](https://debian.org)** — 🔴 No for AI desktop · Debian 13 Trixie · Set-and-forget server · DKMS dance · Non-free + headers needed · 2-yr stable cycle  
  Best set-and-forget SERVER distro — rock-solid, conservative, runs forever. Wrong for an AI desktop in 2026. NVIDIA drivers live in non-free + contrib; DKMS silently fails unless you install kernel-headers first; stable and backports both still ship the 550.163.01 driver (`550.163.01-4~bpo13+1`), and it fails to build against the 7.2 kernel now in trixie-backports (Debian bug #1148283, 2026-09-18). 2-year stable release cycle = ancient packages — "from when AI meant chess engines."
- **[Linux Mint](https://linuxmint.com)** — 🔴 Gateway only · Ubuntu LTS base · Cinnamon · CUDA cadence lag · Snap blocked  
  Best Windows-refugee landing pad — Cinnamon is genuinely pleasant, casual desktop fine. But: Ubuntu LTS base means packages are old by design (Mint 22.x still sits on 24.04; Mint 23 on 26.04 targets December 2026), Mint adds extra stability-verification delay on top of that, and for an AI workstation where CUDA moves every six weeks, you're always behind. (Mint does block snap by default — the one Canonical decision it refuses.) Gateway only.
- **[NixOS 26.05](https://nixos.org)** — 🔴 Specific use only · NixOS 26.05 · Reproducible (flakes) · Steep Nix learning curve · Fleet-friendly · Genius + unpaid labour  
  Reproducibility gold standard — pin your CUDA version, kernel, and PyTorch build in a flake; your colleague clones the flake and gets the identical environment six months later. But: Nix language is a math proof, flakes still "experimental" after years, your Bluetooth headset becomes a packaging project, your bank's .deb installer becomes a packaging project. Specific use only: fleets of identical workstations, not a single desktop.

## Snub Round

Distros Nova called out by name in the episode's Snub Round. Pretty, themed, or basically Arch with a coat of paint. Listed for completeness; not recommended for the AI workstation role.

- **[Elementary OS](https://elementary.io)** — 🚫 Snubbed · Pantheon DE · Stuck in 2019  
  Pantheon desktop is genuinely beautiful. Pretty but stuck in 2019 — Ubuntu LTS base, old kernel, slow NVIDIA driver adoption. Not an AI workstation.
- **[EndeavourOS](https://endeavouros.com)** — 🚫 Snubbed · Arch + installer wizard · That is the whole pitch  
  Arch with a friendly installer wizard. That is the whole pitch — same currency as Arch, same risks. If you want Arch, install Arch.
- **[Garuda Linux](https://garudalinux.org)** — 🚫 Snubbed · Ricer-bait · Arch-based  
  Looks like a gaming peripheral exploded. Beautiful, ricer-bait — Arch-based with extreme defaults that mostly serve screenshot collections rather than a working AI rig.
- **[Manjaro](https://manjaro.org)** — 🚫 Snubbed · Held-back repos vs AUR · Worst of both worlds  
  Arch with its repos held back ~2 weeks — but the AUR tracks current Arch, so AUR packages build against libraries Manjaro does not have yet. Constant breakage when you actually need a current package. Worst of both worlds.
- **[openSUSE Tumbleweed](https://www.opensuse.org)** — 🚫 Snubbed · Rolling (Tumbleweed) · zypper + Myrlyn · Mostly in Germany  
  Still alive, I think — genuinely a fine rolling distro that nobody outside of Germany installs. zypper is solid (YaST is in maintenance mode, giving way to Agama, Myrlyn and Cockpit); CUDA via NVIDIA's official repo. Just not a meaningful presence in the AI-distro conversation.
- **[Zorin OS](https://zorin.com)** — 🚫 Snubbed · Windows cosplay  
  Windows cosplay. Tries so hard to look like Windows that it forgets the point of switching.

<!-- LIST:END -->

## Related work

- **[awesome-local-ai](https://github.com/BrethofAI/awesome-local-ai)** — Local-first AI tools (runtimes, chat apps, agents) that will live on these distros.
- **[awesome-private-ai](https://github.com/BrethofAI/awesome-private-ai)** — Privacy-respecting AI more broadly.
- **[awesome-mcp-servers](https://github.com/BrethofAI/awesome-mcp-servers)** — MCP servers that sit happily next to a local LLM.
- **[awesome-ai-minefield](https://github.com/BrethofAI/awesome-ai-minefield)** — Licence + ToS analysis for the models you'll run locally.
- **[awesome-llms-txt](https://github.com/BrethofAI/awesome-llms-txt)** — Tools that publish `llms.txt` for agent discovery.

## Watch the episode

The companion video — **[Nova ep 002: Best OS for Local AI in 2026](https://brethof.ai/nova/ep-002-best-os-local-ai/)** — has the long-form pros / cons walkthrough per distro, the catchphrases, and the editorial argument. This README is the short reference; the episode is the argument.

## Contributing

Open an issue with:

- The distro name + homepage URL.
- The tier you think it belongs to + one paragraph on **why specifically for AI workloads** — driver cadence, kernel currency, CUDA path, etc. General desktop-friendliness isn't enough.
- A receipt for any factual claim (driver release date, packaging quirk, etc).

Entries live as one YAML file per distro under `entries/`. This
README is generated from them by [`scripts/gen_awesome_readme.py`](scripts/gen_awesome_readme.py)
— so edit the YAML, not this README.

## License

[MIT](LICENSE).

---

Maintained by **[Brethof AI](https://brethof.ai)** — local-first AI tools for people who take their hardware seriously.
