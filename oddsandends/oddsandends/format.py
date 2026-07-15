import json
import csv
import io
import yaml


def to_json(data, indent: int = 2) -> str:
    return json.dumps(data, indent=indent, default=str)


def to_yaml(data) -> str:
    return yaml.dump(data, default_flow_style=False, sort_keys=False)


def to_csv(data: list[dict]) -> str:
    if not data:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def to_table(data: list[dict]) -> str:
    if not data:
        return ""
    keys = data[0].keys()
    col_widths = {k: len(k) for k in keys}
    for row in data:
        for k in keys:
            col_widths[k] = max(col_widths[k], len(str(row.get(k, ""))))
    sep = "+" + "+".join("-" * (w + 2) for w in col_widths.values()) + "+"
    header = "|" + "|".join(
        f" {k.center(col_widths[k])} " for k in keys
    ) + "|"
    lines = [sep, header, sep]
    for row in data:
        line = "|" + "|".join(
            f" {str(row.get(k, '')).ljust(col_widths[k])} " for k in keys
        ) + "|"
        lines.append(line)
    lines.append(sep)
    return "\n".join(lines)


def from_json(text: str):
    return json.loads(text)


def from_yaml(text: str):
    return yaml.safe_load(text)


def from_csv(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text)))
