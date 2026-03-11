from __future__ import annotations

from copy import deepcopy
from typing import Any

from gray_release.models import AppSpec


def make_services(app: AppSpec, active_color: str = "blue", preview_services: bool = True) -> list[dict[str, Any]]:
    resources: list[dict[str, Any]] = []

    stable_service = deepcopy(app.service.raw)
    stable_service.setdefault("spec", {}).setdefault("selector", {})["app.kubernetes.io/name"] = app.app_name
    stable_service["spec"]["selector"]["track"] = active_color
    resources.append(stable_service)

    if preview_services:
        for color in ("blue", "green"):
            svc = deepcopy(app.service.raw)
            svc.setdefault("metadata", {})["name"] = f"{app.service.name}-{color}"
            svc.setdefault("spec", {}).setdefault("selector", {})["app.kubernetes.io/name"] = app.app_name
            svc["spec"]["selector"]["track"] = color
            resources.append(svc)

    return resources
