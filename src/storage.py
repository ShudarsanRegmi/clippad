import json
from pathlib import Path
from typing import Dict

CONFIG_DIR = Path.home() / ".config" / "clippad"
DATA_FILE = CONFIG_DIR / "data.json"
NUM_SLOTS = 9


def ensure_data_file() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        default = {str(i): "" for i in range(1, NUM_SLOTS + 1)}
        DATA_FILE.write_text(json.dumps(default, indent=2), encoding="utf-8")


class Storage:
    """Simple JSON-backed storage for 9 clipboard slots."""

    def __init__(self) -> None:
        ensure_data_file()
        self._path = DATA_FILE
        self._data = self._read()

    def _read(self) -> Dict[str, str]:
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            # if corrupted, reset to defaults
            default = {str(i): "" for i in range(1, NUM_SLOTS + 1)}
            self._write(default)
            return default

    def _write(self, data: Dict[str, str]) -> None:
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_slot(self, idx: int) -> str:
        return self._data.get(str(idx), "")

    def set_slot(self, idx: int, value: str) -> None:
        self._data[str(idx)] = value
        self._write(self._data)

    def all_slots(self) -> Dict[str, str]:
        return dict(self._data)
