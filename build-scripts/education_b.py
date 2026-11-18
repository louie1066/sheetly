"""Templates 9-17: objective tracking, progress, homework, behaviour, parent contact, roster, reading, quizzes, exams."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(202)
NAMES = [f"Student {i:02d}" for i in range(1, 11)]


def assessment_objectives(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Objectives"
    objs = ["Ob 1 Variables", "Ob 2 Sequence", "Ob 3 Selection", "Ob 4 Loops", "Ob 5 Lists", "Ob 6 Functions"]
    setup_sheet(ws, "Assessment Tracker by Learning Objective",
                "Score each objective: 0 = not yet, 1 = developing, 2 = secure", 9,
                [22, 14, 14, 14, 14, 14, 14, 12, 12])
    header_row(ws, 5, 2, ["Student"] + objs + ["Secure count", "% secure"])
    for i, name in enumerate(NAMES):
        r = 6 + i
        put(ws, r, 2, name)
        for c in range(3, 9):
            put(ws, r, c, RNG.choice([0, 1, 1, 2, 2, 2]), "0")
        put(ws, r, 9, f"=COUNTIF(C{r}:H{r},2)", "0", "calc")
        put(ws, r, 10, f'=IFERROR(I{r}/COUNTA(C{r}:H{r}),"")', "0%", "calc")
    validate(ws, "C6:H15", "0", "whole", "between", "2")
    put(ws, 16, 2, "% secure per objective", kind="total")
    for c in range(3, 9):
        col = L(c)
        put(ws, 16, c, f'=IFERROR(COUNTIF({col}6:{col}15,2)/COUNTA($B$6:$B$15),"")', "0%", "total")
    wb.save(path)


def student_progress(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Progress"
    setup_sheet(ws, "Student Progress Tracker",
                "Enter each test as a percentage. Averages, change and flags calculate automatically", 9,
                [22, 12, 12, 12, 12, 12, 12, 16, 14])
    header_row(ws, 5, 2, ["Student", "Test 1", "Test 2", "Test 3", "Test 4", "Test 5", "Average",
                          "Change (Test 5 - Test 1)", "Flag"])
    label_value(ws, 17, "Flag as Support if average is below", 0.5, "0%", "input")
    label_value(ws, 18, "Flag as Stretch if average is at or above", 0.8, "0%", "input")
    for i, name in enumerate(NAMES):
        r = 6 + i
        put(ws, r, 2, name)
        start = RNG.uniform(0.4, 0.7)
        for c in range(3, 8):
            put(ws, r, c, round(min(0.98, max(0.2, start + (c - 3) * RNG.uniform(-0.02, 0.06))), 2), "0%")
        put(ws, r, 8, f'=IF(COUNT(C{r}:G{r})=0,"",AVERAGE(C{r}:G{r}))', "0%", "calc")
        put(ws, r, 9, f'=IF(OR(C{r}="",G{r}=""),"",G{r}-C{r})', "+0%;-0%;0%", "calc")
        put(ws, r, 10, f'=IF(H{r}="","",IF(H{r}<$C$17,"Support",IF(H{r}>=$C$18,"Stretch","On track")))', None, "calc")
    put(ws, 16, 2, "Class average", kind="total")
    for c in range(3, 9):
        col = L(c)
        put(ws, 16, c, f'=IFERROR(AVERAGE({col}6:{col}15),"")', "0%", "total")
    wb.save(path)


def homework(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Homework"
    setup_sheet(ws, "Homework Tracker",
                "Y = on time, L = late, N = not submitted. Counts and completion calculate automatically", 13,
                [22] + [9] * 8 + [12, 10, 10, 14])
    header_row(ws, 5, 2, ["Student"] + [f"HW {i}" for i in range(1, 9)] + ["On time", "Late", "Missing", "Completion %"])
    put(ws, 6, 2, "Due date", kind="label", bold=True)
    for i in range(8):
        put(ws, 6, 3 + i, dt.date(2026, 9, 11) + dt.timedelta(days=7 * i), DATE)
    for i, name in enumerate(NAMES):
        r = 8 + i
        put(ws, r, 2, name)
        for c in range(3, 11):
            put(ws, r, c, RNG.choice(["Y"] * 7 + ["L", "N"]))
        put(ws, r, 11, f'=COUNTIF(C{r}:J{r},"Y")', "0", "calc")
        put(ws, r, 12, f'=COUNTIF(C{r}:J{r},"L")', "0", "calc")
        put(ws, r, 13, f'=COUNTIF(C{r}:J{r},"N")', "0", "calc")
        put(ws, r, 14, f'=IFERROR((K{r}+L{r})/COUNTA(C{r}:J{r}),"")', "0%", "calc")
    validate(ws, "C8:J17", '"Y,L,N"')
    put(ws, 18, 2, "Completion per task", kind="total")
    for c in range(3, 11):
        col = L(c)
        put(ws, 18, c, f'=IFERROR((COUNTIF({col}8:{col}17,"Y")+COUNTIF({col}8:{col}17,"L"))/COUNTA($B$8:$B$17),"")',
            "0%", "total")
    wb.save(path)


def behaviour_points(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Log"
    setup_sheet(ws, "Behaviour Points Log", "Record a positive or negative point each time. Totals are on the Summary sheet", 5,
                [12, 18, 10, 36, 16])
    header_row(ws, 5, 2, ["Date", "Student", "Points (+ or -)", "Reason", "Recorded by"])
    reasons = [("Helped a classmate", 2), ("Completed all tasks", 2), ("Late to lesson", -1),
               ("Forgot equipment", -1), ("Excellent teamwork", 3), ("Phone out in class", -2)]
    for i in range(18):
        r = 6 + i
        put(ws, r, 2, dt.date(2026, 9, 14) + dt.timedelta(days=i % 9), DATE)
        put(ws, r, 3, RNG.choice(NAMES))
        reason, pts = RNG.choice(reasons)
        put(ws, r, 4, pts, "+0;-0;0")
        put(ws, r, 5, reason)
        put(ws, r, 6, "Teacher A")
    validate(ws, "C6:C45", "=Summary!$B$6:$B$15")
    validate(ws, "D6:D45", "-5", "whole", "between", "5")
    s = wb.create_sheet("Summary")
    setup_sheet(s, "Behaviour Points Summary", "Totals by student. Names must match the Student column on the Log sheet", 4,
                [22, 14, 14, 14])
    header_row(s, 5, 2, ["Student", "Positive points", "Negative points", "Total"])
    for i, name in enumerate(NAMES):
        r = 6 + i
        put(s, r, 2, name)
        put(s, r, 3, f'=SUMIFS(Log!$D$6:$D$45,Log!$C$6:$C$45,B{r},Log!$D$6:$D$45,">0")', "+0;-0;0", "calc")
        put(s, r, 4, f'=SUMIFS(Log!$D$6:$D$45,Log!$C$6:$C$45,B{r},Log!$D$6:$D$45,"<0")', "+0;-0;0", "calc")
        put(s, r, 5, f"=SUMIF(Log!$C$6:$C$45,B{r},Log!$D$6:$D$45)", "+0;-0;0", "calc")
    put(s, 16, 2, "Class total", kind="total")
    for c in (3, 4, 5):
        put(s, 16, c, f"=SUM({L(c)}6:{L(c)}15)", "+0;-0;0", "total")
    wb.save(path)


def parent_contact(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Log"
    setup_sheet(ws, "Parent Contact Log", "One row per contact. Open follow-ups appear on the Summary sheet", 8,
                [12, 16, 22, 12, 30, 28, 14, 10])
    header_row(ws, 5, 2, ["Date", "Student", "Parent or carer", "Method", "Reason", "Outcome", "Follow-up by", "Done?"])
    methods = ["Phone", "Email", "Meeting", "Letter"]
    reasons = ["Missing homework", "Positive progress", "Attendance concern", "Behaviour follow-up", "Assessment result"]
    for i in range(10):
        r = 6 + i
        n = RNG.randint(1, 10)
        put(ws, r, 2, dt.date(2026, 9, 21) + dt.timedelta(days=3 * i), DATE)
        put(ws, r, 3, f"Student {n:02d}")
        put(ws, r, 4, f"Parent of Student {n:02d}")
        put(ws, r, 5, RNG.choice(methods))
        put(ws, r, 6, RNG.choice(reasons))
        put(ws, r, 7, "Agreed a weekly check-in" if i % 2 == 0 else "Left a voicemail")
        put(ws, r, 8, dt.date(2026, 10, 2) + dt.timedelta(days=3 * i), DATE)
        put(ws, r, 9, "Yes" if i % 3 else "No")
    validate(ws, "C6:C45", "=Summary!$B$6:$B$15")
    validate(ws, "E6:E45", '"Phone,Email,Meeting,Letter"')
    validate(ws, "I6:I45", '"Yes,No"')
    s = wb.create_sheet("Summary")
    setup_sheet(s, "Parent Contact Summary", "Contacts and open follow-ups by student", 3, [22, 14, 16])
    header_row(s, 5, 2, ["Student", "Contacts", "Open follow-ups"])
    for i, name in enumerate(NAMES):
        r = 6 + i
        put(s, r, 2, name)
        put(s, r, 3, f"=COUNTIF(Log!$C$6:$C$45,B{r})", "0", "calc")
        put(s, r, 4, f'=COUNTIFS(Log!$C$6:$C$45,B{r},Log!$I$6:$I$45,"No")', "0", "calc")
    put(s, 16, 2, "Total", kind="total")
    put(s, 16, 3, "=SUM(C6:C15)", "0", "total")
    put(s, 16, 4, "=SUM(D6:D15)", "0", "total")
    label_value(s, 18, "Open follow-ups overall", '=COUNTIF(Log!$I$6:$I$45,"No")', "0", "summary")
    wb.save(path)


def class_roster(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Roster"
    setup_sheet(ws, "Class Roster", "Use invented or anonymised details only in the template. Keep real records in your school system", 10,
                [12, 18, 18, 26, 14, 14, 30, 3, 14, 12])
    header_row(ws, 5, 2, ["Student ID", "Surname", "Forename", "Full name", "Tutor group", "Class", "Notes"])
    header_row(ws, 5, 10, ["Tutor group", "Students"])
    for i in range(24):
        r = 6 + i
        put(ws, r, 2, f"S{1001 + i}")
        put(ws, r, 3, "Sample")
        put(ws, r, 4, f"Student {i + 1:02d}")
        put(ws, r, 5, f'=IF(C{r}="","",D{r}&" "&C{r})', None, "calc")
        put(ws, r, 6, "7A" if i < 12 else "7B")
        put(ws, r, 7, "Computing 1" if i % 2 == 0 else "Computing 2")
        put(ws, r, 8, "")
    validate(ws, "F6:F35", '"7A,7B"')
    put(ws, 6, 10, "7A", kind="input")
    put(ws, 7, 10, "7B", kind="input")
    put(ws, 6, 11, '=COUNTIF($F$6:$F$35,J6)', "0", "calc")
    put(ws, 7, 11, '=COUNTIF($F$6:$F$35,J7)', "0", "calc")
    put(ws, 8, 10, "Total", kind="total")
    put(ws, 8, 11, "=SUM(K6:K7)", "0", "total")
    wb.save(path)


def reading_log(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reading"
    setup_sheet(ws, "Reading Log", "Log each book. Days taken and pages per day calculate automatically", 8,
                [30, 20, 14, 10, 12, 12, 10, 12])
    header_row(ws, 5, 2, ["Book title", "Author", "Genre", "Pages", "Start date", "Finish date", "Days taken", "Pages per day"])
    books = [("The Lost Cable", "A. Writer", "Mystery", 210, dt.date(2026, 9, 7), dt.date(2026, 9, 14)),
             ("Robots in the Lab", "B. Author", "Science fiction", 180, dt.date(2026, 9, 15), dt.date(2026, 9, 22)),
             ("Coding for Kids", "C. Teacher", "Non-fiction", 150, dt.date(2026, 9, 23), dt.date(2026, 9, 27)),
             ("Island of Stars", "D. Novelist", "Adventure", 320, dt.date(2026, 10, 1), dt.date(2026, 10, 12)),
             ("Short Stories Vol 1", "E. Editor", "Anthology", 120, dt.date(2026, 10, 13), None),
             ("The Green Door", "F. Writer", "Fantasy", 260, dt.date(2026, 10, 14), None)]
    for i, (t, a, g, p, s, f) in enumerate(books):
        r = 6 + i
        put(ws, r, 2, t)
        put(ws, r, 3, a)
        put(ws, r, 4, g)
        put(ws, r, 5, p, "0")
        put(ws, r, 6, s, DATE)
        put(ws, r, 7, f, DATE)
        put(ws, r, 8, f'=IF(OR(F{r}="",G{r}=""),"",G{r}-F{r}+1)', "0", "calc")
        put(ws, r, 9, f'=IF(H{r}="","",E{r}/H{r})', "0.0", "calc")
    for r in range(6 + len(books), 26):
        for c in range(2, 8):
            put(ws, r, c, None)
        put(ws, r, 8, f'=IF(OR(F{r}="",G{r}=""),"",G{r}-F{r}+1)', "0", "calc")
        put(ws, r, 9, f'=IF(H{r}="","",E{r}/H{r})', "0.0", "calc")
    label_value(ws, 28, "Books finished", '=COUNT(G6:G25)', "0", "summary")
    label_value(ws, 29, "Pages in finished books", '=SUMPRODUCT((G6:G25<>"")*E6:E25)', "0", "summary")
    label_value(ws, 30, "Average pages per day", '=IFERROR(AVERAGE(I6:I25),"")', "0.0", "summary")
    wb.save(path)


def quiz_analyser(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Quiz"
    setup_sheet(ws, "Quiz Score Analyser", "Enter 1 for a correct answer and 0 for incorrect. Question difficulty calculates automatically", 13,
                [20] + [7] * 10 + [9, 11])
    header_row(ws, 5, 2, ["Student"] + [f"Q{i}" for i in range(1, 11)] + ["Score", "Score %"])
    put(ws, 6, 2, "% correct", kind="total")
    put(ws, 7, 2, "Difficulty", kind="label", bold=True)
    for c in range(3, 13):
        col = L(c)
        put(ws, 6, c, f'=IFERROR(COUNTIF({col}8:{col}17,1)/COUNTA($B$8:$B$17),"")', "0%", "total")
        put(ws, 7, c, f'=IF({col}6="","",IF({col}6<0.4,"Hard",IF({col}6>0.8,"Easy","OK")))', None, "calc")
    for i, name in enumerate(NAMES):
        r = 8 + i
        put(ws, r, 2, name)
        p = RNG.uniform(0.4, 0.9)
        for c in range(3, 13):
            put(ws, r, c, 1 if RNG.random() < p else 0, "0")
        put(ws, r, 13, f"=SUM(C{r}:L{r})", "0", "calc")
        put(ws, r, 14, f'=IF(COUNT(C{r}:L{r})=0,"",M{r}/COUNTA($C$5:$L$5))', "0%", "calc")
    validate(ws, "C8:L17", "0", "whole", "between", "1")
    label_value(ws, 19, "Quiz average %", '=IFERROR(AVERAGE(N8:N17),"")', "0%", "summary")
    label_value(ws, 20, "Hardest question", '=INDEX(C5:L5,MATCH(MIN(C6:L6),C6:L6,0))', None, "summary")
    wb.save(path)


def exam_timetable(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Exams"
    setup_sheet(ws, "Exam Timetable Planner", "Enter the date, start time and length. End time and same-day checks calculate automatically", 8,
                [18, 12, 10, 14, 10, 12, 18, 26])
    header_row(ws, 5, 2, ["Subject", "Date", "Start", "Duration (min)", "End", "Room", "Invigilator", "Same-day check"])
    exams = [("Computing paper 1", dt.date(2026, 12, 7), dt.time(9, 0), 90, "Hall A", "Teacher A"),
             ("Maths paper 1", dt.date(2026, 12, 7), dt.time(13, 0), 75, "Hall B", "Teacher B"),
             ("English paper", dt.date(2026, 12, 8), dt.time(9, 0), 105, "Hall A", "Teacher C"),
             ("Science paper 1", dt.date(2026, 12, 9), dt.time(9, 0), 75, "Hall B", "Teacher D"),
             ("Computing paper 2", dt.date(2026, 12, 10), dt.time(9, 0), 90, "Hall A", "Teacher A"),
             ("Art portfolio", dt.date(2026, 12, 10), dt.time(13, 30), 60, "Studio", "Teacher E")]
    for i in range(12):
        r = 6 + i
        if i < len(exams):
            s, d, t, m, room, inv = exams[i]
            put(ws, r, 2, s)
            put(ws, r, 3, d, DATE)
            put(ws, r, 4, t, "hh:mm")
            put(ws, r, 5, m, "0")
            put(ws, r, 7, room)
            put(ws, r, 8, inv)
        else:
            for c in (2, 3, 4, 5, 7, 8):
                put(ws, r, c, None)
        put(ws, r, 6, f'=IF(OR(D{r}="",E{r}=""),"",D{r}+E{r}/1440)', "hh:mm", "calc")
        put(ws, r, 9, f'=IF(C{r}="","",IF(COUNTIF($C$6:$C$17,C{r})>1,"Same day as another exam",""))', None, "calc")
    label_value(ws, 19, "Exams scheduled", '=COUNTA(B6:B17)', "0", "summary")
    label_value(ws, 20, "Exams sharing a day", '=COUNTIF(I6:I17,"Same*")', "0", "summary")
    wb.save(path)
