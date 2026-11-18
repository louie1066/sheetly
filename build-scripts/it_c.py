"""IT & Computing templates 18-25: API docs, release checklist, lab maintenance, printers, onboarding, binary/hex, traces, testing."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(606)
REPORT = dt.date(2026, 12, 1)


def api_docs(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Endpoints"
    setup_sheet(ws, "API Endpoint Documentation", "Document each endpoint. Totals by method and authentication calculate automatically", 7,
                [9, 30, 10, 30, 14, 14, 36])
    header_row(ws, 5, 2, ["Method", "Endpoint", "Auth required?", "Request parameters", "Success response", "Error responses", "Description"])
    eps = [("GET", "/students", "Yes", "class (optional)", "200 OK", "401, 403", "List students in a class"),
           ("POST", "/students", "Yes", "name, tutor_group", "201 Created", "400, 401", "Add a new student"),
           ("GET", "/students/{id}", "Yes", "id (path)", "200 OK", "404", "Get one student"),
           ("PUT", "/students/{id}", "Yes", "id (path), name, tutor_group", "200 OK", "400, 404", "Update a student's details"),
           ("POST", "/results", "Yes", "student_id, test_id, score", "201 Created", "400, 401", "Record a test score"),
           ("DELETE", "/results/{id}", "Yes", "id (path)", "204 No Content", "404", "Delete a recorded score"),
           ("POST", "/login", "No", "username, password", "200 OK", "401", "Get an access token"),
           ("GET", "/reports/class", "Yes", "test_id", "200 OK", "404", "Class summary for one test")]
    for i, row in enumerate(eps):
        r = 6 + i
        for c, v in enumerate(row):
            put(ws, r, 2 + c, v)
    for r in range(6 + len(eps), 21):
        for c in range(2, 9):
            put(ws, r, c, None)
    validate(ws, "B6:B20", '"GET,POST,PUT,DELETE,PATCH"')
    validate(ws, "D6:D20", '"Yes,No"')
    label_value(ws, 23, "Endpoints documented", '=COUNTA(C6:C20)', "0", "summary")
    label_value(ws, 24, "GET endpoints", '=COUNTIF(B6:B20,"GET")', "0", "summary")
    label_value(ws, 25, "Endpoints needing a token", '=COUNTIF(D6:D20,"Yes")', "0", "summary")
    wb.save(path)


def release_checklist(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Release"
    setup_sheet(ws, "Release Checklist", "Set the version, then tick each task. Progress by stage calculates automatically", 10,
                [16, 36, 14, 10, 26, 3, 16, 10, 10, 12])
    label_value(ws, 5, "Version number", "1.2.0", None, "input")
    label_value(ws, 6, "Release date", dt.date(2026, 12, 15), DATE, "input")
    header_row(ws, 8, 2, ["Stage", "Task", "Owner", "Done?", "Notes"])
    header_row(ws, 8, 8, ["Stage", "Tasks", "Done", "% done"])
    tasks = [("Build", "Merge approved changes"), ("Build", "Update version number"), ("Build", "Run the build script"),
             ("Test", "Run unit tests"), ("Test", "Check the main user journey"), ("Test", "Test on a phone and a laptop"),
             ("Test", "Check known bugs are logged"), ("Deploy", "Back up the live site"), ("Deploy", "Upload files"),
             ("Deploy", "Check the live site loads"), ("Deploy", "Check downloads work"), ("Document", "Update release notes"),
             ("Document", "Update user guide"), ("Document", "Tell users about the release"), ("Review", "Record lessons learned"),
             ("Review", "Close the release ticket"), ("Review", "Archive build files")]
    for i, (stage, task) in enumerate(tasks):
        r = 9 + i
        put(ws, r, 2, stage)
        put(ws, r, 3, task)
        put(ws, r, 4, f"Member {chr(65 + i % 3)}")
        put(ws, r, 5, "Yes" if i < 11 else "No")
        put(ws, r, 6, "")
    last = 8 + len(tasks)
    validate(ws, f"E9:E{last}", '"Yes,No"')
    for i, stage in enumerate(["Build", "Test", "Deploy", "Document", "Review"]):
        r = 9 + i
        put(ws, r, 8, stage)
        put(ws, r, 9, f"=COUNTIF($B$9:$B${last},H{r})", "0", "calc")
        put(ws, r, 10, f'=COUNTIFS($B$9:$B${last},H{r},$E$9:$E${last},"Yes")', "0", "calc")
        put(ws, r, 11, f'=IFERROR(J{r}/I{r},"")', "0%", "calc")
    put(ws, 14, 8, "Overall", kind="total")
    put(ws, 14, 9, "=SUM(I9:I13)", "0", "total")
    put(ws, 14, 10, "=SUM(J9:J13)", "0", "total")
    put(ws, 14, 11, '=IFERROR(J14/I14,"")', "0%", "summary")
    wb.save(path)


def lab_maintenance(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Log"
    setup_sheet(ws, "Computer Lab Booking and Maintenance Log", "Log bookings and maintenance tasks. Costs and tasks due soon calculate automatically", 7,
                [12, 12, 20, 26, 14, 12, 13])
    header_row(ws, 5, 2, ["Date", "Lab", "Booked for", "Maintenance task", "Done by", "Cost", "Next due"])
    tasks = ["Clean keyboards and screens", "Update operating system", "Check network cables", "Replace faulty mouse",
             "Re-image lab PCs", "Test UPS battery", "Check projector filter"]
    for i in range(12):
        r = 6 + i
        put(ws, r, 2, dt.date(2026, 11, 2) + dt.timedelta(days=7 * i), DATE)
        put(ws, r, 3, f"Lab {1 + i % 2}")
        put(ws, r, 4, f"Year {7 + i % 3} class")
        put(ws, r, 5, tasks[i % len(tasks)])
        put(ws, r, 6, f"Technician {chr(65 + i % 2)}")
        put(ws, r, 7, RNG.choice([0, 0, 15, 45, 120]), MONEY)
        put(ws, r, 8, dt.date(2026, 11, 2) + dt.timedelta(days=7 * i + 84), DATE)
    label_value(ws, 23, "Report date", REPORT, DATE, "input")
    label_value(ws, 25, "Total maintenance cost", "=SUM(G6:G20)", MONEY, "summary")
    label_value(ws, 26, "Tasks due in next 30 days", '=COUNTIFS(H6:H20,">="&C23,H6:H20,"<="&(C23+30))', "0", "summary")
    wb.save(path)


def printers(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Printers"
    setup_sheet(ws, "Printer and Consumables Tracker", "Enter toner levels and costs. Reorder flags and cost per page calculate automatically", 9,
                [16, 14, 12, 12, 12, 14, 12, 12, 12])
    header_row(ws, 5, 2, ["Printer", "Location", "Toner level", "Reorder at", "Status", "Pages this month",
                          "Cost per cartridge", "Cartridge yield", "Cost per page"])
    prn = [("Printer A", "Staff room", 0.15), ("Printer B", "Lab 1", 0.62), ("Printer C", "Lab 2", 0.08),
           ("Printer D", "Library", 0.45), ("Printer E", "Office", 0.30), ("Printer F", "Corridor", 0.90)]
    for i, (name, loc, lvl) in enumerate(prn):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, loc)
        put(ws, r, 4, lvl, "0%")
        put(ws, r, 5, 0.2, "0%")
        put(ws, r, 6, f'=IF(D{r}="","",IF(D{r}<=E{r},"Reorder","OK"))', None, "calc")
        put(ws, r, 7, RNG.randint(300, 2500), "#,##0")
        put(ws, r, 8, 45, MONEY)
        put(ws, r, 9, 2000, "#,##0")
        put(ws, r, 10, f'=IFERROR(H{r}/I{r},"")', "0.0000", "calc")
    label_value(ws, 14, "Printers to reorder", '=COUNTIF(F6:F11,"Reorder")', "0", "summary")
    label_value(ws, 15, "Pages printed this month", '=SUM(G6:G11)', "#,##0", "summary")
    label_value(ws, 16, "Estimated consumables cost", '=SUMPRODUCT(G6:G11,J6:J11)', MONEY, "summary")
    wb.save(path)


def onboarding(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Devices"
    setup_sheet(ws, "New-Device Onboarding Checklist", "Mark each step Yes as it is done. Completion for each device calculates automatically", 10,
                [12, 14, 12, 12, 12, 12, 12, 12, 12, 14])
    header_row(ws, 5, 2, ["Asset tag", "Assigned to", "Image installed", "Updates applied", "Accounts created",
                          "Security software", "Printers added", "Labelled", "Handed over", "% complete"])
    for i in range(12):
        r = 6 + i
        put(ws, r, 2, f"AT-{2001 + i}")
        put(ws, r, 3, f"Staff {chr(65 + i % 5)}")
        for c in range(4, 11):
            put(ws, r, c, "Yes" if (i < 8 or c < 8) else "No")
        put(ws, r, 11, f'=IF(B{r}="","",COUNTIF(D{r}:J{r},"Yes")/7)', "0%", "calc")
    validate(ws, "D6:J17", '"Yes,No"')
    label_value(ws, 19, "Devices fully onboarded", '=COUNTIF(K6:K17,1)', "0", "summary")
    label_value(ws, 20, "Average completion", '=IFERROR(AVERAGE(K6:K17),"")', "0%", "summary")
    wb.save(path)


def binary_hex(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Practice"
    setup_sheet(ws, "Binary and Hexadecimal Conversion Practice",
                "Type answers as text (put an apostrophe before binary, such as '00101010). Checks update automatically", 8,
                [12, 14, 12, 12, 12, 14, 14, 12])
    header_row(ws, 5, 2, ["Decimal", "Binary answer", "Binary check", "Hex answer", "Hex check",
                          "Binary", "Decimal answer", "Check"])
    decs = [42, 200, 15, 255, 99, 128, 7, 64, 170, 33]
    bins = ["1011", "11001", "101010", "1111", "100001", "1000000", "110", "11111111", "10101", "1100100"]
    for i, n in enumerate(decs):
        r = 6 + i
        put(ws, r, 2, n, "0")
        put(ws, r, 3, format(n, "08b") if i % 4 else "0" * 8, None)
        put(ws, r, 4, f'=IF(C{r}="","",IF(C{r}=DEC2BIN(B{r},8),"Correct","Check"))', None, "calc")
        put(ws, r, 5, format(n, "02X") if i % 3 else "", None)
        put(ws, r, 6, f'=IF(E{r}="","",IF(E{r}=DEC2HEX(B{r},2),"Correct","Check"))', None, "calc")
        put(ws, r, 7, bins[i])
        put(ws, r, 8, int(bins[i], 2) if i % 2 else None, "0")
        put(ws, r, 9, f'=IF(H{r}="","",IF(H{r}=BIN2DEC(G{r}),"Correct","Check"))', None, "calc")
    label_value(ws, 17, "Binary answers correct", '=COUNTIF(D6:D15,"Correct")', "0", "summary")
    label_value(ws, 18, "Hex answers correct", '=COUNTIF(F6:F15,"Correct")', "0", "summary")
    label_value(ws, 19, "Binary to decimal correct", '=COUNTIF(I6:I15,"Correct")', "0", "summary")
    wb.save(path)


def algorithm_trace(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Trace"
    setup_sheet(ws, "Algorithm Trace Table",
                "Trace this program by hand: total = 0, FOR n = 1 TO 4, total = total + n * 2, then PRINT total", 6,
                [8, 34, 10, 12, 14, 24])
    header_row(ws, 5, 2, ["Step", "Statement", "n", "total", "Output", "Notes"])
    steps = [("total = 0", None, 0, None), ("FOR n = 1 TO 4", 1, 0, None), ("total = total + n * 2", 1, 2, None),
             ("NEXT n", 2, 2, None), ("total = total + n * 2", 2, 6, None), ("NEXT n", 3, 6, None),
             ("total = total + n * 2", None, None, None), ("NEXT n", None, None, None),
             ("total = total + n * 2", None, None, None), ("PRINT total", None, None, None)]
    for i, (stmt, n, tot, out) in enumerate(steps):
        r = 6 + i
        put(ws, r, 2, i + 1, "0", "label")
        put(ws, r, 3, stmt, kind="label")
        put(ws, r, 4, n, "0")
        put(ws, r, 5, tot, "0")
        put(ws, r, 6, out, "0")
        put(ws, r, 7, "")
    label_value(ws, 18, "Expected final total", 20, "0", "input")
    label_value(ws, 19, "Largest total in your trace", '=MAX(E6:E15)', "0", "summary")
    label_value(ws, 20, "Trace result", '=IF(C19="","",IF(C19=C18,"Correct","Check your trace"))', None, "summary")
    wb.save(path)


def program_testing(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tests"
    setup_sheet(ws, "Program Testing Record", "Record each test's input, expected and actual output. Pass or fail calculates automatically", 8,
                [10, 26, 14, 16, 16, 12, 12, 26])
    header_row(ws, 5, 2, ["Test ID", "Function tested", "Input", "Expected output", "Actual output", "Result", "Tester", "Notes"])
    tests = [("grade(95)", 95, "A*"), ("grade(85)", 85, "A"), ("grade(72)", 72, "B"), ("grade(40)", 40, "E"),
             ("grade(0)", 0, "U"), ("grade(101)", 101, "Error"), ("grade(-5)", -5, "Error"), ("grade('abc')", "abc", "Error"),
             ("grade(50)", 50, "D")]
    actual = {95: "A*", 85: "A", 72: "B", 40: "E", 0: "U", 101: "Error", -5: "Error", "abc": "Error"}
    for i, (fn, inp, exp) in enumerate(tests):
        r = 6 + i
        put(ws, r, 2, f"PT-{i + 1:02d}")
        put(ws, r, 3, fn)
        put(ws, r, 4, str(inp))
        put(ws, r, 5, exp)
        put(ws, r, 6, actual.get(inp, ""))
        put(ws, r, 7, f'=IF(F{r}="","Not run",IF(F{r}=E{r},"Pass","Fail"))', None, "calc")
        put(ws, r, 8, f"Tester {chr(65 + i % 2)}")
        put(ws, r, 9, "")
    for r in range(6 + len(tests), 26):
        for c in range(2, 10):
            put(ws, r, c, None)
        put(ws, r, 7, f'=IF(C{r}="","",IF(F{r}="","Not run",IF(F{r}=E{r},"Pass","Fail")))', None, "calc")
    label_value(ws, 28, "Passed", '=COUNTIF(G6:G25,"Pass")', "0", "summary")
    label_value(ws, 29, "Failed", '=COUNTIF(G6:G25,"Fail")', "0", "summary")
    label_value(ws, 30, "Not run", '=COUNTIF(G6:G25,"Not run")', "0", "summary")
    label_value(ws, 31, "Pass rate (of tests run)", '=IFERROR(C28/(C28+C29),"")', "0%", "summary")
    wb.save(path)
