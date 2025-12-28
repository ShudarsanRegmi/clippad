"""Entry point for clippad using PyQt5."""

import sys
import time
from src.storage import Storage
from src.gui import Manager

from pynput import keyboard
from pynput.keyboard import Controller

from PyQt5 import QtWidgets

controller = Controller()


def paste_slot(storage: Storage, idx: int, app: QtWidgets.QApplication = None):
    content = storage.get_slot(idx)
    if not content:
        return
    # prefer Qt clipboard if app provided
    if app is not None:
        app.clipboard().setText(content)
    else:
        try:
            import pyperclip

            pyperclip.copy(content)
        except Exception:
            pass
    # small delay to ensure clipboard is set
    time.sleep(0.05)
    # simulate Ctrl+V
    controller.press(keyboard.Key.ctrl)
    controller.press('v')
    controller.release('v')
    controller.release(keyboard.Key.ctrl)


def make_hotkey_mapping(storage: Storage, manager: Manager, app: QtWidgets.QApplication):
    mapping = {}
    for i in range(1, 10):
        mapping[f"<ctrl>+<alt>+{i}"] = lambda i=i: paste_slot(storage, i, app)
        mapping[f"<ctrl>+<alt>+<shift>+{i}"] = lambda i=i: manager.open_editor_signal.emit(i)
    mapping["<ctrl>+<alt>+0"] = lambda: manager.show()
    return mapping


def start_listener(mapping):
    hk = keyboard.GlobalHotKeys(mapping)
    hk.start()
    return hk


def main():
    app = QtWidgets.QApplication(sys.argv)
    # do not quit the app when the last window is closed; keep tray icon and hotkeys active
    app.setQuitOnLastWindowClosed(False)
    storage = Storage()
    manager = Manager(storage)

    mapping = make_hotkey_mapping(storage, manager, app)
    hk = start_listener(mapping)

    manager.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
