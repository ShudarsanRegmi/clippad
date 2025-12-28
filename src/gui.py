from PyQt5 import QtWidgets, QtGui, QtCore
from typing import Dict


class Manager(QtWidgets.QMainWindow):
    """PyQt5-based manager with a 3x3 grid, editor dialogs, and system tray.

    Thread-safe entry from other threads: emit `open_editor_signal`.
    """

    open_editor_signal = QtCore.pyqtSignal(int)

    def __init__(self, storage):
        super().__init__()
        self.storage = storage
        self.setWindowTitle("Clippad")
        self.resize(480, 480)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QGridLayout()
        central.setLayout(layout)

        self.buttons: Dict[int, QtWidgets.QPushButton] = {}
        for n in range(1, 10):
            r = (n - 1) // 3
            c = (n - 1) % 3
            bt = QtWidgets.QPushButton(str(n))
            bt.setMinimumSize(120, 120)
            bt.setStyleSheet("font-size: 16px; text-align: left; padding: 8px;")
            bt.clicked.connect(lambda checked, n=n: self.open_editor(n))
            layout.addWidget(bt, r, c)
            self.buttons[n] = bt

        self._refresh_buttons()

        # tray icon
        self.tray = QtWidgets.QSystemTrayIcon(self)
        ico = QtGui.QIcon()  # default
        self.tray.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogInfoView))
        menu = QtWidgets.QMenu()
        show_action = menu.addAction("Show")
        hide_action = menu.addAction("Hide")
        quit_action = menu.addAction("Quit")
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray)
        self.tray.show()

        self.open_editor_signal.connect(self.open_editor)

    def _on_tray(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()

    def _preview(self, text: str) -> str:
        txt = text.strip().splitlines()[0] if text.strip() else ""
        return (txt[:40] + "...") if len(txt) > 43 else txt

    def _refresh_buttons(self):
        for n, bt in self.buttons.items():
            text = self.storage.get_slot(n)
            preview = self._preview(text)
            bt.setText(f"{n}\n{preview}")

    def open_editor(self, idx: int):
        current = self.storage.get_slot(idx)
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle(f"Edit slot {idx}")
        dlg.resize(600, 400)
        v = QtWidgets.QVBoxLayout(dlg)
        txt = QtWidgets.QTextEdit()
        txt.setPlainText(current)
        txt.setFontPointSize(12)
        v.addWidget(txt)

        btns = QtWidgets.QHBoxLayout()
        v.addLayout(btns)
        btns.addStretch()
        save_btn = QtWidgets.QPushButton("Save")
        btns.addWidget(save_btn)

        def save_and_close():
            content = txt.toPlainText()
            self.storage.set_slot(idx, content)
            self._refresh_buttons()
            dlg.accept()

        save_btn.clicked.connect(save_and_close)

        # numeric navigation inside dialog
        def keyPressEvent(event: QtGui.QKeyEvent):
            k = event.key()
            if QtCore.Qt.Key_0 <= k <= QtCore.Qt.Key_9:
                digit = k - QtCore.Qt.Key_0
                if 1 <= digit <= 9:
                    dlg.accept()
                    QtCore.QTimer.singleShot(50, lambda d=digit: self.open_editor(d))

        dlg.keyPressEvent = keyPressEvent
        dlg.exec_()

    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Intercept window close (X) and hide instead so the app keeps running in tray."""
        # hide the window and ignore the close so the application stays alive
        self.hide()
        event.ignore()

