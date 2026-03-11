from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from gray_release.io.yaml import load_yaml_documents


@dataclass(slots=True)
class ReleaseConfig:
    namespace: str | None = None
    app_name: str | None = None
    active_color: str = "blue"
    preview_services: bool = True


DEFAULT_CONFIG_FILE = "gray-release.yaml"


def load_release_config(config_path: str | None = None) -> ReleaseConfig:
    if not config_path:
        candidate = Path(DEFAULT_CONFIG_FILE)
        if not candidate.exists():
            return ReleaseConfig()
        config_path = str(candidate)

    docs = load_yaml_documents(config_path)
    if not docs:
        return ReleaseConfig()

    cfg: dict[str, Any] = docs[0] or {}
    spec = cfg.get("spec", {})
    return ReleaseConfig(
        namespace=spec.get("namespace"),
        app_name=spec.get("appName"),
        active_color=spec.get("activeColor", "blue"),
        preview_services=bool(spec.get("previewServices", True)),
    )
