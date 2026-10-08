#!/usr/bin/env python3
"""Aplica docs/sitio.yml: perfil del autor y nombres/descripciones de categorías."""
import importlib.util
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("publish", ROOT / "scripts" / "publish.py")
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)


def main():
    cfg = yaml.safe_load((ROOT / "docs" / "sitio.yml").read_text(encoding="utf-8"))
    wp = pub.WP(pub.env("WP_URL"), pub.env("WP_USER"), pub.env("WP_APP_PASSWORD"))
    wp.whoami()
    errors = 0

    autor = cfg.get("autor") or {}
    if autor:
        try:
            me = wp.req("POST", "users/me", json=autor)
            print(f"Autor actualizado: {me.get('name')}")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR autor: {e}")

    for c in cfg.get("categorias") or []:
        try:
            found = wp.req("GET", "categories", params={"slug": c["slug"]})
            payload = {"name": c["name"], "description": c.get("description", "")}
            if found:
                wp.req("POST", f"categories/{found[0]['id']}", json=payload)
                print(f"Categoría actualizada: {c['slug']} -> {c['name']}")
            else:
                wp.req("POST", "categories", json={**payload, "slug": c["slug"]})
                print(f"Categoría creada: {c['slug']} -> {c['name']}")
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR categoría {c.get('slug')}: {e}")

    if errors:
        sys.exit(f"{errors} error(es)")


if __name__ == "__main__":
    main()
