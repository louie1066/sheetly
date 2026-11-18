"""Health, Fitness & Wellbeing templates 17-25: recipe nutrition, baby log, childcare, symptom diary, stretching, sports stats, check-ups, gym cost, screen time."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda m, d: dt.date(2026, m, d)
T = lambda h, m: dt.time(h, m)
REPORT = dt.date(2026, 12, 1)


def recipe_nutrition(path):
    build_log(path, "Recipe", "Recipe Nutrition Calculator", "Enter each ingredient's grams and its values per 100 g from a trusted source. Totals and per-serving values calculate automatically",
              [("Ingredient", 22, "input", None), ("Grams used", 11, "input", "0"),
               ("kcal per 100 g", 12, "input", "0"), ("Protein per 100 g (g)", 13, "input", "0.0"),
               ("Carbs per 100 g (g)", 13, "input", "0.0"), ("Fat per 100 g (g)", 12, "input", "0.0"),
               ("Total kcal", 11, '=IF(OR(C{r}="",D{r}=""),"",C{r}*D{r}/100)', "#,##0"),
               ("Total protein (g)", 12, '=IF(OR(C{r}="",E{r}=""),"",C{r}*E{r}/100)', "0.0"),
               ("Total carbs (g)", 12, '=IF(OR(C{r}="",F{r}=""),"",C{r}*F{r}/100)', "0.0"),
               ("Total fat (g)", 11, '=IF(OR(C{r}="",G{r}=""),"",C{r}*G{r}/100)', "0.0")],
              [("Rolled oats", 320, 370, 13, 59, 7), ("Milk, semi-skimmed", 500, 46, 3.4, 4.8, 1.7),
               ("Banana", 200, 89, 1.1, 23, 0.3), ("Peanut butter", 40, 588, 25, 20, 50)],
              nrows=15, totals=[6, 7, 8, 9],
              inputs=[("Number of servings", 4, "0")],
              summary=[("Energy per serving (kcal)", '=IFERROR(SUM(H{R0}:H{R1})/{IN0},"")', "#,##0"),
                       ("Protein per serving (g)", '=IFERROR(SUM(I{R0}:I{R1})/{IN0},"")', "0.0"),
                       ("Carbohydrate per serving (g)", '=IFERROR(SUM(J{R0}:J{R1})/{IN0},"")', "0.0"),
                       ("Fat per serving (g)", '=IFERROR(SUM(K{R0}:K{R1})/{IN0},"")', "0.0")],
              note_text="Values are estimates. Take per-100 g figures from the packet or a food database you trust.")


def baby_log(path):
    build_log(path, "Log", "Baby Feeding and Nappy Log", "Record each feed and nappy with its time. Daily totals calculate in the summary",
              [("Date", 12, "input", DATE), ("Time", 9, "input", "hh:mm"),
               ("Event", 16, "input", None), ("Amount (ml)", 12, "input", "0"),
               ("Duration (min)", 13, "input", "0"), ("Notes", 26, "input", None)],
              [(D(11, 23), T(6, 40), "Feed", 90, 15, None), (D(11, 23), T(7, 30), "Wet nappy", None, None, None),
               (D(11, 23), T(9, 10), "Feed", 110, 20, None), (D(11, 23), T(10, 0), "Wet and dirty", None, None, None),
               (D(11, 23), T(12, 15), "Feed", 100, 18, "Settled quickly")],
              nrows=60, totals=[3, 4],
              validations=[("D{R0}:D{R1}", '"Feed,Wet nappy,Dirty nappy,Wet and dirty"')],
              summary=[("Feeds logged", '=COUNTIF(D{R0}:D{R1},"Feed")', "0"),
                       ("Wet nappies", '=COUNTIF(D{R0}:D{R1},"Wet nappy")+COUNTIF(D{R0}:D{R1},"Wet and dirty")', "0"),
                       ("Dirty nappies", '=COUNTIF(D{R0}:D{R1},"Dirty nappy")+COUNTIF(D{R0}:D{R1},"Wet and dirty")', "0"),
                       ("Total milk logged (ml)", "=SUM(E{R0}:E{R1})", "#,##0")],
              note_text="A personal record for your own use. Raise any feeding or nappy concerns with your health visitor or doctor.")


def childcare_schedule(path):
    build_log(path, "Week", "Childcare Schedule", "Plan who looks after the children on each day and when. Hours booked calculate for each slot",
              [("Day", 12, "input", None), ("Start", 9, "input", "hh:mm"), ("End", 9, "input", "hh:mm"),
               ("Hours", 9, '=IF(OR(C{r}="",D{r}=""),"",MOD(D{r}-C{r},1)*24)', "0.0"),
               ("Child or children", 18, "input", None), ("Carer", 18, "input", None), ("Notes", 26, "input", None)],
              [("Monday", T(8, 0), T(15, 0), "Both children", "Grandparent", "Pick-up 3:15 pm"),
               ("Tuesday", T(8, 0), T(12, 30), "Youngest", "Childminder", None),
               ("Wednesday", T(9, 0), T(17, 0), "Both children", "Childminder", None)],
              nrows=21, totals=[3],
              validations=[("B{R0}:B{R1}", '"Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"')],
              summary=[("Slots planned", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Hours booked", "=SUM(E{R0}:E{R1})", "0.0")],
              note_text="Check local childcare rules and carer-to-child ratios before you set a schedule.")


def symptom_diary(path):
    build_log(path, "Diary", "Symptom Diary", "A personal record to bring to appointments. Log when a symptom started, how strong it was and what was happening",
              [("Date", 12, "input", DATE), ("Time", 9, "input", "hh:mm"), ("Symptom", 22, "input", None),
               ("Severity (0-10)", 12, "input", "0"), ("What was happening", 28, "input", None),
               ("Notes", 26, "input", None)],
              [(D(11, 21), T(14, 0), "Headache", 4, "Long screen session", "Eased after a break"),
               (D(11, 22), T(9, 30), "Headache", 6, "Poor sleep", None)],
              nrows=40,
              validations=[("E{R0}:E{R1}", ("whole", "0", "10"))],
              summary=[("Entries", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Average severity", '=IFERROR(AVERAGE(E{R0}:E{R1}),"")', "0.0")],
              note_text="This diary records what you notice. It does not diagnose. Contact your doctor about any symptom that worries you, and seek urgent help in an emergency.")


def stretching_planner(path):
    build_log(path, "Routine", "Stretching Routine Planner", "Plan each stretch with its hold time and sets. Total time per stretch and for the whole routine calculate automatically",
              [("Stretch", 24, "input", None), ("Hold (seconds)", 12, "input", "0"), ("Sets", 8, "input", "0"),
               ("Sides", 13, "input", None), ("Total time (sec)", 14, '=IF(OR(C{r}="",D{r}=""),"",C{r}*D{r}*IF(E{r}="Both sides",2,1))', "0"),
               ("Done this week?", 14, "input", None)],
              [("Hamstring stretch", 30, 2, "Both sides", "Yes"), ("Hip flexor stretch", 30, 2, "Both sides", "No"),
               ("Child's pose", 45, 2, "One side", "Yes"), ("Neck rolls", 20, 3, "One side", None)],
              nrows=12, totals=[4],
              validations=[("E{R0}:E{R1}", '"Both sides,One side"'), ("G{R0}:G{R1}", '"Yes,No"')],
              summary=[("Routine length (minutes)", "=SUM(F{R0}:F{R1})/60", "0.0"),
                       ("Stretches done this week", '=COUNTIF(G{R0}:G{R1},"Yes")', "0")],
              note_text="Hold each stretch comfortably. Stop if it causes pain, and ask a professional about any injury.")


def sports_stats(path):
    build_log(path, "Matches", "Team Sports Stats Tracker", "Record each player's match stats. Goals per 90 minutes calculate for each line",
              [("Date", 12, "input", DATE), ("Opponent", 18, "input", None), ("Player", 16, "input", None),
               ("Goals", 9, "input", "0"), ("Assists", 9, "input", "0"), ("Minutes played", 12, "input", "0"),
               ("Goals per 90 min", 14, '=IF(OR(D{r}="",N(G{r})=0),"",E{r}/G{r}*90)', "0.00")],
              [(D(11, 14), "Riverside FC", "Ana", 1, 0, 90), (D(11, 14), "Riverside FC", "Ben", 0, 1, 70),
               (D(11, 21), "Hill Town", "Ana", 2, 0, 85), (D(11, 21), "Hill Town", "Chloe", 0, 0, 20)],
              nrows=30, totals=[3, 4, 5],
              summary=[("Match lines", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Total goals", "=SUM(E{R0}:E{R1})", "0"),
                       ("Total assists", "=SUM(F{R0}:F{R1})", "0")])


def health_check_reminders(path):
    build_log(path, "Check-ups", "Annual Health Check Reminders", "List each check-up, when it was last done and when it is next due. Days until due and status calculate from the report date",
              [("Check-up", 26, "input", None), ("Provider", 20, "input", None), ("Last done", 12, "input", DATE),
               ("Next due", 12, "input", DATE),
               ("Days until due", 13, '=IF(E{r}="","",E{r}-{RD})', "0"),
               ("Status", 14, '=IF(F{r}="","",IF(F{r}<0,"Overdue",IF(F{r}<=30,"Due soon","OK")))', None)],
              [("Dental check-up", "Dental practice", D(6, 10), D(12, 10)),
               ("Eye test", "Optician", D(1, 15), D(1, 15)),
               ("Blood pressure review", "GP surgery", D(9, 2), D(12, 2)),
               ("Cholesterol test", "GP surgery", D(3, 3), D(3, 3))],
              nrows=20, report=("Report date", REPORT),
              summary=[("Check-ups listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Overdue", '=COUNTIF(G{R0}:G{R1},"Overdue")', "0"),
                       ("Due within 30 days", '=COUNTIF(G{R0}:G{R1},"Due soon")', "0")],
              note_text="Dates for check-ups are set by your provider. Confirm them with the surgery or clinic.")


def gym_cost(path):
    build_log(path, "Costs", "Gym Membership Cost Tracker", "Record each month's fees and visits. Total spend and cost per visit calculate automatically",
              [("Month", 12, "input", DATE), ("Membership fee", 14, "input", MONEY), ("Classes and extras", 16, "input", MONEY),
               ("Visits", 9, "input", "0"),
               ("Total spend", 14, '=IF(B{r}="","",N(C{r})+N(D{r}))', MONEY),
               ("Cost per visit", 14, '=IF(OR(B{r}="",N(E{r})=0),"",F{r}/E{r})', MONEY)],
              [(D(9, 1), 32.0, 8.0, 10), (D(10, 1), 32.0, 0, 6), (D(11, 1), 32.0, 12.0, 9)],
              nrows=24, totals=[1, 2, 3, 4],
              summary=[("Total spend", "=SUM(F{R0}:F{R1})", MONEY),
                       ("Average cost per visit", '=IFERROR(SUM(F{R0}:F{R1})/SUM(E{R0}:E{R1}),"")', MONEY)])


def screen_time(path):
    build_log(path, "Log", "Screen Time Log", "Log screen time by device or app and what it was used for. Hours calculate for each entry",
              [("Date", 12, "input", DATE), ("Device or app", 22, "input", None), ("Minutes", 10, "input", "0"),
               ("Category", 16, "input", None), ("Hours", 10, '=IF(D{r}="","",D{r}/60)', "0.00")],
              [(D(11, 23), "Phone: messaging", 45, "Social"), (D(11, 23), "Laptop: homework", 90, "Study"),
               (D(11, 24), "Tablet: video", 60, "Entertainment"), (D(11, 24), "Laptop: email", 35, "Work")],
              nrows=40, totals=[2, 4],
              validations=[("E{R0}:E{R1}", '"Work,Study,Social,Entertainment,Other"')],
              summary=[("Total hours", "=SUM(F{R0}:F{R1})", "0.0"),
                       ("Average minutes per entry", '=IFERROR(AVERAGE(D{R0}:D{R1}),"")', "0")])
