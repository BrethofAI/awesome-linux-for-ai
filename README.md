# awesome-linux-for-ai

> Linux distributions ranked for AI/ML developer workstations in 2026.

Maintained by [Brethof AI](https://brethof.com). Companion to
[awesome-local-ai](https://github.com/BrethofAI/awesome-local-ai),
which is about the tools — this list is about what to run them on.

## Why this list exists

"Just install Ubuntu" is no longer the answer for AI work. The reasons:

- **New GPUs need new kernels.** RTX 50-series (Blackwell, sm_120) needs
  Linux ≥ 6.11; RDNA 4 needs ≥ 6.10. Many LTS distros lag a year.
- **NVIDIA driver matters more than ever.** Open-kernel modules on
  Blackwell, GSP firmware, container-toolkit version, and CUDA forward-compat
  all need to line up. Some installers do this for you, some make it
  homework.
- **PyTorch and CUDA versions move quarterly.** A distro that pins old
  glibc / old CUDA on its release branch wastes hours of compat work.
- **Container runtime matters.** Docker, Podman, NVIDIA Container
  Toolkit (NCT), and CDI mode interactions are fiddly. Distros differ
  in how clean the path is.

Our ranking reflects: how fast you get to a working PyTorch/CUDA setup
out of the box, how recent the kernel is, NVIDIA driver friendliness,
and how well the distro handles dual-GPU / VFIO / multi-monitor edge
cases that AI developers actually hit.

## How we rank

Each distro is rated on five axes. Higher is better.

- **🆕 Currency** — kernel + driver age vs upstream
- **⚙️ Day-1 setup** — how close `pytorch.cuda.is_available()` is to a fresh install
- **🎮 GPU happiness** — NVIDIA / AMD / Intel reality, not slideware
- **🧱 Stability** — does it stay working after package updates
- **♻️ Reproducibility** — can you recreate the same setup six months later

## Tier definitions

| Tier | Meaning |
|------|---------|
| **S** | Drop in. CUDA / ROCm working in one boot. Kernel current. NVIDIA happy. |
| **A** | Excellent with one or two well-known config steps. |
| **B** | Works fine if you accept its trade-offs. Common in practice. |
| **C** | Possible but you'll fight it. Choose only with strong reason. |
| **D** | Don't, for AI work. |

## Contents

- [Tier S — Drop in and run](#tier-s--drop-in-and-run)
- [Tier A — Great with a config step or two](#tier-a--great-with-a-config-step-or-two)
- [Tier B — Solid trade-offs](#tier-b--solid-trade-offs)
- [Tier C — Only with a reason](#tier-c--only-with-a-reason)
- [Tier D — Avoid for AI work](#tier-d--avoid-for-ai-work)
- [Community-recommended (untested by us)](#community-recommended-untested-by-us)
- [Specialised / Niche](#specialised--niche)
- [Container-only / atomic distros](#container-only--atomic-distros)
- [What we test](#what-we-test)

## Tier S — Drop in and run

### CachyOS — 🆕 5/5 ⚙️ 5/5 🎮 5/5 🧱 4/5 ♻️ 3/5

Arch-based, performance-tuned. Ships kernel 6.16+ with zen / lto / x86-64-v3
optimisations. NVIDIA proprietary driver works out of the box; switch
to `nvidia-open-dkms` for Blackwell. NVIDIA Container Toolkit available
via `cachyos-cli` setup; CUDA `13.1` builds available.

- **Site:** [cachyos.org](https://cachyos.org)
- **Why S:** Best out-of-box experience for new NVIDIA hardware in
  2026. KDE Plasma desktop ergonomics; rolling release keeps drivers
  current.
- **Caveat:** Rolling means the occasional `pacman -Syu` regression.
  Use `snapper-tools` (default) for one-command rollback.

> **Why CachyOS sits alone in S.** Tier S is what we'll bet our own
> production AI workloads on, today. We've validated it daily on the
> rig described in [What we test](#what-we-test). Other promising
> candidates are listed elsewhere with that distinction made explicit:
> Bazzite in [Community-recommended (untested by us)](#community-recommended-untested-by-us)
> because we haven't lived on it yet, Pop!_OS COSMIC in Tier B because
> of compositor-stability issues we *have* seen on the rig.

## Tier A — Great with a config step or two

### Ubuntu 24.04 LTS — 🆕 3/5 ⚙️ 5/5 🎮 5/5 🧱 5/5 ♻️ 4/5

Industry default. Most AI tools have an "ubuntu 22.04/24.04 install
guide" first. NVIDIA drivers via `ubuntu-drivers autoinstall`; Lambda
Labs publishes [Lambda Stack](https://lambdalabs.com/lambda-stack-deep-learning-software)
which gives you matched driver + CUDA + cuDNN + PyTorch in one install.

- **Site:** [ubuntu.com](https://ubuntu.com)
- **Why A:** Stability + ecosystem. Ships HWE kernel rolling forward
  every 6 months for newer-hardware cases.
- **Caveat:** Snap-by-default for some packages frustrates dev work.
  Ship date for new GPU support can lag rolling distros by months.

### Fedora Workstation 41 — 🆕 5/5 ⚙️ 4/5 🎮 4/5 🧱 4/5 ♻️ 3/5

Fast-moving but not Arch-fast. Kernel 6.11 in 41, 6.13 in 42. NVIDIA
drivers via RPM Fusion in one extra repo step. CUDA via NVIDIA's
official RHEL-9 RPMs (works on Fedora with minor symlink dance).

- **Site:** [fedoraproject.org/workstation](https://fedoraproject.org/workstation)
- **Why A:** Strong middle-ground between LTS and rolling. SELinux
  enforcing-by-default catches misconfigured AI containers early.

### Arch Linux — 🆕 5/5 ⚙️ 3/5 🎮 5/5 🧱 3/5 ♻️ 2/5

Vanilla Arch. AUR has packages for every CUDA / NVIDIA / ROCm release.
Manual install but every component is current.

- **Site:** [archlinux.org](https://archlinux.org)
- **Why A:** No middleman. The Arch wiki is the reference manual for
  GPU-on-Linux generally.
- **Caveat:** You own all updates. Use [`paru` / `yay`](https://github.com/Morganamilo/paru)
  + [`informant`](https://github.com/bradford-smith94/informant) to
  catch breaking news posts before installing them.

### NixOS 24.11+ — 🆕 4/5 ⚙️ 4/5 🎮 4/5 🧱 5/5 ♻️ 5/5

Reproducibility champion. Pin your CUDA version, kernel, and PyTorch
build to a flake; your colleague can clone the flake and reproduce the
identical environment six months later.

- **Site:** [nixos.org](https://nixos.org)
- **Why A:** Best in class for reproducibility. The
  [`nixos-cuda` cookbook](https://nixos.wiki/wiki/CUDA) covers most
  AI-workstation needs.
- **Caveat:** Steep learning curve. Nix language is the cost of
  reproducibility.

## Tier B — Solid trade-offs

### Pop!_OS COSMIC (24.04 alpha / 25.04) — 🆕 4/5 ⚙️ 3/5 🎮 3/5 🧱 2/5 ♻️ 3/5

System76's own next-generation desktop on Pop!_OS. Rust-based,
ambitious, visually polished. The classic Pop!_OS GNOME edition has
effectively been retired — System76's roadmap is COSMIC-only, so this
is the only Pop!_OS variant you can install fresh today.

As of 2026 the COSMIC desktop still ships with crashes, NVIDIA-driver
flakiness, and regressions that disrupt long-running GPU sessions —
exactly the workload AI users hit hardest. Promising future, not a
reliable present.

- **Site:** [pop.system76.com](https://pop.system76.com)
- **Why B (not S):** Good idea, ship date pulled in too aggressively.
  Daily-driver complaints across [r/pop_os](https://www.reddit.com/r/pop_os/)
  and the [System76 chat](https://chat.system76.com/community/channels/cosmic)
  cluster around compositor crashes, multi-monitor regressions, NVIDIA
  driver edge cases, and Wayland session loss. None of this is fatal —
  recovery is a relog — but it disqualifies COSMIC from "drop in and
  run" for AI work where a long-running training job that crashes is
  hours of wall-clock lost.
- **Recommendation:** Watch this space. When COSMIC 1.0 ships stable
  with the NVIDIA driver matrix solid, it has a real shot at Tier S.
  Until then, run something else for production AI work.

### Debian 12 (Bookworm) — 🆕 2/5 ⚙️ 4/5 🎮 4/5 🧱 5/5 ♻️ 4/5

Rock-stable. Kernel 6.1 by default; backports kernel up to 6.11.
NVIDIA non-free drivers in the contrib repos.

- **Site:** [debian.org](https://debian.org)
- **Why B:** Best server choice that is also acceptable for
  workstation work. Drops a tier for kernel currency on bleeding-edge
  GPUs.

### openSUSE Tumbleweed — 🆕 5/5 ⚙️ 3/5 🎮 4/5 🧱 4/5 ♻️ 3/5

Rolling, but with a strong QA pipeline (`openQA`). NVIDIA drivers via
official zypper repo; YaST is friendly for non-CLI configuration.

- **Site:** [opensuse.org/tumbleweed](https://www.opensuse.org/tumbleweed/)
- **Why B:** Excellent stability for a rolling distro. SUSE container
  toolchain is enterprise-grade.

### Manjaro — 🆕 4/5 ⚙️ 4/5 🎮 4/5 🧱 3/5 ♻️ 2/5

Arch with a 2-week-delayed package window. NVIDIA + CUDA work; the
delay window catches some upstream regressions.

- **Site:** [manjaro.org](https://manjaro.org)
- **Why B:** Arch-flavoured for users who don't want bleeding edge.
  The 2-week delay does *not* protect you from all regressions and
  occasionally creates conflicts of its own.

## Tier C — Only with a reason

### CentOS Stream 9 / Rocky / AlmaLinux 9 — 🆕 2/5 ⚙️ 4/5 🎮 5/5 🧱 5/5 ♻️ 4/5

Enterprise RHEL clones. NVIDIA's official CUDA RPMs target this family
first. Stable, conservative kernel.

- **Sites:** [Rocky Linux](https://rockylinux.org) · [AlmaLinux](https://almalinux.org)
- **Why C (workstation):** Old kernel hurts on new GPUs. As production
  servers for AI workloads they sit much higher; here we rank
  desktop / dev experience.

### Endeavour OS — 🆕 5/5 ⚙️ 3/5 🎮 4/5 🧱 3/5 ♻️ 2/5

Arch with a friendly installer. Same currency as Arch; same risks.

- **Site:** [endeavouros.com](https://endeavouros.com)
- **Why C:** Slot for users who want Arch but find vanilla install
  daunting. CachyOS does the same thing better for AI specifically.

### Linux Mint — 🆕 2/5 ⚙️ 4/5 🎮 4/5 🧱 5/5 ♻️ 3/5

Ubuntu LTS-derived. Kernel currency lags; NVIDIA drivers fine.

- **Site:** [linuxmint.com](https://linuxmint.com)
- **Why C:** Excellent for general desktop use; the kernel-lag plus
  Ubuntu-Snap-bleed-through hurts AI-specific workflows.

## Tier D — Avoid for AI work

### Elementary OS — 🆕 2/5 ⚙️ 3/5 🎮 3/5 🧱 4/5 ♻️ 3/5

Beautiful Pantheon DE; not AI-focused. Old kernel, slow NVIDIA driver
adoption, snap-everywhere.

- **Site:** [elementary.io](https://elementary.io)
- **Why D:** No advantage for AI work. Choose for aesthetics on a
  laptop you won't use for ML training.

### Kali / Parrot — 🆕 4/5 ⚙️ 2/5 🎮 3/5 🧱 3/5 ♻️ 2/5

Penetration-testing distros. Their package selection is wrong for AI;
their system tuning is for offensive security workloads.

- **Sites:** [kali.org](https://kali.org) · [parrotsec.org](https://parrotsec.org)
- **Why D:** Wrong tool for the job. Don't pick for AI; if you need
  pentest tools too, dual-boot or VM them.

## Community-recommended (untested by us)

Distros widely praised in the AI/Linux community that we haven't yet
field-validated on our own [test rig](#what-we-test). Listed here
without a tier rating to keep the methodology honest: a tier is
something we earn by living on the distro. We'll move entries up into
the tier list once we have day-to-day receipts.

### Bazzite — Fedora-Atomic with NVIDIA preinstalled

Fedora-Atomic + COSMIC / KDE images with NVIDIA drivers preinstalled
(both proprietary and open variants). Container-native (rpm-ostree),
making CUDA toolchain experiments safe and reversible. The
"Bazzite-DX" developer-focused variant looks best-in-class on paper
for AI on immutable filesystems.

- **Site:** [bazzite.gg](https://bazzite.gg)
- **Why community-recommended:** Atomic rollback in one reboot,
  preinstalled NVIDIA drivers, declarative-ish config. The
  immutable-host + containerised-CUDA pattern is what serious AI ops
  teams converge on for production fleets.
- **Why not yet tier-rated:** We've been daily-driving CachyOS and
  haven't moved an AI workstation to Bazzite-DX yet. Marketing-grade
  vs measured is a real gap and we won't rate it until we've lived on
  it through actual training runs and driver upgrades. PRs welcome
  from anyone running it on Blackwell with NVIDIA Container Toolkit.

## Specialised / Niche

### Asahi Linux — 🍎 Apple Silicon

Linux on M-series Macs. Asahi's ML stack uses the GPU via custom
kernel-side support; Asahi-Fedora is the production-grade variant.
[`asahi.dev`](https://asahilinux.org)

- Useful when: you have an M-series Mac and don't want macOS for AI work.
- Caveat: Apple's GPU is great for inference but the toolchain is
  custom; CUDA is not available, so you're tied to MLX or
  Apple-native runtimes.

### Bluefin — 🐂 atomic workstation

Fedora-Silverblue-derived, container-first, immutable. Ships NVIDIA
DX images with CUDA dev container ready.

- **Site:** [projectbluefin.io](https://projectbluefin.io)
- Useful when: you want one immutable host and to keep all dev tools
  in containers.

### Lambda Stack on Ubuntu — 🟦 vendor-tuned

Lambda Labs's matched driver + CUDA + cuDNN + PyTorch packaged for
Ubuntu. Closest thing to "drop in PyTorch" for an Ubuntu base.

- **Site:** [lambdalabs.com/lambda-stack-deep-learning-software](https://lambdalabs.com/lambda-stack-deep-learning-software)

### TUXEDO OS — 🟦 hardware-tuned

TUXEDO's fork of Ubuntu LTS with tuning for their workstations. NVIDIA
drivers and TLP / fan-control sane defaults. Decent option if you buy
their hardware.

- **Site:** [tuxedocomputers.com](https://www.tuxedocomputers.com/)

### EndeavourOS Galileo Neo — see Tier C

## Container-only / atomic distros

For those running AI workloads in containers and treating the host as
disposable.

- **[Talos Linux](https://www.talos.dev)** — Kubernetes-native, no
  shell, declarative config. Excellent for AI inference clusters.
- **[k3os / kairos](https://kairos.io)** — kairos extends k3os; immutable
  with config-as-code. AI workloads via k3s + GPU operator.
- **[Flatcar Linux](https://www.flatcar.org)** — CoreOS continuation;
  container-only host designed for fleet management.
- **[Bottlerocket](https://aws.amazon.com/bottlerocket/)** — AWS-built
  immutable container OS. Strong fit for AWS-hosted AI inference.

## What we test

This is a living document. When we benchmark a distro for ranking
changes, we record:

- Kernel version at install
- NVIDIA driver branch + open-vs-proprietary
- `nvidia-smi` working out of the box (yes / no)
- Steps from fresh install to `import torch; torch.cuda.is_available() == True`
- Time-to-CUDA-working in minutes
- Whether NVIDIA Container Toolkit + Docker compose works without
  extra config

PRs welcome — please attach the test environment (host, GPU, kernel)
and the time it took.

## Related work

- **[awesome-local-ai](https://github.com/BrethofAI/awesome-local-ai)** — The tools you'll run on these distros.
- **[awesome-private-ai](https://github.com/BrethofAI/awesome-private-ai)** — Privacy-architecture context for cloud vs self-host trade-offs.
- **[awesome-ai-mine](https://github.com/BrethofAI/awesome-ai-mine)** — License + ToS analysis for the models you'll run on these distros.
- **[comfyui-workflows](https://github.com/BrethofAI/comfyui-workflows)** — ComfyUI workflows tested on the same hardware tier.
- **[awesome-mcp-servers](https://github.com/BrethofAI/awesome-mcp-servers)** — MCP servers you'll wire into your local agents.
- **[anti-dev-tier-list](https://github.com/BrethofAI/anti-dev-tier-list)** — Why some "Linux for AI" defaults from big-tech repos are actively user-hostile.

## Contributing

Open an issue with the distro, your hardware, the kernel and driver
versions you saw, and a plain time-to-CUDA-working measurement. We
update the ranking based on reproducible tests, not vibes.

## License

[MIT](LICENSE).

---

Maintained by **[Brethof AI](https://brethof.com)** — AI tools built for
people who take their data seriously.
