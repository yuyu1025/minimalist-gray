from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


Color = str


@dataclass(slots=True)
class DeploymentSpec:
    name: str
    namespace: str | None
    replicas: int
    labels: dict[str, str] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ServiceSpec:
    name: str
    namespace: str | None
    selector: dict[str, str]
    labels: dict[str, str] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AppSpec:
    app_name: str
    namespace: str | None
    deployment: DeploymentSpec
    service: ServiceSpec


@dataclass(slots=True)
class BlueGreenPlan:
    app_name: str
    namespace: str | None
    active_color: Color
    preview_services: bool
    resources: list[dict[str, Any]]
