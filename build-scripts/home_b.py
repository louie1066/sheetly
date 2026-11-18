"""Home & Household templates 9-16: utilities, moving, renovation budget, paint, wardrobe, pets, plants, birthdays."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda m, d: dt.date(2026, m, d)
Y = lambda m, d: dt.date(2027, m, d)
REPORT = dt.date(2026, 12, 1)


def utility_comparison(path):
    build_log(path, "Compare", "Utility Bill Comparison", "Enter each tariff's standing charge and unit rate. Estimated monthly cost and ranking calculate automatically",
              [("Provider", 20, "input", None), ("Plan", 20, "input", None), ("Standing charge (per month)", 16, "input", MONEY),
               ("Unit rate (per kWh)", 13, "input", "0.000"), ("Expected use (kWh per month)", 15, "input", "#,##0"),
               ("Estimated monthly cost", 15, '=IF(OR(F{r}="",E{r}=""),"",N(D{r})+E{r}*F{r})', MONEY),
               ("Rank (1 = cheapest)", 12, '=IF(G{r}="","",RANK(G{r},$G${R0}:$G${R1},1))', "0")],
              [("Provider A", "Fixed 12 months", 8.50, 0.28, 260), ("Provider B", "Variable", 9.10, 0.25, 260),
               ("Provider C", "Green tariff", 7.20, 0.31, 260)],
              nrows=8,
              summary=[("Cheapest option", '=IFERROR(INDEX($B${R0}:$B${R1},MATCH(MIN($G${R0}:$G${R1}),$G${R0}:$G${R1},0)),"")', None),
                       ("Cheapest estimated monthly cost", '=IF(COUNT($G${R0}:$G${R1})=0,"",MIN($G${R0}:$G${R1}))', MONEY)],
              note_text="Use your own usage from the energy tracker. Check each tariff's exit fees and contract end dates as well as the price.")


def moving_checklist(path):
    build_log(path, "Checklist", "Moving Checklist", "List each task before the move with its owner, due date and status. Days left calculate from the report date",
              [("Task", 40, "input", None), ("Owner", 16, "input", None), ("Due date", 13, "input", DATE),
               ("Days left", 11, '=IF(D{r}="","",D{r}-{RD})', "0"),
               ("Status", 14, "input", None)],
              [("Book removal company", "Me", Y(1, 8), "Done"), ("Notify utilities of move date", "Partner", Y(1, 15), "In progress"),
               ("Change address with bank", "Me", Y(1, 20), "Not started"), ("Pack kitchen", "Partner", Y(2, 1), "Not started"),
               ("Clean old property", "Me", Y(2, 12), "Not started")],
              nrows=40, report=("Report date", REPORT),
              validations=[("F{R0}:F{R1}", '"Not started,In progress,Done"')],
              summary=[("Tasks listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Done", '=COUNTIF(F{R0}:F{R1},"Done")', "0"),
                       ("Overdue and not done", '=COUNTIFS(E{R0}:E{R1},"<0",F{R0}:F{R1},"<>Done")', "0")])


def renovation_budget(path):
    build_log(path, "Budget", "Home Renovation Budget", "Record the quote and actual cost for each item, by room. Differences and totals calculate automatically",
              [("Room", 16, "input", None), ("Item", 30, "input", None), ("Quote", 13, "input", MONEY),
               ("Actual cost", 13, "input", MONEY),
               ("Difference (quote - actual)", 16, '=IF(OR(D{r}="",E{r}=""),"",D{r}-E{r})', MONEY),
               ("Status", 15, '=IF(D{r}="","",IF(E{r}="","Not yet paid",IF(E{r}>D{r},"Over quote","Within quote")))', None)],
              [("Kitchen", "New worktops", 1400, 1450), ("Kitchen", "Electrician", 600, 600),
               ("Bathroom", "Tiling", 1100, None), ("Living room", "Paint and decorating", 350, 320)],
              nrows=25, totals=[2, 3, 4],
              inputs=[("Contingency allowance (%)", 0.10, "0%")],
              summary=[("Total quoted", "=SUM(D{R0}:D{R1})", MONEY),
                       ("Budget including contingency", '=SUM(D{R0}:D{R1})*(1+{IN0})', MONEY),
                       ("Items over quote", '=COUNTIF(G{R0}:G{R1},"Over quote")', "0")])


def paint_calculator(path):
    build_log(path, "Paint", "Paint and Materials Calculator", "Enter each room's size and openings. Wall area, litres and tins calculate automatically",
              [("Room", 18, "input", None), ("Length (m)", 11, "input", "0.00"), ("Width (m)", 11, "input", "0.00"),
               ("Height (m)", 11, "input", "0.00"), ("Doors and windows (m²)", 14, "input", "0.0"),
               ("Wall area (m²)", 13, '=IF(OR(C{r}="",D{r}="",E{r}=""),"",(C{r}+D{r})*2*E{r}-N(F{r}))', "0.0"),
               ("Coats", 9, "input", "0"),
               ("Paint needed (litres)", 16, '=IF(OR(G{r}="",N(H{r})=0,N({IN0})=0),"",G{r}*H{r}/{IN0})', "0.0")],
              [("Living room", 5.0, 4.0, 2.4, 3.0, 2), ("Hall", 6.0, 1.2, 2.4, 2.0, 2), ("Bedroom", 4.0, 3.5, 2.4, 2.5, 2)],
              nrows=15,
              inputs=[("Coverage per litre (m²)", 12, "0.0"), ("Litres per tin", 2.5, "0.0")],
              summary=[("Total wall area (m²)", "=SUM(G{R0}:G{R1})", "0.0"),
                       ("Total paint needed (litres)", "=SUM(I{R0}:I{R1})", "0.0"),
                       ("Tins to buy", '=IFERROR(ROUNDUP(SUM(I{R0}:I{R1})/{IN1},0),"")', "0")],
              note_text="Coverage varies by paint, surface and colour change. Check the tin label and buy a little extra.")


def wardrobe_inventory(path):
    build_log(path, "Wardrobe", "Wardrobe Inventory", "Record each item with its price and how often you wear it. Cost per wear calculates for each item",
              [("Item", 22, "input", None), ("Category", 14, "input", None), ("Colour", 12, "input", None),
               ("Season", 12, "input", None), ("Size", 9, "input", None), ("Price paid", 12, "input", MONEY),
               ("Times worn", 11, "input", "0"),
               ("Cost per wear", 13, '=IF(OR(G{r}="",N(H{r})=0),"",G{r}/H{r})', MONEY),
               ("Last worn", 12, "input", DATE)],
              [("Wool jumper", "Tops", "Navy", "Winter", "M", 45, 22, D(11, 20)),
               ("Denim jeans", "Bottoms", "Blue", "All year", "32", 60, 40, D(11, 14)),
               ("Summer dress", "Tops", "Green", "Summer", "10", 30, 2, D(7, 9))],
              nrows=60, totals=[5],
              validations=[("E{R0}:E{R1}", '"Spring,Summer,Autumn,Winter,All year"')],
              summary=[("Items listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total value", "=SUM(G{R0}:G{R1})", MONEY),
                       ("Average cost per wear", '=IFERROR(AVERAGE(I{R0}:I{R1}),"")', MONEY)])


def pet_care_log(path):
    build_log(path, "Log", "Pet Care Log", "Record feeding, walks, vet visits and costs for each pet. Totals and vet visits calculate automatically",
              [("Date", 12, "input", DATE), ("Pet", 14, "input", None), ("Activity", 16, "input", None),
               ("Details", 26, "input", None), ("Cost", 12, "input", MONEY), ("Notes", 26, "input", None)],
              [(D(11, 18), "Biscuit", "Vet visit", "Annual check-up", 65, "Next visit in a year"),
               (D(11, 19), "Biscuit", "Walk", "30 minutes", None, None),
               (D(11, 25), "Tango", "Groom", "Full brush", 18, None),
               (D(11, 27), "Biscuit", "Feed", "Dry food, 2 cups", 9, None)],
              nrows=60, totals=[4],
              validations=[("D{R0}:D{R1}", '"Feed,Walk,Vet visit,Groom,Medicine given,Play,Other"')],
              summary=[("Entries", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Total cost", "=SUM(F{R0}:F{R1})", MONEY),
                       ("Vet visits", '=COUNTIF(D{R0}:D{R1},"Vet visit")', "0")],
              note_text="Follow your vet's instructions for medicines and diet. This record does not replace veterinary advice.")


def plant_watering(path):
    build_log(path, "Watering", "Plant Watering Schedule", "Set how often each plant needs water and when it was last watered. Next watering and status calculate from the report date",
              [("Plant", 22, "input", None), ("Location", 16, "input", None), ("Water every (days)", 13, "input", "0"),
               ("Last watered", 13, "input", DATE),
               ("Next watering", 13, '=IF(OR(D{r}="",E{r}=""),"",E{r}+D{r})', DATE),
               ("Days left", 10, '=IF(F{r}="","",F{r}-{RD})', "0"),
               ("Status", 13, '=IF(G{r}="","",IF(G{r}<=0,"Water now",IF(G{r}<=2,"Due soon","OK")))', None)],
              [("Peace lily", "Living room", 7, D(11, 24)), ("Basil", "Kitchen windowsill", 3, D(11, 29)),
               ("Snake plant", "Bedroom", 14, D(11, 15))],
              nrows=25, report=("Report date", REPORT),
              summary=[("Plants listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Water now", '=COUNTIF(H{R0}:H{R1},"Water now")', "0"),
                       ("Due within 2 days", '=COUNTIF(H{R0}:H{R1},"Due soon")', "0")])


def birthday_reminders(path):
    build_log(path, "Dates", "Birthday and Anniversary Reminder List", "Record each date by day and month. Days until the next one calculate from the report date, whatever year it is",
              [("Name", 20, "input", None), ("Occasion", 14, "input", None), ("Date", 12, "input", DATE),
               ("Days until next", 14,
                '=IF(D{r}="","",IF(DATE(YEAR({RD}),MONTH(D{r}),DAY(D{r}))<{RD},DATE(YEAR({RD})+1,MONTH(D{r}),DAY(D{r})),DATE(YEAR({RD}),MONTH(D{r}),DAY(D{r})))-{RD})', "0"),
               ("Gift or card idea", 24, "input", None), ("Sent?", 10, "input", None)],
              [("Sam", "Birthday", D(3, 14), "Book token", "No"), ("Priya and Ravi", "Anniversary", D(8, 2), "Dinner out", "No"),
               ("Grandma", "Birthday", D(11, 28), "Card and flowers", "Yes")],
              nrows=40, report=("Report date", REPORT),
              validations=[("C{R0}:C{R1}", '"Birthday,Anniversary,Other"'), ("G{R0}:G{R1}", '"Yes,No"')],
              summary=[("Dates listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Within 30 days", '=COUNTIFS(E{R0}:E{R1},"<=30")', "0"),
                       ("Not yet sent", '=COUNTIFS(B{R0}:B{R1},"<>",G{R0}:G{R1},"<>Yes")', "0")])
