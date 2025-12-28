#!/usr/bin/env bash
set -euo pipefail

# Uninstall clippad installed by install.sh
INSTALL_DIR="${1:-$HOME/.local/clippad}"
BIN_DIR="${2:-$HOME/.local/bin}"


echo "Removing symlink launcher in $BIN_DIR"
if [ -L "$BIN_DIR/clippad" ]; then
	rm -f "$BIN_DIR/clippad"
else
	echo "No symlink $BIN_DIR/clippad found (skipping)"
fi

echo "Removing $INSTALL_DIR"
rm -rf "$INSTALL_DIR"

echo "Removing desktop entries"
rm -f "$HOME/.local/share/applications/clippad.desktop"
rm -f "$HOME/.config/autostart/clippad.desktop"

echo "Uninstall complete."
