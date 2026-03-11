from __future__ import annotations

import json
import subprocess


class KubectlError(RuntimeError):
    pass


def run_kubectl(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["kubectl", *args]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if check and completed.returncode != 0:
        raise KubectlError(completed.stderr.strip() or completed.stdout.strip())
    return completed


def apply_file(path: str) -> str:
    out = run_kubectl(["apply", "-f", path]).stdout.strip()
    return out


def get_service(name: str, namespace: str) -> dict:
    out = run_kubectl(["get", "svc", name, "-n", namespace, "-o", "json"]).stdout
    return json.loads(out)


def patch_service_selector(name: str, namespace: str, selector: dict[str, str]) -> str:
    payload = {"spec": {"selector": selector}}
    out = run_kubectl(
        ["patch", "svc", name, "-n", namespace, "--type", "merge", "-p", json.dumps(payload)]
    ).stdout.strip()
    return out
