from __future__ import annotations

from gray_release.k8s.kubectl import apply_file


def run(args) -> int:
    result = apply_file(args.file)
    print(result)
    return 0
