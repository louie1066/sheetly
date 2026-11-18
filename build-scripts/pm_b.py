"""Project & Task Management templates 9-16: actions, resources, time, dashboard, weekly status, decisions, stakeholders, change control."""
import datetime as dt
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from common import *

REPORT = dt.date(2026, 12, 1)


def action_items(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Actions"
    setup_sheet(ws, "Action Items Tracker", "Record each action from meetings. Days overdue calculates from the report date", 7,
                [40, 14, 12, 12, 13, 13, 22])
    header_row(ws, 5, 2, ["Action", "Owner", "Raised", "Due", "Status", "Days overdue", "Source meeting"])
    acts = [
        ("Send revised budget to finance", "Maya", dt.date(2026, 11, 24), dt.date(2026, 11, 27), "Done", "Kick-off"),
        ("Confirm supplier delivery date", "Leo", dt.date(2026, 11, 24), dt.date(2026, 11, 28), "Open", "Kick-off"),
        ("Book user testing sessions", "Sam", dt.date(2026, 12, 1), dt.date(2026, 12, 5), "In progress", "Stand-up"),
        ("Update risk register", "Maya", dt.date(2026, 12, 1), dt.date(2026, 12, 4), "Blocked", "Stand-up"),
        ("Share requirements draft", "Ana", dt.date(2026, 12, 8), dt.date(2026, 12, 11), "Open", "Requirements review"),
        ("Arrange training room", "Sam", dt.date(2026, 12, 8), dt.date(2026, 12, 18), "Open", "Requirements review"),
    ]
    for r in range(6, 26):
        a = acts[r - 6] if r - 6 < len(acts) else (None,) * 6
        put(ws, r, 2, a[0])
        put(ws, r, 3, a[1])
        put(ws, r, 4, a[2], DATE)
        put(ws, r, 5, a[3], DATE)
        put(ws, r, 6, a[4])
        put(ws, r, 7, f'=IF(OR(B{r}="",E{r}="",F{r}="Done"),"",MAX(0,$C$28-E{r}))', "0", "calc")
        put(ws, r, 8, a[5])
    validate(ws, "F6:F25", '"Open,In progress,Blocked,Done"')
    label_value(ws, 28, "Report date", REPORT, DATE)
    label_value(ws, 30, "Open actions", '=COUNTIFS(B6:B25,"<>",F6:F25,"<>Done")', "0", "summary")
    label_value(ws, 31, "Overdue", '=COUNTIF(G6:G25,">0")', "0", "summary")
    label_value(ws, 32, "Completed", '=COUNTIF(F6:F25,"Done")', "0", "summary")
    label_value(ws, 33, "Completion rate", '=IFERROR(COUNTIF(F6:F25,"Done")/COUNTA(B6:B25),0)', "0%", "summary")
    wb.save(path)


def resource_allocation(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Allocation"
    setup_sheet(ws, "Resource Allocation Planner", "Enter hours per week for each project. Total, utilisation and flags calculate for each person", 9,
                [22, 16, 13, 12, 12, 12, 13, 13, 16])
    header_row(ws, 5, 2, ["Team member", "Role", "Capacity (h/week)", "Project A", "Project B", "Project C",
                          "Total allocated", "Utilisation", "Flag"])
    team = [("Maya", "Project lead", 37.5, 10, 8, 6), ("Leo", "Developer", 37.5, 20, 10, 0),
            ("Sam", "Analyst", 37.5, 12, 12, 4), ("Ana", "Designer", 30, 8, 6, 8),
            ("Ben", "Developer", 37.5, 25, 12, 5), ("Chloe", "Tester", 37.5, 4, 6, 3),
            ("Dev", "Developer", 30, 15, 16, 2), ("Priya", "Trainer", 20, 0, 4, 0)]
    for r in range(6, 16):
        t = team[r - 6] if r - 6 < len(team) else (None,) * 6
        put(ws, r, 2, t[0])
        put(ws, r, 3, t[1])
        put(ws, r, 4, t[2], "0.0")
        put(ws, r, 5, t[3], "0.0")
        put(ws, r, 6, t[4], "0.0")
        put(ws, r, 7, t[5], "0.0")
        put(ws, r, 8, f'=IF(B{r}="","",SUM(E{r}:G{r}))', "0.0", "calc")
        put(ws, r, 9, f'=IF(OR(B{r}="",N(D{r})=0),"",H{r}/D{r})', "0%", "calc")
        put(ws, r, 10, f'=IF(I{r}="","",IF(I{r}>1,"Over-allocated",IF(I{r}<0.6,"Under-used","OK")))', None, "calc")
    put(ws, 16, 2, "Total", kind="total")
    put(ws, 16, 3, "", kind="total")
    for col, letter in zip(range(4, 9), "DEFGH"):
        put(ws, 16, col, f"=SUM({letter}6:{letter}15)", "0.0", "total")
    put(ws, 16, 9, '=IFERROR(H16/D16,0)', "0%", "total")
    put(ws, 16, 10, "", kind="total")
    label_value(ws, 19, "Over-allocated people", '=COUNTIF(J6:J15,"Over-allocated")', "0", "summary")
    label_value(ws, 20, "Under-used people", '=COUNTIF(J6:J15,"Under-used")', "0", "summary")
    label_value(ws, 21, "Average utilisation", '=IFERROR(AVERAGE(I6:I15),0)', "0%", "summary")
    note(ws, 23, "Utilisation = total allocated / capacity. Over 100% is Over-allocated; under 60% is Under-used.")
    wb.save(path)


def time_tracking(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Time log"
    setup_sheet(ws, "Time Tracking by Project", "Log hours against each project. Billable hours and the project summary calculate automatically", 7,
                [14, 14, 14, 30, 10, 12, 14])
    header_row(ws, 5, 2, ["Date", "Person", "Project", "Task", "Hours", "Billable?", "Billable hours"])
    entries = [(dt.date(2026, 11, 23), "Leo", "Project A", "Build login API", 6.5, "Yes"),
               (dt.date(2026, 11, 23), "Sam", "Project B", "Requirements interviews", 4, "Yes"),
               (dt.date(2026, 11, 24), "Ana", "Project A", "Wireframes", 5, "Yes"),
               (dt.date(2026, 11, 24), "Maya", "Admin", "Weekly admin and reports", 2, "No"),
               (dt.date(2026, 11, 25), "Ben", "Project C", "Data migration script", 7, "Yes"),
               (dt.date(2026, 11, 25), "Leo", "Project A", "Code review", 1.5, "Yes"),
               (dt.date(2026, 11, 26), "Sam", "Project B", "Test plan", 3, "Yes"),
               (dt.date(2026, 11, 26), "Chloe", "Project C", "Test data prep", 4, "No"),
               (dt.date(2026, 11, 27), "Ana", "Project A", "Usability notes", 3.5, "Yes"),
               (dt.date(2026, 11, 27), "Maya", "Project B", "Steering meeting", 1.5, "Yes")]
    for r in range(6, 36):
        e = entries[r - 6] if r - 6 < len(entries) else (None,) * 6
        put(ws, r, 2, e[0], DATE)
        put(ws, r, 3, e[1])
        put(ws, r, 4, e[2])
        put(ws, r, 5, e[3])
        put(ws, r, 6, e[4], "0.0")
        put(ws, r, 7, e[5])
        put(ws, r, 8, f'=IF(F{r}="","",IF(G{r}="Yes",F{r},0))', "0.0", "calc")
    validate(ws, "D6:D35", '"Project A,Project B,Project C,Admin"')
    validate(ws, "G6:G35", '"Yes,No"')
    header_row(ws, 38, 2, ["Project", "Total hours", "Billable hours", "Billable %"])
    for i, name in enumerate(["Project A", "Project B", "Project C", "Admin"]):
        r = 39 + i
        put(ws, r, 2, name, kind="label", bold=True)
        put(ws, r, 3, f'=SUMIF($D$6:$D$35,B{r},$F$6:$F$35)', "0.0", "calc")
        put(ws, r, 4, f'=SUMIF($D$6:$D$35,B{r},$H$6:$H$35)', "0.0", "calc")
        put(ws, r, 5, f'=IFERROR(D{r}/C{r},0)', "0%", "calc")
    put(ws, 43, 2, "Total", kind="total")
    put(ws, 43, 3, "=SUM(C39:C42)", "0.0", "total")
    put(ws, 43, 4, "=SUM(D39:D42)", "0.0", "total")
    put(ws, 43, 5, "=IFERROR(D43/C43,0)", "0%", "total")
    wb.save(path)


def project_dashboard(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Dashboard"
    setup_sheet(ws, "Project Status Dashboard", "Enter budget spent and planned and actual progress. Health rating and the chart update automatically", 8,
                [24, 14, 14, 14, 14, 14, 14, 12])
    header_row(ws, 5, 2, ["Project", "Owner", "Budget", "Spent to date", "Planned % complete", "Actual % complete",
                          "% budget used", "Health"])
    projects = [("Website redesign", "Ana", 20000, 13000, 0.70, 0.65),
                ("Library system", "Ben", 45000, 33000, 0.50, 0.40),
                ("Staff app", "Chloe", 15000, 6000, 0.30, 0.30),
                ("Network upgrade", "Dev", 30000, 12000, 0.40, 0.45)]
    for r in range(6, 12):
        p = projects[r - 6] if r - 6 < len(projects) else (None,) * 6
        put(ws, r, 2, p[0])
        put(ws, r, 3, p[1])
        put(ws, r, 4, p[2], MONEY)
        put(ws, r, 5, p[3], MONEY)
        put(ws, r, 6, p[4], "0%")
        put(ws, r, 7, p[5], "0%")
        put(ws, r, 8, f'=IF(OR(B{r}="",N(D{r})=0),"",E{r}/D{r})', "0%", "calc")
        put(ws, r, 9, f'=IF(OR(B{r}="",F{r}="",G{r}=""),"",IF(OR(G{r}<F{r}-0.15,N(H{r})>G{r}+0.15),"Red",'
                      f'IF(OR(G{r}<F{r}-0.05,N(H{r})>G{r}+0.05),"Amber","Green")))', None, "calc")
    label_value(ws, 14, "Green", '=COUNTIF(I6:I11,"Green")', "0", "summary")
    label_value(ws, 15, "Amber", '=COUNTIF(I6:I11,"Amber")', "0", "summary")
    label_value(ws, 16, "Red", '=COUNTIF(I6:I11,"Red")', "0", "summary")
    note(ws, 17, "Red: progress more than 15 points behind plan, or budget used more than 15 points ahead of progress. Amber: 5 to 15 points.")
    chart = BarChart()
    chart.type = "col"
    chart.title = "Planned vs actual progress"
    chart.y_axis.title = "% complete"
    chart.y_axis.number_format = "0%"
    chart.y_axis.scaling.min = 0
    chart.y_axis.scaling.max = 1
    chart.add_data(Reference(ws, min_col=6, max_col=7, min_row=5, max_row=11), titles_from_data=True)
    chart.set_categories(Reference(ws, min_col=2, min_row=6, max_row=11))
    chart.x_axis.delete = False
    chart.y_axis.delete = False
    chart.height, chart.width = 8, 18
    ws.add_chart(chart, "B19")
    wb.save(path)


def weekly_status(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Status"
    setup_sheet(ws, "Weekly Team Status Report", "One row per team member. Choose a RAG status and rate confidence from 1 (low) to 5 (high)", 6,
                [22, 12, 34, 34, 30, 14])
    header_row(ws, 5, 2, ["Team member", "RAG status", "Done last week", "Planned this week", "Blockers", "Confidence (1-5)"])
    rows = [("Maya", "Green", "Signed off the project plan", "Budget review with finance", "None", 5),
            ("Leo", "Amber", "Built login API (80%)", "Finish API and write tests", "Supplier delivery unconfirmed", 3),
            ("Sam", "Green", "Ran two requirement interviews", "Draft requirements document", "None", 4),
            ("Ana", "Red", "Wireframes for three screens", "Usability test prep", "Waiting for client feedback", 2),
            ("Ben", "Amber", "Data migration script in progress", "Test on sample data", "Test server not ready", 3)]
    for r in range(6, 16):
        s = rows[r - 6] if r - 6 < len(rows) else (None,) * 6
        for j, v in enumerate(s):
            put(ws, r, 2 + j, v, "0" if j == 5 else None)
    validate(ws, "C6:C15", '"Green,Amber,Red"')
    validate(ws, "G6:G15", "1", kind="whole", operator="between", formula2="5")
    label_value(ws, 18, "Week commencing", dt.date(2026, 11, 30), DATE)
    label_value(ws, 20, "Green", '=COUNTIF(C6:C15,"Green")', "0", "summary")
    label_value(ws, 21, "Amber", '=COUNTIF(C6:C15,"Amber")', "0", "summary")
    label_value(ws, 22, "Red", '=COUNTIF(C6:C15,"Red")', "0", "summary")
    label_value(ws, 23, "Average confidence", '=IFERROR(AVERAGE(G6:G15),0)', "0.0", "summary")
    wb.save(path)


def decision_log(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Decisions"
    setup_sheet(ws, "Decision Log", "Record each decision, what was considered, and when to review it. Review flags calculate from the report date", 8,
                [34, 12, 14, 28, 26, 12, 12, 14])
    header_row(ws, 5, 2, ["Decision", "Date", "Decided by", "Options considered", "Impact", "Status", "Review date", "Review flag"])
    decs = [("Use a shared drive for all project files", dt.date(2026, 11, 24), "Project board",
             "Shared drive; email attachments; wiki", "Single place for versions", "Active", dt.date(2027, 1, 15)),
            ("Delay pilot by two weeks", dt.date(2026, 12, 1), "Sponsor",
             "Keep date; cut scope; delay", "Pilot moves to 2 Feb", "Active", dt.date(2026, 12, 15)),
            ("Buy licences instead of building a tool", dt.date(2026, 11, 20), "Finance",
             "Build; buy; hybrid", "Saves about 60 developer days", "Superseded", None)]
    for r in range(6, 20):
        d = decs[r - 6] if r - 6 < len(decs) else (None,) * 7
        put(ws, r, 2, d[0])
        put(ws, r, 3, d[1], DATE)
        put(ws, r, 4, d[2])
        put(ws, r, 5, d[3])
        put(ws, r, 6, d[4])
        put(ws, r, 7, d[5])
        put(ws, r, 8, d[6], DATE)
        put(ws, r, 9, f'=IF(OR(B{r}="",H{r}="",G{r}<>"Active"),"",IF(H{r}<=$C$22,"Review due","Not yet"))', None, "calc")
    validate(ws, "G6:G19", '"Active,Superseded,Reversed"')
    label_value(ws, 22, "Report date", REPORT, DATE)
    label_value(ws, 24, "Decisions logged", '=COUNTA(B6:B19)', "0", "summary")
    label_value(ws, 25, "Active decisions", '=COUNTIF(G6:G19,"Active")', "0", "summary")
    label_value(ws, 26, "Reviews due", '=COUNTIF(I6:I19,"Review due")', "0", "summary")
    wb.save(path)


def stakeholder_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stakeholders"
    setup_sheet(ws, "Stakeholder Register", "Rate each stakeholder's interest and influence, then set where you want their support to be. The approach and gap calculate automatically", 8,
                [24, 18, 11, 11, 15, 15, 17, 14])
    header_row(ws, 5, 2, ["Stakeholder", "Role", "Interest", "Influence", "Current stance", "Desired stance", "Approach", "Gap"])
    people = [("Head teacher", "Sponsor", "High", "High", "Supportive", "Supportive"),
              ("Finance officer", "Budget holder", "Low", "High", "Neutral", "Supportive"),
              ("IT technicians", "Delivery team", "High", "Low", "Neutral", "Supportive"),
              ("Parents", "End users", "Low", "Low", "Unaware", "Neutral"),
              ("Department heads", "Users", "High", "Low", "Resistant", "Neutral")]
    for r in range(6, 20):
        p = people[r - 6] if r - 6 < len(people) else (None,) * 6
        for j, v in enumerate(p):
            put(ws, r, 2 + j, v)
        put(ws, r, 8, f'=IF(B{r}="","",IF(AND(D{r}="High",E{r}="High"),"Manage closely",IF(E{r}="High","Keep satisfied",'
                      f'IF(D{r}="High","Keep informed","Monitor"))))', None, "calc")
        put(ws, r, 9, f'=IF(OR(B{r}="",F{r}="",G{r}=""),"",IF(MATCH(F{r},{{"Resistant","Unaware","Neutral","Supportive"}},0)'
                      f'<MATCH(G{r},{{"Resistant","Unaware","Neutral","Supportive"}},0),"Move forward","On target"))', None, "calc")
    validate(ws, "D6:E19", '"High,Low"')
    validate(ws, "F6:G19", '"Resistant,Unaware,Neutral,Supportive"')
    label_value(ws, 22, "Manage closely", '=COUNTIF(H6:H19,"Manage closely")', "0", "summary")
    label_value(ws, 23, "Keep satisfied", '=COUNTIF(H6:H19,"Keep satisfied")', "0", "summary")
    label_value(ws, 24, "Keep informed", '=COUNTIF(H6:H19,"Keep informed")', "0", "summary")
    label_value(ws, 25, "Monitor", '=COUNTIF(H6:H19,"Monitor")', "0", "summary")
    label_value(ws, 26, "Need engagement (gap)", '=COUNTIF(I6:I19,"Move forward")', "0", "summary")
    wb.save(path)


def change_control(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Changes"
    setup_sheet(ws, "Change Control Log", "Log each change request with its effort and schedule impact. Approved impact adds up as you go", 9,
                [36, 13, 14, 14, 14, 13, 13, 16, 16])
    header_row(ws, 5, 2, ["Change request", "Date raised", "Requested by", "Effort (hours)", "Schedule impact (days)",
                          "Decision", "Decision date", "Approved schedule days", "Running total (days)"])
    chg = [("Add export to PDF", dt.date(2026, 11, 26), "Sponsor", 12, 2, "Approved", dt.date(2026, 11, 28)),
           ("Change login provider", dt.date(2026, 12, 2), "IT", 30, 6, "Pending", None),
           ("Add dark mode", dt.date(2026, 12, 3), "Users", 8, 1, "Rejected", dt.date(2026, 12, 5))]
    for r in range(6, 20):
        c = chg[r - 6] if r - 6 < len(chg) else (None,) * 7
        put(ws, r, 2, c[0])
        put(ws, r, 3, c[1], DATE)
        put(ws, r, 4, c[2])
        put(ws, r, 5, c[3], "0.0")
        put(ws, r, 6, c[4], "0.0")
        put(ws, r, 7, c[5])
        put(ws, r, 8, c[6], DATE)
        put(ws, r, 9, f'=IF(B{r}="","",IF(G{r}="Approved",N(F{r}),0))', "0.0", "calc")
        put(ws, r, 10, f'=IF(B{r}="","",SUM($I$6:I{r}))', "0.0", "calc")
    validate(ws, "G6:G19", '"Pending,Approved,Rejected"')
    label_value(ws, 22, "Changes logged", '=COUNTA(B6:B19)', "0", "summary")
    label_value(ws, 23, "Pending decision", '=COUNTIF(G6:G19,"Pending")', "0", "summary")
    label_value(ws, 24, "Approved changes", '=COUNTIF(G6:G19,"Approved")', "0", "summary")
    label_value(ws, 25, "Approved effort (hours)", '=SUMIF(G6:G19,"Approved",E6:E19)', "0.0", "summary")
    label_value(ws, 26, "Approved schedule impact (days)", '=SUM(I6:I19)', "0.0", "summary")
    wb.save(path)
