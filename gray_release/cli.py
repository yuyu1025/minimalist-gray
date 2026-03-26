from __future__ import annotations

import argparse
import importlib


def _bind(subparsers, name: str, help_text: str) -> argparse.ArgumentParser:
    return subparsers.add_parser(name, help=help_text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gray-release")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = _bind(subparsers, "init", "Parse and generate blue/green YAML")
    init_parser.add_argument("-f", "--file", required=True)
    init_parser.add_argument("-o", "--output")
    init_parser.add_argument("--config")
    init_parser.add_argument("--active-color", choices=["blue", "green"])
    init_parser.add_argument("--preview-services", action=argparse.BooleanOptionalAction, default=None)

    render_parser = _bind(subparsers, "render", "Render blue/green YAML from source YAML")
    render_parser.add_argument("-f", "--file", required=True)
    render_parser.add_argument("-o", "--output")
    render_parser.add_argument("--config")
    render_parser.add_argument("--active-color", choices=["blue", "green"])
    render_parser.add_argument("--preview-services", action=argparse.BooleanOptionalAction, default=None)

    apply_parser = _bind(subparsers, "apply", "Apply YAML file")
    apply_parser.add_argument("-f", "--file", required=True)

    status_parser = _bind(subparsers, "status", "Show active color from stable Service")
    status_parser.add_argument("--name", required=True)
    status_parser.add_argument("--namespace", required=True)

    switch_parser = _bind(subparsers, "switch", "Switch Service selector.track")
    switch_parser.add_argument("--name", required=True)
    switch_parser.add_argument("--namespace", required=True)
    switch_parser.add_argument("--to", required=True, choices=["blue", "green"])

    rollback_parser = _bind(subparsers, "rollback", "Switch to inactive color")
    rollback_parser.add_argument("--name", required=True)
    rollback_parser.add_argument("--namespace", required=True)

    pods_parser = _bind(subparsers, "pods", "List Pods for app")
    pods_parser.add_argument("--name", required=True)
    pods_parser.add_argument("--namespace", required=True)
    pods_parser.add_argument("--color", choices=["blue", "green"])

    exec_parser = _bind(subparsers, "exec", "Exec into Pod")
    exec_parser.add_argument("--namespace", required=True)
    exec_parser.add_argument("--pod", required=True)
    exec_parser.add_argument("-c", "--container")
    exec_parser.add_argument("command", nargs="*", default=["/bin/sh"])

    log_parser = _bind(subparsers, "log", "View logs")
    log_parser.add_argument("--name", required=True)
    log_parser.add_argument("--namespace", required=True)
    log_parser.add_argument("--pod")
    log_parser.add_argument("--color", choices=["blue", "green"])
    log_parser.add_argument("-c", "--container")
    log_parser.add_argument("-f", "--follow", action="store_true")
    log_parser.add_argument("--since")
    log_parser.add_argument("--previous", action="store_true")
    log_parser.add_argument("--trace")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    module = importlib.import_module(f"gray_release.commands.{args.command}")
    return module.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
