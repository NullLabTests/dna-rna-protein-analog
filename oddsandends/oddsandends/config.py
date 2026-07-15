import json
import os
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(os.environ.get("ODDS_CONFIG_DIR", Path.home() / ".config" / "oddsandends"))
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_MODEL = "gpt-4o"


def _ensure_config() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps({"default_model": DEFAULT_MODEL, "aliases": {}}, indent=2))


def get(key: str, default: Any = None) -> Any:
    _ensure_config()
    data = json.loads(CONFIG_FILE.read_text())
    return data.get(key, default)


def set_config(key: str, value: Any) -> dict:
    _ensure_config()
    data = json.loads(CONFIG_FILE.read_text())
    data[key] = value
    CONFIG_FILE.write_text(json.dumps(data, indent=2))
    return data


def get_default_model() -> str:
    return get("default_model", DEFAULT_MODEL)


def set_default_model(model: str) -> None:
    set_config("default_model", model)


def show() -> dict:
    _ensure_config()
    return json.loads(CONFIG_FILE.read_text())
