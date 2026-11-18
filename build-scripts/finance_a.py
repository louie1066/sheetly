"""Templates 1-8: budgets, expense tracking, debt payoff and amortisation."""
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from openpyxl.styles import Alignment
from common import *


def monthly_budget(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget"
    setup_sheet(ws, "Monthly Household Budget", "Plan each month's income and spending, then compare with actuals", 6,
                [30, 16, 16, 16, 14, 14])
    header_row(ws, 5, 2, ["Income source", "Planned", "Actual", "Difference", "", ""])
    income = [("Salary (main)", 3200, 3200), ("Side income", 300, 180), ("Other", 0, 0)]
    r = 6
    for name, p, a in income:
        put(ws, r, 2, name, kind="input")
        put(ws, r, 3, p, MONEY, "input")
        put(ws, r, 4, a, MONEY, "input")
        put(ws, r, 5, f"=D{r}-C{r}", MONEY, "calc")
        r += 1
    inc_tot = r
    put(ws, r, 2, "Total income", kind="total")
    for c in (3, 4, 5):
        put(ws, r, c, f"=SUM({L(c)}6:{L(c)}{r-1})", MONEY, "total")
    r += 2
    header_row(ws, r, 2, ["Expense category", "Planned", "Actual", "Difference", "% of plan used", "Status"])
    r += 1
    first = r
    exp = [("Rent or mortgage", 1100, 1100), ("Utilities", 180, 205), ("Groceries", 420, 388),
           ("Transport", 150, 170), ("Insurance", 120, 120), ("Phone and internet", 85, 85),
           ("Dining out", 120, 160), ("Entertainment", 80, 45), ("Savings", 300, 300), ("Other", 100, 60)]
    for name, p, a in exp:
        put(ws, r, 2, name)
        put(ws, r, 3, p, MONEY, "input")
        put(ws, r, 4, a, MONEY, "input")
        put(ws, r, 5, f"=C{r}-D{r}", MONEY)
        put(ws, r, 6, f'=IF(C{r}=0,"",D{r}/C{r})', "0%")
        put(ws, r, 7, f'=IF(D{r}>C{r},"Over","OK")')
        r += 1
    last = r - 1
    exp_tot = r
    put(ws, r, 2, "Total expenses", kind="total")
    for c in (3, 4, 5):
        put(ws, r, c, f"=SUM({L(c)}{first}:{L(c)}{last})", MONEY, "total")
    put(ws, r, 6, f"=IF(C{r}=0,\"\",D{r}/C{r})", "0%", "total")
    put(ws, r, 7, "", kind="total")
    r += 2
    section_label(ws, r, 2, "Result")
    r += 1
    label_value(ws, r, "Planned net (income - expenses)", f"=C{inc_tot}-C{exp_tot}", MONEY, "summary")
    r += 1
    label_value(ws, r, "Actual net (income - expenses)", f"=D{inc_tot}-D{exp_tot}", MONEY, "summary")
    ws.column_dimensions["G"].width = 12
    wb.save(path)


def zero_based(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Zero-Based Budget"
    setup_sheet(ws, "Zero-Based Budget", "Every pound of income gets a job. Aim for 'Left to assign' = 0", 4,
                [32, 18, 40, 16])
    label_value(ws, 5, "Total monthly income", 3500, MONEY, "input")
    header_row(ws, 7, 2, ["Category", "Amount assigned", "Notes", ""])
    items = [("Housing", 1100, "Rent plus service charge"), ("Utilities", 200, "Power, water, gas"),
             ("Food", 450, "Groceries and occasional meals out"), ("Transport", 180, "Fuel and bus pass"),
             ("Debt repayments", 300, "Minimum payments"), ("Savings", 500, "Emergency fund first"),
             ("Investing", 250, "Monthly index fund"), ("Personal", 150, "Clothing, haircuts"),
             ("Fun", 200, "Hobbies and outings"), ("Buffer", 170, "Unexpected costs")]
    r = 8
    for name, amt, note in items:
        put(ws, r, 2, name)
        put(ws, r, 3, amt, MONEY, "input")
        put(ws, r, 4, note, kind="input")
        r += 1
    last = r - 1
    put(ws, r, 2, "Total assigned", kind="total")
    put(ws, r, 3, f"=SUM(C8:C{last})", MONEY, "total")
    put(ws, r, 4, "", kind="total")
    tot = r
    r += 2
    label_value(ws, r, "Left to assign", f"=C5-C{tot}", MONEY, "summary")
    r += 1
    label_value(ws, r, "Status", f'=IF(ROUND(C{r-1},2)=0,"Every pound has a job",IF(C{r-1}>0,"Assign the rest","Over budget: reduce a category"))', None, "summary")
    ws.column_dimensions["D"].width = 40
    wb.save(path)


def envelope(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Envelopes"
    setup_sheet(ws, "Envelope Budgeting Tracker", "Give each spending area a fixed envelope and track what is left", 5,
                [26, 16, 16, 16, 18])
    label_value(ws, 5, "Money available this month", 1800, MONEY, "input")
    header_row(ws, 7, 2, ["Envelope", "Monthly allocation", "Spent so far", "Remaining", "Status"])
    envs = [("Groceries", 400, 287.5), ("Eating out", 120, 135), ("Fuel", 150, 96), ("Fun", 100, 42),
            ("Gifts", 60, 0), ("Household supplies", 80, 73.2), ("Clothing", 90, 0)]
    r = 8
    for name, alloc, spent in envs:
        put(ws, r, 2, name)
        put(ws, r, 3, alloc, MONEY, "input")
        put(ws, r, 4, spent, MONEY, "input")
        put(ws, r, 5, f"=C{r}-D{r}", MONEY)
        put(ws, r, 6, f'=IF(E{r}<0,"Overspent",IF(E{r}<=C{r}*0.2,"Almost empty","On track"))')
        r += 1
    last = r - 1
    put(ws, r, 2, "Totals", kind="total")
    for c in (3, 4, 5):
        put(ws, r, c, f"=SUM({L(c)}8:{L(c)}{last})", MONEY, "total")
    put(ws, r, 6, "", kind="total")
    tot = r
    r += 2
    label_value(ws, r, "Unallocated money", f"=C5-C{tot}", MONEY, "summary")
    ws.column_dimensions["F"].width = 16
    wb.save(path)


def expense_tracker(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"
    setup_sheet(ws, "Expense Tracker", "Log each spend as it happens. The summary sheet totals each category", 5,
                [14, 30, 18, 16, 18])
    header_row(ws, 5, 2, ["Date", "Description", "Category", "Amount", "Payment method"])
    cats = ["Groceries", "Transport", "Dining", "Utilities", "Entertainment", "Health", "Other"]
    sample = [("01/11/2026", "Supermarket weekly shop", "Groceries", 84.20, "Debit card"),
              ("02/11/2026", "Bus pass top-up", "Transport", 30.00, "Cash"),
              ("04/11/2026", "Lunch with colleague", "Dining", 14.50, "Credit card"),
              ("05/11/2026", "Electricity bill", "Utilities", 96.00, "Bank transfer"),
              ("07/11/2026", "Cinema tickets", "Entertainment", 26.00, "Debit card"),
              ("09/11/2026", "Pharmacy", "Health", 12.75, "Debit card")]
    for i in range(60):
        r = 6 + i
        if i < len(sample):
            d, desc, cat, amt, pm = sample[i]
            put(ws, r, 2, d, kind="input")
            put(ws, r, 3, desc, kind="input")
            put(ws, r, 4, cat, kind="input")
            put(ws, r, 5, amt, MONEY, "input")
            put(ws, r, 6, pm, kind="input")
        else:
            for c in range(2, 7):
                put(ws, r, c, None, MONEY if c == 5 else None, "input")
    ws.column_dimensions["G"].width = 3
    # Summary sheet
    s = wb.create_sheet("Summary")
    setup_sheet(s, "Expense Summary by Category", "Calculated automatically from the Expenses sheet", 3, [24, 18, 14])
    header_row(s, 5, 2, ["Category", "Total spent", "Share"])
    r = 6
    for cat in cats:
        put(s, r, 2, cat)
        put(s, r, 3, f"=SUMIF(Expenses!$D$6:$D$65,B{r},Expenses!$E$6:$E$65)", MONEY)
        put(s, r, 4, f"=IF($C$13=0,0,C{r}/$C$13)", "0.0%")
        r += 1
    put(s, r, 2, "Total", kind="total")
    put(s, r, 3, f"=SUM(C6:C{r-1})", MONEY, "total")
    put(s, r, 4, "", kind="total")
    s.cell(13, 3).value = f"=SUM(C6:C12)"
    s.cell(13, 3).number_format = MONEY
    s.cell(13, 2).value = "Total"
    s.cell(13, 2).font = font(10, True)
    s.cell(13, 3).fill = fill(TOTAL)
    s.column_dimensions["D"].width = 12
    wb.save(path)


def income_vs_expenses(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Year Summary"
    setup_sheet(ws, "Income vs Expenses Summary", "Twelve-month view of income, spending and savings rate", 7,
                [14, 16, 16, 16, 18, 14])
    header_row(ws, 5, 2, ["Month", "Income", "Expenses", "Net", "Cumulative net", "Savings rate"])
    inc = [3300, 3300, 3450, 3300, 3300, 3700, 3300, 3300, 3300, 3300, 3300, 3900]
    exp = [2650, 2710, 2800, 2620, 2580, 3050, 2700, 2640, 2690, 2735, 2880, 3320]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, m in enumerate(months):
        r = 6 + i
        put(ws, r, 2, m)
        put(ws, r, 3, inc[i], MONEY, "input")
        put(ws, r, 4, exp[i], MONEY, "input")
        put(ws, r, 5, f"=C{r}-D{r}", MONEY)
        put(ws, r, 6, f"=SUM($E$6:E{r})", MONEY)
        put(ws, r, 7, f'=IF(C{r}=0,"",E{r}/C{r})', "0.0%")
    put(ws, 18, 2, "Year total", kind="total")
    for c in (3, 4, 5):
        put(ws, 18, c, f"=SUM({L(c)}6:{L(c)}17)", MONEY, "total")
    put(ws, 18, 6, "", kind="total")
    put(ws, 18, 7, "=IF(C18=0,\"\",E18/C18)", "0.0%", "total")
    label_value(ws, 20, "Average monthly net", "=AVERAGE(E6:E17)", MONEY, "summary")
    label_value(ws, 21, "Best month (highest net)", '=INDEX(B6:B17,MATCH(MAX(E6:E17),E6:E17,0))', None, "summary")
    label_value(ws, 22, "Tightest month (lowest net)", '=INDEX(B6:B17,MATCH(MIN(E6:E17),E6:E17,0))', None, "summary")
    ws.column_dimensions["H"].width = 3
    wb.save(path)


def _debt_sheet(path, title, subtitle, rank_formula, rank_label):
    wb = Workbook()
    ws = wb.active
    ws.title = "Debts"
    setup_sheet(ws, title, subtitle, 8, [24, 16, 12, 16, 14, 16, 18, 18])
    label_value(ws, 5, "Extra monthly payment available", 150, MONEY, "input")
    header_row(ws, 7, 2, ["Debt", "Balance", "Annual rate", "Minimum payment", rank_label,
                          "Monthly interest", "Payment this month", "Months to clear (minimum only)"])
    debts = [("Credit card A", 2400, 0.229, 80), ("Store card", 650, 0.249, 35),
             ("Car loan", 6800, 0.069, 210), ("Personal loan", 3200, 0.114, 120)]
    first, last = 8, 8 + len(debts) - 1
    for i, (n, b, rate, mp) in enumerate(debts):
        r = first + i
        put(ws, r, 2, n, kind="input")
        put(ws, r, 3, b, MONEY, "input")
        put(ws, r, 4, rate, PCT, "input")
        put(ws, r, 5, mp, MONEY, "input")
        put(ws, r, 6, rank_formula(r, first, last), "0")
        put(ws, r, 7, f"=C{r}*D{r}/12", MONEY)
        put(ws, r, 8, f"=E{r}+IF(F{r}=1,$C$5,0)", MONEY)
        put(ws, r, 9, f'=IFERROR(NPER(D{r}/12,-E{r},C{r}),"Never")', "0")
    tot = last + 1
    put(ws, tot, 2, "Totals", kind="total")
    for c, f in ((3, MONEY), (5, MONEY), (7, MONEY), (8, MONEY)):
        put(ws, tot, c, f"=SUM({L(c)}{first}:{L(c)}{last})", f, "total")
    put(ws, tot, 4, "", kind="total")
    put(ws, tot, 6, "", kind="total")
    put(ws, tot, 9, "", kind="total")
    r = tot + 2
    label_value(ws, r, "Total debt", f"=C{tot}", MONEY, "summary")
    label_value(ws, r + 1, "Total monthly payment", f"=H{tot}", MONEY, "summary")
    label_value(ws, r + 2, "First debt to target", f'=INDEX(B{first}:B{last},MATCH(1,F{first}:F{last},0))', None, "summary")
    ws.column_dimensions["J"].width = 3
    wb.save(path)


def snowball(path):
    _debt_sheet(path, "Debt Snowball Calculator",
                "Pay the smallest balance first while paying minimums on the rest",
                lambda r, a, b: f"=RANK(C{r},$C${a}:$C${b},1)", "Priority (smallest balance = 1)")


def avalanche(path):
    _debt_sheet(path, "Debt Avalanche Calculator",
                "Pay the highest interest rate first to cut total interest",
                lambda r, a, b: f"=RANK(D{r},$D${a}:$D${b},0)", "Priority (highest rate = 1)")


def amortisation(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Loan Schedule"
    setup_sheet(ws, "Loan Amortisation Schedule", "Monthly repayment, interest and balance for a fixed-rate loan", 7,
                [12, 18, 16, 16, 16, 18])
    label_value(ws, 5, "Loan amount", 20000, MONEY, "input")
    label_value(ws, 6, "Annual interest rate", 0.065, PCT, "input")
    label_value(ws, 7, "Term (years)", 5, "0", "input")
    label_value(ws, 8, "Monthly payment", "=PMT(C6/12,C7*12,-C5)", MONEY, "summary")
    label_value(ws, 9, "Total interest paid", "=SUM(E14:E373)", MONEY, "summary")
    header_row(ws, 13, 2, ["Month", "Opening balance", "Payment", "Interest", "Principal", "Closing balance"])
    for m in range(1, 361):
        r = 13 + m
        put(ws, r, 2, f'=IF({m}<=$C$7*12,{m},"")', "0")
        put(ws, r, 3, f'=IF(B{r}="","",{"$C$5" if m == 1 else "G" + str(r - 1)})', MONEY)
        put(ws, r, 4, f'=IF(B{r}="","",$C$8)', MONEY)
        put(ws, r, 5, f'=IF(B{r}="","",C{r}*$C$6/12)', MONEY)
        put(ws, r, 6, f'=IF(B{r}="","",D{r}-E{r})', MONEY)
        put(ws, r, 7, f'=IF(B{r}="","",C{r}-F{r})', MONEY)
    ws.column_dimensions["H"].width = 3
    wb.save(path)
