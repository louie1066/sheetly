"""Wire one category into build.py and build_site.py from a spec module (see spec_health.py).

Usage:  python3 wire.py spec_health
Strings are written with json.dumps, so apostrophes and quotes are safe.
"""
import importlib
import json
import re
import sys

BUILD = "/home/claude/build/build.py"
SITE = "/home/claude/build/build_site.py"


def q(s):
    return json.dumps(s, ensure_ascii=False)


def insert_before_close(src, opener, insert):
    """Insert text just before the closing brace of a dict/list that starts with opener."""
    start = src.index(opener)
    end = src.index("\n}", start) if "\n}" in src[start:] else None
    close = src.index("}", start)
    return src[:close] + insert + src[close:]


def main(spec_name):
    spec = importlib.import_module(spec_name).SPEC
    key, slug, out = spec["key"], spec["slug"], spec["out"]
    mods, tmpl, groups = spec["modules"], spec["templates"], spec["groups"]
    K = key.upper()

    # ---- build.py
    b = open(BUILD, encoding="utf-8").read()
    if f"{K}_TEMPLATES" in b:
        sys.exit("already wired: " + key)
    anchor = "import pm_a as PA, pm_b as PB, pm_c as PC\n"
    assert b.count(anchor) == 1
    b = b.replace(anchor, anchor + "import " + ", ".join(mods) + "\n")
    anchor = 'PM_OUT = "/home/claude/site/downloads/project-management"\n'
    assert b.count(anchor) == 1
    b = b.replace(anchor, anchor + f'{K}_OUT = {q("/home/claude/site/downloads/" + out)}\nos.makedirs({K}_OUT, exist_ok=True)\n')
    lines = "".join(
        f"    ({q(t['slug'])}, {q(t['title'])}, {t['fn']}, {q(t['step'])}),\n" for t in tmpl)
    block = f"{K}_TEMPLATES = [\n{lines}]\n\n"
    anchor = "_orig_save = Workbook.save\n"
    assert b.count(anchor) == 1
    b = b.replace(anchor, block + anchor)
    anchor = "    for out_dir, (slug, title, fn, step) in jobs:\n"
    assert b.count(anchor) == 1
    b = b.replace(anchor, f"    jobs += [({K}_OUT, t) for t in {K}_TEMPLATES]\n" + anchor)
    open(BUILD, "w", encoding="utf-8").write(b)

    # ---- build_site.py
    s = open(SITE, encoding="utf-8").read()
    s = s.replace("CATEGORIES = {", "CATEGORIES = {", 1)
    s = insert_before_close(s, "CATEGORIES = {", f"    {q(slug)}: {q(spec['name'])},\n")
    s = insert_before_close(s, "CATEGORY_INTRO = {", f"    {q(slug)}: {q(spec['intro'])},\n")
    s = insert_before_close(s, "CATEGORY_DESC = {", f"    {q(slug)}: {q(spec['desc'])},\n")
    entries = "".join(f"    ({q(t['slug'])}, {q(t['name'])}, {q(t['site'])}),\n" for t in tmpl)
    anchor = "]\n\n# Groups for the category pages"
    assert s.count(anchor) == 1
    s = s.replace(anchor, entries + anchor)
    gtxt = f"{K}_GROUPS = [\n"
    for heading, slugs in groups:
        gtxt += f"    ({q(heading)}, [" + ", ".join(q(x) for x in slugs) + "]),\n"
    gtxt += "]\n\n"
    anchor = "GROUPS_BY_CAT = {"
    assert s.count(anchor) == 1
    s = s.replace(anchor, gtxt + anchor)
    s = insert_before_close(s, "GROUPS_BY_CAT = {", f", {q(slug)}: {K}_GROUPS")
    open(SITE, "w", encoding="utf-8").write(s)
    import ast
    ast.parse(b); ast.parse(s)
    print("wired", key, len(tmpl), "templates")


if __name__ == "__main__":
    main(sys.argv[1])
