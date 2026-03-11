from __future__ import annotations

from gray_release.k8s.kubectl import run_kubectl


def run(args) -> int:
    kubectl_args = ["logs", "-n", args.namespace]
    if args.pod:
        kubectl_args.append(args.pod)
    else:
        selector = f"app.kubernetes.io/name={args.name}"
        if args.color:
            selector += f",track={args.color}"
        kubectl_args.extend(["-l", selector])

    if args.container:
        kubectl_args.extend(["-c", args.container])
    if args.follow:
        kubectl_args.append("-f")
    if args.since:
        kubectl_args.extend(["--since", args.since])
    if args.previous:
        kubectl_args.append("--previous")

    out = run_kubectl(kubectl_args).stdout
    if args.trace:
        for line in out.splitlines():
            if args.trace in line:
                print(line)
        return 0

    print(out.strip())
    return 0
