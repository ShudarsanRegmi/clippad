# Clippad — minimal clipboard manager

Clippad is a tiny, keyboard-driven clipboard manager that keeps 9 frequently-used snippets.
This version uses PyQt5 for a clean, responsive UI. It provides a tray icon, a 3x3 grid manager, and global hotkeys.

Features
- 9 slots (1..9)
- Ctrl+Alt+1..9 — paste slot into current focus (sets clipboard and sends Ctrl+V)
- Ctrl+Alt+Shift+1..9 — open editor for that slot
- Ctrl+Alt+0 — open the manager window (3x3 grid)
- System tray icon for show/hide and quit

Quick start
1. Create a virtualenv and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:

```bash
python -m src.main
```

Notes & permissions
- On some Linux setups, global hotkeys may require additional permissions or a running X11/Wayland support; `pynput` works commonly with X11. If you get errors, check whether `python3-pyqt5` is installed and whether `pynput` can access input devices in your environment.
- `pyperclip` uses the system clipboard. On Linux it may need `xclip` or `xsel` installed; install via your distro package manager if clipboard operations fail. This implementation prefers the Qt clipboard when available.

Next steps
- Improve visuals (icons and styling)
- Add import/export for snippets
- Add locking or encryption for sensitive snippets

Installation (one-step installer)

To install Clippad for the current user (copies the project to ~/.local/clippad, creates a venv, installs deps, creates a launcher in ~/.local/bin and enables autostart):

```bash
./install.sh
```

After install ensure `~/.local/bin` is in your PATH (many distros add it automatically). Start Clippad with:

```bash
clippad
```

To uninstall the installed copy:

```bash
./uninstall.sh
```

If you prefer not to use the installer, you can run directly from the repo during development:

```bash
./clippad      # runs python -m src.main
```

Notes
- The installer is per-user and does not require sudo.
- If you prefer system-wide installation, change paths in `install.sh` accordingly.
- Autostart is implemented using a desktop autostart entry (`~/.config/autostart/clippad.desktop`) which works with most Linux desktop environments.

Systemd user service (optional)

If you prefer using systemd user units (more robust autostart and restart on failure), you can enable the provided template at `packaging/clippad.service`:

1. Edit `packaging/clippad.service` and update the `ExecStart` path to point to the installed venv python (e.g. `/home/youruser/.local/clippad/venv/bin/python -m src.main`).
2. Copy it to `~/.config/systemd/user/clippad.service` and enable:

```bash
mkdir -p ~/.config/systemd/user
cp packaging/clippad.service ~/.config/systemd/user/clippad.service
systemctl --user daemon-reload
systemctl --user enable --now clippad.service
```

To stop and disable:

```bash
systemctl --user disable --now clippad.service
```
