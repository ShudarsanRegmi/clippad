#!/usr/bin/env bash
set -euo pipefail

# Simple per-user installer for clippad
# Installs into ~/.local/clippad by default, creates a venv, installs requirements,
# creates a launcher at ~/.local/bin/clippad and adds a desktop entry + autostart.

INSTALL_DIR="${1:-$HOME/.local/clippad}"
BIN_DIR="${2:-$HOME/.local/bin}"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing Clippad to: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copy project files (exclude VCS)
rsync -a --exclude='.git' --exclude='venv' ./ "$INSTALL_DIR/"

echo "Creating virtualenv in $INSTALL_DIR/venv"
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "$INSTALL_DIR/requirements.txt"

echo "Creating launcher inside $INSTALL_DIR and symlink in $BIN_DIR"
mkdir -p "$BIN_DIR"

# create an internal launcher in the install dir
LAUNCHER="$INSTALL_DIR/clippad"
cat > "$LAUNCHER" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
# Resolve the real directory of this launcher (follow symlinks) so it works whether
# invoked directly or via the symlink in ~/.local/bin.
DIR="$(dirname "$(readlink -f "$0")")"
exec "$DIR/venv/bin/python" -m src.main "${@}"
EOF
chmod +x "$LAUNCHER"

# create symlink in BIN_DIR; if a non-symlink file exists, back it up first
LINK="$BIN_DIR/clippad"
if [ -e "$LINK" ] && [ ! -L "$LINK" ]; then
	BACKUP="$LINK.bak.$(date +%s)"
	echo "Backing up existing $LINK to $BACKUP"
	mv "$LINK" "$BACKUP"
fi
rm -f "$LINK"
ln -s "$LAUNCHER" "$LINK"

echo "Creating desktop entry and autostart"
mkdir -p "$DESKTOP_DIR" "$AUTOSTART_DIR"
cat > "$DESKTOP_DIR/clippad.desktop" <<EOF
[Desktop Entry]
Name=Clippad
Comment=Minimal clipboard manager
Exec=$LAUNCHER
Terminal=false
Type=Application
Categories=Utility;
EOF

cat > "$AUTOSTART_DIR/clippad.desktop" <<EOF
[Desktop Entry]
Type=Application
Exec=$LAUNCHER
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Clippad
Comment=Start Clippad at login
EOF

echo
echo "Installation complete. Make sure $BIN_DIR is in your PATH."
echo "You can start Clippad with: clippad"
echo "To uninstall run: ./uninstall.sh or remove $INSTALL_DIR and created files manually."
