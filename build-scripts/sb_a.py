"""Small Business templates 1-8: invoice, quote, purchase orders, receivables, payables, P&L, cash flow, break-even."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

CLIENTS = ["Client A Ltd", "Client B Co", "Client C Studio", "Client D Trust", "Client E Shop", "Client F Partners"]

RNG = random.Random(707)
REPORT = dt.date(2026, 12, 1)


def _lines(ws, first, rows):
    """Line items: description (B), qty (C), unit price (D), line total (E)."""
    for i in range(rows):
        r = first + i
        put(ws, r, 2, "")
        put(ws, r, 3, None, "0")
        put(ws, r, 4, None, MONEY)
        put(ws, r, 5, f'=IF(OR(C{r}="",D{r}=""),"",C{r}*D{r})', MONEY, "calc")


def invoice(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice"
    setup_sheet(ws, "Invoice Generator", "Enter your details and each line item. Subtotal, VAT and balance calculate automatically", 4,
                [40, 12, 16, 18])
    label_value(ws, 5, "Invoice number", "INV-0001", None, "input")
    label_value(ws, 6, "Invoice date", dt.date(2026, 12, 1), DATE, "input")
    label_value(ws, 7, "Payment due", dt.date(2026, 12, 31), DATE, "input")
    label_value(ws, 8, "Bill to", "Client A Ltd", None, "input")
    label_value(ws, 9, "From", "Your business name", None, "input")
    header_row(ws, 11, 2, ["Description", "Qty", "Unit price", "Line total"])
    items = [("Website design (10 hours)", 10, 45), ("Hosting, one year", 1, 180), ("Domain renewal", 1, 15)]
    _lines(ws, 12, 8)
    for i, (d, q, p) in enumerate(items):
        put(ws, 12 + i, 2, d)
        put(ws, 12 + i, 3, q, "0")
        put(ws, 12 + i, 4, p, MONEY)
    totals = [("Subtotal", "=SUM(E12:E19)", MONEY, "calc"), ("VAT rate", 0.2, "0%", "input"),
              ("VAT", "=E21*E22", MONEY, "calc"), ("Total due", "=E21+E23", MONEY, "summary"),
              ("Amount paid", 0, MONEY, "input"), ("Balance due", "=E24-E25", MONEY, "summary")]
    for i, (lab, val, fmt, kind) in enumerate(totals):
        put(ws, 21 + i, 4, lab, kind="label", bold=True)
        put(ws, 21 + i, 5, val, fmt, kind)
    wb.save(path)


def quote(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Quote"
    setup_sheet(ws, "Quote and Estimate", "Enter the work, prices and any discount. Totals calculate automatically", 4,
                [40, 12, 16, 18])
    label_value(ws, 5, "Quote number", "Q-0001", None, "input")
    label_value(ws, 6, "Quote date", dt.date(2026, 12, 1), DATE, "input")
    label_value(ws, 7, "Valid until", dt.date(2026, 12, 31), DATE, "input")
    label_value(ws, 8, "Prepared for", "Client B Co", None, "input")
    header_row(ws, 11, 2, ["Description", "Qty", "Unit price", "Line total"])
    _lines(ws, 12, 8)
    items = [("Kitchen refit, design stage", 1, 1200), ("Materials allowance", 1, 850), ("Installation (days)", 3, 320)]
    for i, (d, q, p) in enumerate(items):
        put(ws, 12 + i, 2, d)
        put(ws, 12 + i, 3, q, "0")
        put(ws, 12 + i, 4, p, MONEY)
    totals = [("Subtotal", "=SUM(E12:E19)", MONEY, "calc"), ("Discount rate", 0.05, "0%", "input"),
              ("Discount", "=E21*E22", MONEY, "calc"), ("Net total", "=E21-E23", MONEY, "calc"),
              ("VAT rate", 0.2, "0%", "input"), ("VAT", "=E24*E25", MONEY, "calc"),
              ("Quote total", "=E24+E26", MONEY, "summary")]
    for i, (lab, val, fmt, kind) in enumerate(totals):
        put(ws, 21 + i, 4, lab, kind="label", bold=True)
        put(ws, 21 + i, 5, val, fmt, kind)
    wb.save(path)


def purchase_orders(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Purchase orders"
    setup_sheet(ws, "Purchase Order Log", "Log each order. Order totals and the value of open orders calculate automatically", 10,
                [12, 12, 18, 22, 8, 12, 12, 12, 14, 14])
    header_row(ws, 5, 2, ["PO number", "Date", "Supplier", "Item", "Qty", "Unit cost", "Total", "Status", "Approved by", "Received"])
    suppliers = ["Supplier A", "Supplier B", "Supplier C"]
    for i in range(12):
        r = 6 + i
        put(ws, r, 2, f"PO-{1001 + i}")
        put(ws, r, 3, dt.date(2026, 11, 2) + dt.timedelta(days=4 * i), DATE)
        put(ws, r, 4, suppliers[i % 3])
        put(ws, r, 5, RNG.choice(["Paper A4", "Ink cartridges", "Cleaning supplies", "Cable pack", "Printer toner"]))
        put(ws, r, 6, RNG.randint(2, 40), "0")
        put(ws, r, 7, RNG.choice([4.5, 12, 28, 65]), MONEY)
        put(ws, r, 8, f'=IF(OR(F{r}="",G{r}=""),"",F{r}*G{r})', MONEY, "calc")
        status = "Received" if i < 7 else ("Open" if i < 11 else "Cancelled")
        put(ws, r, 9, status)
        put(ws, r, 10, "Manager")
        put(ws, r, 11, dt.date(2026, 11, 20) + dt.timedelta(days=4 * i) if status == "Received" else None, DATE)
    validate(ws, "I6:I20", '"Open,Received,Cancelled"')
    label_value(ws, 22, "Value of open orders", '=SUMIF(I6:I20,"Open",H6:H20)', MONEY, "summary")
    label_value(ws, 23, "Open orders", '=COUNTIF(I6:I20,"Open")', "0", "summary")
    wb.save(path)


def receivables(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Receivables"
    setup_sheet(ws, "Accounts Receivable Aging Report", "Enter each unpaid invoice. Balances, days overdue and age buckets calculate from the report date", 9,
                [20, 12, 13, 13, 12, 12, 12, 12, 14])
    header_row(ws, 5, 2, ["Client", "Invoice", "Invoice date", "Due date", "Amount", "Paid", "Balance", "Days overdue", "Age"])
    for i in range(14):
        r = 6 + i
        due = dt.date(2026, 10, 1) + dt.timedelta(days=RNG.randint(0, 90))
        amt = RNG.choice([250, 480, 900, 1500, 2200])
        put(ws, r, 2, CLIENTS[i % len(CLIENTS)])
        put(ws, r, 3, f"INV-{201 + i}")
        put(ws, r, 4, due - dt.timedelta(days=30), DATE)
        put(ws, r, 5, due, DATE)
        put(ws, r, 6, amt, MONEY)
        put(ws, r, 7, round(amt * RNG.choice([0, 0, 0.5]), 2), MONEY)
        put(ws, r, 8, f'=IF(F{r}="","",F{r}-G{r})', MONEY, "calc")
        put(ws, r, 9, f'=IF(E{r}="","",MAX(0,$C$22-E{r}))', "0", "calc")
        put(ws, r, 10, f'=IF(H{r}="","",IF(H{r}<=0,"Paid",IF(I{r}<=0,"Current",IF(I{r}<=30,"1-30 days",'
                       f'IF(I{r}<=60,"31-60 days",IF(I{r}<=90,"61-90 days","Over 90 days"))))))', None, "calc")
    label_value(ws, 22, "Report date", REPORT, DATE, "input")
    header_row(ws, 24, 2, ["Age", "Balance owed"])
    buckets = ["Current", "1-30 days", "31-60 days", "61-90 days", "Over 90 days"]
    for i, b in enumerate(buckets):
        r = 25 + i
        put(ws, r, 2, b, kind="label")
        put(ws, r, 3, f'=SUMIF($J$6:$J$19,B{r},$H$6:$H$19)', MONEY, "calc")
    put(ws, 30, 2, "Total owed", kind="total")
    put(ws, 30, 3, "=SUM(C25:C29)", MONEY, "total")
    wb.save(path)


def payables(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Payables"
    setup_sheet(ws, "Accounts Payable Tracker", "Log each supplier bill. Balances and payment status calculate from the report date", 9,
                [20, 12, 13, 13, 12, 12, 12, 12, 16])
    header_row(ws, 5, 2, ["Supplier", "Bill number", "Bill date", "Due date", "Amount", "Paid", "Balance", "Days to due", "Status"])
    for i in range(12):
        r = 6 + i
        due = dt.date(2026, 11, 20) + dt.timedelta(days=RNG.randint(0, 40))
        amt = RNG.choice([120, 350, 640, 980, 1800])
        put(ws, r, 2, f"Supplier {chr(65 + i % 4)}")
        put(ws, r, 3, f"BILL-{3001 + i}")
        put(ws, r, 4, due - dt.timedelta(days=30), DATE)
        put(ws, r, 5, due, DATE)
        put(ws, r, 6, amt, MONEY)
        put(ws, r, 7, amt if i % 4 == 0 else 0, MONEY)
        put(ws, r, 8, f'=IF(F{r}="","",F{r}-G{r})', MONEY, "calc")
        put(ws, r, 9, f'=IF(E{r}="","",E{r}-$C$22)', "0", "calc")
        put(ws, r, 10, f'=IF(H{r}="","",IF(H{r}<=0,"Paid",IF(I{r}<0,"Overdue",IF(I{r}<=7,"Due this week","Later"))))', None, "calc")
    label_value(ws, 22, "Report date", REPORT, DATE, "input")
    label_value(ws, 24, "Total owed", '=SUM(H6:H17)', MONEY, "summary")
    label_value(ws, 25, "Overdue", '=SUMIF(J6:J17,"Overdue",H6:H17)', MONEY, "summary")
    label_value(ws, 26, "Due this week", '=SUMIF(J6:J17,"Due this week",H6:H17)', MONEY, "summary")
    wb.save(path)


def profit_and_loss(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "P&L"
    setup_sheet(ws, "Profit and Loss Statement", "Enter the year's income and costs. Totals, profit and percentages of revenue calculate automatically", 3,
                [36, 16, 14])
    header_row(ws, 5, 2, ["Line item", "Amount", "% of revenue"])
    rows = [
        ("Revenue", None, "label"),
        ("Sales revenue", 150000, "input"),
        ("Other income", 3000, "input"),
        ("Total revenue", "=SUM(C7:C8)", "total"),
        ("Cost of sales", None, "label"),
        ("Materials", 42000, "input"),
        ("Direct labour", 28000, "input"),
        ("Total cost of sales", "=SUM(C11:C12)", "total"),
        ("Gross profit", "=C9-C13", "summary"),
        ("Operating expenses", None, "label"),
        ("Rent", 12000, "input"),
        ("Utilities", 3600, "input"),
        ("Marketing", 4800, "input"),
        ("Insurance", 1800, "input"),
        ("Admin and software", 2400, "input"),
        ("Total operating expenses", "=SUM(C16:C20)", "total"),
        ("Operating profit", "=C14-C21", "summary"),
        ("Tax rate (example)", 0.2, "input"),
        ("Tax", "=MAX(0,C22)*C23", "calc"),
        ("Net profit", "=C22-C24", "summary"),
    ]
    for i, (lab, val, kind) in enumerate(rows):
        r = 6 + i
        if kind == "label":
            put(ws, r, 2, lab, kind="label", bold=True)
            put(ws, r, 3, None, kind="label")
            put(ws, r, 4, None, kind="label")
            continue
        put(ws, r, 2, lab, kind="total" if kind == "total" else ("summary" if kind == "summary" else "input"))
        put(ws, r, 3, val, "0%" if lab.startswith("Tax rate") else MONEY, kind if kind != "label" else "input")
        if not lab.startswith("Tax rate"):
            put(ws, r, 4, f'=IFERROR(C{r}/$C$9,"")', "0.0%", "calc")
    wb.save(path)


def cash_flow(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cash flow"
    setup_sheet(ws, "Cash Flow Forecast", "Enter the opening cash and expected money in and out each month. Closing balances carry forward", 6,
                [14, 16, 16, 16, 16, 16])
    header_row(ws, 5, 2, ["Month", "Opening cash", "Cash in", "Cash out", "Net flow", "Closing cash"])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, m in enumerate(months):
        r = 6 + i
        put(ws, r, 2, f"{m} 2027", kind="label")
        if i == 0:
            put(ws, r, 3, 5000, MONEY)
        else:
            put(ws, r, 3, f"=G{r - 1}", MONEY, "calc")
        put(ws, r, 4, 9000 + RNG.choice([0, 500, 1500, 3000]), MONEY)
        put(ws, r, 5, 8200 + RNG.choice([0, 400, 1200]), MONEY)
        put(ws, r, 6, f"=D{r}-E{r}", MONEY, "calc")
        put(ws, r, 7, f"=C{r}+F{r}", MONEY, "calc")
    label_value(ws, 19, "Lowest closing balance", "=MIN(G6:G17)", MONEY, "summary")
    label_value(ws, 20, "Month of lowest balance", "=INDEX(B6:B17,MATCH(MIN(G6:G17),G6:G17,0))", None, "summary")
    label_value(ws, 21, "Year-end cash", "=G17", MONEY, "summary")
    wb.save(path)


def break_even(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Break-even"
    setup_sheet(ws, "Break-even Analysis", "Enter your costs and price. Break-even point and profit at your planned sales calculate automatically", 4,
                [30, 16, 16, 16])
    label_value(ws, 5, "Fixed costs per month", 4000, MONEY, "input")
    label_value(ws, 6, "Selling price per unit", 25, MONEY, "input")
    label_value(ws, 7, "Variable cost per unit", 10, MONEY, "input")
    label_value(ws, 8, "Contribution per unit", "=C6-C7", MONEY, "calc")
    label_value(ws, 9, "Break-even units per month", '=IFERROR(C5/C8,"")', "#,##0", "summary")
    label_value(ws, 10, "Break-even revenue per month", '=IFERROR(C9*C6,"")', MONEY, "summary")
    label_value(ws, 11, "Planned units per month", 350, "#,##0", "input")
    label_value(ws, 12, "Profit at planned sales", "=C11*C8-C5", MONEY, "summary")
    label_value(ws, 13, "Margin of safety (units)", '=IFERROR(C11-C9,"")', "#,##0", "calc")
    header_row(ws, 15, 2, ["Units sold", "Revenue", "Total cost", "Profit"])
    for i in range(11):
        r = 16 + i
        put(ws, r, 2, i * 50, "#,##0", "label")
        put(ws, r, 3, f"=B{r}*$C$6", MONEY, "calc")
        put(ws, r, 4, f"=$C$5+B{r}*$C$7", MONEY, "calc")
        put(ws, r, 5, f"=C{r}-D{r}", MONEY, "calc")
    wb.save(path)
