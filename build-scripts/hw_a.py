"""Health, Fitness & Wellbeing templates 1-8: workouts, running plan, weight, calories, meals, water, sleep, habits."""
import datetime as dt
from openpyxl import Workbook
from common import *
from tplkit import build_log

D = lambda m, d: dt.date(2026, m, d)
T = lambda h, m: dt.time(h, m)


def workout_log(path):
    build_log(path, "Workouts", "Workout Log", "Record each exercise, sets, reps and weight. Volume calculates for each line",
              [("Date", 12, "input", DATE), ("Exercise", 24, "input", None), ("Sets", 8, "input", "0"),
               ("Reps", 8, "input", "0"), ("Weight (kg)", 12, "input", "0.0"),
               ("Volume (kg)", 13, '=IF(OR(C{r}="",D{r}="",E{r}=""),"",D{r}*E{r}*N(F{r}))', "#,##0")],
              [(D(11, 23), "Back squat", 4, 8, 60), (D(11, 23), "Push-up", 3, 12, 0),
               (D(11, 25), "Romanian deadlift", 3, 10, 40), (D(11, 25), "Row", 3, 10, 30),
               (D(11, 27), "Back squat", 4, 6, 65)],
              nrows=20, totals=[5],
              summary=[("Entries logged", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Total volume (kg)", "=SUM(G{R0}:G{R1})", "#,##0")])


def running_plan(path):
    build_log(path, "Plan", "Running Training Plan", "Plan each week's runs, then log what you actually ran. Differences calculate automatically",
              [("Week", 8, "input", "0"), ("Week starting", 13, "input", DATE), ("Session", 14, "input", None),
               ("Planned (km)", 12, "input", "0.0"), ("Actual (km)", 12, "input", "0.0"),
               ("Time (min)", 11, "input", "0"),
               ("Difference (km)", 13, '=IF(OR(E{r}="",F{r}=""),"",F{r}-E{r})', "+0.0;-0.0;0.0")],
              [(1, D(12, 7), "Easy run", 4, 4.1, 32), (1, D(12, 7), "Intervals", 5, 5, 35),
               (2, D(12, 14), "Easy run", 5, 5.2, 34), (2, D(12, 14), "Long run", 8, 7, 52),
               (3, D(12, 21), "Tempo run", 6, 6, 36)],
              nrows=16, totals=[3, 4, 5],
              validations=[("D{R0}:D{R1}", '"Easy run,Intervals,Tempo run,Long run,Rest,Cross-training"')],
              summary=[("Planned distance (km)", "=SUM(E{R0}:E{R1})", "0.0"),
                       ("Actual distance (km)", "=SUM(F{R0}:F{R1})", "0.0"),
                       ("Distance completed", '=IFERROR(SUM(F{R0}:F{R1})/SUM(E{R0}:E{R1}),0)', "0%")])


def weight_tracker(path):
    build_log(path, "Weight", "Weight Tracker", "Log your weight over time. Change since the first entry calculates automatically",
              [("Date", 12, "input", DATE), ("Weight (kg)", 13, "input", "0.0"),
               ("Change since first entry (kg)", 18, '=IF(OR(C{r}="",$C$6=""),"",C{r}-$C$6)', "+0.0;-0.0;0.0"),
               ("Notes", 30, "input", None)],
              [(D(11, 2), 78.4, None), (D(11, 9), 78.0, None), (D(11, 16), 77.6, "Weighed after breakfast"),
               (D(11, 23), 77.9, None), (D(11, 30), 77.2, None)],
              nrows=30,
              summary=[("Entries", "=COUNT(C{R0}:C{R1})", "0"),
                       ("Lowest recorded (kg)", "=IF(COUNT(C{R0}:C{R1})=0,\"\",MIN(C{R0}:C{R1}))", "0.0"),
                       ("Highest recorded (kg)", "=IF(COUNT(C{R0}:C{R1})=0,\"\",MAX(C{R0}:C{R1}))", "0.0"),
                       ("Average (kg)", "=IFERROR(AVERAGE(C{R0}:C{R1}),\"\")", "0.0")],
              note_text="Use the same scale, time of day and clothing each time for comparable readings.")


def calorie_macro(path):
    build_log(path, "Food log", "Calorie and Macro Tracker", "Log each food with its energy and macronutrients. Totals calculate for each day you enter",
              [("Date", 12, "input", DATE), ("Meal", 13, "input", None), ("Food or drink", 26, "input", None),
               ("Energy (kcal)", 13, "input", "0"), ("Protein (g)", 12, "input", "0.0"),
               ("Carbohydrate (g)", 14, "input", "0.0"), ("Fat (g)", 11, "input", "0.0")],
              [(D(11, 23), "Breakfast", "Porridge with milk", 320, 12, 52, 7),
               (D(11, 23), "Lunch", "Chicken wrap", 480, 28, 45, 16),
               (D(11, 23), "Snack", "Apple", 80, 0.4, 21, 0.2),
               (D(11, 23), "Dinner", "Lentil soup and bread", 410, 18, 62, 9)],
              nrows=30, totals=[3, 4, 5, 6],
              validations=[("C{R0}:C{R1}", '"Breakfast,Lunch,Dinner,Snack"')],
              summary=[("Energy logged (kcal)", "=SUM(E{R0}:E{R1})", "#,##0"),
                       ("Protein logged (g)", "=SUM(F{R0}:F{R1})", "0.0"),
                       ("Carbohydrate logged (g)", "=SUM(G{R0}:G{R1})", "0.0"),
                       ("Fat logged (g)", "=SUM(H{R0}:H{R1})", "0.0")],
              note_text="This sheet does not set targets. Enter your own targets, or ones agreed with a dietitian or doctor, and compare them with the totals.")


def meal_planner(path):
    build_log(path, "Week", "Meal Planner", "Plan breakfast, lunch and dinner for each day, with prep time. Totals calculate at the foot of the sheet",
              [("Day", 12, "input", None), ("Breakfast", 24, "input", None), ("Lunch", 24, "input", None),
               ("Dinner", 26, "input", None), ("Snack", 16, "input", None), ("Prep time (min)", 13, "input", "0")],
              [("Monday", "Overnight oats", "Leftover soup", "Vegetable curry", "Fruit", 35),
               ("Tuesday", "Eggs on toast", "Chicken wrap", "Pasta bolognese", "Yoghurt", 40),
               ("Wednesday", "Overnight oats", "Chickpea salad", "Fish and potatoes", "Nuts", 30),
               ("Thursday", "Yoghurt and granola", "Leftover pasta", "Bean chilli", "Fruit", 25)],
              nrows=7, totals=[5],
              validations=[("B{R0}:B{R1}", '"Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday"')],
              summary=[("Days planned", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total prep time (hours)", "=SUM(G{R0}:G{R1})/60", "0.0")],
              note_text="Use the Shopping list in the Home & Household category to turn the week into a shopping list.")


def water_intake(path):
    build_log(path, "Water", "Water Intake Tracker", "Log cups of water each day. Each cup is 250 ml and millilitres calculate automatically",
              [("Date", 12, "input", DATE), ("Cups (250 ml)", 13, "input", "0"),
               ("Water (ml)", 13, '=IF(C{r}="","",C{r}*250)', "#,##0")],
              [(D(11, 23), 6), (D(11, 24), 8), (D(11, 25), 5), (D(11, 26), 7), (D(11, 27), 9)],
              nrows=31, totals=[1, 2],
              summary=[("Days logged", "=COUNT(C{R0}:C{R1})", "0"),
                       ("Total (litres)", "=SUM(D{R0}:D{R1})/1000", "0.0"),
                       ("Average per logged day (ml)", "=IFERROR(AVERAGE(D{R0}:D{R1}),\"\")", "#,##0")],
              note_text="Enter your own daily amount. This sheet does not set a target.")


def sleep_log(path):
    build_log(path, "Sleep", "Sleep Log", "Record bedtime, wake time and how rested you felt. Hours slept calculate automatically",
              [("Date", 12, "input", DATE), ("Bedtime", 11, "input", "hh:mm"), ("Wake time", 11, "input", "hh:mm"),
               ("Hours slept", 12, '=IF(OR(C{r}="",D{r}=""),"",MOD(D{r}-C{r},1)*24)', "0.0"),
               ("Rested (1-5)", 12, "input", "0"), ("Notes", 30, "input", None)],
              [(D(11, 23), T(23, 0), T(6, 45), 4, "Woke once"), (D(11, 24), T(22, 45), T(7, 0), 5, None),
               (D(11, 25), T(23, 30), T(6, 30), 3, "Late screen use"), (D(11, 26), T(22, 30), T(6, 40), 4, None)],
              nrows=31,
              validations=[("F{R0}:F{R1}", ("whole", "1", "5"))],
              summary=[("Nights logged", "=COUNT(E{R0}:E{R1})", "0"),
                       ("Average hours slept", "=IFERROR(AVERAGE(E{R0}:E{R1}),\"\")", "0.0"),
                       ("Average rested score", "=IFERROR(AVERAGE(F{R0}:F{R1}),\"\")", "0.0")])


def habit_tracker(path):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = [("Habit", 26, "input", None), ("Target (days/week)", 12, "input", "0")]
    cols += [(d, 7, "input", None) for d in days]
    cols += [("Days done", 11, '=IF(B{r}="","",COUNTIF(D{r}:J{r},"Yes"))', "0"),
             ("% of target", 12, '=IF(OR(B{r}="",N(C{r})=0),"",MIN(1,K{r}/C{r}))', "0%")]
    rows = [("Walk 30 minutes", 5, "Yes", "Yes", None, "Yes", None, "Yes", "Yes"),
            ("Drink water with meals", 7, "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
            ("Read before bed", 4, "Yes", None, "Yes", None, "Yes", "Yes", None),
            ("Stretch after waking", 3, None, "Yes", None, "Yes", None, None, "Yes")]
    build_log(path, "Habits", "Habit Tracker", "Mark Yes on the days you did each habit. Days done and percent of target calculate automatically",
              cols, rows, nrows=12, totals=[],
              validations=[("D{R0}:J{R1}", '"Yes,No"')],
              summary=[("Habits tracked", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Average completion", "=IFERROR(AVERAGE(L{R0}:L{R1}),\"\")", "0%")])
