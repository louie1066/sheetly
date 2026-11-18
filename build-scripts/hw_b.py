"""Health, Fitness & Wellbeing templates 9-16: reflection, medicine schedule, blood pressure, blood glucose, steps, body measurements, strength, cycling."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda m, d: dt.date(2026, m, d)
T = lambda h, m: dt.time(h, m)
REPORT = dt.date(2026, 12, 1)


def daily_reflection(path):
    build_log(path, "Journal", "Daily Reflection Journal", "A private record of each day. Nothing is calculated, so write as much or as little as you like",
              [("Date", 12, "input", DATE), ("Highlight of the day", 32, "input", None),
               ("Challenge", 32, "input", None), ("Something I am grateful for", 32, "input", None),
               ("Focus for tomorrow", 32, "input", None)],
              [(D(11, 23), "Finished the project plan", "Ran out of time for lunch", "A quiet walk home", "Book the room"),
               (D(11, 24), "Good conversation with a friend", "Tired after a long day", "Warm dinner", "Rest early")],
              nrows=31, summary=[("Entries", "=COUNTA(B{R0}:B{R1})", "0")],
              note_text="Keep this file on your own device or cloud drive. Share it only if you choose to.")


def medication_schedule(path):
    build_log(path, "Schedule", "Medication Reminder Schedule", "List each medicine, when it is taken and when to reorder. Days to refill calculate from the report date",
              [("Medicine", 22, "input", None), ("Dose (as written on label)", 22, "input", None),
               ("Time of day", 12, "input", "hh:mm"), ("Frequency", 15, "input", None),
               ("Start date", 12, "input", DATE), ("Refill due", 12, "input", DATE),
               ("Days to refill", 13, '=IF(OR(B{r}="",G{r}=""),"",G{r}-{RD})', "0")],
              [("Example medicine 1", "1 tablet", T(8, 0), "Once daily", D(10, 1), D(12, 15)),
               ("Example medicine 2", "5 ml", T(20, 0), "Twice daily", D(11, 1), D(12, 3))],
              nrows=12, report=("Report date", REPORT),
              validations=[("E{R0}:E{R1}", '"Once daily,Twice daily,Three times daily,Weekly,As needed,Other"')],
              summary=[("Medicines listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Refills due within 14 days", '=COUNTIFS(H{R0}:H{R1},"<=14",H{R0}:H{R1},">=0")', "0")],
              note_text="Follow the label or your prescriber's instructions. This sheet records times and reminders only and gives no dosing advice.")


def _bp_rows():
    return [(D(11, 23), T(8, 15), 128, 82, 66, "Before breakfast"), (D(11, 23), T(20, 0), 124, 80, 70, None),
            (D(11, 24), T(8, 10), 131, 84, 68, None), (D(11, 25), T(8, 5), 126, 79, 64, "Rested 10 min first")]


def blood_pressure(path):
    build_log(path, "Readings", "Blood Pressure Log", "Record each reading. Enter the upper limits your doctor gave you and each reading is checked against them",
              [("Date", 12, "input", DATE), ("Time", 9, "input", "hh:mm"), ("Systolic (mmHg)", 13, "input", "0"),
               ("Diastolic (mmHg)", 13, "input", "0"), ("Pulse (bpm)", 11, "input", "0"), ("Notes", 24, "input", None),
               ("Against your limits", 20, '=IF(OR(D{r}="",E{r}=""),"",IF(OR({IN0}="",{IN1}=""),"Enter your limits",'
                                           'IF(OR(D{r}>{IN0},E{r}>{IN1}),"Above your limit","Within your limit")))', None)],
              _bp_rows(), nrows=30,
              inputs=[("Your upper limit: systolic (mmHg)", None, "0"), ("Your upper limit: diastolic (mmHg)", None, "0")],
              summary=[("Readings logged", "=COUNT(D{R0}:D{R1})", "0"),
                       ("Average systolic (mmHg)", "=IFERROR(AVERAGE(D{R0}:D{R1}),\"\")", "0"),
                       ("Average diastolic (mmHg)", "=IFERROR(AVERAGE(E{R0}:E{R1}),\"\")", "0"),
                       ("Readings above your limit", '=COUNTIF(H{R0}:H{R1},"Above*")', "0")],
              note_text="This sheet does not set limits. Use the limits your doctor or nurse gives you, and bring the log to appointments.")


def _glucose_rows():
    return [(D(11, 23), T(7, 30), 5.4, "Fasting", None), (D(11, 23), T(13, 0), 7.1, "After meal", None),
            (D(11, 24), T(7, 25), 5.6, "Fasting", None), (D(11, 24), T(18, 30), 6.2, "Before meal", "Felt fine")]


def blood_glucose(path):
    build_log(path, "Readings", "Blood Glucose Log", "Record each reading in the units your meter shows. Enter the range your clinician gave you and each reading is checked",
              [("Date", 12, "input", DATE), ("Time", 9, "input", "hh:mm"), ("Reading", 11, "input", "0.0"),
               ("Context", 14, "input", None), ("Notes", 24, "input", None),
               ("Against your range", 20, '=IF(D{r}="","",IF(OR({IN0}="",{IN1}=""),"Enter your range",'
                                         'IF(D{r}<{IN0},"Below your range",IF(D{r}>{IN1},"Above your range","Within your range"))))', None)],
              _glucose_rows(), nrows=30,
              validations=[("E{R0}:E{R1}", '"Fasting,Before meal,After meal,Bedtime,Other"')],
              inputs=[("Your lower limit of range", None, "0.0"), ("Your upper limit of range", None, "0.0")],
              summary=[("Readings logged", "=COUNT(D{R0}:D{R1})", "0"),
                       ("Average reading", "=IFERROR(AVERAGE(D{R0}:D{R1}),\"\")", "0.0"),
                       ("Readings outside your range", '=COUNTIF(G{R0}:G{R1},"Below*")+COUNTIF(G{R0}:G{R1},"Above*")', "0")],
              note_text="Limits are not set by this template. Use the range your clinician gives you.")


def step_count(path):
    build_log(path, "Steps", "Step Count Tracker", "Log your steps each day. Enter your own goal above the table and the goal check updates automatically",
              [("Date", 12, "input", DATE), ("Steps", 12, "input", "#,##0"),
               ("Goal met?", 12, '=IF(C{r}="","",IF({IN0}="","Set goal",IF(C{r}>={IN0},"Yes","No")))', None)],
              [(D(11, 23), 6400), (D(11, 24), 9120), (D(11, 25), 4850), (D(11, 26), 10230), (D(11, 27), 7700)],
              nrows=31, totals=[1],
              inputs=[("Your daily step goal", 8000, "#,##0")],
              summary=[("Days logged", "=COUNT(C{R0}:C{R1})", "0"),
                       ("Average steps per logged day", "=IFERROR(AVERAGE(C{R0}:C{R1}),\"\")", "#,##0"),
                       ("Days goal met", '=COUNTIF(D{R0}:D{R1},"Yes")', "0")])


def body_measurements(path):
    build_log(path, "Measurements", "Body Measurement Tracker", "Measure at the same points each time with a soft tape. Waist change since the first entry calculates automatically",
              [("Date", 12, "input", DATE), ("Chest (cm)", 11, "input", "0.0"), ("Waist (cm)", 11, "input", "0.0"),
               ("Hips (cm)", 11, "input", "0.0"), ("Upper arm (cm)", 13, "input", "0.0"), ("Thigh (cm)", 11, "input", "0.0"),
               ("Waist change since first (cm)", 18, '=IF(OR(D{r}="",$D$6=""),"",D{r}-$D$6)', "+0.0;-0.0;0.0")],
              [(D(11, 2), 96.0, 84.5, 98.0, 31.0, 56.0), (D(11, 30), 95.5, 83.0, 97.5, 31.5, 55.5)],
              nrows=24,
              summary=[("Entries", "=COUNT(D{R0}:D{R1})", "0"),
                       ("Lowest waist (cm)", '=IF(COUNT(D{R0}:D{R1})=0,"",MIN(D{R0}:D{R1}))', "0.0"),
                       ("Highest waist (cm)", '=IF(COUNT(D{R0}:D{R1})=0,"",MAX(D{R0}:D{R1}))', "0.0")],
              note_text="Measure in the same place, at the same time of day, relaxed and not holding your breath.")


def strength_progression(path):
    build_log(path, "Lifts", "Strength Progression Chart", "Log each lift. Estimated one-rep max and your best so far for each exercise calculate automatically",
              [("Exercise", 22, "input", None), ("Date", 12, "input", DATE), ("Weight (kg)", 12, "input", "0.0"),
               ("Reps", 9, "input", "0"),
               ("Estimated 1RM (kg)", 14, '=IF(OR(D{r}="",E{r}=""),"",D{r}*(1+E{r}/30))', "0.0"),
               ("Best so far (kg)", 14, '=IF(OR(B{r}="",F{r}=""),"",_xlfn.MAXIFS($F${R0}:$F${R1},$B${R0}:$B${R1},B{r}))', "0.0")],
              [("Squat", D(11, 2), 60, 8), ("Squat", D(11, 16), 62.5, 6), ("Squat", D(11, 30), 65, 5),
               ("Bench press", D(11, 4), 40, 8), ("Bench press", D(11, 18), 42.5, 6)],
              nrows=40, summary=[("Entries", "=COUNTA(B{R0}:B{R1})", "0"),
                                 ("Best estimated 1RM (kg)", "=IF(COUNT(F{R0}:F{R1})=0,\"\",MAX(F{R0}:F{R1}))", "0.0")],
              note_text="Estimated one-rep max uses weight x (1 + reps / 30). It is an estimate, not a test. Work within your own ability and get coaching for new lifts.")


def cycling_log(path):
    build_log(path, "Rides", "Cycling Log", "Log each ride. Average speed calculates from distance and moving time",
              [("Date", 12, "input", DATE), ("Distance (km)", 12, "input", "0.0"), ("Moving time (min)", 13, "input", "0"),
               ("Average speed (km/h)", 14, '=IF(OR(C{r}="",N(D{r})=0),"",C{r}/(D{r}/60))', "0.0"),
               ("Elevation gain (m)", 13, "input", "0"), ("Notes", 26, "input", None)],
              [(D(11, 22), 18.4, 58, 120, "Flat route"), (D(11, 26), 32.0, 118, 410, "Hills near the reservoir"),
               (D(11, 29), 9.5, 35, 40, None)],
              nrows=30, totals=[1, 2, 4],
              summary=[("Rides logged", "=COUNT(C{R0}:C{R1})", "0"),
                       ("Total time (hours)", "=SUM(D{R0}:D{R1})/60", "0.0"),
                       ("Average speed overall (km/h)", '=IFERROR(SUM(C{R0}:C{R1})/(SUM(D{R0}:D{R1})/60),"")', "0.0")])
