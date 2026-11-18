# sheetly

Free, ready-to-use Excel templates for money, school, IT, business and everyday life. Every template is licensed under [CC BY 4.0](site/licence.html), so you can use, adapt and share them, including commercially, as long as you credit the author.

## What's included

- 250 `.xlsx` templates in 10 categories, plus a search page, a "most downloaded" page and a site map.
- A static website built from one generator script.
- A small Cloudflare Pages Function that counts downloads.

## Folder layout

| Folder | What it contains |
| --- | --- |
| `site/` | The website: HTML pages, CSS, JavaScript, the template files and the template data. Deploy this folder. |
| `functions/` | The Cloudflare Pages Functions for the download counter. Keep this next to `site/`, not inside it. |
| `build-scripts/` | `build_site.py`, which generates the category pages, search page, site map and download function. |
| `docs/` | `HANDOFF.md`, the full handoff notes and deployment steps. |

## Rebuilding the site

The build script writes into `site/`. Before you run it, change the `SITE` path near the top of `build-scripts/build_site.py` so it points to the `site/` folder on your computer. Then run:

```
python3 build-scripts/build_site.py
```

Don't edit the generated HTML files directly. Make changes in the generator or in `site/index.html` and `site/css/style.css`, then rebuild.

## Deploying

The site is designed for Cloudflare Pages:

- **Build command:** none
- **Build output directory:** `site`
- **KV binding:** a namespace bound as `DOWNLOADS` for the download counter

The full steps are in [`docs/HANDOFF.md`](docs/HANDOFF.md).

## Licence

Templates and site content are licensed under [CC BY 4.0](site/licence.html).
