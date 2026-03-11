from __future__ import annotations

import subprocess


def run(args) -> int:
    cmd = [
        "kubectl",
        "exec",
        "-it",
        "-n",
        args.namespace,
        args.pod,
    ]
    if args.container:
        cmd.extend(["-c", args.container])
    cmd.extend(["--", *args.command])
    return subprocess.call(cmd)
