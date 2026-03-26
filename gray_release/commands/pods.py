from __future__ import annotations

from gray_release.k8s.kubectl import run_kubectl


def run(args) -> int:
    selector = f"app.kubernetes.io/name={args.name}"
    if args.color:
        selector += f",track={args.color}"
    out = run_kubectl(["get", "pods", "-n", args.namespace, "-l", selector, "-o", "wide"]).stdout
    print(out.strip())
    return 0
