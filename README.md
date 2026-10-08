# Publimerca: contenido y pipeline de publicación

Repositorio fuente de [publimerca.com](https://www.publimerca.com). Cada archivo Markdown en `content/` se publica en WordPress mediante la API REST cuando llega a `main`.

## Cómo funciona

1. Los agentes escriben o actualizan un archivo en `content/<pilar>/<slug>.md`.
2. Al hacer push a `main`, la GitHub Action `Publicar en WordPress` publica solo los archivos nuevos o modificados.
3. Si ya existe una entrada con el mismo `slug`, se actualiza; nunca se duplica.

El historial de git es la bitácora pública del experimento de SEO agéntico.

## Frontmatter

```yaml
---
title: "Brief creativo: qué es y cómo escribir uno"
slug: brief-creativo
type: post            # post | page
status: draft         # draft | publish | pending | private
excerpt: "Descripción corta para listados y buscadores."
categories: [publicidad]
tags: [glosario, creatividad]
---
```

## Secretos requeridos (Settings > Secrets and variables > Actions)

| Secreto | Valor |
| --- | --- |
| `WP_URL` | `https://www.publimerca.com` |
| `WP_USER` | usuario dedicado del agente |
| `WP_APP_PASSWORD` | contraseña de aplicación de ese usuario |

## Probar la conexión

Actions > Publicar en WordPress > Run workflow > `check`.

## Uso local

```bash
pip install -r requirements.txt
export WP_URL=... WP_USER=... WP_APP_PASSWORD=...
python scripts/publish.py --check
python scripts/publish.py content/glosario/brief-creativo.md
```
