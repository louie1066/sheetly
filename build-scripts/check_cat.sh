#!/bin/bash
# usage: check_cat.sh <category-folder-name>
F=$1
OUT=/home/claude/recalc/$F
rm -rf "$OUT" && mkdir -p "$OUT"
timeout 600 soffice --headless --calc --convert-to xlsx --outdir "$OUT" /home/claude/site/downloads/$F/*.xlsx >/dev/null 2>&1
python3 - "$OUT" <<'PY'
import glob, sys, openpyxl
files = sorted(glob.glob(sys.argv[1] + "/*.xlsx"))
bad = []
for f in files:
    wb = openpyxl.load_workbook(f, data_only=True)
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and (c.value.startswith("#") or c.value.startswith("Err:")):
                    bad.append((f.split("/")[-1], ws.title, c.coordinate, c.value))
print("files:", len(files), "error cells:", len(bad))
for b in bad[:30]:
    print(*b)
PY
