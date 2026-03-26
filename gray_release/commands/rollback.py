from __future__ import annotations

from types import SimpleNamespace

from gray_release.commands.switch import run as run_switch
from gray_release.k8s.kubectl import get_service


def run(args) -> int:
    svc = get_service(args.name, args.namespace)
    active = svc.get("spec", {}).get("selector", {}).get("track", "blue")
    target = "green" if active == "blue" else "blue"
    switch_args = SimpleNamespace(name=args.name, namespace=args.namespace, to=target)
    return run_switch(switch_args)
