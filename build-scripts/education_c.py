"""Templates 18-25: revision, projects, lab bookings, classroom budget, clubs, group work, report comments, checklists."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(303)
NAMES = [f"Student {i:02d}" for i in range(1, 11)]


def revision_schedule(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Revision"
    setup_sheet(ws, "Revision Schedule",
                "Plan hours for each topic, then log hours done. Hours left and % complete calculate automatically", 7,
                [28, 11, 12, 12, 12, 12, 14])
    header_row(ws, 5, 2, ["Topic", "Priority", "Hours planned", "Hours done", "Hours left", "% complete", "Target date"])
    topics = ["Algorithms and flowcharts", "Binary and hexadecimal", "Data representation", "Networks and security",
              "Databases", "Programming constructs", "Testing", "Boolean logic", "Systems architecture",
              "Ethics and legal issues", "Spreadsheets", "Past paper practice"]
    prios = ["High", "High", "Medium", "Medium", "Low"]
    for i, t in enumerate(topics):
        r = 6 + i
        put(ws, r, 2, t)
        put(ws, r, 3, prios[i % len(prios)])
        put(ws, r, 4, RNG.choice([2, 3, 4, 5]), "0.0")
        put(ws, r, 5, RNG.choice([0, 1, 2, 3, 4]) if i < 7 else None, "0.0")
        put(ws, r, 6, f'=IF(D{r}="","",MAX(0,D{r}-N(E{r})))', "0.0", "calc")
        put(ws, r, 7, f'=IF(OR(D{r}="",D{r}=0),"",MIN(1,N(E{r})/D{r}))', "0%", "calc")
        put(ws, r, 8, dt.date(2026, 12, 14) + dt.timedelta(days=i), DATE)
    validate(ws, "C6:C17", '"High,Medium,Low"')
    put(ws, 18, 2, "Total", kind="total")
    put(ws, 18, 3, "", kind="total")
    put(ws, 18, 4, "=SUM(D6:D17)", "0.0", "total")
    put(ws, 18, 5, "=SUM(E6:E17)", "0.0", "total")
    put(ws, 18, 6, "=SUM(F6:F17)", "0.0", "total")
    put(ws, 18, 7, '=IFERROR(E18/D18,0)', "0%", "total")
    put(ws, 18, 8, "", kind="total")
    wb.save(path)


def project_tracker(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Milestones"
    setup_sheet(ws, "Student Project Tracker",
                "Set the report date, then enter due dates and completion dates. Status updates automatically", 6,
                [30, 16, 14, 16, 18, 14])
    label_value(ws, 5, "Report date", dt.date(2026, 12, 10), DATE, "input")
    header_row(ws, 7, 2, ["Milestone", "Team", "Due date", "Date completed", "Status"])
    milestones = [("Project proposal", "Team A"), ("Research notes", "Team A"), ("Design sketches", "Team B"),
                  ("Prototype", "Team B"), ("Testing log", "Team C"), ("Peer feedback", "Team C"),
                  ("Final build", "Team A"), ("Presentation", "Team B"), ("Written report", "Team C"),
                  ("Reflection", "Team A")]
    for i, (m, team) in enumerate(milestones):
        r = 8 + i
        put(ws, r, 2, m)
        put(ws, r, 3, team)
        put(ws, r, 4, dt.date(2026, 11, 20) + dt.timedelta(days=5 * i), DATE)
        done = dt.date(2026, 11, 20) + dt.timedelta(days=5 * i + (2 if i % 3 == 0 else -1)) if i < 6 else None
        put(ws, r, 5, done, DATE)
        put(ws, r, 6,
            f'=IF(D{r}="","",IF(E{r}<>"",IF(E{r}>D{r},"Done late","Done on time"),IF($C$5>D{r},"Overdue","Open")))',
            None, "calc")
    validate(ws, "C8:C17", '"Team A,Team B,Team C"')
    label_value(ws, 19, "Milestones", '=COUNTA(B8:B17)', "0", "summary")
    label_value(ws, 20, "Done (on time or late)", '=COUNTIF(F8:F17,"Done*")', "0", "summary")
    label_value(ws, 21, "Overdue", '=COUNTIF(F8:F17,"Overdue")', "0", "summary")
    label_value(ws, 22, "Percent done", '=IFERROR(C20/C19,0)', "0%", "summary")
    wb.save(path)


def lab_booking(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bookings"
    setup_sheet(ws, "Lab Equipment Booking",
                "Book a room and equipment for each period. Clashes and over-booked stock are flagged", 10,
                [12, 12, 9, 16, 22, 10, 18, 3, 22, 12])
    header_row(ws, 5, 2, ["Date", "Room", "Period", "Teacher", "Equipment", "Quantity", "Booking check"])
    header_row(ws, 5, 10, ["Equipment", "Stock"])
    stock = [("Tablets", 20), ("Microcontrollers", 15), ("Laptops", 30), ("Robots", 10), ("Projectors", 4), ("Headsets", 25)]
    for i, (e, n) in enumerate(stock):
        put(ws, 6 + i, 10, e)
        put(ws, 6 + i, 11, n, "0")
    bookings = [("Lab 1", 1, "Teacher A", "Laptops", 30), ("Lab 1", 2, "Teacher B", "Laptops", 28),
                ("Lab 2", 1, "Teacher C", "Microcontrollers", 12), ("Lab 2", 3, "Teacher C", "Robots", 5),
                ("Lab 1", 1, "Teacher D", "Tablets", 10), ("Lab 2", 1, "Teacher E", "Projectors", 2)]
    for i in range(25):
        r = 6 + i
        if i < len(bookings):
            room, per, teacher, eq, qty = bookings[i]
            put(ws, r, 2, dt.date(2026, 12, 1) + dt.timedelta(days=i // 4), DATE)
            put(ws, r, 3, room)
            put(ws, r, 4, per, "0")
            put(ws, r, 5, teacher)
            put(ws, r, 6, eq)
            put(ws, r, 7, qty, "0")
        else:
            for c in range(2, 8):
                put(ws, r, c, None, DATE if c == 2 else ("0" if c in (4, 7) else None))
        put(ws, r, 8,
            f'=IF(B{r}="","",IF(COUNTIFS($B$6:$B$30,B{r},$C$6:$C$30,C{r},$D$6:$D$30,D{r})>1,"Room clash",'
            f'IF(F{r}="","OK",IF(SUMIFS($G$6:$G$30,$B$6:$B$30,B{r},$F$6:$F$30,F{r})>'
            f'IFERROR(VLOOKUP(F{r},$J$6:$K$11,2,FALSE),0),"Over stock","OK"))))', None, "calc")
    validate(ws, "F6:F30", "=$J$6:$J$11")
    validate(ws, "C6:C30", '"Lab 1,Lab 2,Studio"')
    validate(ws, "G6:G30", "1", "whole", "greaterThanOrEqual")
    wb.save(path)


def classroom_budget(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget"
    setup_sheet(ws, "Classroom Budget Tracker", "Set each category's budget. Spending from the Spending sheet appears here", 5,
                [26, 16, 16, 16, 12])
    header_row(ws, 5, 2, ["Category", "Allocated", "Spent", "Remaining", "% used"])
    cats = [("Stationery", 300), ("Printing", 250), ("Software licences", 400), ("Books and resources", 500),
            ("Equipment repairs", 200), ("Trips and events", 350)]
    for i, (name, amt) in enumerate(cats):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, amt, MONEY)
        put(ws, r, 4, f"=SUMIF(Spending!$C$6:$C$60,B{r},Spending!$F$6:$F$60)", MONEY, "calc")
        put(ws, r, 5, f"=C{r}-D{r}", MONEY, "calc")
        put(ws, r, 6, f'=IFERROR(D{r}/C{r},"")', "0%", "calc")
    put(ws, 12, 2, "Total", kind="total")
    for c in (3, 4, 5):
        put(ws, 12, c, f"=SUM({L(c)}6:{L(c)}11)", MONEY, "total")
    put(ws, 12, 6, '=IFERROR(D12/C12,"")', "0%", "total")
    label_value(ws, 14, "Money left overall", "=E12", MONEY, "summary")
    sp = wb.create_sheet("Spending")
    setup_sheet(sp, "Spending Log", "Log each purchase. Choose a category from the Budget sheet", 5, [12, 22, 28, 18, 14])
    header_row(sp, 5, 2, ["Date", "Category", "Item", "Supplier", "Amount"])
    items = [("Stationery", "Pens and paper", "Supplier A", 42.5), ("Printing", "Worksheet printing", "Supplier B", 60),
             ("Software licences", "Coding IDE licences", "Supplier C", 180), ("Books and resources", "Class readers", "Supplier A", 120),
             ("Equipment repairs", "Projector lamp", "Supplier D", 95), ("Trips and events", "Museum visit bus", "Supplier E", 150),
             ("Stationery", "Whiteboard markers", "Supplier A", 18.75), ("Printing", "Exam papers", "Supplier B", 45)]
    for i, (cat, item, sup, amt) in enumerate(items):
        r = 6 + i
        put(sp, r, 2, dt.date(2026, 9, 10) + dt.timedelta(days=9 * i), DATE)
        put(sp, r, 3, cat)
        put(sp, r, 4, item)
        put(sp, r, 5, sup)
        put(sp, r, 6, amt, MONEY)
    for r in range(6 + len(items), 61):
        put(sp, r, 2, None, DATE)
        for c in (3, 4, 5, 6):
            put(sp, r, c, None, MONEY if c == 6 else None)
    validate(sp, "C6:C60", "=Budget!$B$6:$B$11")
    validate(sp, "F6:F60", "0", "decimal", "greaterThanOrEqual")
    wb.save(path)


def club_signup(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Clubs"
    setup_sheet(ws, "Club Sign-up Sheet",
                "Enter each student's first and second choice. Sign-ups and spaces update automatically", 6,
                [24, 16, 16, 18, 14, 22])
    header_row(ws, 5, 2, ["Club", "Meets", "Capacity", "First-choice sign-ups", "Spaces left", "Status"])
    clubs = [("Coding Club", "Monday"), ("Robotics Club", "Tuesday"), ("Chess Club", "Wednesday"),
             ("Art Club", "Thursday"), ("Debate Club", "Thursday"), ("Gaming Club", "Friday")]
    for i, (name, day) in enumerate(clubs):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, day)
        put(ws, r, 4, 12, "0")
        put(ws, r, 5, f"=COUNTIF($C$16:$C$35,B{r})", "0", "calc")
        put(ws, r, 6, f"=D{r}-E{r}", "0", "calc")
        put(ws, r, 7, f'=IF(E{r}>D{r},"Over: move some students",IF(E{r}=D{r},"Full","Open"))', None, "calc")
    header_row(ws, 15, 2, ["Student", "First choice", "Second choice"])
    for i in range(20):
        r = 16 + i
        put(ws, r, 2, f"Student {i + 1:02d}")
        put(ws, r, 3, RNG.choice(clubs)[0])
        put(ws, r, 4, RNG.choice(clubs)[0])
    validate(ws, "C16:D35", "=$B$6:$B$11")
    wb.save(path)


def group_rotation(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rotation"
    setup_sheet(ws, "Group-Work Rotation Planner",
                "Students are placed in the same order each time. Groups rotate each round and group sizes are checked", 11,
                [22, 12, 12, 12, 12, 3, 10, 12, 12, 12, 12])
    label_value(ws, 4, "Number of groups (1 to 6)", 6, "0", "input")
    header_row(ws, 5, 2, ["Student", "Round 1", "Round 2", "Round 3", "Round 4"])
    header_row(ws, 5, 8, ["Group", "Round 1", "Round 2", "Round 3", "Round 4"])
    n_students = 24
    for i in range(n_students):
        r = 6 + i
        put(ws, r, 2, f"Student {i + 1:02d}")
        for k in range(4):
            # Within a block of G students, each round shifts the group by the block number.
            put(ws, r, 3 + k,
                f"=MOD(MOD({i},$C$4)+{k}*INT({i}/$C$4),$C$4)+1", "0", "calc")
    for g in range(6):
        r = 6 + g
        put(ws, r, 8, g + 1, "0", "label")
        for k in range(4):
            col = L(3 + k)
            put(ws, r, 9 + k, f'=IF($H{r}>$C$4,"",COUNTIF(${col}$6:${col}$29,$H{r}))', "0", "calc")
    label_value(ws, 13, "Group sizes balanced (within 1)?",
                '=IF(MAX(I6:L11)-MIN(I6:L11)<=1,"Yes","Check")', None, "summary")
    wb.save(path)


def report_comments(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    bank = wb.create_sheet("Comment bank")
    setup_sheet(bank, "Report Comment Bank", "Use [Name] where the student's name should go. Codes appear in the Report sheet", 3,
                [12, 18, 90])
    header_row(bank, 5, 2, ["Code", "Area", "Comment"])
    comments = [
        ("S1", "Strength", "[Name] works carefully and checks their code before asking for help."),
        ("S2", "Strength", "[Name] explains ideas clearly and supports classmates in group work."),
        ("S3", "Strength", "[Name] shows strong problem-solving skills and tries new approaches."),
        ("T1", "Target", "[Name] should practise tracing algorithms step by step before running code."),
        ("T2", "Target", "[Name] should add comments to programs so others can follow the logic."),
        ("T3", "Target", "[Name] should test programs with a range of inputs, including unusual ones."),
        ("E1", "Effort", "[Name] has worked consistently this term and met most deadlines."),
        ("E2", "Effort", "[Name] should complete homework tasks on time to build confidence."),
    ]
    for i, (code, area, text) in enumerate(comments):
        r = 6 + i
        put(bank, r, 2, code, kind="label", bold=True)
        put(bank, r, 3, area, kind="label")
        put(bank, r, 4, text)
        bank.row_dimensions[r].height = 30
    setup_sheet(ws, "Report Comments",
                "Choose codes for each student. The full comment and word count are built automatically", 6,
                [22, 12, 12, 12, 90, 12])
    header_row(ws, 5, 2, ["Student", "Strength code", "Target code", "Effort code", "Report comment", "Words"])
    lookup = "'Comment bank'!$B$6:$D$13"

    def part(cell):
        return f'SUBSTITUTE(IFERROR(VLOOKUP({cell},{lookup},3,FALSE),""),"[Name]",$B{{r}})'

    for i, name in enumerate(NAMES):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, f"S{RNG.randint(1, 3)}")
        put(ws, r, 4, f"T{RNG.randint(1, 3)}")
        put(ws, r, 5, f"E{RNG.randint(1, 2)}")
        combined = "&\" \"&".join(part(f"{c}{r}").replace("{r}", str(r)) for c in ("C", "D", "E"))
        put(ws, r, 6, f'=TRIM({combined})', None, "calc")
        put(ws, r, 7, f'=IF(F{r}="","",LEN(TRIM(F{r}))-LEN(SUBSTITUTE(TRIM(F{r})," ",""))+1)', "0", "calc")
        ws.row_dimensions[r].height = 45
    validate(ws, "C6:E15", "='Comment bank'!$B$6:$B$13")
    wb.save(path)


def course_checklist(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Checklist"
    setup_sheet(ws, "Course Completion Checklist", "Tick each item Yes when it is done. Section progress calculates automatically", 10,
                [22, 40, 10, 12, 28, 3, 22, 12, 12, 12])
    header_row(ws, 5, 2, ["Section", "Item", "Done?", "Due", "Notes"])
    header_row(ws, 5, 8, ["Section", "Items", "Done", "% complete"])
    items = [("Unit 1: Foundations", "Complete the baseline quiz"), ("Unit 1: Foundations", "Set up the programming environment"),
             ("Unit 1: Foundations", "Submit first program"), ("Unit 1: Foundations", "Reflection on errors"),
             ("Unit 2: Algorithms", "Write three flowcharts"), ("Unit 2: Algorithms", "Trace an algorithm by hand"),
             ("Unit 2: Algorithms", "Pass the algorithms test"), ("Unit 3: Data", "Binary conversion practice"),
             ("Unit 3: Data", "Data types worksheet"), ("Unit 3: Data", "Pass the data assessment"),
             ("Unit 4: Project", "Project proposal approved"), ("Unit 4: Project", "Prototype demonstrated"),
             ("Unit 4: Project", "Final project submitted"), ("Unit 4: Project", "Peer review completed")]
    for i, (sec, item) in enumerate(items):
        r = 6 + i
        put(ws, r, 2, sec)
        put(ws, r, 3, item)
        put(ws, r, 4, "Yes" if i < 9 else "No")
        put(ws, r, 5, dt.date(2026, 10, 2) + dt.timedelta(days=7 * (i // 3)), DATE)
        put(ws, r, 6, "")
    for r in range(6 + len(items), 36):
        for c in range(2, 7):
            put(ws, r, c, None, DATE if c == 5 else None)
    validate(ws, "D6:D35", '"Yes,No"')
    sections = ["Unit 1: Foundations", "Unit 2: Algorithms", "Unit 3: Data", "Unit 4: Project"]
    for i, sec in enumerate(sections):
        r = 6 + i
        put(ws, r, 8, sec)
        put(ws, r, 9, f"=COUNTIF($B$6:$B$35,H{r})", "0", "calc")
        put(ws, r, 10, f'=COUNTIFS($B$6:$B$35,H{r},$D$6:$D$35,"Yes")', "0", "calc")
        put(ws, r, 11, f'=IFERROR(J{r}/I{r},"")', "0%", "calc")
    put(ws, 10, 8, "Overall", kind="total")
    put(ws, 10, 9, "=SUM(I6:I9)", "0", "total")
    put(ws, 10, 10, "=SUM(J6:J9)", "0", "total")
    put(ws, 10, 11, '=IFERROR(J10/I10,"")', "0%", "summary")
    wb.save(path)
