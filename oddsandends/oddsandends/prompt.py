import json
import re
from pathlib import Path
from typing import Any

VARIABLE_PATTERN = re.compile(r'\{\{(\w+)\}\}')


def render(template: str, **kwargs: Any) -> str:
    def _replace(m: re.Match) -> str:
        key = m.group(1)
        if key not in kwargs:
            raise KeyError(f"Missing variable: {key}")
        val = kwargs[key]
        if isinstance(val, (dict, list)):
            return json.dumps(val, indent=2)
        return str(val)

    return VARIABLE_PATTERN.sub(_replace, template)


def extract_variables(template: str) -> list[str]:
    return VARIABLE_PATTERN.findall(template)


def load_template(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return p.read_text()


def system_prompt(content: str) -> dict:
    return {"role": "system", "content": content}


def user_prompt(content: str) -> dict:
    return {"role": "user", "content": content}


def assistant_prompt(content: str) -> dict:
    return {"role": "assistant", "content": content}


def build_messages(
    system: str = "",
    user: str = "",
    history: list[dict] | None = None,
) -> list[dict]:
    messages = []
    if system:
        messages.append(system_prompt(system))
    if history:
        messages.extend(history)
    if user:
        messages.append(user_prompt(user))
    return messages
