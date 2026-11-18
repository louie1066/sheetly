"""Project & Task Management templates 1-8: Gantt, Kanban, budget, task list, milestones, risks, RACI, meetings."""
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from openpyxl.formatting.rule import FormulaRule
from common import *

REPORT = dt.date(2026, 12, 1)
START = dt.date(2026, 12, 7)  # a Monday


def gantt_chart(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Gantt"
    weeks = 12
    setup_sheet(ws, "Gantt Chart", "Enter each task's start and end date. Bars fill the weeks the task runs, counting from the project start", 6 + weeks,
                [28, 14, 12, 12, 8, 11] + [6.5] * weeks)
    header_row(ws, 5, 2, ["Task", "Owner", "Start", "End", "Days", "% complete"])
    for k in range(weeks):
        col = 8 + k
        c = ws.cell(5, col, "=$C$22" if k == 0 else f"={L(col - 1)}5+7")
        c.number_format = "dd/mm"
        c.font = font(8, True)
        c.fill = fill(HEADER)
        c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center")
    tasks = [
        ("Define scope and goals", "Project lead", dt.date(2026, 12, 7), dt.date(2026, 12, 11), 1),
        ("Gather requirements", "Business analyst", dt.date(2026, 12, 9), dt.date(2026, 12, 18), 1),
        ("Design solution", "Designer", dt.date(2026, 12, 14), dt.date(2026, 12, 22), 0.6),
        ("Build prototype", "Developer", dt.date(2026, 12, 21), dt.date(2027, 1, 8), 0.2),
        ("Test with users", "Tester", dt.date(2027, 1, 11), dt.date(2027, 1, 22), 0),
        ("Fix issues", "Developer", dt.date(2027, 1, 19), dt.date(2027, 1, 29), 0),
        ("Staff training", "Trainer", dt.date(2027, 1, 25), dt.date(2027, 2, 5), 0),
        ("Pilot launch", "Project lead", dt.date(2027, 2, 2), dt.date(2027, 2, 6), 0),
        ("Full launch", "Project lead", dt.date(2027, 2, 9), dt.date(2027, 2, 9), 0),
        ("Review and close", "Project lead", dt.date(2027, 2, 16), dt.date(2027, 2, 20), 0),
    ]
    for r in range(6, 18):
        t = tasks[r - 6] if r - 6 < len(tasks) else (None, None, None, None, None)
        put(ws, r, 2, t[0])
        put(ws, r, 3, t[1])
        put(ws, r, 4, t[2], DATE)
        put(ws, r, 5, t[3], DATE)
        put(ws, r, 6, f'=IF(OR(D{r}="",E{r}=""),"",E{r}-D{r}+1)', "0", "calc")
        put(ws, r, 7, t[4], "0%")
        for col in range(8, 8 + weeks):
            put(ws, r, col, None, kind="calc")
    ws.conditional_formatting.add("H6:S17", FormulaRule(
        formula=['AND($D6<>"",$E6<>"",H$5<=$E6,H$5+6>=$D6)'], fill=fill("9DC3E6")))
    validate(ws, "G6:G17", "0", kind="decimal", operator="between", formula2="1")
    label_value(ws, 22, "Project start (a Monday)", START, DATE)
    label_value(ws, 24, "Tasks listed", '=COUNTA(B6:B17)', "0", "summary")
    label_value(ws, 25, "Average % complete", '=IFERROR(AVERAGE(G6:G17),0)', "0%", "summary")
    label_value(ws, 26, "Project finish date", '=IF(COUNT(E6:E17)=0,"",MAX(E6:E17))', DATE, "summary")
    wb.save(path)


def kanban_board(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Board"
    setup_sheet(ws, "Kanban Board", "Log each card and move it between columns. Days to due and the WIP check calculate automatically", 8,
                [10, 32, 14, 14, 11, 12, 12, 14])
    header_row(ws, 5, 2, ["Card ID", "Task", "Owner", "Column", "Priority", "Due date", "Days to due", "Flag"])
    cards = [
        ("K-01", "Write user guide", "Ana", "Backlog", "Low", dt.date(2027, 1, 15)),
        ("K-02", "Set up test server", "Ben", "To do", "High", dt.date(2026, 12, 18)),
        ("K-03", "Design login page", "Chloe", "In progress", "High", dt.date(2026, 12, 10)),
        ("K-04", "Fix export bug", "Ben", "In progress", "Medium", dt.date(2026, 11, 28)),
        ("K-05", "Review data model", "Dev", "Review", "Medium", dt.date(2026, 12, 4)),
        ("K-06", "Update privacy notice", "Ana", "To do", "Low", dt.date(2027, 1, 30)),
        ("K-07", "Load test results", "Dev", "Done", "High", dt.date(2026, 11, 25)),
        ("K-08", "Create onboarding video", "Chloe", "Backlog", "Low", None),
    ]
    for r in range(6, 20):
        c = cards[r - 6] if r - 6 < len(cards) else (None,) * 6
        put(ws, r, 2, c[0])
        put(ws, r, 3, c[1])
        put(ws, r, 4, c[2])
        put(ws, r, 5, c[3])
        put(ws, r, 6, c[4])
        put(ws, r, 7, c[5], DATE)
        put(ws, r, 8, f'=IF(OR(B{r}="",G{r}="",E{r}="Done"),"",G{r}-$C$22)', "0", "calc")
        put(ws, r, 9, f'=IF(B{r}="","",IF(E{r}="Done","Complete",IF(H{r}="","No due date",IF(H{r}<0,"Overdue",IF(H{r}<=3,"Due soon","On track")))))',
            None, "calc")
    validate(ws, "E6:E19", '"Backlog,To do,In progress,Review,Done"')
    validate(ws, "F6:F19", '"High,Medium,Low"')
    label_value(ws, 22, "Report date", REPORT, DATE)
    header_row(ws, 24, 2, ["Column", "Cards", "WIP limit", "Status"])
    wip = {"Backlog": None, "To do": 5, "In progress": 3, "Review": 3, "Done": None}
    for i, (name, limit) in enumerate(wip.items()):
        r = 25 + i
        put(ws, r, 2, name, kind="label", bold=True)
        put(ws, r, 3, f'=COUNTIF($E$6:$E$19,B{r})', "0", "calc")
        put(ws, r, 4, limit, "0")
        put(ws, r, 5, f'=IF(D{r}="","No limit",IF(C{r}>D{r},"Over limit","Within limit"))', None, "calc")
    wb.save(path)


def project_budget(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget"
    setup_sheet(ws, "Project Budget Tracker", "Enter budget, spend and commitments per line. Forecast, variance and status calculate automatically", 8,
                [30, 14, 14, 14, 14, 14, 11, 16])
    header_row(ws, 5, 2, ["Cost line", "Budget", "Actual to date", "Committed (not yet paid)", "Forecast cost", "Variance", "% of budget used", "Status"])
    lines = [("Staff time", 42000, 18500, 12000), ("Software licences", 6000, 5200, 800), ("Hardware", 9000, 3100, 5600),
             ("Training", 3000, 0, 1500), ("Travel", 2000, 900, 400), ("Printing and materials", 800, 310, 120),
             ("Consultants", 12000, 7000, 6500), ("Contingency", 4000, 0, 0)]
    for i in range(12):
        r = 6 + i
        ln = lines[i] if i < len(lines) else (None, None, None, None)
        put(ws, r, 2, ln[0])
        put(ws, r, 3, ln[1], MONEY)
        put(ws, r, 4, ln[2], MONEY)
        put(ws, r, 5, ln[3], MONEY)
        put(ws, r, 6, f'=IF(B{r}="","",D{r}+E{r})', MONEY, "calc")
        put(ws, r, 7, f'=IF(B{r}="","",C{r}-F{r})', MONEY, "calc")
        put(ws, r, 8, f'=IF(OR(B{r}="",C{r}=0),"",F{r}/C{r})', "0%", "calc")
        put(ws, r, 9, f'=IF(B{r}="","",IF(G{r}<0,"Over budget","Within budget"))', None, "calc")
    put(ws, 18, 2, "Total", kind="total")
    for col, letter in zip(range(3, 8), "CDEFG"):
        put(ws, 18, col, f"=SUM({letter}6:{letter}17)", MONEY, "total")
    put(ws, 18, 8, '=IFERROR(F18/C18,0)', "0%", "total")
    put(ws, 18, 9, "", kind="total")
    label_value(ws, 21, "Total budget", '=C18', MONEY, "summary")
    label_value(ws, 22, "Forecast cost", '=F18', MONEY, "summary")
    label_value(ws, 23, "Forecast variance (+ under, - over)", '=G18', MONEY, "summary")
    label_value(ws, 24, "Lines over budget", '=COUNTIF(I6:I17,"Over budget")', "0", "summary")
    wb.save(path)


def task_list(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tasks"
    setup_sheet(ws, "Task List with Priorities", "List each task with its priority, status and due date. Days left and flags calculate from the report date", 8,
                [34, 14, 11, 14, 12, 11, 15, 3])
    header_row(ws, 5, 2, ["Task", "Owner", "Priority", "Status", "Due date", "Days left", "Flag"])
    tasks = [
        ("Confirm project scope with sponsor", "Maya", "High", "Done", dt.date(2026, 11, 27)),
        ("Book kick-off meeting room", "Sam", "Low", "Done", dt.date(2026, 11, 30)),
        ("Draft risk register", "Maya", "High", "In progress", dt.date(2026, 12, 3)),
        ("Get supplier quotes", "Leo", "Medium", "Blocked", dt.date(2026, 12, 2)),
        ("Set up shared folder", "Sam", "Medium", "In progress", dt.date(2026, 12, 6)),
        ("Agree budget with finance", "Maya", "High", "Not started", dt.date(2026, 12, 14)),
        ("Write communication plan", "Leo", "Low", "Not started", dt.date(2026, 12, 18)),
        ("Schedule stakeholder reviews", "Sam", "Medium", "Not started", None),
    ]
    for r in range(6, 20):
        t = tasks[r - 6] if r - 6 < len(tasks) else (None,) * 5
        put(ws, r, 2, t[0])
        put(ws, r, 3, t[1])
        put(ws, r, 4, t[2])
        put(ws, r, 5, t[3])
        put(ws, r, 6, t[4], DATE)
        put(ws, r, 7, f'=IF(OR(B{r}="",F{r}=""),"",F{r}-$C$22)', "0", "calc")
        put(ws, r, 8, f'=IF(B{r}="","",IF(E{r}="Done","Complete",IF(F{r}="","No due date",IF(F{r}<$C$22,"Overdue",IF(F{r}-$C$22<=3,"Due soon","On track")))))',
            None, "calc")
    validate(ws, "D6:D19", '"High,Medium,Low"')
    validate(ws, "E6:E19", '"Not started,In progress,Blocked,Done"')
    label_value(ws, 22, "Report date", REPORT, DATE)
    label_value(ws, 24, "Open tasks", '=COUNTIFS(B6:B19,"<>",E6:E19,"<>Done")', "0", "summary")
    label_value(ws, 25, "High priority still open", '=COUNTIFS(D6:D19,"High",E6:E19,"<>Done")', "0", "summary")
    label_value(ws, 26, "Overdue", '=COUNTIF(H6:H19,"Overdue")', "0", "summary")
    label_value(ws, 27, "Due within 3 days", '=COUNTIF(H6:H19,"Due soon")', "0", "summary")
    wb.save(path)


def milestone_tracker(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Milestones"
    setup_sheet(ws, "Milestone Tracker", "Compare each target date with the forecast date. Slip and the traffic-light rating calculate automatically", 8,
                [30, 15, 13, 13, 11, 13, 12])
    header_row(ws, 5, 2, ["Milestone", "Owner", "Target date", "Forecast date", "Slip (days)", "Status", "Rating"])
    ms = [("Project charter signed", "Maya", dt.date(2026, 12, 4), dt.date(2026, 12, 4), "Achieved"),
          ("Requirements approved", "Leo", dt.date(2026, 12, 18), dt.date(2026, 12, 21), "At risk"),
          ("Design sign-off", "Sam", dt.date(2027, 1, 8), dt.date(2027, 1, 8), "On track"),
          ("Prototype ready", "Dev lead", dt.date(2027, 1, 15), dt.date(2027, 1, 27), "Late"),
          ("User testing complete", "Tester", dt.date(2027, 1, 29), dt.date(2027, 1, 29), "On track"),
          ("Training delivered", "Trainer", dt.date(2027, 2, 5), None, "On track"),
          ("Pilot launch", "Maya", dt.date(2027, 2, 9), None, "On track"),
          ("Project closed", "Maya", dt.date(2027, 2, 26), None, "On track")]
    for r in range(6, 18):
        m = ms[r - 6] if r - 6 < len(ms) else (None,) * 5
        put(ws, r, 2, m[0])
        put(ws, r, 3, m[1])
        put(ws, r, 4, m[2], DATE)
        put(ws, r, 5, m[3], DATE)
        put(ws, r, 6, f'=IF(OR(D{r}="",E{r}=""),"",E{r}-D{r})', "0;-0;0", "calc")
        put(ws, r, 7, m[4])
        put(ws, r, 8, f'=IF(OR(B{r}="",G{r}=""),"",IF(G{r}="Achieved","Done",IF(OR(G{r}="Late",N(F{r})>7),"Red",IF(OR(G{r}="At risk",N(F{r})>0),"Amber","Green"))))',
            None, "calc")
    validate(ws, "G6:G17", '"Achieved,On track,At risk,Late"')
    label_value(ws, 20, "Milestones", '=COUNTA(B6:B17)', "0", "summary")
    label_value(ws, 21, "Achieved", '=COUNTIF(G6:G17,"Achieved")', "0", "summary")
    label_value(ws, 22, "Rated red", '=COUNTIF(H6:H17,"Red")', "0", "summary")
    label_value(ws, 23, "Average slip (days)", '=IFERROR(AVERAGE(F6:F17),0)', "0.0", "summary")
    note(ws, 25, "Rating: Red if late or slipped more than 7 days; Amber if at risk or slipped; Green otherwise.")
    wb.save(path)


def risk_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Risks"
    setup_sheet(ws, "Risk Register", "Score each risk as likelihood x impact (1 to 5 each). The rating and summary calculate automatically", 10,
                [22, 34, 14, 12, 12, 10, 11, 14, 12, 12])
    header_row(ws, 5, 2, ["Risk ID", "Risk description", "Category", "Likelihood (1-5)", "Impact (1-5)", "Score",
                          "Rating", "Owner", "Response", "Status"])
    risks = [
        ("R-01", "Key developer leaves mid-project", "People", 3, 4, "Maya", "Reduce", "Open"),
        ("R-02", "Supplier delivers hardware late", "Supplier", 4, 3, "Leo", "Reduce", "Monitoring"),
        ("R-03", "Budget overspend on consultants", "Financial", 3, 4, "Sam", "Avoid", "Open"),
        ("R-04", "Scope creep from new requests", "Scope", 4, 2, "Maya", "Accept", "Open"),
        ("R-05", "Data migration errors", "Technical", 2, 5, "Dev lead", "Reduce", "Open"),
        ("R-06", "Staff unavailable for training", "People", 2, 2, "Trainer", "Accept", "Closed"),
    ]
    for r in range(6, 21):
        k = risks[r - 6] if r - 6 < len(risks) else (None,) * 8
        put(ws, r, 2, k[0] if k[0] else None)
        put(ws, r, 3, k[1])
        put(ws, r, 4, k[2])
        put(ws, r, 5, k[3], "0")
        put(ws, r, 6, k[4], "0")
        put(ws, r, 7, f'=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})', "0", "calc")
        put(ws, r, 8, f'=IF(G{r}="","",IF(G{r}>=15,"High",IF(G{r}>=8,"Medium","Low")))', None, "calc")
        put(ws, r, 9, k[5])
        put(ws, r, 10, k[6])
        put(ws, r, 11, k[7])
    validate(ws, "E6:F20", "1", kind="whole", operator="between", formula2="5")
    validate(ws, "J6:J20", '"Avoid,Reduce,Transfer,Accept"')
    validate(ws, "K6:K20", '"Open,Monitoring,Closed"')
    label_value(ws, 23, "Risks logged", '=COUNTA(C6:C20)', "0", "summary")
    label_value(ws, 24, "High rated", '=COUNTIF(H6:H20,"High")', "0", "summary")
    label_value(ws, 25, "Medium rated", '=COUNTIF(H6:H20,"Medium")', "0", "summary")
    label_value(ws, 26, "Average score", '=IFERROR(AVERAGE(G6:G20),0)', "0.0", "summary")
    note(ws, 28, "Score = likelihood x impact. 15 or more is High, 8 to 14 is Medium, under 8 is Low.")
    wb.save(path)


def raci_matrix(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "RACI"
    roles = ["Project lead", "Product owner", "Developer", "Tester", "Client", "Finance"]
    setup_sheet(ws, "RACI Matrix", "R = does the work, A = accountable (one per activity), C = consulted, I = informed", 8,
                [34, 13, 13, 13, 13, 13, 13, 16])
    header_row(ws, 5, 2, ["Activity"] + roles + ["Check"])
    rows = [
        ("Approve project plan", ["A", "R", "C", "I", "C", "C"]),
        ("Set budget", ["R", "C", "I", "I", "C", "A"]),
        ("Manage schedule", ["A", "R", "C", "I", "I", "I"]),
        ("Build deliverables", ["I", "C", "A", "C", "I", "I"]),
        ("Test deliverables", ["I", "C", "C", "A", "I", "I"]),
        ("Sign off release", ["C", "A", "I", "C", "R", "I"]),
        ("Communicate progress", ["A", "R", "I", "I", "I", "I"]),
        ("Manage risks", ["A", "R", "C", "C", "I", "I"]),
        ("Pay supplier invoices", ["C", "I", "I", "I", "I", "A"]),
        ("Close project", ["A", "C", "C", "C", "C", "I"]),
    ]
    for r in range(6, 16):
        row = rows[r - 6] if r - 6 < len(rows) else (None, [None] * 6)
        put(ws, r, 2, row[0])
        for j, v in enumerate(row[1]):
            put(ws, r, 3 + j, v, None)
            ws.cell(r, 3 + j).alignment = Alignment(horizontal="center", vertical="center")
        put(ws, r, 9, f'=IF(B{r}="","",IF(COUNTIF(C{r}:H{r},"A")=1,"OK","Needs one A"))', None, "calc")
    validate(ws, "C6:H15", '"R,A,C,I"')
    label_value(ws, 18, "Activities", '=COUNTA(B6:B15)', "0", "summary")
    label_value(ws, 19, "Activities needing one A", '=COUNTIF(I6:I15,"Needs one A")', "0", "summary")
    wb.save(path)


def meeting_log(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Meetings"
    setup_sheet(ws, "Meeting Agenda and Minutes Log", "Log each meeting, its attendance and outcomes. Totals and averages calculate at the foot of the sheet", 9,
                [22, 30, 14, 14, 12, 12, 12, 12, 12])
    header_row(ws, 5, 2, ["Date", "Meeting", "Chair", "Minutes by", "Agenda sent?", "Attendees", "Duration (min)", "Decisions", "Actions raised"])
    mtgs = [(dt.date(2026, 11, 24), "Project kick-off", "Maya", "Sam", "Yes", 9, 90, 3, 6),
            (dt.date(2026, 12, 1), "Weekly stand-up", "Leo", "Ana", "Yes", 6, 20, 1, 3),
            (dt.date(2026, 12, 8), "Requirements review", "Maya", "Sam", "Yes", 8, 60, 4, 5),
            (dt.date(2026, 12, 15), "Budget check-in", "Maya", "Leo", "No", 4, 45, 2, 2)]
    for r in range(6, 21):
        m = mtgs[r - 6] if r - 6 < len(mtgs) else (None,) * 9
        put(ws, r, 2, m[0], DATE)
        put(ws, r, 3, m[1])
        put(ws, r, 4, m[2])
        put(ws, r, 5, m[3])
        put(ws, r, 6, m[4])
        put(ws, r, 7, m[5], "0")
        put(ws, r, 8, m[6], "0")
        put(ws, r, 9, m[7], "0")
        put(ws, r, 10, m[8], "0")
    validate(ws, "F6:F20", '"Yes,No"')
    label_value(ws, 23, "Meetings logged", '=COUNTA(C6:C20)', "0", "summary")
    label_value(ws, 24, "Total meeting hours", '=SUM(H6:H20)/60', "0.0", "summary")
    label_value(ws, 25, "Average attendees", '=IFERROR(AVERAGE(G6:G20),0)', "0.0", "summary")
    label_value(ws, 26, "Meetings without agenda", '=COUNTIF(F6:F20,"No")', "0", "summary")
    label_value(ws, 27, "Actions raised", '=SUM(J6:J20)', "0", "summary")
    wb.save(path)
