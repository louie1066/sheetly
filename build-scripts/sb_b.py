"""Small Business templates 9-17: stock count, reorder, payroll, timesheets, mileage, expenses, petty cash, VAT, pricing."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(808)
REPORT = dt.date(2026, 12, 1)


def inventory_count(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stock count"
    setup_sheet(ws, "Inventory Stock Count Sheet", "Enter the system count and the physical count. Differences and their value calculate automatically", 9,
                [12, 26, 14, 12, 12, 12, 12, 14, 14])
    header_row(ws, 5, 2, ["Item code", "Item", "Location", "System count", "Counted", "Difference", "Unit cost", "Value difference", "Status"])
    items = ["Paper A4 (box)", "Ink cartridge black", "Ink cartridge colour", "USB cable", "Headphones", "Mouse",
             "Keyboard", "Whiteboard marker (pack)", "Notebook A5", "Batteries AA (pack)", "HDMI cable", "Toner cartridge"]
    for i, name in enumerate(items):
        r = 6 + i
        sys_n = RNG.randint(5, 60)
        counted = sys_n + RNG.choice([0, 0, 0, -2, 1, -1]) if i < 10 else None
        put(ws, r, 2, f"SKU-{100 + i}")
        put(ws, r, 3, name)
        put(ws, r, 4, "Store room" if i % 2 else "Shelf A")
        put(ws, r, 5, sys_n, "0")
        put(ws, r, 6, counted, "0")
        put(ws, r, 7, f'=IF(F{r}="","",F{r}-E{r})', "0;-0;0", "calc")
        put(ws, r, 8, RNG.choice([2.5, 6, 12.5, 25]), MONEY)
        put(ws, r, 9, f'=IF(G{r}="","",G{r}*H{r})', MONEY, "calc")
        put(ws, r, 10, f'=IF(F{r}="","Not counted",IF(G{r}=0,"Match",IF(G{r}<0,"Short","Over")))', None, "calc")
    label_value(ws, 19, "Items short", '=COUNTIF(J6:J17,"Short")', "0", "summary")
    label_value(ws, 20, "Items over", '=COUNTIF(J6:J17,"Over")', "0", "summary")
    label_value(ws, 21, "Net value difference", '=SUM(I6:I17)', MONEY, "summary")
    wb.save(path)


def reorder_level(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reorder"
    setup_sheet(ws, "Reorder Level Calculator", "Enter sales rate, lead time and safety stock. The reorder level and action calculate automatically", 8,
                [24, 14, 12, 12, 14, 12, 16, 14])
    header_row(ws, 5, 2, ["Item", "Average daily sales", "Lead time (days)", "Safety stock", "Reorder level",
                          "Stock on hand", "Action", "Order quantity"])
    items = ["Paper A4 (box)", "Ink cartridge black", "USB cable", "Headphones", "Mouse", "Keyboard", "Notebook A5",
             "Batteries AA (pack)", "HDMI cable", "Toner cartridge"]
    for i, name in enumerate(items):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, round(RNG.uniform(0.5, 6), 1), "0.0")
        put(ws, r, 4, RNG.choice([3, 5, 7, 10]), "0")
        put(ws, r, 5, RNG.choice([5, 10, 15]), "0")
        put(ws, r, 6, f'=IF(C{r}="","",C{r}*D{r}+E{r})', "0.0", "calc")
        put(ws, r, 7, RNG.randint(0, 60), "0")
        put(ws, r, 8, f'=IF(F{r}="","",IF(G{r}<=F{r},"Reorder now","OK"))', None, "calc")
        put(ws, r, 9, 30, "0")
    label_value(ws, 18, "Items to reorder now", '=COUNTIF(H6:H15,"Reorder now")', "0", "summary")
    put(ws, 19, 2, "Reorder level = average daily sales x lead time + safety stock.", kind="label")
    wb.save(path)


def payroll(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Payroll"
    setup_sheet(ws, "Payroll Calculator",
                "Enter gross pay for each employee. The rates below are examples only: replace them with your current local rates", 7,
                [30, 14, 14, 16, 14, 16, 18])
    label_value(ws, 5, "Income tax rate (example)", 0.2, "0%", "input")
    label_value(ws, 6, "Employee contribution rate (example)", 0.08, "0%", "input")
    label_value(ws, 7, "Employer contribution rate (example)", 0.1, "0%", "input")
    header_row(ws, 9, 2, ["Employee", "Gross pay", "Income tax", "Employee contribution", "Net pay", "Employer contribution", "Total cost to business"])
    for i in range(10):
        r = 10 + i
        gross = RNG.choice([2200, 2650, 3100, 3600, 4200])
        put(ws, r, 2, f"Employee {i + 1:02d}")
        put(ws, r, 3, gross, MONEY)
        put(ws, r, 4, f"=C{r}*$C$5", MONEY, "calc")
        put(ws, r, 5, f"=C{r}*$C$6", MONEY, "calc")
        put(ws, r, 6, f"=C{r}-D{r}-E{r}", MONEY, "calc")
        put(ws, r, 7, f"=C{r}*$C$7", MONEY, "calc")
        put(ws, r, 8, f"=C{r}+G{r}", MONEY, "calc")
    put(ws, 20, 2, "Totals", kind="total")
    for c in range(3, 9):
        put(ws, 20, c, f"=SUM({L(c)}10:{L(c)}19)", MONEY, "total")
    wb.save(path)


def timesheet(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Timesheet"
    setup_sheet(ws, "Timesheet with Overtime", "Enter hours for each day. Regular hours, overtime and gross pay calculate automatically", 13,
                [16] + [7] * 7 + [9, 10, 10, 10, 12])
    header_row(ws, 5, 2, ["Employee", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total hours",
                          "Regular hours", "Overtime hours", "Hourly rate", "Gross pay"])
    for i in range(10):
        r = 6 + i
        put(ws, r, 2, f"Employee {i + 1:02d}")
        for c in range(3, 10):
            put(ws, r, c, RNG.choice([7, 8, 8, 8, 0]) if c < 9 else RNG.choice([0, 0, 4]), "0.0")
        put(ws, r, 10, f"=SUM(C{r}:I{r})", "0.0", "calc")
        put(ws, r, 11, f"=MIN(J{r},$C$22)", "0.0", "calc")
        put(ws, r, 12, f"=MAX(0,J{r}-$C$22)", "0.0", "calc")
        put(ws, r, 13, RNG.choice([12, 14, 16, 18]), MONEY)
        put(ws, r, 14, f"=K{r}*M{r}+L{r}*M{r}*$C$23", MONEY, "calc")
    label_value(ws, 22, "Overtime starts after (hours per week)", 40, "0", "input")
    label_value(ws, 23, "Overtime multiplier", 1.5, "0.0", "input")
    label_value(ws, 25, "Total gross pay", "=SUM(N6:N15)", MONEY, "summary")
    wb.save(path)


def mileage(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Mileage"
    setup_sheet(ws, "Mileage Log", "Log each business journey. Claim amounts calculate from the rate per kilometre", 6,
                [12, 26, 16, 16, 14, 14])
    header_row(ws, 5, 2, ["Date", "Purpose", "From", "To", "Distance (km)", "Claim"])
    trips = [("Visit client", "Office", "Client A"), ("Supplier meeting", "Office", "Supplier B"),
             ("Bank deposit", "Office", "Bank branch"), ("Training day", "Office", "Training centre")]
    for i in range(20):
        r = 6 + i
        if i < 10:
            p, f, t = trips[i % len(trips)]
            put(ws, r, 2, dt.date(2026, 11, 2) + dt.timedelta(days=3 * i), DATE)
            put(ws, r, 3, p)
            put(ws, r, 4, f)
            put(ws, r, 5, t)
            put(ws, r, 6, RNG.choice([12, 24, 36, 48]), "0.0")
        else:
            for c in range(2, 6):
                put(ws, r, c, None, DATE if c == 2 else None)
            put(ws, r, 6, None, "0.0")
        put(ws, r, 7, f'=IF(F{r}="","",F{r}*$C$22)', MONEY, "calc")
    label_value(ws, 22, "Claim rate per km (example)", 0.45, "0.00", "input")
    label_value(ws, 24, "Total distance (km)", "=SUM(F6:F25)", "0.0", "summary")
    label_value(ws, 25, "Total claim", "=SUM(G6:G25)", MONEY, "summary")
    wb.save(path)


def expense_claim(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Claim"
    setup_sheet(ws, "Expense Claim Form", "Enter each expense with its receipt status. Lines without a receipt are flagged", 6,
                [12, 28, 16, 14, 14, 20])
    label_value(ws, 5, "Employee name", "Employee 01", None, "input")
    label_value(ws, 6, "Department", "Sales", None, "input")
    label_value(ws, 7, "Claim period", "November 2026", None, "input")
    header_row(ws, 9, 2, ["Date", "Description", "Category", "Amount", "Receipt attached?", "Check"])
    lines = [("Train to client", "Travel", 46.5, "Yes"), ("Lunch with client", "Meals", 28, "No"),
             ("Printer ink", "Equipment", 64, "Yes"), ("Cloud software", "Software", 19.99, "Yes")]
    for i in range(15):
        r = 10 + i
        if i < len(lines):
            d, c, amt, rec = lines[i]
            put(ws, r, 2, dt.date(2026, 11, 3 + i * 4), DATE)
            put(ws, r, 3, d)
            put(ws, r, 4, c)
            put(ws, r, 5, amt, MONEY)
            put(ws, r, 6, rec)
        else:
            for c in range(2, 7):
                put(ws, r, c, None, DATE if c == 2 else (MONEY if c == 5 else None))
        put(ws, r, 7, f'=IF(E{r}="","",IF(F{r}="No","Receipt needed","OK"))', None, "calc")
    validate(ws, "D10:D24", '"Travel,Meals,Equipment,Software,Other"')
    validate(ws, "F10:F24", '"Yes,No"')
    label_value(ws, 26, "Total claimed", "=SUM(E10:E24)", MONEY, "summary")
    label_value(ws, 27, "Lines needing a receipt", '=COUNTIF(G10:G24,"Receipt needed")', "0", "summary")
    wb.save(path)


def petty_cash(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Petty cash"
    setup_sheet(ws, "Petty Cash Register", "Enter the opening float, then log money in and out. The running balance calculates automatically", 6,
                [12, 30, 14, 14, 14, 12])
    label_value(ws, 5, "Opening float", 200, MONEY, "input")
    header_row(ws, 7, 2, ["Date", "Description", "Money in", "Money out", "Balance", "Receipt no"])
    entries = [("Stamps", None, 18.5), ("Tea and coffee", None, 12), ("Top-up from bank", 150, None),
               ("Courier fee", None, 9.75), ("Cleaning supplies", None, 23.4), ("Stationery", None, 14.2)]
    for i in range(20):
        r = 8 + i
        if i < len(entries):
            d, inn, out = entries[i]
            put(ws, r, 2, dt.date(2026, 11, 2) + dt.timedelta(days=2 * i), DATE)
            put(ws, r, 3, d)
            put(ws, r, 4, inn, MONEY)
            put(ws, r, 5, out, MONEY)
            put(ws, r, 7, f"PC-{i + 1:03d}")
        else:
            put(ws, r, 2, None, DATE)
            put(ws, r, 3, None)
            put(ws, r, 4, None, MONEY)
            put(ws, r, 5, None, MONEY)
            put(ws, r, 7, None)
        prev = "$C$5" if i == 0 else f"F{r - 1}"
        put(ws, r, 6, f'=IF(B{r}="","",{prev}+N(D{r})-N(E{r}))', MONEY, "calc")
    label_value(ws, 29, "Cash counted", None, MONEY, "input")
    label_value(ws, 30, "Expected balance", '=IFERROR(INDEX(F8:F27,COUNTA(B8:B27)),"")', MONEY, "summary")
    label_value(ws, 31, "Difference (should be 0)", '=IF(C29="","",C29-C30)', MONEY, "summary")
    wb.save(path)


def vat_calculator(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "VAT"
    setup_sheet(ws, "VAT and Sales Tax Calculator", "Enter net amounts and the rate for each item. VAT and gross totals calculate automatically. Check rates locally", 6,
                [28, 14, 12, 14, 14, 14])
    header_row(ws, 5, 2, ["Item", "Net amount", "VAT rate", "VAT", "Gross amount", "Net check"])
    items = [("Consulting services", 1200, 0.2), ("Printed books (reduced rate example)", 300, 0.05),
             ("Exported goods (zero-rated example)", 800, 0), ("Office supplies", 150, 0.2),
             ("Software subscription", 420, 0.2)]
    for i in range(10):
        r = 6 + i
        if i < len(items):
            n, a, rate = items[i]
            put(ws, r, 2, n)
            put(ws, r, 3, a, MONEY)
            put(ws, r, 4, rate, "0%")
        else:
            put(ws, r, 2, None)
            put(ws, r, 3, None, MONEY)
            put(ws, r, 4, None, "0%")
        put(ws, r, 5, f'=IF(C{r}="","",C{r}*D{r})', MONEY, "calc")
        put(ws, r, 6, f'=IF(C{r}="","",C{r}+E{r})', MONEY, "calc")
        put(ws, r, 7, f'=IF(F{r}="","",F{r}/(1+D{r})-C{r})', "0.00", "calc")
    put(ws, 16, 2, "Totals", kind="total")
    put(ws, 16, 3, "=SUM(C6:C15)", MONEY, "total")
    put(ws, 16, 4, "", kind="total")
    put(ws, 16, 5, "=SUM(E6:E15)", MONEY, "total")
    put(ws, 16, 6, "=SUM(F6:F15)", MONEY, "total")
    put(ws, 16, 7, "", kind="total")
    label_value(ws, 18, "Standard rate (example)", 0.2, "0%", "input")
    label_value(ws, 19, "Reduced rate (example)", 0.05, "0%", "input")
    wb.save(path)


def pricing_margin(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Pricing"
    setup_sheet(ws, "Product Pricing and Margin Calculator", "Enter the cost and markup for each product. Selling price, margin and the price for your target margin calculate automatically", 7,
                [24, 12, 12, 14, 16, 12, 18])
    header_row(ws, 5, 2, ["Product", "Cost price", "Markup %", "Selling price", "Profit per unit", "Margin %", "Price for target margin"])
    products = [("Notebook A5", 1.8, 0.8), ("Pen pack", 2.5, 0.6), ("Printed poster", 4.2, 1.2), ("Sticker sheet", 0.9, 1.5),
                ("Tote bag", 6.5, 0.9), ("Mug", 3.4, 1.0), ("Calendar", 5.0, 0.7)]
    for i in range(10):
        r = 6 + i
        if i < len(products):
            n, c, m = products[i]
            put(ws, r, 2, n)
            put(ws, r, 3, c, MONEY)
            put(ws, r, 4, m, "0%")
        else:
            put(ws, r, 2, None)
            put(ws, r, 3, None, MONEY)
            put(ws, r, 4, None, "0%")
        put(ws, r, 5, f'=IF(C{r}="","",C{r}*(1+D{r}))', MONEY, "calc")
        put(ws, r, 6, f'=IF(C{r}="","",E{r}-C{r})', MONEY, "calc")
        put(ws, r, 7, f'=IF(C{r}="","",IFERROR(F{r}/E{r},""))', "0%", "calc")
        put(ws, r, 8, f'=IF(C{r}="","",IFERROR(C{r}/(1-$C$18),""))', MONEY, "calc")
    label_value(ws, 18, "Target gross margin", 0.4, "0%", "input")
    wb.save(path)
