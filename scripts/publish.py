#!/usr/bin/env python3
"""Publica archivos Markdown con frontmatter en WordPress vía API REST.

Uso:
    python scripts/publish.py content/glosario/brief-creativo.md [...]
    python scripts/publish.py --all

Variables de entorno requeridas:
    WP_URL           https://www.publimerca.com
    WP_USER          usuario de WordPress (aiagent)
    WP_APP_PASSWORD  contraseña de aplicación

Frontmatter soportado:
    title:        título (obligatorio)
    slug:         slug de la URL (obligatorio)
    type:         post | page (por defecto post)
    status:       draft | publish | pending | private (por defecto draft)
    excerpt:      extracto / descripción corta
    categories:   lista de slugs de categoría (se crean si no existen)
    tags:         lista de nombres de etiqueta (se crean si no existen)
    parent:       slug de la página padre (solo páginas)

Si ya existe una entrada o página con el mismo slug, se actualiza en lugar de duplicarse.
"""
import argparse
import base64
import os
import pathlib
import sys

import markdown
import requests
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
VALID_STATUS = {"draft", "publish", "pending", "private"}


def env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit(f"Falta la variable de entorno {name}")
    return value


class WP:
    def __init__(self, base, user, password):
        # Resolver redirecciones (http->https, sin www->www) antes de autenticar:
        # requests descarta el encabezado Authorization al cambiar de host.
        probe = requests.get(base.rstrip("/") + "/wp-json/", timeout=30,
                             headers={"User-Agent": "publimerca-agente/1.0"})
        final = probe.url.split("/wp-json")[0]
        if final.rstrip("/") != base.rstrip("/"):
            print(f"Aviso: {base} redirige a {final}; uso la URL final.")
        print(f"Endpoint: {final}/wp-json/ (HTTP {probe.status_code})")
        try:
            auth = list((probe.json().get("authentication") or {}).keys())
            print(f"Métodos de autenticación anunciados: {', '.join(auth) or 'ninguno'}")
        except ValueError:
            print("Aviso: /wp-json/ no devolvió JSON")
        self.api = final.rstrip("/") + "/wp-json/wp/v2"
        self.s = requests.Session()
        self.s.auth = (user, password.replace(" ", ""))
        self.s.headers["User-Agent"] = "publimerca-agente/1.0"
        # Copia de la credencial en un encabezado propio, por si el servidor borra Authorization
        # (lo recibe el mu-plugin wordpress/mu-plugins/publimerca-auth.php).
        token = base64.b64encode(f"{user}:{password.replace(' ', '')}".encode()).decode()
        self.s.headers["X-Publimerca-Auth"] = f"Basic {token}"
        self._term_cache = {}

    def req(self, method, path, **kw):
        r = self.s.request(method, f"{self.api}/{path}", timeout=30, **kw)
        if r.status_code >= 400:
            raise RuntimeError(f"{method} {path} -> {r.status_code}: {r.text[:300]}")
        return r.json()

    def whoami(self):
        import time
        params = {"context": "edit", "_nc": str(int(time.time() * 1000))}
        r = self.s.get(f"{self.api}/users/me", params=params, timeout=30,
                       headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
        if r.status_code == 200:
            return r.json()
        print(f"Servidor: {r.headers.get('server', '?')} | via: {r.headers.get('via', '-')} "
              f"| cf-ray: {'sí' if 'cf-ray' in r.headers else 'no'}")
        interesting = {k: v for k, v in r.headers.items()
                       if any(s in k.lower() for s in ("cache", "litespeed", "x-", "allow", "www-auth", "set-cookie"))}
        for k, v in interesting.items():
            print(f"  encabezado {k}: {v[:120]}")
        print(f"Respuesta con credencial real: {r.status_code} {r.json().get('code') if r.headers.get('content-type','').startswith('application/json') else r.text[:120]}")
        fake = base64.b64encode(f"{self.s.auth[0]}:xxxxxxxxxxxxxxxxxxxxxxxx".encode()).decode()
        bogus = requests.get(f"{self.api}/users/me", auth=(self.s.auth[0], "xxxxxxxxxxxxxxxxxxxxxxxx"),
                             headers={**self.s.headers, "X-Publimerca-Auth": f"Basic {fake}"}, timeout=30)
        code = bogus.json().get("code") if bogus.headers.get("content-type", "").startswith("application/json") else bogus.text[:120]
        print(f"Respuesta con contraseña falsa: {bogus.status_code} {code}")
        if code == "rest_not_logged_in":
            sys.exit("DIAGNÓSTICO: el encabezado Authorization NO llega a WordPress (lo borra el servidor o un plugin).")
        sys.exit("DIAGNÓSTICO: el encabezado SÍ llega; la credencial real es la que falla (usuario o contraseña).")

    def find_by_slug(self, endpoint, slug):
        res = self.req("GET", endpoint, params={"slug": slug, "status": "any", "context": "edit"})
        return res[0] if res else None

    def term_id(self, taxonomy, value, by="slug"):
        key = (taxonomy, value)
        if key in self._term_cache:
            return self._term_cache[key]
        params = {"slug": value} if by == "slug" else {"search": value}
        found = [t for t in self.req("GET", taxonomy, params=params)
                 if (t["slug"] == value if by == "slug" else t["name"].lower() == value.lower())]
        if found:
            tid = found[0]["id"]
        else:
            payload = {"name": value.replace("-", " ").capitalize() if by == "slug" else value}
            if by == "slug":
                payload["slug"] = value
            tid = self.req("POST", taxonomy, json=payload)["id"]
            label = {"categories": "categoría", "tags": "etiqueta"}.get(taxonomy, taxonomy)
            print(f"  + {label} creada: {value}")
        self._term_cache[key] = tid
        return tid


def parse(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path}: falta frontmatter YAML")
    _, fm, body = text.split("---", 2)
    meta = yaml.safe_load(fm) or {}
    for field in ("title", "slug"):
        if not meta.get(field):
            raise ValueError(f"{path}: falta '{field}' en el frontmatter")
    status = meta.get("status", "draft")
    if status not in VALID_STATUS:
        raise ValueError(f"{path}: status inválido '{status}'")
    html = markdown.markdown(body.strip(), extensions=["tables", "fenced_code", "sane_lists"])
    return meta, html


def publish(wp, path):
    meta, html = parse(path)
    kind = meta.get("type", "post")
    endpoint = "pages" if kind == "page" else "posts"
    payload = {
        "title": meta["title"],
        "slug": meta["slug"],
        "content": html,
        "status": meta.get("status", "draft"),
    }
    if meta.get("excerpt"):
        payload["excerpt"] = meta["excerpt"]
    if kind == "post":
        if meta.get("categories"):
            payload["categories"] = [wp.term_id("categories", c) for c in meta["categories"]]
        if meta.get("tags"):
            payload["tags"] = [wp.term_id("tags", t, by="name") for t in meta["tags"]]
    elif meta.get("parent"):
        parent = wp.find_by_slug("pages", meta["parent"])
        if parent:
            payload["parent"] = parent["id"]

    existing = wp.find_by_slug(endpoint, meta["slug"])
    if existing:
        res = wp.req("POST", f"{endpoint}/{existing['id']}", json=payload)
        action = "actualizada"
    else:
        res = wp.req("POST", endpoint, json=payload)
        action = "creada"
    print(f"{path.relative_to(ROOT)}: {kind} {action} ({res['status']}) id={res['id']} {res['link']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true", help="publicar todo content/")
    ap.add_argument("--check", action="store_true", help="solo validar credenciales")
    args = ap.parse_args()

    wp = WP(env("WP_URL"), env("WP_USER"), env("WP_APP_PASSWORD"))
    me = wp.whoami()
    print(f"Conectado como {me.get('username', me.get('name'))} (roles: {', '.join(me.get('roles', []))})")
    if args.check:
        return

    files = sorted(CONTENT_DIR.rglob("*.md")) if args.all else [ROOT / f for f in args.files]
    files = [f for f in files if f.exists() and f.suffix == ".md" and CONTENT_DIR in f.resolve().parents]
    if not files:
        print("Nada que publicar.")
        return

    errors = 0
    for f in files:
        try:
            publish(wp, f)
        except Exception as e:  # noqa: BLE001
            errors += 1
            print(f"ERROR {f.relative_to(ROOT)}: {e}")
    if errors:
        sys.exit(f"{errors} archivo(s) con error")


if __name__ == "__main__":
    main()
