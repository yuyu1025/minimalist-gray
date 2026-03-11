from __future__ import annotations

from gray_release.config import load_release_config
from gray_release.io.yaml import dump_yaml_documents, load_yaml_documents
from gray_release.k8s.loader import build_app_spec
from gray_release.transform.deployment import make_blue_green_deployments
from gray_release.transform.service import make_services


def run(args) -> int:
    cfg = load_release_config(args.config)
    resources = load_yaml_documents(args.file)
    app = build_app_spec(resources, app_name=cfg.app_name)

    active_color = args.active_color or cfg.active_color
    preview_services = args.preview_services if args.preview_services is not None else cfg.preview_services

    generated = [
        *make_blue_green_deployments(app, active_color=active_color),
        *make_services(app, active_color=active_color, preview_services=preview_services),
    ]

    if args.output:
        dump_yaml_documents(generated, path=args.output)
        print(f"Rendered blue/green resources to: {args.output}")
        return 0

    print(dump_yaml_documents(generated))
    return 0
