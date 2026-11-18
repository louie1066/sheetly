"""Shared builder for the standard log-style templates: one table, optional totals, report date,
user settings cells, a summary block and an optional note.

Column spec: (header, width, kind, number_format)
  kind = "input"      a cream cell; values come from the sample rows, in column order
  kind = "<formula>"  a calculated cell. Placeholders: {r} this row, {p} the row above, {R0}/{R1} first/last data row,
                      {RD} the report date cell, {IN0}, {IN1}... the settings cells (in the order given)
"""
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *


def _sub(text, r, R0, R1, RD, IN):
    out = text.replace("{r}", str(r)).replace("{p}", str(r - 1)).replace("{R0}", str(R0)).replace("{R1}", str(R1)).replace("{RD}", RD or "")
    for i, ref in enumerate(IN):
        out = out.replace("{IN%d}" % i, ref)
    return out


def build_log(path, sheet, title, sub, cols, rows, nrows=15, summary=(), report=None, totals=(),
              validations=(), note_text=None, inputs=()):
    """
    report:      None, or (label, date): a report date cell for formulas that compare with today's date
    inputs:      settings the user fills in once, as (label, value, number_format), e.g. a personal goal
    totals:      column indices (0-based in cols) to sum in a peach totals row
    validations: list of (range_template, spec); spec is '"a,b,c"' for a list, or ("whole", "min", "max")
    summary:     list of (label, formula_template, number_format)
    """
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    setup_sheet(ws, title, sub, len(cols), [c[1] for c in cols])
    header_row(ws, 5, 2, [c[0] for c in cols])

    input_idx = [j for j, c in enumerate(cols) if c[2] == "input"]
    R0, R1 = 6, 5 + nrows
    pos = R1 + 1
    tot_row = None
    if totals:
        tot_row = pos
        pos += 2
    rep_row = None
    if report:
        rep_row = pos
        pos += 2
    RD = f"$C${rep_row}" if rep_row else None
    in_rows = []
    for _ in inputs:
        in_rows.append(pos)
        pos += 1
    if inputs:
        pos += 1
    IN = [f"$C${r}" for r in in_rows]

    for k in range(nrows):
        r = R0 + k
        sample = rows[k] if k < len(rows) else None
        for j, (head, width, kind, fmt) in enumerate(cols):
            c = j + 2
            if kind == "input":
                val = sample[input_idx.index(j)] if sample else None
                put(ws, r, c, val, fmt)
            else:
                put(ws, r, c, _sub(kind, r, R0, R1, RD, IN), fmt, "calc")

    if tot_row:
        for j, (head, width, kind, fmt) in enumerate(cols):
            c = j + 2
            if j == 0:
                put(ws, tot_row, c, "Total", kind="total")
            elif j in totals:
                letter = L(c)
                put(ws, tot_row, c, f"=SUM({letter}{R0}:{letter}{R1})", fmt, "total")
            else:
                put(ws, tot_row, c, "", kind="total")

    if rep_row:
        label_value(ws, rep_row, report[0], report[1], DATE)
    for (label, value, fmt), row in zip(inputs, in_rows):
        label_value(ws, row, label, value, fmt, "input")

    for rng, spec in validations:
        rng = _sub(rng, 0, R0, R1, RD, IN)
        if isinstance(spec, tuple):
            validate(ws, rng, spec[1], kind=spec[0], operator="between", formula2=spec[2])
        else:
            validate(ws, rng, spec)

    for label, formula, fmt in summary:
        label_value(ws, pos, label, _sub(formula, 0, R0, R1, RD, IN), fmt, "summary")
        pos += 1
    if note_text:
        pos += 1
        note(ws, pos, note_text)
    wb.save(path)
    return ws
