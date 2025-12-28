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
