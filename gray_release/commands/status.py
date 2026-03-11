from __future__ import annotations

from gray_release.k8s.kubectl import get_service


def run(args) -> int:
    svc = get_service(args.name, args.namespace)
    selector = svc.get("spec", {}).get("selector", {})
    active_color = selector.get("track", "unknown")
    inactive_color = "green" if active_color == "blue" else "blue"

    print(f"name: {args.name}")
    print(f"namespace: {args.namespace}")
    print(f"active color: {active_color}")
    print(f"inactive color: {inactive_color}")
    print(f"selector: {selector}")
    return 0
