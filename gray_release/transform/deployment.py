from __future__ import annotations

from copy import deepcopy
from typing import Any

from gray_release.models import AppSpec


def make_blue_green_deployments(app: AppSpec, active_color: str = "blue") -> list[dict[str, Any]]:
    original = app.deployment.raw
    original_replicas = app.deployment.replicas

    generated: list[dict[str, Any]] = []
    for color in ("blue", "green"):
        dep = deepcopy(original)
        dep.setdefault("metadata", {})["name"] = f"{app.deployment.name}-{color}"

        dep_spec = dep.setdefault("spec", {})
        dep_spec["replicas"] = original_replicas if color == active_color else 0

        selector = dep_spec.setdefault("selector", {}).setdefault("matchLabels", {})
        selector.setdefault("app.kubernetes.io/name", app.app_name)
        selector["track"] = color

        pod_meta = dep_spec.setdefault("template", {}).setdefault("metadata", {})
        labels = pod_meta.setdefault("labels", {})
        labels.setdefault("app.kubernetes.io/name", app.app_name)
        labels["track"] = color

        generated.append(dep)

    return generated
