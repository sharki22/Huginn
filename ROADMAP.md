# Huginn - Roadmap

## v0.2 - Browser Extension
Browser extension (Chrome/Firefox) for real-time AI tab blocking.

**Features:**
- Detect and close AI-related tabs in real time
- Block navigation to AI domains before page loads
- Extension popup with kill statistics
- Sync with main app via WebSocket or local file

**Files:**
- `extension/manifest.json`
- `extension/background.js`
- `extension/popup.html`

## v0.3 - GUI Whitelist Editor
Simple GUI for managing whitelist without editing text files.

**Features:**
- Tkinter/Qt window with two lists: domains and processes
- Add/remove entries
- Live reload without restart
- Import/export whitelist

## v0.4 - Statistics & Logs
Track and display blocking statistics.

**Features:**
- Log all blocked attempts to file
- Daily/weekly statistics in tray menu
- Export logs as CSV
- Optional: send summary via notify-send on interval

## v0.5 - Silent Mode
Run without any notifications.

**Features:**
- Config option to suppress all notifications
- Tray icon only shows status, no popups
- Silent process killing

## v0.6 - Network-Level Blocking
Alternative blocking via nftables/iptables instead of /etc/hosts.

**Features:**
- Use firewall rules for blocking (more robust)
- Block at network level, not just DNS
- Support for UDP/DNS-over-HTTPS bypass prevention

## v0.7 - Multi-User Support
Block AI for all users on the system.

**Features:**
- Shared /etc/hosts blocking (already works)
- Per-user process monitoring
- Systemd service for root-level process killing

## v0.8 - Cross-Platform Support
Make the tool work on Linux, macOS, and Windows.

**Features:**
- Platform-specific hosts file paths (`/etc/hosts`, `C:\Windows\System32\drivers\etc\hosts`)
- Cross-platform notifications (replace `notify-send` with `plyer` or `notifpy`)
- Platform-specific autostart mechanisms (XDG on Linux, LaunchAgents on macOS, Registry on Windows)
- Conditional network-level blocking (nftables/iptables on Linux, pf on macOS, Windows Firewall)
- Test suite run on all platforms

## Future Ideas
- VPN/Proxy detection and blocking
- AI model detection via file scanning
- Integration with parental control systems
- Mobile companion app (via Termux on Android)
