from __future__ import annotations

from gray_release.commands.render import run as run_render


def run(args) -> int:
    return run_render(args)
