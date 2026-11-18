# Sheetly: handoff notes

Sheetly is a free, static website of spreadsheet templates (Excel .xlsx), licensed CC BY 4.0. Author: Mark. The site name, email and author name are placeholders to change before launch.

## Folder contents
- `site/`: the website, ready to upload. Keep the folder structure.
- `functions/`: the Cloudflare download counter. It sits next to `site/`, not inside it.
- `build-scripts/`: Python scripts that generate the 250 Excel templates and the generated web pages.
- `docs/spreadsheet-ideas-250.md`: the 250 template ideas in 10 categories.

## Status
All 10 categories are built: 250 templates in total, 25 per category. Every workbook recalculates in LibreOffice with zero error cells, and the summary values were checked by hand against the sample data.

- Homepage: header with logo, category links (desktop) or dropdown (mobile), light/dark mode, header hides on scroll down and returns on scroll up, footer.
- Personal Finance (25), Education & Classroom (25), IT & Computing (25), Small Business & Invoicing (25), Project & Task Management (25): built earlier. Hand-checked figures include break-even, payroll, depreciation, dashboard health ratings, WBS totals and OKR progress.
- Health, Fitness & Wellbeing (25): workouts, meals, water, sleep, habits, medication, blood pressure and glucose, weight, body measurements, appointments and more. Records only, not medical advice.
- Home & Household (25): chores, maintenance, inventories, pantry, meal shopping, cleaning, garden, energy, bills, renovation, moving, vehicles, pets and more.
- Travel & Events (25): itineraries, travel and event budgets, currency log, packing, flight and hotel comparison, road-trip fuel, guest lists, run sheets, seating, volunteers, passports and visas, insurance, expense splitting and more.
- Hobbies & Creative Projects (25): photography, recipes and baking ratios, brewing, knitting, woodworking cut lists, sewing, collections, reading and film logs, games, music practice, writing, podcasts, fishing and birdwatching.
- Sales, Marketing & Operations (25): social media and email campaigns, marketing ROI, leads, customers, commission, forecasts, NPS, churn, competitor matrix, SWOT, support SLAs, warehouse picking, fulfilment, shipping, food cost, staff training, leave, reviews, recruitment and shift handovers.
- Most Downloaded page: ranked list, 25 per page.
- Footer pages: About, Privacy Policy, Terms of Use, Licence, Contact us (email form that opens the visitor's email app).

## Download counter (Cloudflare Pages)
- `functions/api/download/[slug].js`: counts each download and redirects to the file. Used by the background counter in the homepage script; the download link itself points straight at the .xlsx file, so downloads work even without the counter.
- `functions/api/counts.js`: returns all counts as JSON.
- Free plan allows about 1,000 counted downloads per day. Counts are read and written one at a time, so two downloads at the same moment can count as one.

Deploy steps:
1. In Cloudflare, create a KV namespace (Workers & Pages > KV), for example `sheetly-downloads`.
2. Create a Pages project from the Git repository (or upload with Wrangler from the project root, so `functions/` is picked up).
3. Build settings: no build command, build output directory `site`. The `functions/` folder at the project root is picked up automatically.
4. Pages project > Settings > Bindings: add a KV namespace binding with variable name `DOWNLOADS`, pointing to the namespace from step 1. Set it for production (and preview if you use it). Redeploy after adding it.
5. Check: `/api/counts` should return `{}`. Download one template, then `/api/counts` should show it as 1.

Test locally: `npx wrangler@3 pages dev site --kv DOWNLOADS` from the project root.

## Build scripts
- `common.py`: shared styles, logo and layout helpers. `validate()` adds drop-down lists and number limits. `note()` writes a one-line note under a table without wrapping it.
- `tplkit.py`: `build_log()`, the shared builder for log-style templates (one table, optional totals, report date cell, settings cells, summary block, note).
- Category generators, 25 templates each, split into three modules (`a` = templates 1-8 or 1-9, `b` and `c` for the rest):
  - `finance_a/b/c.py`, `education_a/b/c.py`, `it_a/b/c.py`, `sb_a/b/c.py`, `pm_a/b/c.py`
  - `hw_a/b/c.py` (Health), `home_a/b/c.py` (Home), `travel_a/b/c.py` (Travel), `hobby_a/b/c.py` (Hobbies), `sales_a/b/c.py` (Sales)
- Category specs, one per newer category, read by `wire.py`: `spec_health.py`, `spec_home.py`, `spec_travel.py`, `spec_hobbies.py`, `spec_sales.py`. Each holds the template slugs, titles, function names, short descriptions, step text and the category groups shown on its page.
- `wire.py`: adds a category to `build.py` and `build_site.py` from its spec (`python3 wire.py spec_travel`). It refuses to run twice for the same category.
- `build.py`: builds all 250 workbooks into `site/downloads/<category>/`. Run it with no arguments for everything, or with template slugs to rebuild only those. Needs `openpyxl` and `Pillow`.
- `build_site.py`: regenerates one page per category (listed in `CATEGORIES`, grouped by each category's `*_GROUPS`), the Most Downloaded page, footer pages, `data/templates.json` and the download function. It takes its header and footer from `site/index.html`, so edit the homepage there.
- To add a category: write the generator modules and a spec, run `wire.py`, then rebuild both scripts. Edit these files, not the generated HTML.

Build lessons:
- Text in `TEMPLATES` and `build.py` lists: apostrophes must be typographic (’) or escaped, or the file will not parse. `wire.py` avoids this by writing strings with `json.dumps`.
- Newer Excel functions need the `_xlfn.` prefix when written with openpyxl, or they show `#NAME?` on recalculation. Examples: `_xlfn.MAXIFS`, `_xlfn.MINIFS`.
- Paths are hard-coded to `/home/claude/...` (for example `SITE` in `build_site.py`, `OUT` in `build.py`, `LOGO` in `common.py`). Change them to your local folders before running.

## Recalculation check
- `check_cat.sh <category-folder>` recalculates every workbook in a category with LibreOffice headless and reports any error cells (`#NAME?`, `#REF!`, `#DIV/0!` and so on).
- `dump_summary.py <category-folder>` prints the summary values from the recalculated copies, for hand-checking against the sample data.
- Run both after every build. A category is only complete when it reports zero error cells.

## Known issues and decisions
- Health: "Weight Tracker" and "Body Measurement Tracker" are separate templates with different columns and descriptions. They were kept as two templates so the category keeps 25.
- Home: the Utility Bill Comparison uses made-up provider names and sample rates. The Home Energy Usage Tracker leaves tariff prices blank for the user to enter. Neither contains real tariff data.
- Currency in templates is unspecified (plain number format). Tax bands in the tax estimate are placeholders.
- Debt snowball and avalanche templates estimate payoff using minimum payments, and they don't roll freed-up payments forward.
- Sample data in every template is generic and made up, including example.com emails and 555 phone numbers.
- Footer links: every page now opens at the top. Please confirm in a normal browser.
- Email address `hello@sheetly.example` is made up. Replace it everywhere (footer, contact page, privacy and terms pages, and `CONTACT_EMAIL` in `build_site.py`).
- Privacy and terms pages are drafts and need a legal review.
- Fixed this session: the homepage linked to `categories/hobbies-creative.html` and `categories/sales-marketing.html`, which did not exist. The links now point to the real category pages.

## Next steps
1. Deploy to Cloudflare Pages and bind the KV namespace.
2. Replace placeholders (site name, email, author name) and review the legal pages.
3. Browser-test the category pages and the download counter on phone, tablet and desktop widths.
