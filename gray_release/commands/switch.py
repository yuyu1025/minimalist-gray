from __future__ import annotations

from gray_release.k8s.kubectl import get_service, patch_service_selector


def run(args) -> int:
    svc = get_service(args.name, args.namespace)
    selector = svc.get("spec", {}).get("selector", {})
    selector["track"] = args.to
    selector.setdefault("app.kubernetes.io/name", args.name)
    out = patch_service_selector(args.name, args.namespace, selector)
    print(out)
    return 0
