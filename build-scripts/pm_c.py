"""Project & Task Management templates 17-25: WBS, capacity, vendor scorecard, lessons, OKRs, goals, event run, versions, onboarding."""
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

REPORT = dt.date(2026, 12, 1)
START = dt.date(2026, 12, 7)


def work_breakdown(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "WBS"
    setup_sheet(ws, "Work Breakdown Structure", "Break the project into phases and work packages. Level calculates from the code, and estimates total the work packages", 6,
                [14, 36, 14, 14, 13, 9])
    header_row(ws, 5, 2, ["WBS code", "Deliverable or work package", "Type", "Owner", "Estimate (hours)", "Level"])
    items = [("1", "Initiation", "Phase", "", None), ("1.1", "Project charter", "Work package", "Maya", 8),
             ("1.2", "Stakeholder analysis", "Work package", "Sam", 6), ("2", "Delivery", "Phase", "", None),
             ("2.1", "Design", "Work package", "Ana", 40), ("2.2", "Build", "Work package", "Leo", 80),
             ("2.3", "Testing", "Work package", "Ben", 30), ("3", "Closure", "Phase", "", None),
             ("3.1", "Handover and training", "Work package", "Sam", 10), ("3.2", "Lessons learned report", "Work package", "Maya", 4)]
    for r in range(6, 26):
        it = items[r - 6] if r - 6 < len(items) else (None,) * 5
        put(ws, r, 2, it[0])
        put(ws, r, 3, it[1])
        put(ws, r, 4, it[2])
        put(ws, r, 5, it[3] or None)
        put(ws, r, 6, it[4], "0.0")
        put(ws, r, 7, f'=IF(B{r}="","",LEN(B{r})-LEN(SUBSTITUTE(B{r},".",""))+1)', "0", "calc")
    validate(ws, "D6:D25", '"Phase,Work package"')
    label_value(ws, 28, "Total estimate (work packages)", '=SUMIF(D6:D25,"Work package",F6:F25)', "0.0", "summary")
    label_value(ws, 29, "Phases", '=COUNTIF(D6:D25,"Phase")', "0", "summary")
    label_value(ws, 30, "Work packages", '=COUNTIF(D6:D25,"Work package")', "0", "summary")
    label_value(ws, 31, "Work packages without estimate", '=COUNTIFS(D6:D25,"Work package",F6:F25,"")', "0", "summary")
    wb.save(path)


def capacity_planning(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Capacity"
    setup_sheet(ws, "Capacity Planning Sheet", "Enter headcount, hours and demand for each role over four weeks. Capacity and gaps calculate automatically", 11,
                [22, 11, 14, 14, 12, 12, 12, 12, 13, 13, 12])
    header_row(ws, 5, 2, ["Role", "Headcount", "Hours per person per week", "Weekly capacity (h)", "Demand week 1 (h)",
                          "Demand week 2 (h)", "Demand week 3 (h)", "Demand week 4 (h)", "Peak demand (h)", "Gap at peak (h)", "Status"])
    roles = [("Project lead", 1, 37.5, [30, 30, 30, 30]), ("Developer", 4, 30, [100, 120, 130, 110]),
             ("Analyst", 2, 35, [50, 60, 55, 40]), ("Tester", 1, 30, [10, 20, 35, 25]),
             ("Designer", 1, 28, [20, 25, 15, 10]), ("Trainer", 1, 20, [5, 5, 10, 15])]
    for r in range(6, 13):
        ro = roles[r - 6] if r - 6 < len(roles) else (None, None, None, [None] * 4)
        put(ws, r, 2, ro[0])
        put(ws, r, 3, ro[1], "0")
        put(ws, r, 4, ro[2], "0.0")
        put(ws, r, 5, f'=IF(B{r}="","",C{r}*D{r})', "0.0", "calc")
        for j, v in enumerate(ro[3]):
            put(ws, r, 6 + j, v, "0.0")
        put(ws, r, 10, f'=IF(B{r}="","",MAX(F{r}:I{r}))', "0.0", "calc")
        put(ws, r, 11, f'=IF(B{r}="","",E{r}-J{r})', "0.0;[Red]-0.0", "calc")
        put(ws, r, 12, f'=IF(B{r}="","",IF(K{r}<0,"Short","OK"))', None, "calc")
    put(ws, 13, 2, "Total", kind="total")
    put(ws, 13, 3, "=SUM(C6:C12)", "0", "total")
    put(ws, 13, 4, "", kind="total")
    for col, letter in zip(range(5, 10), "EFGHI"):
        put(ws, 13, col, f"=SUM({letter}6:{letter}12)", "0.0", "total")
    put(ws, 13, 10, "", kind="total")
    put(ws, 13, 11, "=SUM(K6:K12)", "0.0;[Red]-0.0", "total")
    put(ws, 13, 12, "", kind="total")
    label_value(ws, 16, "Roles short at peak", '=COUNTIF(L6:L12,"Short")', "0", "summary")
    label_value(ws, 17, "Total headcount", '=C13', "0", "summary")
    note(ws, 19, "Gap = weekly capacity minus the highest weekly demand. A negative gap means the role is short at its peak.")
    wb.save(path)


def vendor_scorecard(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Scorecard"
    setup_sheet(ws, "Vendor Evaluation Scorecard", "Set the weights, then score each vendor from 1 (poor) to 5 (excellent). Weighted scores and ranks calculate automatically", 7,
                [30, 12, 14, 14, 14, 14])
    header_row(ws, 5, 2, ["Criterion", "Weight", "Vendor A", "Vendor B", "Vendor C", "Vendor D"])
    crit = [("Price", 0.25, [4, 3, 5, 2]), ("Support", 0.15, [4, 5, 3, 3]), ("Features", 0.15, [5, 4, 3, 4]),
            ("Security", 0.15, [3, 4, 4, 5]), ("Ease of use", 0.10, [4, 4, 3, 2]), ("Reliability", 0.10, [5, 3, 4, 4]),
            ("Integration with current systems", 0.10, [3, 5, 4, 3])]
    for r in range(6, 13):
        c = crit[r - 6]
        put(ws, r, 2, c[0])
        put(ws, r, 3, c[1], "0%")
        for j, v in enumerate(c[2]):
            put(ws, r, 4 + j, v, "0")
    validate(ws, "D6:G12", "1", kind="whole", operator="between", formula2="5")
    put(ws, 13, 2, "Total weight", kind="total")
    put(ws, 13, 3, "=SUM(C6:C12)", "0%", "total")
    for col in range(4, 8):
        put(ws, 13, col, "", kind="total")
    put(ws, 14, 2, "Weighted score (out of 5)", kind="summary")
    put(ws, 14, 3, "", kind="summary")
    for col in range(4, 8):
        L_ = L(col)
        put(ws, 14, col, f"=IFERROR(SUMPRODUCT($C$6:$C$12,{L_}6:{L_}12)/SUM($C$6:$C$12),0)", "0.00", "summary")
    put(ws, 15, 2, "Rank (1 = best)", kind="label", bold=True)
    for col in range(4, 8):
        L_ = L(col)
        put(ws, 15, col, f"=RANK({L_}14,$D$14:$G$14)", "0", "calc")
    label_value(ws, 17, "Highest scoring vendor", '=INDEX($D$5:$G$5,MATCH(MAX($D$14:$G$14),$D$14:$G$14,0))', None, "summary")
    label_value(ws, 18, "Weights check", '=IF(ROUND(C13,4)=1,"Weights total 100%","Weights should total 100%")', None, "summary")
    wb.save(path)


def lessons_learned(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lessons"
    setup_sheet(ws, "Lessons Learned Log", "Record what happened, the lesson, and the action to take next time. Totals by category calculate below the log", 9,
                [12, 14, 15, 34, 12, 34, 30, 14, 12])
    header_row(ws, 5, 2, ["Date", "Project phase", "Category", "What happened", "Impact", "Lesson learned",
                          "Recommended action", "Owner", "Status"])
    les = [(dt.date(2026, 11, 27), "Initiation", "Process", "Scope changed twice before sign-off", "Negative",
            "Agree scope in writing before planning starts", "Add a scope sign-off step to the template", "Maya", "Open"),
           (dt.date(2026, 12, 2), "Delivery", "Supplier", "Hardware delivery slipped by a week", "Negative",
            "Confirm delivery dates with suppliers weekly", "Add supplier check to the stand-up", "Leo", "Open"),
           (dt.date(2026, 12, 4), "Delivery", "Communication", "Weekly update reached stakeholders on time", "Positive",
            "A fixed reporting day builds trust", "Keep the Friday update", "Sam", "Applied"),
           (dt.date(2026, 12, 8), "Delivery", "Technical", "Test server set up late", "Negative",
            "Build the test environment before coding starts", "Add environment setup to the plan", "Ben", "Open")]
    for r in range(6, 26):
        x = les[r - 6] if r - 6 < len(les) else (None,) * 9
        put(ws, r, 2, x[0], DATE)
        put(ws, r, 3, x[1])
        put(ws, r, 4, x[2])
        put(ws, r, 5, x[3])
        put(ws, r, 6, x[4])
        put(ws, r, 7, x[5])
        put(ws, r, 8, x[6])
        put(ws, r, 9, x[7])
        put(ws, r, 10, x[8])
    validate(ws, "D6:D25", '"Process,Technical,People,Supplier,Communication"')
    validate(ws, "F6:F25", '"Positive,Negative"')
    validate(ws, "J6:J25", '"Open,Applied"')
    label_value(ws, 28, "Lessons logged", '=COUNTA(E6:E25)', "0", "summary")
    label_value(ws, 29, "Negative impacts", '=COUNTIF(F6:F25,"Negative")', "0", "summary")
    label_value(ws, 30, "Actions still open", '=COUNTIF(J6:J25,"Open")', "0", "summary")
    for i, cat in enumerate(["Process", "Technical", "People", "Supplier", "Communication"]):
        label_value(ws, 31 + i, f"Logged as {cat.lower()}", f'=COUNTIF(D6:D25,"{cat}")', "0", "summary")
    wb.save(path)


def okr_tracker(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "OKRs"
    setup_sheet(ws, "OKR Tracker", "Enter each key result's start, target and current value. Progress and status calculate automatically", 8,
                [30, 34, 11, 11, 11, 11, 13, 14])
    header_row(ws, 5, 2, ["Objective", "Key result", "Start value", "Target", "Current", "Progress", "Confidence (1-10)", "Status"])
    krs = [("Improve help desk response", "Average first response (hours) down to target", 6, 2, 3.5, 7),
           ("Improve help desk response", "Tickets resolved within 48 hours (%)", 60, 90, 78, 6),
           ("Train all staff on the new system", "Staff trained (number)", 0, 40, 40, 9),
           ("Launch the pilot", "Pilot sites live (number)", 0, 3, 1, 5),
           ("Launch the pilot", "Pilot satisfaction score (out of 5)", 0, 4.5, 0, 3),
           ("Reduce costs", "Licence spend cut (%)", 0, 15, 6, 7)]
    for r in range(6, 18):
        k = krs[r - 6] if r - 6 < len(krs) else (None,) * 6
        put(ws, r, 2, k[0])
        put(ws, r, 3, k[1])
        put(ws, r, 4, k[2], "0.0")
        put(ws, r, 5, k[3], "0.0")
        put(ws, r, 6, k[4], "0.0")
        put(ws, r, 7, f'=IF(OR(C{r}="",D{r}="",E{r}=""),"",IF(E{r}=D{r},"",MIN(1,MAX(0,(N(F{r})-D{r})/(E{r}-D{r})))))', "0%", "calc")
        put(ws, r, 8, k[5], "0")
        put(ws, r, 9, f'=IF(C{r}="","",IF(N(G{r})>=1,"Achieved",IF(N(H{r})<=4,"At risk","On track")))', None, "calc")
    validate(ws, "H6:H17", "1", kind="whole", operator="between", formula2="10")
    label_value(ws, 20, "Key results", '=COUNTA(C6:C17)', "0", "summary")
    label_value(ws, 21, "Average progress", '=IFERROR(AVERAGE(G6:G17),0)', "0%", "summary")
    label_value(ws, 22, "Achieved", '=COUNTIF(I6:I17,"Achieved")', "0", "summary")
    label_value(ws, 23, "At risk", '=COUNTIF(I6:I17,"At risk")', "0", "summary")
    note(ws, 25, "Progress = (current - start) / (target - start), capped between 0% and 100%. Confidence 4 or lower is At risk.")
    wb.save(path)


def personal_goals(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Goals"
    setup_sheet(ws, "Personal Goal Tracker", "Break each goal into milestones and record how many are done. Progress and days left calculate automatically", 8,
                [32, 13, 12, 12, 12, 12, 12, 18])
    header_row(ws, 5, 2, ["Goal", "Area", "Target date", "Milestones planned", "Milestones done", "% complete", "Days left", "Status"])
    goals = [("Complete a Python course", "Learning", dt.date(2027, 3, 31), 10, 6),
             ("Run 5 km without stopping", "Health", dt.date(2027, 2, 28), 8, 3),
             ("Build an emergency savings fund", "Finance", dt.date(2027, 6, 30), 12, 4),
             ("Publish first template pack", "Career", dt.date(2026, 12, 20), 5, 5),
             ("Plan a family holiday", "Family", dt.date(2026, 11, 30), 4, 2),
             ("Read 12 books", "Learning", dt.date(2027, 12, 31), 12, 1)]
    for r in range(6, 18):
        g = goals[r - 6] if r - 6 < len(goals) else (None,) * 5
        put(ws, r, 2, g[0])
        put(ws, r, 3, g[1])
        put(ws, r, 4, g[2], DATE)
        put(ws, r, 5, g[3], "0")
        put(ws, r, 6, g[4], "0")
        put(ws, r, 7, f'=IF(OR(B{r}="",N(E{r})=0),"",MIN(1,N(F{r})/E{r}))', "0%", "calc")
        put(ws, r, 8, f'=IF(OR(B{r}="",D{r}=""),"",D{r}-$C$20)', "0", "calc")
        put(ws, r, 9, f'=IF(B{r}="","",IF(G{r}="","No milestones",IF(G{r}>=1,"Complete",IF(H{r}="","No date",'
                      f'IF(H{r}<0,"Overdue",IF(AND(H{r}<=30,G{r}<0.5),"Needs attention","On track"))))))', None, "calc")
    validate(ws, "C6:C17", '"Career,Health,Learning,Finance,Family,Other"')
    label_value(ws, 20, "Report date", REPORT, DATE)
    label_value(ws, 22, "Goals", '=COUNTA(B6:B17)', "0", "summary")
    label_value(ws, 23, "Complete", '=COUNTIF(I6:I17,"Complete")', "0", "summary")
    label_value(ws, 24, "Needs attention", '=COUNTIF(I6:I17,"Needs attention")', "0", "summary")
    label_value(ws, 25, "Overdue", '=COUNTIF(I6:I17,"Overdue")', "0", "summary")
    wb.save(path)


def event_run_sheet(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Run sheet"
    setup_sheet(ws, "Event Run Sheet", "Plan each item with its start time and length. Finish times and the event timings calculate automatically", 7,
                [10, 12, 10, 32, 14, 16, 28])
    header_row(ws, 5, 2, ["Start time", "Duration (min)", "Finish", "Item", "Owner", "Location", "Equipment and notes"])
    items = [(dt.time(17, 0), 15, "Welcome and registration", "Ana", "Hall", "Name badges, sign-in sheet"),
             (dt.time(17, 15), 20, "Opening remarks", "Maya", "Stage", "Microphone"),
             (dt.time(17, 35), 30, "Student showcase", "Ben", "Stage", "Two laptops, projector"),
             (dt.time(18, 5), 20, "Break and refreshments", "Sam", "Foyer", "Urn, cups"),
             (dt.time(18, 25), 25, "Prize giving", "Leo", "Stage", ""),
             (dt.time(18, 50), 10, "Closing thanks", "Maya", "Stage", "")]
    for r in range(6, 26):
        it = items[r - 6] if r - 6 < len(items) else (None,) * 6
        put(ws, r, 2, it[0], "hh:mm")
        put(ws, r, 3, it[1], "0")
        put(ws, r, 4, f'=IF(OR(B{r}="",C{r}=""),"",B{r}+C{r}/1440)', "hh:mm", "calc")
        put(ws, r, 5, it[2])
        put(ws, r, 6, it[3])
        put(ws, r, 7, it[4])
        put(ws, r, 8, it[5])
    label_value(ws, 28, "Items", '=COUNTA(E6:E25)', "0", "summary")
    label_value(ws, 29, "Total run time (hours)", '=SUM(C6:C25)/60', "0.0", "summary")
    label_value(ws, 30, "Event starts", '=IF(COUNT(B6:B25)=0,"",MIN(B6:B25))', "hh:mm", "summary")
    label_value(ws, 31, "Event finishes", '=IF(COUNT(D6:D25)=0,"",MAX(D6:D25))', "hh:mm", "summary")
    wb.save(path)


def document_versions(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Versions"
    setup_sheet(ws, "Document Version Register", "Track every version of each project document, who reviewed it, and what changed", 9,
                [30, 10, 14, 12, 13, 14, 14, 36, 24])
    header_row(ws, 5, 2, ["Document", "Version", "Author", "Date", "Status", "Reviewer", "Approved by", "Change summary", "Location"])
    docs = [("Project charter", "1.0", "Maya", dt.date(2026, 11, 24), "Approved", "Sponsor", "Sponsor", "First approved version", "Shared drive / Governance"),
            ("Project charter", "1.1", "Maya", dt.date(2026, 12, 3), "Approved", "Sponsor", "Sponsor", "Added budget ceiling", "Shared drive / Governance"),
            ("Requirements specification", "0.3", "Sam", dt.date(2026, 12, 8), "In review", "Ana", "", "Added reporting needs", "Shared drive / Requirements"),
            ("Test plan", "0.1", "Ben", dt.date(2026, 12, 9), "Draft", "", "", "First draft", "Shared drive / Testing")]
    for r in range(6, 26):
        d = docs[r - 6] if r - 6 < len(docs) else (None,) * 9
        put(ws, r, 2, d[0])
        put(ws, r, 3, d[1])
        put(ws, r, 4, d[2])
        put(ws, r, 5, d[3], DATE)
        put(ws, r, 6, d[4])
        put(ws, r, 7, d[5])
        put(ws, r, 8, d[6])
        put(ws, r, 9, d[7])
        put(ws, r, 10, d[8])
    validate(ws, "F6:F25", '"Draft,In review,Approved,Superseded"')
    label_value(ws, 28, "Documents listed", '=COUNTA(B6:B25)', "0", "summary")
    label_value(ws, 29, "Approved versions", '=COUNTIF(F6:F25,"Approved")', "0", "summary")
    label_value(ws, 30, "In review", '=COUNTIF(F6:F25,"In review")', "0", "summary")
    label_value(ws, 31, "Drafts", '=COUNTIF(F6:F25,"Draft")', "0", "summary")
    label_value(ws, 32, "Latest update", '=IF(COUNT(E6:E25)=0,"",MAX(E6:E25))', DATE, "summary")
    wb.save(path)


def onboarding_checklist(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist"
    setup_sheet(ws, "Onboarding Task Checklist", "Set the start date, then give each task a day offset. Due dates and completion calculate automatically", 7,
                [40, 14, 12, 12, 10, 14, 30])
    header_row(ws, 5, 2, ["Task", "Owner", "Days after start", "Due date", "Done?", "Date completed", "Notes"])
    tasks = [("Get laptop and login details", "IT", 0, "Yes", dt.date(2026, 12, 7)),
             ("Sign data protection policy", "HR", 0, "Yes", dt.date(2026, 12, 7)),
             ("Meet line manager", "Manager", 1, "Yes", dt.date(2026, 12, 8)),
             ("Set up email and calendar", "IT", 1, "No", None),
             ("Read the project charter", "New starter", 2, "No", None),
             ("Join team stand-up", "Team", 3, "No", None),
             ("Complete safeguarding training", "HR", 5, "No", None),
             ("Review the project plan", "New starter", 7, "No", None),
             ("First one-to-one review", "Manager", 10, "No", None),
             ("Shadow a team member", "Team", 14, "No", None)]
    for r in range(6, 26):
        t = tasks[r - 6] if r - 6 < len(tasks) else (None,) * 5
        put(ws, r, 2, t[0])
        put(ws, r, 3, t[1])
        put(ws, r, 4, t[2], "0")
        put(ws, r, 5, f'=IF(OR(B{r}="",D{r}=""),"",$C$28+D{r})', DATE, "calc")
        put(ws, r, 6, t[3])
        put(ws, r, 7, t[4], DATE)
        put(ws, r, 8, "")
    validate(ws, "F6:F25", '"Yes,No"')
    label_value(ws, 28, "Start date", START, DATE)
    label_value(ws, 30, "Tasks", '=COUNTA(B6:B25)', "0", "summary")
    label_value(ws, 31, "Completed", '=COUNTIF(F6:F25,"Yes")', "0", "summary")
    label_value(ws, 32, "Completion rate", '=IFERROR(COUNTIF(F6:F25,"Yes")/COUNTA(B6:B25),0)', "0%", "summary")
    label_value(ws, 33, "Due in the first 7 days", '=COUNTIFS(B6:B25,"<>",D6:D25,"<=7")', "0", "summary")
    wb.save(path)
