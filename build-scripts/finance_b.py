"""Templates 9-17: loans, savings, net worth, subscriptions, bills, cash flow and card payoff."""
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from common import *


def mortgage(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Mortgage"
    setup_sheet(ws, "Mortgage Repayment Calculator", "Estimate monthly repayments and the total cost of a home loan", 3,
                [34, 20, 20])
    section_label(ws, 5, 2, "Inputs")
    label_value(ws, 6, "Property price", 250000, MONEY, "input")
    label_value(ws, 7, "Deposit", 50000, MONEY, "input")
    label_value(ws, 8, "Annual interest rate", 0.048, PCT, "input")
    label_value(ws, 9, "Term (years)", 25, "0", "input")
    label_value(ws, 10, "Fees and closing costs", 3500, MONEY, "input")
    section_label(ws, 12, 2, "Results")
    label_value(ws, 13, "Loan amount", "=C6-C7", MONEY)
    label_value(ws, 14, "Deposit as % of price", "=IF(C6=0,0,C7/C6)", "0.0%")
    label_value(ws, 15, "Monthly repayment", "=PMT(C8/12,C9*12,-C13)", MONEY, "summary")
    label_value(ws, 16, "Total repaid over term", "=C15*C9*12", MONEY)
    label_value(ws, 17, "Total interest", "=C16-C13", MONEY)
    label_value(ws, 18, "Total cost incl. deposit and fees", "=C16+C7+C10", MONEY, "summary")
    label_value(ws, 19, "Minimum income suggested (28% rule)", "=C15/0.28", MONEY)
    wb.save(path)


def car_loan(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Compare Offers"
    setup_sheet(ws, "Car Loan Comparison", "Compare up to three finance offers side by side", 4, [30, 20, 20, 20])
    header_row(ws, 5, 2, ["Measure", "Offer A", "Offer B", "Offer C"])
    rows = [("Car price", [18000, 18000, 18000]), ("Deposit", [2000, 3000, 1500]),
            ("Annual interest rate", [0.079, 0.059, 0.089]), ("Term (months)", [48, 60, 36]),
            ("Fees", [295, 499, 0])]
    r = 6
    for name, vals in rows:
        put(ws, r, 2, name, kind="label", bold=True)
        fmt = PCT if "rate" in name else ("0" if "Term" in name else MONEY)
        for i, v in enumerate(vals):
            put(ws, r, 3 + i, v, fmt, "input")
        r += 1
    # r == 11
    calc = [("Amount financed", "={c}6-{c}7", MONEY),
            ("Monthly payment", "=PMT({c}8/12,{c}9,-{c}11)", MONEY),
            ("Total paid (deposit + payments + fees)", "={c}7+{c}12*{c}9+{c}10", MONEY),
            ("Total interest and fees", "={c}13-{c}6", MONEY)]
    for name, f, fmt in calc:
        put(ws, r, 2, name, kind="label", bold=True)
        for i in range(3):
            col = L(3 + i)
            put(ws, r, 3 + i, f.format(c=col), fmt, "calc")
        r += 1
    put(ws, r, 2, "Lowest total paid", kind="summary")
    put(ws, r, 3, "=INDEX(C5:E5,MATCH(MIN(C13:E13),C13:E13,0))", None, "summary")
    ws.column_dimensions["E"].width = 20
    wb.save(path)


def savings_goal(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Goal"
    setup_sheet(ws, "Savings Goal Tracker", "Log each deposit and see how close you are to your target", 4,
                [30, 18, 18, 18])
    label_value(ws, 5, "Goal name", "Holiday fund", None, "input")
    label_value(ws, 6, "Target amount", 3000, MONEY, "input")
    label_value(ws, 7, "Planned monthly deposit", 250, MONEY, "input")
    label_value(ws, 8, "Saved so far", "=SUM(C13:C42)", MONEY, "calc")
    label_value(ws, 9, "Progress", "=IF(C6=0,0,MIN(1,C8/C6))", "0%", "summary")
    label_value(ws, 10, "Remaining", "=MAX(0,C6-C8)", MONEY, "summary")
    label_value(ws, 11, "Months left at planned deposit", '=IF(C7<=0,"",ROUNDUP(C10/C7,0))', "0", "summary")
    header_row(ws, 12, 2, ["Deposit date", "Amount", "Running total", "Note"])
    sample = [("01/09/2026", 250, "September"), ("01/10/2026", 250, "October"), ("01/11/2026", 300, "November")]
    for i in range(30):
        r = 13 + i
        if i < len(sample):
            d, a, n = sample[i]
            put(ws, r, 2, d, kind="input")
            put(ws, r, 3, a, MONEY, "input")
            put(ws, r, 5, n, kind="input")
        else:
            put(ws, r, 2, None, kind="input")
            put(ws, r, 3, None, MONEY, "input")
            put(ws, r, 5, None, kind="input")
        put(ws, r, 4, f"=SUM($C$13:C{r})", MONEY)
    ws.column_dimensions["E"].width = 22
    wb.save(path)


def emergency_fund(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Emergency Fund"
    setup_sheet(ws, "Emergency Fund Calculator", "Work out how much to save for unexpected costs", 3, [36, 20, 20])
    header_row(ws, 5, 2, ["Essential monthly expense", "Amount"])
    items = [("Rent or mortgage", 1100), ("Utilities", 200), ("Groceries", 420), ("Transport", 180),
             ("Insurance", 120), ("Debt minimums", 300), ("Phone and internet", 85)]
    r = 6
    for n, a in items:
        put(ws, r, 2, n, kind="input")
        put(ws, r, 3, a, MONEY, "input")
        r += 1
    put(ws, r, 2, "Total essentials per month", kind="total")
    put(ws, r, 3, f"=SUM(C6:C{r-1})", MONEY, "total")
    tot = r
    r += 2
    label_value(ws, r, "Months of cover wanted (3 to 6)", 6, "0", "input")
    cover = r
    label_value(ws, r + 1, "Target emergency fund", f"=C{tot}*C{cover}", MONEY, "summary")
    label_value(ws, r + 2, "Current savings", 2400, MONEY, "input")
    cur = r + 2
    label_value(ws, r + 3, "Gap to target", f"=MAX(0,C{r+1}-C{cur})", MONEY, "summary")
    label_value(ws, r + 4, "Monthly saving planned", 200, MONEY, "input")
    mon = r + 4
    label_value(ws, r + 5, "Months to reach target", f'=IF(C{mon}<=0,"",ROUNDUP(C{r+3}/C{mon},0))', "0", "summary")
    wb.save(path)


def net_worth(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Net Worth"
    setup_sheet(ws, "Net Worth Tracker", "List what you own and what you owe to see your net worth", 4,
                [32, 18, 18, 22])
    label_value(ws, 5, "Snapshot date", "30/11/2026", None, "input")
    header_row(ws, 7, 2, ["Assets", "Value", "Notes", ""])
    assets = [("Cash and current account", 2100), ("Savings account", 6400), ("Investments", 9800),
              ("Pension", 15200), ("Car (estimated value)", 7500), ("Home (estimated value)", 0)]
    r = 8
    for n, v in assets:
        put(ws, r, 2, n, kind="input")
        put(ws, r, 3, v, MONEY, "input")
        put(ws, r, 4, None, kind="input")
        put(ws, r, 5, None, kind="input")
        r += 1
    a_tot = r
    put(ws, r, 2, "Total assets", kind="total")
    put(ws, r, 3, f"=SUM(C8:C{r-1})", MONEY, "total")
    r += 2
    header_row(ws, r, 2, ["Liabilities", "Balance", "Notes", ""])
    r += 1
    l_first = r
    liabs = [("Credit cards", 2400), ("Car loan", 6800), ("Student loan", 4100), ("Personal loan", 3200)]
    for n, v in liabs:
        put(ws, r, 2, n, kind="input")
        put(ws, r, 3, v, MONEY, "input")
        put(ws, r, 4, None, kind="input")
        put(ws, r, 5, None, kind="input")
        r += 1
    l_tot = r
    put(ws, r, 2, "Total liabilities", kind="total")
    put(ws, r, 3, f"=SUM(C{l_first}:C{r-1})", MONEY, "total")
    r += 2
    label_value(ws, r, "Net worth (assets - liabilities)", f"=C{a_tot}-C{l_tot}", MONEY, "summary")
    ws.column_dimensions["E"].width = 3
    wb.save(path)


def subscriptions(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Subscriptions"
    setup_sheet(ws, "Subscription Cost Tracker", "See what recurring costs really add up to each year", 7,
                [26, 14, 14, 16, 16, 16, 14])
    header_row(ws, 5, 2, ["Service", "Cost", "Billing", "Monthly equivalent", "Yearly cost", "Renewal date", "Still using?"])
    subs = [("Music streaming", 10.99, "Monthly", "03/12/2026", "Yes"),
            ("Video streaming", 15.99, "Monthly", "10/12/2026", "Yes"),
            ("Cloud storage", 99, "Yearly", "01/05/2027", "Yes"),
            ("Fitness app", 8.50, "Monthly", "18/12/2026", "No"),
            ("News site", 4.00, "Weekly", "20/11/2026", "No"),
            ("Software licence", 60, "Yearly", "15/02/2027", "Yes")]
    dv = DataValidation(type="list", formula1='"Monthly,Yearly,Weekly"', allow_blank=True)
    dv2 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    ws.add_data_validation(dv)
    ws.add_data_validation(dv2)
    for i in range(20):
        r = 6 + i
        if i < len(subs):
            n, c, b, d, u = subs[i]
            put(ws, r, 2, n, kind="input")
            put(ws, r, 3, c, MONEY, "input")
            put(ws, r, 4, b, kind="input")
            put(ws, r, 7, d, kind="input")
            put(ws, r, 8, u, kind="input")
        else:
            for c in (2, 3, 4, 7, 8):
                put(ws, r, c, None, MONEY if c == 3 else None, "input")
        dv.add(f"D{r}")
        dv2.add(f"H{r}")
        put(ws, r, 5, f'=IF(C{r}="","",IF(D{r}="Yearly",C{r}/12,IF(D{r}="Weekly",C{r}*52/12,C{r})))', MONEY)
        put(ws, r, 6, f'=IF(E{r}="","",E{r}*12)', MONEY)
    put(ws, 26, 2, "Totals", kind="total")
    put(ws, 26, 3, "", kind="total")
    put(ws, 26, 4, "", kind="total")
    put(ws, 26, 5, "=SUM(E6:E25)", MONEY, "total")
    put(ws, 26, 6, "=SUM(F6:F25)", MONEY, "total")
    put(ws, 26, 7, "", kind="total")
    put(ws, 26, 8, "", kind="total")
    label_value(ws, 28, "Spent on subscriptions you no longer use (per year)",
                '=SUMIF(H6:H25,"No",F6:F25)', MONEY, "summary")
    ws.column_dimensions["H"].width = 14
    wb.save(path)


def bill_calendar(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bill Calendar"
    setup_sheet(ws, "Bill Payment Calendar", "Track each bill's due day and mark it paid", 5, [28, 14, 16, 16, 16])
    header_row(ws, 5, 2, ["Bill", "Due day of month", "Amount", "Paid this month?", "Payment method"])
    bills = [("Rent", 1, 1100, "Yes", "Standing order"), ("Electricity", 5, 96, "No", "Direct debit"),
             ("Water", 12, 38, "No", "Bank transfer"), ("Council tax", 15, 135, "No", "Direct debit"),
             ("Phone", 20, 35, "No", "Credit card"), ("Insurance", 25, 120, "No", "Direct debit")]
    dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    ws.add_data_validation(dv)
    for i in range(15):
        r = 6 + i
        if i < len(bills):
            n, d, a, p, m = bills[i]
            put(ws, r, 2, n, kind="input")
            put(ws, r, 3, d, "0", "input")
            put(ws, r, 4, a, MONEY, "input")
            put(ws, r, 5, p, kind="input")
            put(ws, r, 6, m, kind="input")
        else:
            put(ws, r, 2, None, kind="input")
            put(ws, r, 3, None, "0", "input")
            put(ws, r, 4, None, MONEY, "input")
            put(ws, r, 5, None, kind="input")
            put(ws, r, 6, None, kind="input")
        dv.add(f"E{r}")
    put(ws, 21, 2, "Total bills", kind="total")
    put(ws, 21, 3, "", kind="total")
    put(ws, 21, 4, "=SUM(D6:D20)", MONEY, "total")
    put(ws, 21, 5, '=COUNTIF(E6:E20,"No")&" unpaid"', None, "total")
    put(ws, 21, 6, "", kind="total")
    label_value(ws, 23, "Unpaid this month", '=SUMIF(E6:E20,"No",D6:D20)', MONEY, "summary")
    ws.column_dimensions["G"].width = 3
    wb.save(path)


def cash_flow(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cash Flow"
    setup_sheet(ws, "Annual Cash-Flow Forecast", "Forecast your bank balance month by month", 6,
                [14, 18, 18, 18, 20, 18])
    label_value(ws, 5, "Opening balance (January)", 1500, MONEY, "input")
    header_row(ws, 7, 2, ["Month", "Income", "Expenses", "Net", "Closing balance", "Lowest point?"])
    inc = [3300, 3300, 3450, 3300, 3300, 3700, 3300, 3300, 3300, 3300, 3300, 3900]
    exp = [2650, 2710, 2800, 2620, 2580, 3050, 2700, 2640, 2690, 2735, 2880, 3320]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, m in enumerate(months):
        r = 8 + i
        put(ws, r, 2, m)
        put(ws, r, 3, inc[i], MONEY, "input")
        put(ws, r, 4, exp[i], MONEY, "input")
        put(ws, r, 5, f"=C{r}-D{r}", MONEY)
        opening = "$C$5" if i == 0 else f"F{r-1}"
        put(ws, r, 6, f"={opening}+E{r}", MONEY)
        put(ws, r, 7, f'=IF(F{r}=MIN($F$8:$F$19),"Lowest","")')
    put(ws, 20, 2, "Year", kind="total")
    put(ws, 20, 3, "=SUM(C8:C19)", MONEY, "total")
    put(ws, 20, 4, "=SUM(D8:D19)", MONEY, "total")
    put(ws, 20, 5, "=SUM(E8:E19)", MONEY, "total")
    put(ws, 20, 6, "=F19", MONEY, "total")
    put(ws, 20, 7, "", kind="total")
    label_value(ws, 22, "Lowest balance in year", "=MIN(F8:F19)", MONEY, "summary")
    label_value(ws, 23, "Months with negative balance", '=COUNTIF(F8:F19,"<0")', "0", "summary")
    ws.column_dimensions["H"].width = 3
    wb.save(path)


def card_payoff(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Payoff"
    setup_sheet(ws, "Credit Card Payoff Planner", "See how long a balance takes to clear and the interest you will pay", 7,
                [14, 18, 16, 16, 18, 18])
    label_value(ws, 5, "Current balance", 2400, MONEY, "input")
    label_value(ws, 6, "Annual interest rate (APR)", 0.229, PCT, "input")
    label_value(ws, 7, "Monthly payment", 150, MONEY, "input")
    label_value(ws, 8, "Months to clear", '=IF(C7<=C5*C6/12,"Payment too low",NPER(C6/12,-C7,C5))', "0", "summary")
    label_value(ws, 9, "Total interest paid", '=IFERROR(C7*C8-C5,"")', MONEY, "summary")
    header_row(ws, 11, 2, ["Month", "Opening balance", "Interest", "Payment", "Closing balance", ""])
    for m in range(1, 121):
        r = 11 + m
        put(ws, r, 2, m, "0")
        if m == 1:
            put(ws, r, 3, "=$C$5", MONEY)
        else:
            put(ws, r, 3, f'=IF(OR(F{r-1}="",F{r-1}<=0.005),"",F{r-1})', MONEY)
        put(ws, r, 4, f'=IF(C{r}="","",C{r}*$C$6/12)', MONEY)
        put(ws, r, 5, f'=IF(C{r}="","",MIN($C$7,C{r}+D{r}))', MONEY)
        put(ws, r, 6, f'=IF(C{r}="","",ROUND(C{r}+D{r}-E{r},2))', MONEY)
    ws.column_dimensions["G"].width = 3
    wb.save(path)
