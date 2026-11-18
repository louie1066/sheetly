"""Small Business templates 18-25: clients, pipeline, suppliers, business plan, depreciation, shifts, stock valuation, refunds."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(909)
REPORT = dt.date(2026, 12, 1)


def client_list(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Clients"
    setup_sheet(ws, "Client Contact List", "Keep one row per client. Days since last contact and follow-ups calculate from the report date", 9,
                [12, 22, 18, 26, 16, 13, 13, 14, 14])
    header_row(ws, 5, 2, ["Client ID", "Company", "Contact name", "Email", "Phone", "Client since", "Last contact",
                          "Days since contact", "Follow up?"])
    companies = ["Client A Ltd", "Client B Co", "Client C Studio", "Client D Trust", "Client E Shop", "Client F Partners"]
    for i in range(12):
        r = 6 + i
        put(ws, r, 2, f"C-{1001 + i}")
        put(ws, r, 3, companies[i % len(companies)])
        put(ws, r, 4, f"Contact {i + 1:02d}")
        put(ws, r, 5, f"contact{i + 1:02d}@example.com")
        put(ws, r, 6, "555-0100")
        put(ws, r, 7, dt.date(2024, 1, 15) + dt.timedelta(days=60 * i), DATE)
        put(ws, r, 8, dt.date(2026, 11, 1) + dt.timedelta(days=RNG.randint(0, 25)), DATE)
        put(ws, r, 9, f'=IF(H{r}="","",$C$22-H{r})', "0", "calc")
        put(ws, r, 10, f'=IF(I{r}="","",IF(I{r}>60,"Yes","No"))', None, "calc")
    label_value(ws, 22, "Report date", REPORT, DATE, "input")
    label_value(ws, 24, "Clients", '=COUNTA(B6:B17)', "0", "summary")
    label_value(ws, 25, "Needing follow-up (60+ days)", '=COUNTIF(J6:J17,"Yes")', "0", "summary")
    wb.save(path)


def sales_pipeline(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Pipeline"
    setup_sheet(ws, "Sales Pipeline Tracker", "Log each deal and its stage. Probability and weighted value calculate from the stage table", 11,
                [16, 18, 14, 12, 12, 14, 14, 14, 3, 12, 12])
    header_row(ws, 5, 2, ["Deal", "Client", "Stage", "Value", "Probability", "Weighted value", "Expected close", "Owner"])
    header_row(ws, 5, 11, ["Stage", "Probability"])
    stages = [("Lead", 0.1), ("Proposal", 0.4), ("Negotiation", 0.7), ("Won", 1), ("Lost", 0)]
    for i, (s, p) in enumerate(stages):
        put(ws, 6 + i, 11, s)
        put(ws, 6 + i, 12, p, "0%")
    deals = ["Website redesign", "Staff training", "Hosting contract", "Office IT support", "Printer leasing",
             "Data backup service", "Mobile app", "Network upgrade", "Training workshop", "Software licence", "Consultancy", "Support plan"]
    names = ["Client A Ltd", "Client B Co", "Client C Studio", "Client D Trust", "Client E Shop"]
    for i, d in enumerate(deals):
        r = 6 + i
        put(ws, r, 2, d)
        put(ws, r, 3, names[i % len(names)])
        put(ws, r, 4, stages[i % 5][0])
        put(ws, r, 5, RNG.choice([800, 1500, 2400, 5000, 9000]), MONEY)
        put(ws, r, 6, f'=IF(D{r}="","",IFERROR(VLOOKUP(D{r},$K$6:$L$10,2,FALSE),""))', "0%", "calc")
        put(ws, r, 7, f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})', MONEY, "calc")
        put(ws, r, 8, dt.date(2026, 12, 15) + dt.timedelta(days=9 * i), DATE)
        put(ws, r, 9, f"Owner {chr(65 + i % 2)}")
    validate(ws, "D6:D20", '"Lead,Proposal,Negotiation,Won,Lost"')
    label_value(ws, 22, "Open pipeline value", '=SUMIFS(E6:E20,D6:D20,"<>Won",D6:D20,"<>Lost")', MONEY, "summary")
    label_value(ws, 23, "Open weighted value", '=SUMIFS(G6:G20,D6:D20,"Lead")+SUMIFS(G6:G20,D6:D20,"Proposal")+SUMIFS(G6:G20,D6:D20,"Negotiation")',
                MONEY, "summary")
    label_value(ws, 24, "Won value", '=SUMIF(D6:D20,"Won",E6:E20)', MONEY, "summary")
    wb.save(path)


def supplier_comparison(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Compare"
    setup_sheet(ws, "Supplier Comparison", "Enter each supplier's unit price. The cheapest supplier and yearly totals calculate automatically", 8,
                [24, 12, 14, 14, 14, 14, 16, 16])
    header_row(ws, 5, 2, ["Item", "Quantity per year", "Supplier A", "Supplier B", "Supplier C", "Lowest price", "Cheapest supplier", "Lowest yearly cost"])
    items = ["Paper A4 (box)", "Ink cartridge", "Toner", "Cable pack", "Cleaning kit", "Notebooks", "Pens (pack)",
             "Batteries (pack)", "Mouse", "Keyboard", "Headset", "Projector bulb"]
    for i, n in enumerate(items):
        r = 6 + i
        base = RNG.uniform(3, 60)
        put(ws, r, 2, n)
        put(ws, r, 3, RNG.randint(4, 120), "0")
        put(ws, r, 4, round(base * RNG.uniform(0.9, 1.1), 2), MONEY)
        put(ws, r, 5, round(base * RNG.uniform(0.9, 1.1), 2), MONEY)
        put(ws, r, 6, round(base * RNG.uniform(0.9, 1.1), 2), MONEY)
        put(ws, r, 7, f"=MIN(D{r}:F{r})", MONEY, "calc")
        put(ws, r, 8, f"=INDEX($D$5:$F$5,MATCH(G{r},D{r}:F{r},0))", None, "calc")
        put(ws, r, 9, f"=C{r}*G{r}", MONEY, "calc")
    put(ws, 19, 2, "Yearly cost from each supplier", kind="total")
    put(ws, 19, 3, "", kind="total")
    for c in (4, 5, 6):
        put(ws, 19, c, f"=SUMPRODUCT($C$6:$C$17,{L(c)}6:{L(c)}17)", MONEY, "total")
    put(ws, 19, 7, "", kind="total")
    put(ws, 19, 8, "", kind="total")
    put(ws, 19, 9, "=SUM(I6:I17)", MONEY, "total")
    label_value(ws, 21, "Cheapest supplier overall", "=INDEX(D5:F5,MATCH(MIN(D19:F19),D19:F19,0))", None, "summary")
    label_value(ws, 22, "Saving versus the dearest supplier", "=MAX(D19:F19)-MIN(D19:F19)", MONEY, "summary")
    wb.save(path)


def business_plan(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan"
    setup_sheet(ws, "Business Plan Financial Projections", "Enter Year 1 and the growth and cost assumptions. Years 2 and 3 calculate from them", 4,
                [36, 16, 16, 16])
    header_row(ws, 5, 2, ["Line", "Year 1", "Year 2", "Year 3"])
    put(ws, 6, 2, "Revenue growth rate", kind="label", bold=True)
    put(ws, 6, 3, None, kind="label")
    put(ws, 6, 4, 0.1, "0%")
    put(ws, 6, 5, 0.12, "0%")
    put(ws, 7, 2, "Revenue", kind="label", bold=True)
    put(ws, 7, 3, 120000, MONEY)
    put(ws, 7, 4, "=C7*(1+D6)", MONEY, "calc")
    put(ws, 7, 5, "=D7*(1+E6)", MONEY, "calc")
    put(ws, 8, 2, "Cost of sales as % of revenue", kind="label", bold=True)
    for c in (3, 4, 5):
        put(ws, 8, c, 0.35, "0%")
    put(ws, 9, 2, "Cost of sales", kind="label", bold=True)
    put(ws, 10, 2, "Gross profit", kind="summary")
    put(ws, 11, 2, "Operating expenses", kind="label", bold=True)
    put(ws, 12, 2, "Operating profit", kind="summary")
    put(ws, 13, 2, "Tax rate (example)", kind="label", bold=True)
    put(ws, 14, 2, "Tax", kind="label", bold=True)
    put(ws, 15, 2, "Net profit", kind="summary")
    put(ws, 16, 2, "Net profit margin", kind="label", bold=True)
    for c, col in zip((3, 4, 5), ("C", "D", "E")):
        put(ws, 9, c, f"={col}7*{col}8", MONEY, "calc")
        put(ws, 10, c, f"={col}7-{col}9", MONEY, "summary")
        put(ws, 11, c, [40000, 44000, 48000][c - 3], MONEY)
        put(ws, 12, c, f"={col}10-{col}11", MONEY, "summary")
        put(ws, 13, c, 0.2, "0%")
        put(ws, 14, c, f"=MAX(0,{col}12)*{col}13", MONEY, "calc")
        put(ws, 15, c, f"={col}12-{col}14", MONEY, "summary")
        put(ws, 16, c, f'=IFERROR({col}15/{col}7,"")', "0.0%", "calc")
    wb.save(path)


def asset_depreciation(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Depreciation"
    setup_sheet(ws, "Asset Depreciation Schedule", "Straight-line depreciation for five years. Enter cost, salvage value and useful life", 10,
                [22, 12, 12, 12, 14, 12, 12, 12, 12, 12])
    header_row(ws, 5, 2, ["Asset", "Cost", "Salvage value", "Useful life (years)", "Annual depreciation",
                          "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"])
    assets = [("Laptop fleet", 9000, 500, 4), ("Server", 6000, 300, 5), ("Projector", 1200, 0, 5),
              ("Interactive whiteboard", 2400, 100, 6), ("Network switches", 3500, 200, 5),
              ("Office furniture", 2800, 0, 8), ("Van", 18000, 3000, 5), ("Printers", 1600, 100, 4)]
    for i, (n, cost, salv, life) in enumerate(assets):
        r = 6 + i
        put(ws, r, 2, n)
        put(ws, r, 3, cost, MONEY)
        put(ws, r, 4, salv, MONEY)
        put(ws, r, 5, life, "0")
        put(ws, r, 6, f'=IFERROR((C{r}-D{r})/E{r},"")', MONEY, "calc")
        for k in range(1, 6):
            put(ws, r, 6 + k, f'=IF({k}<=$E{r},$F{r},0)', MONEY, "calc")
    put(ws, 14, 2, "Totals", kind="total")
    for c in range(3, 12):
        if c == 5:
            put(ws, 14, c, "", kind="total")
        else:
            put(ws, 14, c, f"=SUM({L(c)}6:{L(c)}13)", MONEY, "total")
    label_value(ws, 16, "Total cost of assets", "=SUM(C6:C13)", MONEY, "summary")
    wb.save(path)


def shift_rota(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rota"
    setup_sheet(ws, "Shift Rota", "Enter a shift code for each person each day. Hours and cover per shift calculate automatically", 12,
                [16, 8, 8, 8, 8, 8, 8, 8, 10, 3, 10, 10])
    header_row(ws, 5, 2, ["Employee", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total hours"])
    header_row(ws, 5, 12, ["Shift code", "Hours"])
    codes = [("M", "Morning", 8), ("A", "Afternoon", 8), ("N", "Night", 10), ("O", "Off", 0)]
    for i, (c, _name, h) in enumerate(codes):
        put(ws, 6 + i, 12, c)
        put(ws, 6 + i, 13, h, "0")
    for i in range(8):
        r = 6 + i
        put(ws, r, 2, f"Employee {i + 1:02d}")
        for c in range(3, 10):
            put(ws, r, c, RNG.choice(["M", "A", "N", "O", "O"]))
        put(ws, r, 10, f"=SUMPRODUCT(COUNTIF(C{r}:I{r},$L$6:$L$9)*$M$6:$M$9)", "0", "calc")
    validate(ws, "C6:I13", '"M,A,N,O"')
    for r, (lab, code) in zip((15, 16, 17), [("Morning staff", "M"), ("Afternoon staff", "A"), ("Night staff", "N")]):
        put(ws, r, 2, lab, kind="total")
        for c in range(3, 10):
            put(ws, r, c, f'=COUNTIF({L(c)}6:{L(c)}13,"{code}")', "0", "total")
    label_value(ws, 19, "Total hours, all staff", "=SUM(J6:J13)", "0", "summary")
    wb.save(path)


def stock_valuation(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stock"
    setup_sheet(ws, "Stock Valuation (FIFO and LIFO)", "Enter each purchase batch and the units sold. Cost of sales and remaining stock value calculate both ways", 9,
                [12, 13, 12, 12, 14, 12, 12, 14, 14])
    header_row(ws, 5, 2, ["Batch", "Purchase date", "Quantity", "Unit cost", "Cumulative quantity", "FIFO units used",
                          "LIFO units used", "FIFO cost", "LIFO cost"])
    qty = [100, 150, 120, 80, 200, 90]
    cost = [2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
    for i in range(6):
        r = 6 + i
        put(ws, r, 2, f"Batch {i + 1}", kind="label")
        put(ws, r, 3, dt.date(2026, 7, 1) + dt.timedelta(days=30 * i), DATE)
        put(ws, r, 4, qty[i], "0")
        put(ws, r, 5, cost[i], MONEY)
        put(ws, r, 6, f"=SUM($D$6:D{r})", "0", "calc")
        put(ws, r, 7, f"=MIN(D{r},MAX(0,$C$15-(F{r}-D{r})))", "0", "calc")
        put(ws, r, 8, f"=MIN(D{r},MAX(0,$C$15-($D$12-F{r})))", "0", "calc")
        put(ws, r, 9, f"=G{r}*E{r}", MONEY, "calc")
        put(ws, r, 10, f"=H{r}*E{r}", MONEY, "calc")
    put(ws, 12, 2, "Totals", kind="total")
    put(ws, 12, 3, "", kind="total")
    put(ws, 12, 4, "=SUM(D6:D11)", "0", "total")
    put(ws, 12, 5, "", kind="total")
    put(ws, 12, 6, "", kind="total")
    put(ws, 12, 7, "=SUM(G6:G11)", "0", "total")
    put(ws, 12, 8, "=SUM(H6:H11)", "0", "total")
    put(ws, 12, 9, "=SUM(I6:I11)", MONEY, "total")
    put(ws, 12, 10, "=SUM(J6:J11)", MONEY, "total")
    label_value(ws, 15, "Units sold", 320, "0", "input")
    label_value(ws, 16, "Units left in stock", "=D12-C15", "0", "summary")
    label_value(ws, 17, "Cost of sales (FIFO)", "=I12", MONEY, "summary")
    label_value(ws, 18, "Cost of sales (LIFO)", "=J12", MONEY, "summary")
    label_value(ws, 19, "Stock value left (FIFO)", "=SUMPRODUCT(D6:D11,E6:E11)-I12", MONEY, "summary")
    label_value(ws, 20, "Stock value left (LIFO)", "=SUMPRODUCT(D6:D11,E6:E11)-J12", MONEY, "summary")
    label_value(ws, 21, "Check", '=IF(C15<=D12,"OK","Sold more than stock")', None, "summary")
    wb.save(path)


def refunds_log(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Refunds"
    setup_sheet(ws, "Refunds and Returns Log", "Log each refund or return. Totals by status and reason calculate automatically", 9,
                [12, 12, 18, 20, 20, 14, 12, 14, 14])
    header_row(ws, 5, 2, ["Date", "Order number", "Customer", "Product", "Reason", "Refund amount", "Restocked?", "Method", "Status"])
    reasons = ["Damaged", "Wrong item", "Changed mind", "Late delivery"]
    products = ["Notebook A5", "Headset", "Mouse", "Printer toner", "Tote bag"]
    for i in range(12):
        r = 6 + i
        put(ws, r, 2, dt.date(2026, 11, 3) + dt.timedelta(days=3 * i), DATE)
        put(ws, r, 3, f"ORD-{5001 + i}")
        put(ws, r, 4, f"Customer {i + 1:02d}")
        put(ws, r, 5, products[i % len(products)])
        put(ws, r, 6, reasons[i % len(reasons)])
        put(ws, r, 7, RNG.choice([12.5, 24, 35, 48]), MONEY)
        put(ws, r, 8, "Yes" if reasons[i % len(reasons)] == "Damaged" else "No")
        put(ws, r, 9, RNG.choice(["Card", "Bank transfer", "Store credit"]))
        put(ws, r, 10, "Pending" if i >= 9 else "Refunded")
    validate(ws, "F6:F25", '"Damaged,Wrong item,Changed mind,Late delivery,Other"')
    validate(ws, "H6:H25", '"Yes,No"')
    validate(ws, "I6:I25", '"Card,Bank transfer,Store credit"')
    validate(ws, "J6:J25", '"Pending,Refunded"')
    label_value(ws, 27, "Total refunded", '=SUMIF(J6:J25,"Refunded",G6:G25)', MONEY, "summary")
    label_value(ws, 28, "Pending refunds (value)", '=SUMIF(J6:J25,"Pending",G6:G25)', MONEY, "summary")
    label_value(ws, 29, "Pending refunds (count)", '=COUNTIF(J6:J25,"Pending")', "0", "summary")
    label_value(ws, 30, "Refunds for damaged items", '=SUMIF(F6:F25,"Damaged",G6:G25)', MONEY, "summary")
    label_value(ws, 31, "Items restocked", '=COUNTIF(H6:H25,"Yes")', "0", "summary")
    wb.save(path)
