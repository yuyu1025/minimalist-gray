from __future__ import annotations

from typing import Any

from gray_release.models import AppSpec, DeploymentSpec, ServiceSpec


class ResourceLoadError(ValueError):
    pass


def _get_name(resource: dict[str, Any]) -> str:
    return resource.get("metadata", {}).get("name", "")


def _get_namespace(resource: dict[str, Any]) -> str | None:
    return resource.get("metadata", {}).get("namespace")


def build_app_spec(resources: list[dict[str, Any]], app_name: str | None = None) -> AppSpec:
    deployment = None
    service = None

    for resource in resources:
        kind = resource.get("kind")
        if kind == "Deployment" and deployment is None:
            deployment = resource
        elif kind == "Service" and service is None:
            service = resource

    if deployment is None:
        raise ResourceLoadError("No Deployment resource found in input YAML.")
    if service is None:
        raise ResourceLoadError("No Service resource found in input YAML.")

    dep_name = _get_name(deployment)
    svc_name = _get_name(service)
    namespace = _get_namespace(deployment) or _get_namespace(service)

    dep_labels = deployment.get("spec", {}).get("template", {}).get("metadata", {}).get("labels", {})
    service_selector = service.get("spec", {}).get("selector", {})
    inferred_app_name = (
        app_name
        or dep_labels.get("app.kubernetes.io/name")
        or service_selector.get("app.kubernetes.io/name")
        or dep_name
    )

    return AppSpec(
        app_name=inferred_app_name,
        namespace=namespace,
        deployment=DeploymentSpec(
            name=dep_name,
            namespace=namespace,
            replicas=deployment.get("spec", {}).get("replicas", 1),
            labels=deployment.get("metadata", {}).get("labels", {}),
            raw=deployment,
        ),
        service=ServiceSpec(
            name=svc_name,
            namespace=namespace,
            selector=service_selector,
            labels=service.get("metadata", {}).get("labels", {}),
            raw=service,
        ),
    )
