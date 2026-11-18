"""Home & Household templates 1-8: chores, maintenance, inventory, pantry, meal shopping, cleaning, garden, energy."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda m, d: dt.date(2026, m, d)
Y = lambda m, d: dt.date(2027, m, d)
REPORT = dt.date(2026, 12, 1)


def chore_rota(path):
    build_log(path, "Rota", "Chore Rota", "Assign each chore to a person and day. Minutes total up, and the done column shows progress",
              [("Chore", 26, "input", None), ("Person", 14, "input", None), ("Day", 12, "input", None),
               ("Frequency", 14, "input", None), ("Minutes", 10, "input", "0"), ("Done this week?", 14, "input", None)],
              [("Vacuum living room", "Ana", "Monday", "Weekly", 30, "Yes"), ("Clean bathroom", "Ben", "Wednesday", "Weekly", 40, "No"),
               ("Empty bins", "Chloe", "Tuesday", "Weekly", 5, "Yes"), ("Wash up after dinner", "Ben", "Daily", "Daily", 15, "Yes"),
               ("Change bed linen", "Ana", "Saturday", "Fortnightly", 25, None)],
              nrows=30, totals=[4],
              validations=[("D{R0}:D{R1}", '"Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday,Daily"'),
                           ("E{R0}:E{R1}", '"Daily,Weekly,Fortnightly,Monthly"'),
                           ("G{R0}:G{R1}", '"Yes,No"')],
              summary=[("Chores listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Done this week", '=COUNTIF(G{R0}:G{R1},"Yes")', "0")])


def maintenance_schedule(path):
    build_log(path, "Schedule", "Home Maintenance Schedule", "Record when each job was last done and how often it repeats. Next due and status calculate from the report date",
              [("Task", 30, "input", None), ("Area", 14, "input", None), ("Last done", 12, "input", DATE),
               ("Repeat every (months)", 13, "input", "0"),
               ("Next due", 12, '=IF(OR(D{r}="",E{r}=""),"",EDATE(D{r},E{r}))', DATE),
               ("Days left", 10, '=IF(F{r}="","",F{r}-{RD})', "0"),
               ("Status", 13, '=IF(G{r}="","",IF(G{r}<0,"Overdue",IF(G{r}<=30,"Due soon","OK")))', None)],
              [("Clean gutters", "Roof", D(9, 10), 6), ("Service boiler", "Heating", D(10, 20), 12),
               ("Test smoke alarms", "Whole house", D(11, 1), 3), ("Check fire extinguisher", "Kitchen", D(3, 5), 12)],
              nrows=20, report=("Report date", REPORT),
              summary=[("Tasks listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Overdue", '=COUNTIF(H{R0}:H{R1},"Overdue")', "0"),
                       ("Due within 30 days", '=COUNTIF(H{R0}:H{R1},"Due soon")', "0")])


def inventory_for_insurance(path):
    build_log(path, "Inventory", "Household Inventory for Insurance", "List valuable items with their replacement value and whether you have a receipt or photo. Totals calculate automatically",
              [("Item", 24, "input", None), ("Room", 14, "input", None), ("Category", 14, "input", None),
               ("Quantity", 9, "input", "0"), ("Purchase date", 12, "input", DATE), ("Price paid each", 13, "input", MONEY),
               ("Replacement value each", 15, "input", MONEY),
               ("Total replacement value", 16, '=IF(OR(E{r}="",H{r}=""),"",E{r}*H{r})', MONEY),
               ("Receipt or photo kept?", 14, "input", None)],
              [("Laptop", "Study", "Electronics", 1, D(3, 14), 900, 750, "Yes"),
               ("Dining table", "Kitchen", "Furniture", 1, D(7, 2), 350, 420, "Photo only"),
               ("Bicycle", "Hall", "Other", 1, D(5, 20), 480, 520, "No"),
               ("Sofa", "Living room", "Furniture", 1, D(1, 9), 800, 900, "Yes")],
              nrows=30, totals=[7],
              validations=[("D{R0}:D{R1}", '"Furniture,Electronics,Appliance,Clothing,Jewellery,Other"'),
                           ("J{R0}:J{R1}", '"Yes,No,Photo only"')],
              summary=[("Items listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total replacement value", "=SUM(I{R0}:I{R1})", MONEY),
                       ("Items with no receipt or photo", '=COUNTIF(J{R0}:J{R1},"No")', "0")],
              note_text="Keep a copy of this file and your photos somewhere safe, away from the home. Check your policy for what it covers.")


def pantry_inventory(path):
    build_log(path, "Pantry", "Pantry Inventory", "Track what you have, where it is kept and when it needs using or reordering. Status and days to use-by calculate automatically",
              [("Item", 24, "input", None), ("Category", 16, "input", None), ("Location", 14, "input", None),
               ("Quantity", 10, "input", "0.0"), ("Unit", 10, "input", None), ("Use by", 12, "input", DATE),
               ("Reorder at", 11, "input", "0.0"),
               ("Status", 12, '=IF(OR(E{r}="",H{r}=""),"",IF(E{r}<=H{r},"Reorder","OK"))', None),
               ("Days to use-by", 14, '=IF(G{r}="","",G{r}-{RD})', "0")],
              [("Plain flour", "Dry goods", "Cupboard", 1.5, "kg", Y(2, 14), 1.0),
               ("Chopped tomatoes", "Tins", "Cupboard", 2, "tins", Y(6, 1), 3),
               ("Frozen peas", "Frozen", "Freezer", 1, "bag", None, 1),
               ("Semi-skimmed milk", "Dairy", "Fridge", 2, "pints", D(12, 4), 2)],
              nrows=40, report=("Report date", REPORT),
              summary=[("Items listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("To reorder", '=COUNTIF(I{R0}:I{R1},"Reorder")', "0"),
                       ("Use by within 7 days", '=COUNTIFS(J{R0}:J{R1},"<=7",J{R0}:J{R1},">=0")', "0")])


def meal_plan_shopping(path):
    build_log(path, "Shopping", "Meal Plan and Shopping List", "List the ingredients for each planned meal, then tick them off as you shop",
              [("Day", 12, "input", None), ("Meal", 18, "input", None), ("Ingredient", 24, "input", None),
               ("Quantity", 14, "input", None), ("Aisle or section", 16, "input", None), ("Got it?", 10, "input", None)],
              [("Monday", "Pasta bolognese", "Minced beef", "500 g", "Meat and fish", "Yes"),
               ("Monday", "Pasta bolognese", "Spaghetti", "400 g", "Tins and dry", "No"),
               ("Tuesday", "Vegetable curry", "Chopped tomatoes", "2 tins", "Tins and dry", "Yes"),
               ("Tuesday", "Vegetable curry", "Spinach", "200 g", "Produce", "No"),
               ("Wednesday", "Omelette and salad", "Eggs", "6", "Dairy", None)],
              nrows=40,
              validations=[("F{R0}:F{R1}", '"Produce,Bakery,Dairy,Meat and fish,Tins and dry,Frozen,Household,Other"'),
                           ("G{R0}:G{R1}", '"Yes,No"')],
              summary=[("Items on list", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Still to buy", '=COUNTA(D{R0}:D{R1})-COUNTIF(G{R0}:G{R1},"Yes")', "0")])


def cleaning_schedule(path):
    build_log(path, "Cleaning", "Cleaning Schedule", "Record when each cleaning task was last done. Next due and status calculate from the report date",
              [("Area", 16, "input", None), ("Task", 30, "input", None), ("Frequency", 14, "input", None),
               ("Last done", 12, "input", DATE),
               ("Next due", 12, '=IF(OR(D{r}="",E{r}=""),"",E{r}+IF(D{r}="Daily",1,IF(D{r}="Weekly",7,IF(D{r}="Fortnightly",14,IF(D{r}="Monthly",30,0)))))', DATE),
               ("Days left", 10, '=IF(F{r}="","",F{r}-{RD})', "0"),
               ("Status", 13, '=IF(G{r}="","",IF(G{r}<0,"Overdue",IF(G{r}<=2,"Due soon","OK")))', None)],
              [("Kitchen", "Clean oven", "Monthly", D(11, 5)), ("Kitchen", "Wipe worktops", "Daily", D(11, 30)),
               ("Bathroom", "Scrub shower", "Weekly", D(11, 22)), ("Living room", "Dust shelves", "Weekly", D(11, 29)),
               ("Bedrooms", "Wash bedding", "Fortnightly", D(11, 16))],
              nrows=25, report=("Report date", REPORT),
              validations=[("D{R0}:D{R1}", '"Daily,Weekly,Fortnightly,Monthly"')],
              summary=[("Tasks listed", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Overdue", '=COUNTIF(H{R0}:H{R1},"Overdue")', "0"),
                       ("Due within 2 days", '=COUNTIF(H{R0}:H{R1},"Due soon")', "0")])


def garden_planner(path):
    build_log(path, "Planting", "Garden Planting Planner", "Enter the sowing and harvest windows for each crop. The stage and plants per row calculate from the report date",
              [("Crop", 18, "input", None), ("Sow from", 12, "input", DATE), ("Sow to", 12, "input", DATE),
               ("Harvest from", 12, "input", DATE), ("Harvest to", 12, "input", DATE),
               ("Spacing (cm)", 11, "input", "0"), ("Row length (m)", 12, "input", "0.0"),
               ("Plants per row", 12, '=IF(OR(G{r}="",H{r}=""),"",INT(H{r}*100/G{r}))', "0"),
               ("Stage on report date", 20,
                '=IF(C{r}="","",IF({RD}<C{r},"Not yet",IF({RD}<=D{r},"Sowing window",IF({RD}<E{r},"Growing",IF({RD}<=F{r},"Harvesting","Finished")))))', None)],
              [("Garlic", D(10, 1), D(12, 15), Y(6, 1), Y(7, 15), 15, 3),
               ("Carrots", Y(3, 1), Y(5, 31), Y(6, 15), Y(8, 31), 5, 2),
               ("Runner beans", Y(4, 15), Y(6, 1), Y(7, 1), Y(9, 30), 20, 3)],
              nrows=20, report=("Report date", REPORT),
              summary=[("Crops planned", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("In sowing window", '=COUNTIF(J{R0}:J{R1},"Sowing window")', "0"),
                       ("Being harvested", '=COUNTIF(J{R0}:J{R1},"Harvesting")', "0")],
              note_text="Sowing and harvest windows vary by region and season. Use dates from a local gardening guide.")


def energy_tracker(path):
    build_log(path, "Meter readings", "Home Energy Usage Tracker", "Record meter readings each week or month. Use since the last reading calculates automatically; add your tariff rates to see costs",
              [("Date", 12, "input", DATE), ("Electricity meter", 14, "input", "#,##0"),
               ("Electricity used", 14, '=IF(OR(C{r}="",N(C{p})=0),"",C{r}-C{p})', "#,##0"),
               ("Gas meter", 12, "input", "#,##0"),
               ("Gas used", 12, '=IF(OR(E{r}="",N(E{p})=0),"",E{r}-E{p})', "#,##0"),
               ("Notes", 26, "input", None)],
              [(D(10, 1), 12480, 40210, None), (D(10, 15), 12660, 40455, None),
               (D(11, 1), 12940, 40640, None), (D(11, 15), 13230, 40871, "Heating on more")],
              nrows=26,
              inputs=[("Electricity price per unit (your tariff)", None, "0.000"), ("Gas price per unit (your tariff)", None, "0.000")],
              summary=[("Electricity used (units)", "=SUM(D{R0}:D{R1})", "#,##0"),
                       ("Gas used (units)", "=SUM(F{R0}:F{R1})", "#,##0"),
                       ("Electricity cost", '=IF({IN0}="","Enter your price above",SUM(D{R0}:D{R1})*{IN0})', "#,##0.00"),
                       ("Gas cost", '=IF({IN1}="","Enter your price above",SUM(F{R0}:F{R1})*{IN1})', "#,##0.00")],
              note_text="Enter readings in the units on your bill. Each row needs the reading before it to calculate the use.")
