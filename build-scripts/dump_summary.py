"""Print the mint summary values of each recalculated workbook in a category folder."""
import glob, sys, openpyxl
folder = sys.argv[1]
for f in sorted(glob.glob(f"/home/claude/recalc/{folder}/*.xlsx")):
    wb = openpyxl.load_workbook(f, data_only=True)
    ws = wb.worksheets[0]
    out = []
    for r in range(6, ws.max_row + 1):
        c = ws.cell(r, 3)
        lab = ws.cell(r, 2).value
        if lab and c.fill and c.fill.start_color and c.fill.start_color.rgb in ("00D5F5E3", "FFD5F5E3") and c.value not in (None, ""):
            v = c.value
            if isinstance(v, float): v = round(v, 2)
            if hasattr(v, "date"): v = v.date().isoformat()
            out.append(f"{lab}={v}")
    print(f.split("/")[-1][:-5], "|", "; ".join(out))
