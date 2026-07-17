#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOSTART_DIR="$HOME/.config/autostart"
AUTOSTART_FILE="$AUTOSTART_DIR/huginn.desktop"

echo "=== Huginn Installer ==="

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found" >&2
    exit 1
fi

if ! command -v poetry &>/dev/null; then
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "Installing dependencies..."
cd "$SCRIPT_DIR"
poetry install --no-interaction
echo "Done."

read -rp "Add to autostart? (y/N): " choice
if [[ "$choice" =~ ^[Yy]$ ]]; then
    mkdir -p "$AUTOSTART_DIR"
    cat > "$AUTOSTART_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Huginn
Comment=Blocks AI websites and local AI processes
Exec=cd $SCRIPT_DIR && poetry run huginn
Icon=application-exit
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF
    echo "Autostart: $AUTOSTART_FILE"
fi

echo ""
echo "=== Installed ==="
echo "Run:  sudo poetry run huginn"
