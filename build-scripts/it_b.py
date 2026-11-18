"""IT & Computing templates 9-17: bugs, test cases, code review, traffic, cloud cost, uptime, changes, data cleansing, data dictionary."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(505)
REPORT = dt.date(2026, 12, 1)


def bug_tracker(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bugs"
    setup_sheet(ws, "Bug Tracker", "Log each bug with its severity and status. Days open calculate from the report date below the table", 9,
                [10, 30, 11, 12, 14, 14, 12, 12, 11])
    header_row(ws, 5, 2, ["Bug ID", "Title", "Severity", "Status", "Reported by", "Assigned to",
                          "Date opened", "Date closed", "Days open"])
    titles = ["Login fails after timeout", "Quiz score not saved", "Chart labels overlap", "Export drops last row",
              "Typo on results page", "Slow search on large lists", "Button misaligned on phone", "Password reset email missing",
              "Score rounding error", "Page crashes on empty input", "Wrong date format in report", "Sort order reversed",
              "Image not loading", "Session expires too early"]
    sev = ["Critical", "High", "Medium", "Low"]
    for i, t in enumerate(titles):
        r = 6 + i
        opened = dt.date(2026, 11, 2) + dt.timedelta(days=i * 2)
        status = "Closed" if i < 8 else RNG.choice(["Open", "In progress", "Fixed"])
        closed = opened + dt.timedelta(days=RNG.randint(1, 9)) if status in ("Closed", "Fixed") else None
        put(ws, r, 2, f"B-{101 + i}")
        put(ws, r, 3, t)
        put(ws, r, 4, sev[i % 4])
        put(ws, r, 5, status)
        put(ws, r, 6, f"Tester {chr(65 + i % 3)}")
        put(ws, r, 7, f"Developer {chr(65 + i % 2)}")
        put(ws, r, 8, opened, DATE)
        put(ws, r, 9, closed, DATE)
        put(ws, r, 10, f'=IF(H{r}="","",IF(I{r}<>"",I{r}-H{r},$C$23-H{r}))', "0", "calc")
    validate(ws, "D6:D25", '"Critical,High,Medium,Low"')
    validate(ws, "E6:E25", '"Open,In progress,Fixed,Closed"')
    label_value(ws, 23, "Report date", REPORT, DATE, "input")
    label_value(ws, 25, "Not yet closed", '=COUNTIF(E6:E25,"Open")+COUNTIF(E6:E25,"In progress")+COUNTIF(E6:E25,"Fixed")', "0", "summary")
    label_value(ws, 26, "Critical bugs not closed", '=COUNTIFS(D6:D25,"Critical",E6:E25,"<>Closed")', "0", "summary")
    label_value(ws, 27, "Average days open", '=IFERROR(AVERAGE(J6:J25),"")', "0.0", "summary")
    wb.save(path)


def test_cases(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tests"
    setup_sheet(ws, "Test Case Log", "Record each test, its expected result and the actual result. Pass rate calculates automatically", 7,
                [10, 28, 24, 28, 12, 12, 13])
    header_row(ws, 5, 2, ["Test ID", "Requirement", "Precondition", "Expected result", "Result", "Tester", "Date tested"])
    rows = [("Login with valid details", "User account exists", "User reaches dashboard", "Pass"),
            ("Reject wrong password", "User account exists", "Error message shown", "Pass"),
            ("Quiz saves score", "Quiz completed", "Score stored in database", "Fail"),
            ("Teacher sees class list", "Teacher logged in", "Full class list shown", "Pass"),
            ("Export creates CSV", "Results available", "CSV file downloads", "Blocked"),
            ("Empty form is refused", "Form open", "Required-field message shown", "Pass"),
            ("Session timeout after 30 min", "User logged in", "User logged out", "Fail")]
    for i, (req, pre, exp, res) in enumerate(rows):
        r = 6 + i
        put(ws, r, 2, f"TC-{i + 1:03d}")
        put(ws, r, 3, req)
        put(ws, r, 4, pre)
        put(ws, r, 5, exp)
        put(ws, r, 6, res)
        put(ws, r, 7, f"Tester {chr(65 + i % 3)}")
        put(ws, r, 8, dt.date(2026, 11, 20) + dt.timedelta(days=i), DATE)
    for r in range(6 + len(rows), 26):
        for c in range(2, 9):
            put(ws, r, c, None, DATE if c == 8 else None)
    validate(ws, "F6:F25", '"Pass,Fail,Blocked"')
    label_value(ws, 27, "Tests recorded", '=COUNTA(B6:B25)', "0", "summary")
    label_value(ws, 28, "Passed", '=COUNTIF(F6:F25,"Pass")', "0", "summary")
    label_value(ws, 29, "Failed", '=COUNTIF(F6:F25,"Fail")', "0", "summary")
    label_value(ws, 30, "Blocked", '=COUNTIF(F6:F25,"Blocked")', "0", "summary")
    label_value(ws, 31, "Pass rate (of tests run)", '=IFERROR(C28/(C28+C29+C30),"")', "0%", "summary")
    wb.save(path)


def code_review(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Review"
    files = ["login.py", "quiz.py", "report.py", "utils.py"]
    setup_sheet(ws, "Code Review Checklist", "Mark each check Pass, Fail or N/A for each file. Pass rate calculates from the marks", 5,
                [46, 14, 14, 14, 14])
    header_row(ws, 5, 2, ["Check"] + files)
    checks = ["Names are meaningful", "Comments explain why, not what", "Each function does one job",
              "No hard-coded values that should be variables", "User input is validated", "Errors are handled",
              "Repeated code is moved into functions", "Indentation and style are consistent",
              "No unused variables or imports", "Tests cover normal and edge cases",
              "No passwords or keys in the code", "Code runs without errors"]
    for i, c in enumerate(checks):
        r = 6 + i
        put(ws, r, 2, c)
        for j in range(4):
            put(ws, r, 3 + j, RNG.choice(["Pass"] * 5 + ["Fail", "N/A"]))
    validate(ws, "C6:F17", '"Pass,Fail,N/A"')
    put(ws, 18, 2, "Pass rate (excluding N/A)", kind="total")
    for j in range(4):
        col = L(3 + j)
        put(ws, 18, 3 + j,
            f'=IFERROR(COUNTIF({col}6:{col}17,"Pass")/(COUNTIF({col}6:{col}17,"Pass")+COUNTIF({col}6:{col}17,"Fail")),"")',
            "0%", "total")
    wb.save(path)


def traffic_summary(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Traffic"
    setup_sheet(ws, "Website Traffic Summary", "Enter monthly figures from your web statistics. Ratios and changes calculate automatically", 5,
                [14, 14, 14, 16, 18])
    header_row(ws, 5, 2, ["Month", "Visits", "Page views", "Pages per visit", "Change in visits"])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    visits = [1200, 1350, 1500, 1420, 1600, 1380, 900, 850, 1700, 1820, 1950, 2100]
    for i, m in enumerate(months):
        r = 6 + i
        put(ws, r, 2, f"{m} 2026", kind="label")
        put(ws, r, 3, visits[i], "#,##0")
        put(ws, r, 4, int(visits[i] * RNG.uniform(2.1, 3.4)), "#,##0")
        put(ws, r, 5, f'=IFERROR(D{r}/C{r},"")', "0.00", "calc")
        put(ws, r, 6, "" if i == 0 else f'=IFERROR((C{r}-C{r - 1})/C{r - 1},"")', "+0%;-0%;0%", "calc")
    put(ws, 18, 2, "Total", kind="total")
    put(ws, 18, 3, "=SUM(C6:C17)", "#,##0", "total")
    put(ws, 18, 4, "=SUM(D6:D17)", "#,##0", "total")
    put(ws, 18, 5, '=IFERROR(D18/C18,"")', "0.00", "total")
    put(ws, 18, 6, "", kind="total")
    label_value(ws, 20, "Average visits per month", '=IFERROR(AVERAGE(C6:C17),"")', "#,##0", "summary")
    label_value(ws, 21, "Busiest month", '=INDEX(B6:B17,MATCH(MAX(C6:C17),C6:C17,0))', None, "summary")
    wb.save(path)


def cloud_cost(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Estimate"
    setup_sheet(ws, "Cloud Cost Estimator", "Enter the quantity, unit price and hours for each service. Monthly and yearly costs calculate automatically", 7,
                [24, 16, 10, 12, 12, 14, 14])
    header_row(ws, 5, 2, ["Service", "Unit", "Quantity", "Price per unit", "Hours per month", "Monthly cost", "Yearly cost"])
    services = [("Virtual machine", "Instance hour", 2, 0.05, 730), ("Database", "Instance hour", 1, 0.12, 730),
                ("Object storage", "GB per month", 200, 0.02, 1), ("Backup storage", "GB per month", 500, 0.01, 1),
                ("Bandwidth out", "GB transferred", 150, 0.01, 1), ("Load balancer", "Instance hour", 1, 0.03, 730)]
    for i, (name, unit, q, price, hrs) in enumerate(services):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, unit)
        put(ws, r, 4, q, "0")
        put(ws, r, 5, price, "0.000")
        put(ws, r, 6, hrs, "0")
        put(ws, r, 7, f"=D{r}*E{r}*F{r}", "#,##0.00", "calc")
        put(ws, r, 8, f"=G{r}*12", "#,##0.00", "calc")
    put(ws, 12, 2, "Total", kind="total")
    put(ws, 12, 3, "", kind="total")
    put(ws, 12, 4, "", kind="total")
    put(ws, 12, 5, "", kind="total")
    put(ws, 12, 6, "", kind="total")
    put(ws, 12, 7, "=SUM(G6:G11)", "#,##0.00", "total")
    put(ws, 12, 8, "=SUM(H6:H11)", "#,##0.00", "total")
    label_value(ws, 14, "Contingency (extra allowance)", 0.1, "0%", "input")
    label_value(ws, 15, "Yearly budget with contingency", "=H12*(1+C14)", "#,##0.00", "summary")
    wb.save(path)


def uptime_log(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Incidents"
    setup_sheet(ws, "Uptime and Incident Log", "Log each outage. Downtime and uptime for the month calculate automatically", 7,
                [12, 18, 16, 16, 14, 28, 12])
    header_row(ws, 5, 2, ["Incident ID", "Service", "Start", "End", "Downtime (min)", "Cause", "Planned?"])
    incidents = [("Web server", dt.datetime(2026, 11, 3, 14, 10), 25, "Disk full", "No"),
                 ("Database", dt.datetime(2026, 11, 9, 2, 0), 40, "Scheduled patch", "Yes"),
                 ("Web server", dt.datetime(2026, 11, 14, 9, 30), 12, "Memory leak", "No"),
                 ("Email", dt.datetime(2026, 11, 20, 16, 45), 60, "Provider outage", "No"),
                 ("Web server", dt.datetime(2026, 11, 26, 11, 0), 8, "Config error", "No")]
    for i, (svc, start, mins, cause, planned) in enumerate(incidents):
        r = 6 + i
        put(ws, r, 2, f"INC-{i + 1:03d}")
        put(ws, r, 3, svc)
        put(ws, r, 4, start, "dd/mm/yy hh:mm")
        put(ws, r, 5, start + dt.timedelta(minutes=mins), "dd/mm/yy hh:mm")
        put(ws, r, 6, f'=IF(OR(D{r}="",E{r}=""),"",ROUND((E{r}-D{r})*1440,0))', "0", "calc")
        put(ws, r, 7, cause)
        put(ws, r, 8, planned)
    for r in range(6 + len(incidents), 21):
        for c in range(2, 9):
            put(ws, r, c, None)
        put(ws, r, 6, f'=IF(OR(D{r}="",E{r}=""),"",ROUND((E{r}-D{r})*1440,0))', "0", "calc")
    validate(ws, "H6:H20", '"Yes,No"')
    label_value(ws, 23, "Days in month", 30, "0", "input")
    label_value(ws, 24, "Minutes in month", "=C23*1440", "#,##0", "summary")
    label_value(ws, 25, "Unplanned downtime (min)", '=SUMIF(H6:H20,"No",F6:F20)', "#,##0", "summary")
    label_value(ws, 26, "Uptime for the month", '=IFERROR(1-C25/C24,"")', "0.00%", "summary")
    label_value(ws, 27, "Incidents logged", '=COUNTA(B6:B20)', "0", "summary")
    wb.save(path)


def change_requests(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Changes"
    setup_sheet(ws, "Change Request Log", "Log each change, its impact and approval. Days to deliver and overdue items calculate automatically", 9,
                [10, 12, 14, 30, 10, 12, 12, 12, 12])
    header_row(ws, 5, 2, ["Change ID", "Date raised", "Requested by", "Description", "Impact", "Approval",
                          "Planned date", "Completed", "Days to deliver"])
    desc = ["Add new quiz topic", "Update password policy", "Upgrade lab PCs to Windows 11", "Change backup time to 2am",
            "Add student export button", "Retire old printer queue", "Install new projector firmware",
            "Enable two-factor login", "Move website to new host", "Add dark mode to portal"]
    for i, d in enumerate(desc):
        r = 6 + i
        raised = dt.date(2026, 11, 2) + dt.timedelta(days=3 * i)
        appr = "Approved" if i < 7 else RNG.choice(["Pending", "Rejected"])
        planned = raised + dt.timedelta(days=14)
        done = planned + dt.timedelta(days=RNG.randint(-3, 4)) if i < 5 and appr == "Approved" else None
        put(ws, r, 2, f"CR-{i + 1:03d}")
        put(ws, r, 3, raised, DATE)
        put(ws, r, 4, f"Teacher {chr(65 + i % 3)}")
        put(ws, r, 5, d)
        put(ws, r, 6, RNG.choice(["Low", "Medium", "High"]))
        put(ws, r, 7, appr)
        put(ws, r, 8, planned, DATE)
        put(ws, r, 9, done, DATE)
        put(ws, r, 10, f'=IF(OR(C{r}="",I{r}=""),"",I{r}-C{r})', "0", "calc")
    validate(ws, "F6:F25", '"Low,Medium,High"')
    validate(ws, "G6:G25", '"Pending,Approved,Rejected"')
    label_value(ws, 27, "Report date", REPORT, DATE, "input")
    label_value(ws, 28, "Approved", '=COUNTIF(G6:G25,"Approved")', "0", "summary")
    label_value(ws, 29, "Pending approval", '=COUNTIF(G6:G25,"Pending")', "0", "summary")
    label_value(ws, 30, "Approved, planned date passed, not completed",
                '=COUNTIFS(G6:G25,"Approved",H6:H25,"<"&C27,I6:I25,"")', "0", "summary")
    label_value(ws, 31, "Average days to deliver", '=IFERROR(AVERAGE(J6:J25),"")', "0.0", "summary")
    wb.save(path)


def data_cleansing(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist"
    setup_sheet(ws, "Data Cleansing Checklist", "Work through each step in order. Record how many rows each step changed", 4,
                [48, 12, 16, 30])
    header_row(ws, 5, 2, ["Step", "Done?", "Rows affected", "Notes"])
    steps = ["Back up the original file", "Remove duplicate rows", "Trim extra spaces from text", "Standardise capital letters in names",
             "Fix date formats", "Check numbers are stored as numbers", "Fill or flag blank required fields",
             "Check values are within allowed ranges", "Standardise category names", "Check codes match the lookup list",
             "Remove test or dummy records", "Save the cleaned file and record the date"]
    for i, s in enumerate(steps):
        r = 6 + i
        put(ws, r, 2, s)
        put(ws, r, 3, "Yes" if i < 7 else "No")
        put(ws, r, 4, RNG.randint(0, 40) if i < 7 else None, "0")
        put(ws, r, 5, "")
    validate(ws, "C6:C17", '"Yes,No"')
    label_value(ws, 19, "Steps complete", '=IFERROR(COUNTIF(C6:C17,"Yes")/COUNTA(B6:B17),0)', "0%", "summary")
    label_value(ws, 20, "Total rows changed", '=SUM(D6:D17)', "0", "summary")
    wb.save(path)


def data_dictionary(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Dictionary"
    setup_sheet(ws, "Data Dictionary Template", "Describe each field in each table. Completeness is checked automatically", 8,
                [18, 14, 12, 14, 10, 36, 16, 14])
    header_row(ws, 5, 2, ["Field name", "Table", "Data type", "Length or format", "Required?", "Description", "Example", "Complete?"])
    fields = [("student_id", "Students", "Text", "6 characters", "Yes", "Unique ID issued by the school", "S10023"),
              ("surname", "Students", "Text", "50 characters", "Yes", "Student's family name", "Example"),
              ("form_group", "Students", "Text", "4 characters", "Yes", "Tutor group code", "7A"),
              ("score", "Results", "Number", "0 to 100", "No", "Percentage score for the test", "78"),
              ("test_date", "Results", "Date", "dd/mm/yyyy", "Yes", "Date the test was taken", "01/12/2026")]
    for i, f in enumerate(fields):
        r = 6 + i
        for c, v in enumerate(f):
            put(ws, r, 2 + c, v, kind="input")
    for r in range(6, 26):
        put(ws, r, 9, f'=IF(B{r}="","",IF(AND(C{r}<>"",D{r}<>"",G{r}<>""),"Complete","Incomplete"))', None, "calc")
    validate(ws, "D6:D25", '"Text,Number,Date,Yes/No,Currency,Other"')
    validate(ws, "F6:F25", '"Yes,No"')
    label_value(ws, 27, "Fields documented", '=COUNTA(B6:B25)', "0", "summary")
    label_value(ws, 28, "Required fields", '=COUNTIF(F6:F25,"Yes")', "0", "summary")
    label_value(ws, 29, "Incomplete entries", '=COUNTIF(I6:I25,"Incomplete")', "0", "summary")
    wb.save(path)
