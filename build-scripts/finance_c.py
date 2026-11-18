"""Templates 18-25: savings growth, sinking funds, tax, freelance income, shopping and gifts."""
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *


def retirement(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Projection"
    setup_sheet(ws, "Retirement Savings Projection", "Estimate how your pension or savings could grow by retirement age", 6,
                [22, 16, 18, 18, 18, 18])
    label_value(ws, 5, "Current age", 35, "0", "input")
    label_value(ws, 6, "Retirement age", 65, "0", "input")
    label_value(ws, 7, "Current savings", 15000, MONEY, "input")
    label_value(ws, 8, "Yearly contribution", 4800, MONEY, "input")
    label_value(ws, 9, "Expected annual growth", 0.05, PCT, "input")
    header_row(ws, 11, 2, ["Age", "Opening balance", "Contributions", "Growth", "Closing balance", ""])
    for i in range(45):
        r = 12 + i
        put(ws, r, 2, f'=IF($C$5+{i}<=$C$6,$C$5+{i},"")', "0")
        opening = "$C$7" if i == 0 else f'IF(F{r-1}="","",F{r-1})'
        put(ws, r, 3, f'=IF(B{r}="","",{opening})', MONEY)
        put(ws, r, 4, f'=IF(B{r}="","",$C$8)', MONEY)
        put(ws, r, 5, f'=IF(B{r}="","",(C{r}+D{r})*$C$9)', MONEY)
        put(ws, r, 6, f'=IF(B{r}="","",C{r}+D{r}+E{r})', MONEY)
    ws.column_dimensions["G"].width = 3
    wb.save(path)


def compound(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Growth"
    setup_sheet(ws, "Compound Interest Calculator", "See how interest and regular saving grow over time (monthly compounding)", 6,
                [14, 18, 18, 18, 18, 18])
    label_value(ws, 5, "Starting amount", 5000, MONEY, "input")
    label_value(ws, 6, "Monthly contribution", 150, MONEY, "input")
    label_value(ws, 7, "Annual interest rate", 0.06, PCT, "input")
    label_value(ws, 8, "Years", 10, "0", "input")
    label_value(ws, 9, "Final balance", "=IFERROR(C5*(1+C7/12)^(C8*12)+C6*(((1+C7/12)^(C8*12)-1)/(C7/12)),C5+C6*C8*12)", MONEY, "summary")
    label_value(ws, 10, "Total you paid in", "=C5+C6*C8*12", MONEY, "summary")
    label_value(ws, 11, "Interest earned", "=C9-C10", MONEY, "summary")
    header_row(ws, 13, 2, ["Year", "Paid in (total)", "Balance", "Interest earned to date", "", ""])
    for y in range(1, 41):
        r = 13 + y
        put(ws, r, 2, f'=IF({y}<=$C$8,{y},"")', "0")
        put(ws, r, 3, f'=IF(B{r}="","",$C$5+$C$6*B{r}*12)', MONEY)
        put(ws, r, 4, f'=IF(B{r}="","",IFERROR($C$5*(1+$C$7/12)^(B{r}*12)+$C$6*(((1+$C$7/12)^(B{r}*12)-1)/($C$7/12)),C{r}))', MONEY)
        put(ws, r, 5, f'=IF(B{r}="","",D{r}-C{r})', MONEY)
    ws.column_dimensions["G"].width = 3
    wb.save(path)


def sinking_funds(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sinking Funds"
    setup_sheet(ws, "Sinking Funds Planner", "Save a little each month for costs that come once a year", 7,
                [26, 16, 16, 18, 16, 16])
    header_row(ws, 5, 2, ["Future cost", "Expected cost", "Months until due", "Monthly set-aside", "Saved so far", "Remaining"])
    items = [("Car insurance", 480, 6, 200), ("Holiday", 1500, 10, 300), ("Christmas gifts", 600, 8, 120),
             ("Car service", 350, 4, 50), ("Annual subscriptions", 240, 3, 40)]
    for i in range(10):
        r = 6 + i
        if i < len(items):
            n, c, m, s = items[i]
            put(ws, r, 2, n, kind="input")
            put(ws, r, 3, c, MONEY, "input")
            put(ws, r, 4, m, "0", "input")
            put(ws, r, 6, s, MONEY, "input")
        else:
            put(ws, r, 2, None, kind="input")
            put(ws, r, 3, None, MONEY, "input")
            put(ws, r, 4, None, "0", "input")
            put(ws, r, 6, None, MONEY, "input")
        put(ws, r, 5, f'=IF(OR(D{r}="",D{r}<=0),"",C{r}/D{r})', MONEY)
        put(ws, r, 7, f'=IF(C{r}="","",MAX(0,C{r}-F{r}))', MONEY)
    put(ws, 16, 2, "Totals", kind="total")
    put(ws, 16, 3, "=SUM(C6:C15)", MONEY, "total")
    put(ws, 16, 4, "", kind="total")
    put(ws, 16, 5, "=SUM(E6:E15)", MONEY, "total")
    put(ws, 16, 6, "=SUM(F6:F15)", MONEY, "total")
    put(ws, 16, 7, "=SUM(G6:G15)", MONEY, "total")
    label_value(ws, 18, "Monthly amount to set aside", "=SUM(E6:E15)", MONEY, "summary")
    wb.save(path)


def tax_estimate(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tax Estimate"
    setup_sheet(ws, "Tax Estimate Calculator", "Estimate income tax using progressive bands. Check your local rules", 4,
                [30, 18, 18, 18])
    label_value(ws, 5, "Annual gross income", 42000, MONEY, "input")
    label_value(ws, 6, "Tax-free allowance", 12000, MONEY, "input")
    header_row(ws, 8, 2, ["Tax band", "From (taxable income)", "To", "Rate"])
    bands = [("Basic", 0, 37000, 0.20), ("Higher", 37000, 125000, 0.40), ("Additional", 125000, 999999999, 0.45)]
    for i, (n, lo, hi, rt) in enumerate(bands):
        r = 9 + i
        put(ws, r, 2, n, kind="input")
        put(ws, r, 3, lo, MONEY, "input")
        put(ws, r, 4, hi, MONEY, "input")
        put(ws, r, 5, rt, PCT, "input")
    header_row(ws, 13, 2, ["Band", "Income in band", "Tax in band", ""])
    for i in range(3):
        r = 14 + i
        src = 9 + i
        put(ws, r, 2, f"=B{src}")
        put(ws, r, 3, f"=MAX(0,MIN($C$5-$C$6,D{src})-C{src})", MONEY)
        put(ws, r, 4, f"=C{r}*E{src}", MONEY)
    put(ws, 17, 2, "Total", kind="total")
    put(ws, 17, 3, "=SUM(C14:C16)", MONEY, "total")
    put(ws, 17, 4, "=SUM(D14:D16)", MONEY, "total")
    label_value(ws, 19, "Taxable income", "=MAX(0,C5-C6)", MONEY)
    label_value(ws, 20, "Estimated income tax", "=D17", MONEY, "summary")
    label_value(ws, 21, "Effective tax rate", '=IF(C5=0,0,C20/C5)', "0.0%", "summary")
    label_value(ws, 22, "Take-home after tax (before other deductions)", "=C5-C20", MONEY, "summary")
    wb.save(path)


def freelancer(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Income Log"
    setup_sheet(ws, "Freelancer Income Tracker", "Log work, invoices and payments, and set aside money for tax", 8,
                [14, 20, 22, 10, 14, 16, 12])
    label_value(ws, 5, "Percent of income to set aside for tax", 0.25, "0%", "input")
    header_row(ws, 7, 2, ["Date", "Client", "Project", "Hours", "Hourly rate", "Amount", "Paid?"])
    rows = [("03/11/2026", "Northside School", "Worksheet design", 6, 35, "Yes"),
            ("06/11/2026", "Bright Academy", "Website copy", 4, 40, "No"),
            ("10/11/2026", "Northside School", "Quiz bank", 8, 35, "No")]
    from openpyxl.worksheet.datavalidation import DataValidation
    dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    ws.add_data_validation(dv)
    for i in range(30):
        r = 8 + i
        if i < len(rows):
            d, c, p, h, rt, pd = rows[i]
            put(ws, r, 2, d, kind="input")
            put(ws, r, 3, c, kind="input")
            put(ws, r, 4, p, kind="input")
            put(ws, r, 5, h, "0.0", "input")
            put(ws, r, 6, rt, MONEY, "input")
            put(ws, r, 8, pd, kind="input")
        else:
            put(ws, r, 2, None, kind="input")
            put(ws, r, 3, None, kind="input")
            put(ws, r, 4, None, kind="input")
            put(ws, r, 5, None, "0.0", "input")
            put(ws, r, 6, None, MONEY, "input")
            put(ws, r, 8, None, kind="input")
        dv.add(f"H{r}")
        put(ws, r, 7, f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})', MONEY)
    put(ws, 38, 2, "Totals", kind="total")
    for c in (3, 4, 6, 8):
        put(ws, 38, c, "", kind="total")
    put(ws, 38, 5, "=SUM(E8:E37)", "0.0", "total")
    put(ws, 38, 7, "=SUM(G8:G37)", MONEY, "total")
    label_value(ws, 40, "Received so far", '=SUMIF(H8:H37,"Yes",G8:G37)', MONEY, "summary")
    label_value(ws, 41, "Awaiting payment", '=SUMIF(H8:H37,"No",G8:G37)', MONEY, "summary")
    label_value(ws, 42, "Set aside for tax", "=G38*C5", MONEY, "summary")
    ws.column_dimensions["I"].width = 3
    wb.save(path)


def price_compare(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Compare"
    setup_sheet(ws, "Price Comparison Sheet", "Compare prices per unit to find the best value", 7,
                [22, 24, 14, 14, 16, 16])
    header_row(ws, 5, 2, ["Product", "Option / store", "Price", "Quantity", "Price per unit", "Best value?"])
    rows = [("Rice", "Store A, 2 kg", 4.20, 2), ("Rice", "Store B, 5 kg", 9.50, 5),
            ("Rice", "Market, 1 kg", 2.40, 1), ("Cooking oil", "Store A, 1 L", 3.10, 1),
            ("Cooking oil", "Store B, 2 L", 5.60, 2)]
    for i in range(20):
        r = 6 + i
        if i < len(rows):
            p, o, pr, q = rows[i]
            put(ws, r, 2, p, kind="input")
            put(ws, r, 3, o, kind="input")
            put(ws, r, 4, pr, MONEY, "input")
            put(ws, r, 5, q, "0.0", "input")
        else:
            for c in (2, 3):
                put(ws, r, c, None, kind="input")
            put(ws, r, 4, None, MONEY, "input")
            put(ws, r, 5, None, "0.0", "input")
        put(ws, r, 6, f'=IF(OR(D{r}="",E{r}="",E{r}=0),"",D{r}/E{r})', MONEY)
        put(ws, r, 7, f'=IF(F{r}="","",IF(COUNTIFS($B$6:$B$25,B{r},$F$6:$F$25,"<"&F{r})=0,"Best",""))')
    ws.column_dimensions["H"].width = 3
    wb.save(path)


def weekly_grocery(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly Budget"
    setup_sheet(ws, "Weekly Grocery Budget", "Set a weekly food budget and track it against actual spending", 6,
                [16, 16, 16, 16, 18, 14])
    label_value(ws, 5, "Weekly grocery budget", 100, MONEY, "input")
    header_row(ws, 7, 2, ["Week", "Budget", "Actual spent", "Difference", "Running difference", "Status"])
    actual = [96.40, 118.75, 88.10, 104.00]
    for i in range(4):
        r = 8 + i
        put(ws, r, 2, f"Week {i+1}")
        put(ws, r, 3, "=$C$5", MONEY)
        put(ws, r, 4, actual[i], MONEY, "input")
        put(ws, r, 5, f"=C{r}-D{r}", MONEY)
        put(ws, r, 6, f"=SUM($E$8:E{r})", MONEY)
        put(ws, r, 7, f'=IF(D{r}>C{r},"Over","Under")')
    put(ws, 12, 2, "Month", kind="total")
    put(ws, 12, 3, "=SUM(C8:C11)", MONEY, "total")
    put(ws, 12, 4, "=SUM(D8:D11)", MONEY, "total")
    put(ws, 12, 5, "=SUM(E8:E11)", MONEY, "total")
    put(ws, 12, 6, "", kind="total")
    put(ws, 12, 7, "", kind="total")
    label_value(ws, 14, "Average weekly spend", "=AVERAGE(D8:D11)", MONEY, "summary")
    wb.save(path)


def gift_budget(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Gift Budget"
    setup_sheet(ws, "Holiday Gift Budget", "Plan gifts, set limits and track what you have spent", 7,
                [22, 18, 26, 14, 14, 14])
    label_value(ws, 5, "Total gift budget", 600, MONEY, "input")
    header_row(ws, 7, 2, ["Recipient", "Relationship", "Gift idea", "Planned", "Actual", "Difference"])
    gifts = [("Parent", "Family", "Photo book", 80, 72), ("Partner", "Family", "Concert tickets", 150, 160),
             ("Nephew", "Family", "Science kit", 35, 29.5), ("Colleague", "Work", "Coffee voucher", 20, 0),
             ("Friend", "Friend", "Book", 25, 25)]
    for i in range(15):
        r = 8 + i
        if i < len(gifts):
            n, rel, idea, pl, ac = gifts[i]
            put(ws, r, 2, n, kind="input")
            put(ws, r, 3, rel, kind="input")
            put(ws, r, 4, idea, kind="input")
            put(ws, r, 5, pl, MONEY, "input")
            put(ws, r, 6, ac, MONEY, "input")
        else:
            for c in (2, 3, 4):
                put(ws, r, c, None, kind="input")
            put(ws, r, 5, None, MONEY, "input")
            put(ws, r, 6, None, MONEY, "input")
        put(ws, r, 7, f'=IF(E{r}="","",E{r}-F{r})', MONEY)
    put(ws, 23, 2, "Totals", kind="total")
    put(ws, 23, 3, "", kind="total")
    put(ws, 23, 4, "", kind="total")
    put(ws, 23, 5, "=SUM(E8:E22)", MONEY, "total")
    put(ws, 23, 6, "=SUM(F8:F22)", MONEY, "total")
    put(ws, 23, 7, "=SUM(G8:G22)", MONEY, "total")
    label_value(ws, 25, "Left in budget (total budget - actual)", "=C5-F23", MONEY, "summary")
    ws.column_dimensions["H"].width = 3
    wb.save(path)
