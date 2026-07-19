<div align="center">
  <img src="assets/logo.png" alt="Huginn Logo" style="border-radius: 25px; width: 220px;">
  <br>
  <img src="https://img.shields.io/badge/Huginn-AI%20Blocker-red?style=for-the-badge&logo=robot&logoColor=white" alt="Huginn">

# 🐦‍⬛ Huginn

**No more AI distractions. Period.**

Kills local AI processes & blocks AI websites straight from your system tray.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-00ff00?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-58%20passing-brightgreen?style=flat-square)]()
[![Platform](https://img.shields.io/badge/platform-linux-FCC624?style=flat-square&logo=linux&logoColor=black)]()

<br>

**Stop ChatGPT. Stop Claude. Stop Ollama.** All of it. Gone.

</div>

---

## ⚡ What it does

```
   you → open chatgpt.com → 💀 blocked
   you → run ollama       → 💀 killed
   you → start comfyui    → 💀 killed
```

| Layer | How | Effect |
|:-----:|:---:|:------:|
| DNS | `/etc/hosts` rewrite | AI sites don't load |
| Process | `SIGTERM` → `SIGKILL` | Local AI tools crash instantly |
| Tray | `pystray` icon | You're in control |

Desktop notification when something gets axed:

```
🚫 Huginn — Blocked: ollama (PID 12345)
```

## 🚀 Quick start

```bash
git clone https://github.com/kyrie/Huginn.git && cd Huginn
chmod +x install.sh && ./install.sh
```

Or manually:

```bash
poetry install
sudo poetry run huginn    # needs sudo for /etc/hosts
```

> ⚠️ `sudo` is required — the tool modifies `/etc/hosts` to block AI domains.

## 🎮 Tray menu

Right-click the tray icon:

| Menu item | What it does |
|:----------|:-------------|
| **Monitoring: ON/OFF** | Pause/resume process scanning |
| **Killed: N \| Hosts: M** | Live stats |
| **Reblock hosts** | Refresh `/etc/hosts` |
| **Unblock hosts** | Restore `/etc/hosts` |
| **Quit** | Exit & clean up |

## 🚫 What gets blocked

<details>
<summary><b>🌐 Websites (50+)</b></summary>

| Service | Domains |
|:--------|:--------|
| OpenAI | `chatgpt.com` · `openai.com` · `chat.openai.com` |
| Anthropic | `claude.ai` · `anthropic.com` |
| Google AI | `gemini.google.com` · `bard.google.com` · `aistudio.google.com` · `labs.google` · `notebooklm.google` |
| Microsoft | `copilot.microsoft.com` · `copilot.cloud.microsoft` · `bing.com/chat` |
| Meta | `ai.meta.com` · `llama.meta.com` |
| Mistral | `mistral.ai` · `chat.mistral.ai` |
| DeepSeek | `deepseek.com` · `chat.deepseek.com` |
| Image Gen | `midjourney.com` · `stability.ai` · `leonardo.ai` · `civitai.com` · `ideogram.ai` · `flux1.ai` · `dalle.com` |
| Other AI | `perplexity.ai` · `you.com` · `phind.com` · `poe.com` · `character.ai` · `huggingface.co` · `together.ai` · `groq.com` · `cohere.com` · `kimi.moonshot.cn` · `reka.ai` |

</details>

<details>
<summary><b>⚙️ Processes (30+)</b></summary>

| Category | Names |
|:---------|:------|
| LLM runners | `ollama` · `llama.cpp` · `vllm` · `triton` |
| Web UIs | `lmstudio` · `gpt4all` · `koboldcpp` · `jan` · `text-generation-webui` |
| Image gen | `comfyui` · `automatic1111` · `invokeai` · `stable-diffusion-webui` |
| Assistants | `open-interpreter` · `aider` · `continue` · `tabby` |

</details>

## 🧪 Running tests

```bash
poetry install
poetry run pytest tests/ -v
```

58 tests covering config, hosts blocking, process monitoring, and tray icon.

## 🏗️ How it works

```
┌──────────────────────────────────────────────────┐
│                 Huginn (system tray)              │
├────────────────────┬─────────────────────────────┤
│    HostsBlocker    │      ProcessMonitor          │
│                    │                              │
│  • writes to       │  • scans every 5s            │
│    /etc/hosts      │  • matches process names     │
│  • restores on     │  • terminate → wait → kill   │
│    quit            │  • desktop notifications     │
└────────────────────┴─────────────────────────────┘
```

1. **Startup** — injects AI domains into `/etc/hosts`, spawns monitor thread
2. **Runtime** — `psutil.process_iter()` every 5s, kills matches
3. **Quit** — restores `/etc/hosts`, exits clean

## 📁 Project structure

```
Huginn/
├── huginn/
│   ├── __init__.py
│   ├── app.py          # tray icon + main loop
│   ├── config.py       # domains, processes, settings
│   ├── hosts.py        # /etc/hosts management
│   ├── main.py         # entry point
│   └── monitor.py      # process scanning
├── tests/
│   ├── test_config.py  # 15 tests
│   ├── test_hosts.py   # 11 tests
│   ├── test_monitor.py # 18 tests
│   └── test_app.py     # 8 tests
├── install.sh
├── pyproject.toml
├── LICENSE             # MIT
└── README.md
```

## 🗑️ Uninstall

```bash
# remove autostart
rm ~/.config/autostart/huginn.desktop

# restore /etc/hosts (if didn't quit cleanly)
sudo sed -i '/# === Huginn ===/,/# === Huginn ===/d' /etc/hosts

# nuke the project
rm -rf /path/to/Huginn
```

## 🗺️ Roadmap

- [ ] 🌐 Browser extension (Chrome/Firefox)
- [ ] 🎨 GUI whitelist editor
- [ ] 📊 Statistics & logging
- [ ] 🔇 Silent mode
- [ ] 🔥 nftables/iptables blocking

See [ROADMAP.md](ROADMAP.md) for details.

## 📄 License

[MIT](LICENSE) — do whatever you want.
