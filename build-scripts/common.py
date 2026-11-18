"""Shared styling and layout helpers for Sheetly personal finance templates."""
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XLImage

FONT = "Arial"
BAND = "DCE8F7"      # soft blue title band
HEADER = "E4DDF5"    # lavender table headers
TOTAL = "FFE3CC"     # peach totals
SUMMARY = "D5F5E3"   # mint summary blocks
INPUT = "FFF8E1"     # cream input cells
TEXT = "1F2A37"
MUTED = "5B6778"

thin = Side(style="thin", color="C9D1DC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
LOGO = "/home/claude/build/logo.png"

MONEY = '#,##0.00;[Red]-#,##0.00;"-"'
PCT = "0.00%"
DATE = "dd/mm/yyyy"


def fill(hex_):
    return PatternFill("solid", start_color=hex_, end_color=hex_)


def font(size=10, bold=False, color=TEXT, italic=False):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic)


def setup_sheet(ws, title, subtitle, ncols, widths):
    """Hide gridlines, set column widths, add logo in the top-left corner and a title band."""
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 10
    for i, w in enumerate(widths, start=2):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    ws.row_dimensions[1].height = 44
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 18
    last = ws.cell(1, ncols + 1).column_letter
    for r in (1, 2, 3):
        for c in range(1, ncols + 2):
            ws.cell(r, c).fill = fill(BAND)
    ws["B1"] = title
    ws["B1"].font = font(16, True, TEXT)
    ws["B1"].alignment = Alignment(vertical="center")
    ws["B2"] = subtitle
    ws["B2"].font = font(10, False, MUTED, italic=True)
    ws["B3"] = "Sheetly  |  sheetly.example  |  Free to use under CC BY 4.0"
    ws["B3"].font = font(8, False, MUTED)
    img = XLImage(LOGO)
    img.width, img.height = 40, 40
    ws.add_image(img, "A1")
    ws.freeze_panes = None


def header_row(ws, row, col_start, labels):
    for i, lab in enumerate(labels):
        c = ws.cell(row, col_start + i, lab)
        c.font = font(10, True)
        c.fill = fill(HEADER)
        c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 30


def section_label(ws, row, col, text):
    c = ws.cell(row, col, text)
    c.font = font(11, True, TEXT)


def put(ws, row, col, value, fmt=None, kind="input", bold=False):
    """kind: 'input' (cream), 'calc' (white), 'total' (peach), 'summary' (mint), 'label' (plain)."""
    c = ws.cell(row, col, value)
    c.font = font(10, bold)
    c.border = BORDER
    c.alignment = Alignment(vertical="center", wrap_text=True)
    if kind == "input":
        c.fill = fill(INPUT)
    elif kind == "total":
        c.fill = fill(TOTAL)
        c.font = font(10, True)
    elif kind == "summary":
        c.fill = fill(SUMMARY)
        c.font = font(10, True)
    if fmt:
        c.number_format = fmt
    return c


def label_value(ws, row, label, value, fmt=None, kind="input"):
    """Label in column B, value in column C."""
    lab = ws.cell(row, 2, label)
    lab.font = font(10, True)
    lab.border = BORDER
    lab.alignment = Alignment(vertical="center", wrap_text=True)
    put(ws, row, 3, value, fmt, kind)


def how_to_sheet(wb, name, title, steps):
    ws = wb.create_sheet(name)
    setup_sheet(ws, title, "How to use this template", 2, [28, 80])
    r = 5
    for i, s in enumerate(steps, start=1):
        put(ws, r, 2, f"Step {i}", kind="label", bold=True)
        put(ws, r, 3, s, kind="label")
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
    put(ws, r, 2, "Licence", kind="label", bold=True)
    put(ws, r, 3, "Creative Commons Attribution 4.0 (CC BY 4.0). You may use, share and adapt this file, including commercially, if you credit the author.", kind="label")
    ws.row_dimensions[r].height = 30
    r += 1
    put(ws, r, 2, "Author", kind="label", bold=True)
    put(ws, r, 3, "Sheetly (sheetly.example)", kind="label")
    r += 1
    put(ws, r, 2, "Example data", kind="label", bold=True)
    put(ws, r, 3, "All figures are generic examples. Replace them with your own.", kind="label")
    r += 1
    put(ws, r, 2, "Colour key", kind="label", bold=True)
    put(ws, r, 3, "Cream = type here   |   Lavender = headings   |   Peach = totals   |   Mint = key results", kind="label")
    return ws


def validate(ws, rng, formula1, kind="list", operator=None, formula2=None):
    """Add a drop-down (kind='list') or a number limit (kind='whole' or 'decimal') to a range."""
    from openpyxl.worksheet.datavalidation import DataValidation
    dv = DataValidation(type=kind, formula1=formula1, formula2=formula2, operator=operator, allow_blank=True)
    dv.showErrorMessage = True
    dv.error = "Please choose or enter an allowed value."
    ws.add_data_validation(dv)
    dv.add(rng)


def note(ws, row, text):
    """A one-line note under a table. Not wrapped, so it runs across the empty cells to its right."""
    c = ws.cell(row, 2, text)
    c.font = font(9, False, MUTED, italic=True)
    c.alignment = Alignment(vertical="center", wrap_text=False)
    return c
