from __future__ import annotations

from pathlib import Path
from typing import Any


class YamlDependencyError(RuntimeError):
    pass


def _yaml_backend():
    try:
        from ruamel.yaml import YAML  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on env
        raise YamlDependencyError(
            "ruamel.yaml is required. Install dependencies first: pip install -e ."
        ) from exc

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.explicit_start = True
    yaml.width = 4096
    return yaml


def load_yaml_documents(path: str) -> list[dict[str, Any]]:
    file_path = Path(path)
    yaml = _yaml_backend()
    with file_path.open("r", encoding="utf-8") as f:
        docs = [doc for doc in yaml.load_all(f) if doc is not None]
    return docs


def dump_yaml_documents(documents: list[dict[str, Any]], path: str | None = None) -> str:
    yaml = _yaml_backend()
    if path:
        with Path(path).open("w", encoding="utf-8") as f:
            yaml.dump_all(documents, f)
        return path

    from io import StringIO

    buffer = StringIO()
    yaml.dump_all(documents, buffer)
    return buffer.getvalue()
