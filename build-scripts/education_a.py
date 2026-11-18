"""Templates 1-8: gradebook, attendance, seating, lesson planning, scheme of work, timetable, rubric, marks."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(101)
NAMES = [f"Student {i:02d}" for i in range(1, 11)]


def gradebook(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Gradebook"
    setup_sheet(ws, "Gradebook with Weighted Averages",
                "Enter marks and weights. Weighted % and grades calculate automatically", 10,
                [24, 14, 14, 14, 14, 14, 12, 3, 16, 12])
    header_row(ws, 5, 2, ["Student", "Assessment 1", "Assessment 2", "Assessment 3", "Assessment 4", "Weighted %", "Grade"])
    header_row(ws, 5, 10, ["Minimum %", "Grade"])
    put(ws, 6, 2, "Maximum marks", kind="label", bold=True)
    put(ws, 7, 2, "Weight % (must total 100)", kind="label", bold=True)
    for c, mx, w in zip(range(3, 7), [50, 40, 60, 100], [20, 20, 30, 30]):
        put(ws, 6, c, mx, "0")
        put(ws, 7, c, w, "0")
    put(ws, 7, 7, "=SUM(C7:F7)", "0", "total")
    for i, (m, g) in enumerate(zip([0, 0.4, 0.5, 0.6, 0.7], ["U", "E", "D", "C", "A"])):
        put(ws, 6 + i, 10, m, "0%")
        put(ws, 6 + i, 11, g)
    for i, name in enumerate(NAMES):
        r = 8 + i
        put(ws, r, 2, name)
        for c, mx in zip(range(3, 7), [50, 40, 60, 100]):
            put(ws, r, c, RNG.randint(int(mx * 0.45), mx), "0")
        put(ws, r, 7, f'=IF(COUNT(C{r}:F{r})=0,"",SUMPRODUCT(C{r}:F{r}/$C$6:$F$6,$C$7:$F$7)/SUM($C$7:$F$7))', "0.0%", "calc")
        put(ws, r, 8, f'=IF(G{r}="","",LOOKUP(G{r},$J$6:$J$10,$K$6:$K$10))', None, "calc")
    put(ws, 19, 2, "Class average", kind="total")
    put(ws, 19, 7, '=IFERROR(AVERAGE(G8:G17),"")', "0.0%", "summary")
    wb.save(path)


def attendance(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Register"
    setup_sheet(ws, "Attendance Register", "P = present, L = late, A = absent, E = authorised absence", 15,
                [22] + [6] * 10 + [10, 10, 10, 14])
    header_row(ws, 5, 2, ["Student"] + [f"Day {d}" for d in range(1, 11)] + ["Present", "Absent", "Late", "Attendance %"])
    put(ws, 6, 2, "Attendance % by day", kind="total")
    for c in range(3, 13):
        col = L(c)
        put(ws, 6, c, f'=IFERROR((COUNTIF({col}8:{col}17,"P")+COUNTIF({col}8:{col}17,"L"))/COUNTA({col}8:{col}17),"")',
            "0%", "total")
    codes = ["P"] * 8 + ["L", "A", "E"]
    for i, name in enumerate(NAMES):
        r = 8 + i
        put(ws, r, 2, name)
        for c in range(3, 13):
            put(ws, r, c, RNG.choice(codes))
        put(ws, r, 13, f'=COUNTIF(C{r}:L{r},"P")', "0", "calc")
        put(ws, r, 14, f'=COUNTIF(C{r}:L{r},"A")', "0", "calc")
        put(ws, r, 15, f'=COUNTIF(C{r}:L{r},"L")', "0", "calc")
        put(ws, r, 16, f'=IFERROR((M{r}+O{r})/COUNTA(C{r}:L{r}),"")', "0%", "calc")
    validate(ws, "C8:L17", '"P,A,L,E"')
    wb.save(path)


def seating(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Seating plan"
    setup_sheet(ws, "Seating Plan Generator",
                "Type names in list order. The grid fills left to right, row by row", 9,
                [20, 10, 3, 14, 14, 14, 14, 14, 14])
    header_row(ws, 5, 2, ["Student", "Seat"])
    section_label(ws, 4, 5, "Classroom grid")
    names = [f"Student {i:02d}" for i in range(1, 23)] + ["", ""]
    for i, name in enumerate(names):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, f'=IF(B{r}="","",{i + 1})', "0", "calc")
    for r_i in range(4):
        ws.row_dimensions[6 + r_i].height = 30
        for c_i in range(6):
            k = r_i * 6 + c_i + 1
            put(ws, 6 + r_i, 5 + c_i, f'=INDEX($B$6:$B$29,{k})&""', None, "calc")
    put(ws, 10, 5, "Front of room", kind="label", bold=True)
    wb.save(path)


def lesson_plan(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lesson plan"
    setup_sheet(ws, "Lesson Plan Template", "Plan the lesson, its timings and how you will check learning", 4,
                [26, 16, 60, 28])
    details = [
        ("Class and year", "Year 9 Computing", None),
        ("Date", dt.date(2026, 12, 1), DATE),
        ("Lesson length (minutes)", 60, "0"),
        ("Topic", "Selection with if statements", None),
        ("Learning objective", "Write an if statement that changes the output based on a condition", None),
        ("Success criteria", "Predict the output of a short program. Write a program with one if and one else", None),
        ("Key vocabulary", "condition, Boolean, branch, else", None),
        ("Differentiation", "Support: worked example. Extension: add elif for three outcomes", None),
        ("Assessment for learning", "Exit ticket: predict the output of two short programs", None),
    ]
    r = 5
    for label, value, fmt in details:
        put(ws, r, 2, label, kind="label", bold=True)
        put(ws, r, 3, value, fmt)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
        ws.cell(r, 3).alignment = Alignment(horizontal="left", vertical="center")
        r += 1
    header_row(ws, 15, 2, ["Stage", "Minutes", "What happens", "Resources"])
    stages = [
        ("Starter", 5, "Quick prediction on the board: what does this print?", "Board, code snippet"),
        ("Teach", 15, "Model a flowchart and code for one if statement, then add else", "Slides, IDE"),
        ("Guided practice", 15, "Pairs complete a three-step program together", "Worksheet A"),
        ("Independent task", 20, "Students write a program that checks a password length", "Worksheet B"),
        ("Plenary and exit ticket", 5, "Two predictions on paper, collected at the door", "Exit ticket"),
    ]
    for i, (stage, mins, what, res) in enumerate(stages):
        rr = 16 + i
        put(ws, rr, 2, stage)
        put(ws, rr, 3, mins, "0")
        put(ws, rr, 4, what)
        put(ws, rr, 5, res)
        ws.row_dimensions[rr].height = 30
    put(ws, 21, 2, "Total planned minutes", kind="total")
    put(ws, 21, 3, "=SUM(C16:C20)", "0", "total")
    put(ws, 22, 2, "Time left (lesson length minus plan)", kind="summary")
    put(ws, 22, 3, "=C7-C21", "0", "summary")
    put(ws, 22, 4, '=IF(C22<0,"Plan is too long: cut a stage","Plan fits the lesson")', None, "calc")
    wb.save(path)


def scheme_of_work(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Scheme of work"
    setup_sheet(ws, "Scheme of Work Planner",
                "Plan lessons per week, then record lessons taught to see what is left", 6,
                [10, 34, 16, 16, 16, 16])
    header_row(ws, 5, 2, ["Week", "Topic", "Lessons planned", "Lessons taught", "Lessons left", "Status"])
    topics = ["Introduction and safety", "Variables and data types", "Input and output", "Selection (if statements)",
              "Loops (for)", "Loops (while)", "Lists", "Functions", "Testing and debugging", "File handling",
              "Mini project", "Review and assessment"]
    planned = [2] * 11 + [1]
    taught = [2, 2, 2, 2, 2, 1]
    for i, topic in enumerate(topics):
        r = 6 + i
        put(ws, r, 2, i + 1, "0", "label")
        put(ws, r, 3, topic)
        put(ws, r, 4, planned[i], "0")
        put(ws, r, 5, taught[i] if i < len(taught) else None, "0")
        put(ws, r, 6, f'=IF(D{r}="","",D{r}-N(E{r}))', "0", "calc")
        put(ws, r, 7, f'=IF(D{r}="","",IF(N(E{r})>=D{r},"Complete",IF(N(E{r})=0,"Not started","In progress")))',
            None, "calc")
    put(ws, 18, 2, "Total", kind="total")
    put(ws, 18, 3, "", kind="total")
    for c in (4, 5, 6):
        put(ws, 18, c, f"=SUM({L(c)}6:{L(c)}17)", "0", "total")
    put(ws, 18, 7, "", kind="total")
    put(ws, 19, 3, "Progress through scheme", kind="summary")
    put(ws, 19, 4, "=IFERROR(E18/D18,0)", "0%", "summary")
    wb.save(path)


def timetable(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Timetable"
    setup_sheet(ws, "Termly Timetable",
                "Choose a subject for each period. Lesson counts per subject update automatically", 9,
                [14, 18, 18, 18, 18, 18, 3, 3, 18])
    header_row(ws, 5, 2, ["Period", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    header_row(ws, 5, 10, ["Subjects"])
    subjects = ["Computing", "Maths", "English", "Science", "Art", "PE", "Languages", "Tutor time"]
    for i, s in enumerate(subjects):
        put(ws, 6 + i, 10, s)
    for p in range(5):
        put(ws, 6 + p, 2, f"Period {p + 1}", kind="label", bold=True)
        for d in range(5):
            put(ws, 6 + p, 3 + d, RNG.choice(subjects[:7]))
    validate(ws, "C6:G10", "=$J$6:$J$13")
    header_row(ws, 12, 2, ["Subject", "Lessons per week", "Share of week"])
    for i in range(8):
        r = 13 + i
        put(ws, r, 2, f'=IF($J${6 + i}="","",$J${6 + i})', None, "calc")
        put(ws, r, 3, f'=COUNTIF($C$6:$G$10,B{r})', "0", "calc")
        put(ws, r, 4, f'=IFERROR(C{r}/COUNTA($C$6:$G$10),0)', "0%", "calc")
    put(ws, 21, 2, "Total", kind="total")
    put(ws, 21, 3, "=SUM(C13:C20)", "0", "total")
    put(ws, 21, 4, "=SUM(D13:D20)", "0%", "total")
    wb.save(path)


def rubric(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rubric"
    setup_sheet(ws, "Rubric Scoring Sheet",
                "Score each criterion from 1 to 4. The weighted score calculates automatically", 6,
                [22, 18, 18, 18, 18, 16])
    header_row(ws, 5, 2, ["Student", "Understanding", "Accuracy", "Structure", "Presentation", "Weighted score"])
    put(ws, 6, 2, "Weight %", kind="label", bold=True)
    for c, w in zip(range(3, 7), [30, 30, 25, 15]):
        put(ws, 6, c, w, "0")
    put(ws, 6, 7, "=SUM(C6:F6)", "0", "total")
    for i, name in enumerate(NAMES):
        r = 7 + i
        put(ws, r, 2, name)
        for c in range(3, 7):
            put(ws, r, c, RNG.randint(1, 4), "0")
        put(ws, r, 7, f'=IF(COUNT(C{r}:F{r})<4,"",SUMPRODUCT(C{r}:F{r},$C$6:$F$6)/(4*SUM($C$6:$F$6)))', "0%", "calc")
    validate(ws, "C7:F16", "1", "whole", "between", "4")
    put(ws, 17, 2, "Class average", kind="total")
    put(ws, 17, 7, '=IFERROR(AVERAGE(G7:G16),"")', "0%", "summary")
    header_row(ws, 19, 2, ["Level", "What it means"])
    meanings = [("4", "Secure. Goes beyond the task"), ("3", "Good. Secure on most of the task"),
                ("2", "Developing. Partly secure, needs more practice"), ("1", "Beginning. Limited evidence")]
    for i, (lvl, text) in enumerate(meanings):
        r = 20 + i
        put(ws, r, 2, lvl, kind="label", bold=True)
        put(ws, r, 3, text, kind="label")
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
    wb.save(path)


def mark_sheet(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Marks"
    setup_sheet(ws, "Mark Sheet with Grade Boundaries",
                "Enter each mark and its total. Percent, grade and result update from the boundary table", 9,
                [22, 12, 12, 12, 12, 14, 3, 16, 12])
    header_row(ws, 5, 2, ["Student", "Mark", "Out of", "Percent", "Grade", "Result"])
    header_row(ws, 5, 9, ["Minimum %", "Grade"])
    mins = [0, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
    grades = ["U", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i, (m, g) in enumerate(zip(mins, grades)):
        put(ws, 6 + i, 9, m, "0%")
        put(ws, 6 + i, 10, g)
    put(ws, 17, 9, "Pass mark (%)", kind="label", bold=True)
    put(ws, 17, 10, 0.45, "0%")
    for i, name in enumerate(NAMES):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, RNG.randint(15, 80), "0")
        put(ws, r, 4, 80, "0")
        put(ws, r, 5, f'=IF(OR(C{r}="",D{r}=""),"",C{r}/D{r})', "0%", "calc")
        put(ws, r, 6, f'=IF(E{r}="","",LOOKUP(E{r},$I$6:$I$15,$J$6:$J$15))', None, "calc")
        put(ws, r, 7, f'=IF(E{r}="","",IF(E{r}>=$J$17,"Pass","Fail"))', None, "calc")
    put(ws, 16, 2, "Class average", kind="total")
    put(ws, 16, 5, '=IFERROR(AVERAGE(E6:E15),"")', "0%", "summary")
    put(ws, 17, 2, "Students passing", kind="total")
    put(ws, 17, 7, '=COUNTIF(G6:G15,"Pass")', "0", "summary")
    wb.save(path)
