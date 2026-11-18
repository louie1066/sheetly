"""Sales, Marketing & Operations templates 17-25: picking, fulfilment, shipping, food cost, training, leave, reviews, recruitment, shift handover."""
import datetime as dt
from common import *
from tplkit import build_log

REPORT = dt.date(2026, 11, 17)
D = lambda y, m, d: dt.date(y, m, d)


def warehouse_picking_list(path):
    build_log(path, "Picking", "Warehouse Picking List", "List each order line with the quantity ordered and picked. Short lines are flagged for follow-up",
              [("Order no", 12, "input", None), ("SKU", 12, "input", None), ("Item", 26, "input", None),
               ("Location", 12, "input", None), ("Qty ordered", 12, "input", "0"), ("Qty picked", 12, "input", "0"),
               ("Status", 12, '=IF(OR(F{r}="",G{r}=""),"",IF(G{r}<F{r},"Short","OK"))', None)],
              [("SO-2001", "SKU-10", "Steel bolts (box)", "A-03", 4, 4), ("SO-2001", "SKU-22", "Washers (bag)", "A-07", 2, 1),
               ("SO-2002", "SKU-31", "Hinges", "C-11", 6, None)],
              nrows=150, totals=[4, 5],
              summary=[("Lines to pick", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Lines short", '=COUNTIF(H{R0}:H{R1},"Short")', "0"),
                       ("Units still to pick", "=SUM(F{R0}:F{R1})-SUM(G{R0}:G{R1})", "0")])


def order_fulfilment_tracker(path):
    build_log(path, "Orders", "Order Fulfilment Tracker", "Track each order from order date to dispatch. Days to ship and whether it shipped within your target calculate automatically",
              [("Order", 12, "input", None), ("Customer", 20, "input", None), ("Order date", 13, "input", DATE),
               ("Ship date", 13, "input", DATE), ("Carrier", 14, "input", None), ("Tracking number", 18, "input", None),
               ("Days to ship", 12, '=IF(OR(D{r}="",E{r}=""),"",E{r}-D{r})', "0"),
               ("Status", 14, '=IF(B{r}="","",IF(E{r}="","Not shipped",IF(H{r}<={IN0},"On time","Late")))', None)],
              [("SO-2001", "Harbour Cafe", D(2027, 1, 4), D(2027, 1, 5), "Carrier A", "TRK-1001"),
               ("SO-2002", "Lee Designs", D(2027, 1, 4), D(2027, 1, 8), "Carrier B", "TRK-1002"),
               ("SO-2003", "Shah Retail", D(2027, 1, 6), None, None, None)],
              nrows=150,
              inputs=[("Target days to ship", 2, "0")],
              summary=[("Orders", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Shipped", "=COUNT(E{R0}:E{R1})", "0"),
                       ("Late", '=COUNTIF(I{R0}:I{R1},"Late")', "0"),
                       ("Average days to ship", '=IF(COUNT(H{R0}:H{R1})=0,"",AVERAGE(H{R0}:H{R1}))', "0.0")])


def shipping_cost_calculator(path):
    build_log(path, "Shipping", "Shipping Cost Calculator", "Enter each shipment's destination, parcel weight and number of parcels. Cost includes the base fee, the weight charge and the fuel surcharge",
              [("Destination", 22, "input", None), ("Weight per parcel (kg)", 16, "input", "0.00"),
               ("Parcels", 10, "input", "0"),
               ("Shipping cost", 14, '=IF(OR(C{r}="",D{r}=""),"",ROUND((D{r}*{IN0}+C{r}*D{r}*{IN1})*(1+{IN2}),2))', MONEY)],
              [("Zone 1", 2.5, 4), ("Zone 2", 8.0, 1), ("Zone 3", 15.0, 2)],
              nrows=100, totals=[3],
              inputs=[("Base fee per parcel", 4.50, MONEY), ("Charge per kg per parcel", 1.20, MONEY), ("Fuel surcharge", 0.10, "0%")],
              summary=[("Total shipping cost", "=SUM(E{R0}:E{R1})", MONEY),
                       ("Average cost per parcel", '=IF(SUM(D{R0}:D{R1})=0,"",SUM(E{R0}:E{R1})/SUM(D{R0}:D{R1}))', MONEY)],
              note_text="Replace the sample zones and rates with your carrier's prices. The fuel surcharge is applied to the whole cost.")


def restaurant_food_cost_calculator(path):
    build_log(path, "Food cost", "Restaurant Food Cost Calculator", "Enter each dish's ingredient cost and menu price. Food cost percentage and gross profit calculate, with a flag above your target",
              [("Dish", 24, "input", None), ("Ingredient cost", 15, "input", MONEY), ("Menu price", 14, "input", MONEY),
               ("Food cost %", 13, '=IF(OR(C{r}="",N(D{r})=0),"",C{r}/D{r})', "0.0%"),
               ("Gross profit", 14, '=IF(OR(C{r}="",D{r}=""),"",D{r}-C{r})', MONEY),
               ("Against target", 16, '=IF(E{r}="","",IF(E{r}>{IN0},"Above target","On target"))', None)],
              [("Chicken curry", 3.20, 11.50), ("Veggie wrap", 2.10, 7.00), ("House salad", 2.80, 6.50)],
              nrows=60,
              inputs=[("Target food cost %", 0.30, "0%")],
              summary=[("Dishes", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Average food cost %", '=IF(COUNT(E{R0}:E{R1})=0,"",AVERAGE(E{R0}:E{R1}))', "0.0%"),
                       ("Dishes above target", '=COUNTIF(G{R0}:G{R1},"Above target")', "0")],
              note_text="Ingredient cost is the total for one portion, taken from your recipe costing. Menu price should be before tax.")


def staff_training_log(path):
    build_log(path, "Training", "Staff Training Log", "Record each training course with its date, hours and certificate expiry. Expired and soon-to-renew certificates are flagged",
              [("Employee", 20, "input", None), ("Course", 24, "input", None), ("Date", 12, "input", DATE),
               ("Hours", 9, "input", "0.0"), ("Certificate?", 12, "input", None), ("Expiry date", 13, "input", DATE),
               ("Days to expiry", 13, '=IF(OR(G{r}="",{RD}=""),"",G{r}-{RD})', "0"),
               ("Status", 14, '=IF(G{r}="","",IF(H{r}<0,"Expired",IF(H{r}<=60,"Renew soon","Valid")))', None)],
              [("Ana", "Food hygiene", D(2026, 6, 10), 4, "Yes", D(2027, 6, 10)), ("Ben", "First aid", D(2025, 9, 1), 8, "Yes", D(2026, 12, 1)),
               ("Chloe", "Manual handling", D(2026, 10, 5), 2, "No", None)],
              nrows=150, totals=[3], report=("Report date", REPORT),
              validations=[("F{R0}:F{R1}", '"Yes,No"')],
              summary=[("Training records", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Hours trained", "=SUM(E{R0}:E{R1})", "0.0"),
                       ("Expired certificates", '=COUNTIF(I{R0}:I{R1},"Expired")', "0"),
                       ("Renew within 60 days", '=COUNTIF(I{R0}:I{R1},"Renew soon")', "0")])


def employee_leave_tracker(path):
    build_log(path, "Leave", "Employee Leave Tracker", "Log each leave request with its dates and approval. Working days are counted and annual leave left is shown against your allowance",
              [("Employee", 20, "input", None), ("Leave type", 14, "input", None), ("Start date", 13, "input", DATE),
               ("End date", 13, "input", DATE),
               ("Working days", 13, '=IF(OR(D{r}="",E{r}=""),"",NETWORKDAYS(D{r},E{r}))', "0"),
               ("Approved?", 11, "input", None)],
              [("Ana", "Annual", D(2027, 1, 4), D(2027, 1, 8), "Yes"), ("Ben", "Sick", D(2027, 1, 11), D(2027, 1, 12), "Yes"),
               ("Chloe", "Annual", D(2027, 2, 1), D(2027, 2, 5), "No")],
              nrows=100, totals=[4],
              inputs=[("Annual leave allowance (days)", 25, "0")],
              validations=[("C{R0}:C{R1}", '"Annual,Sick,Unpaid,Other"'), ("G{R0}:G{R1}", '"Yes,No"')],
              summary=[("Requests", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Approved annual leave (days)", '=SUMIFS(F{R0}:F{R1},C{R0}:C{R1},"Annual",G{R0}:G{R1},"Yes")', "0"),
                       ("Annual leave remaining (days)", '=IF(N({IN0})=0,"",{IN0}-SUMIFS(F{R0}:F{R1},C{R0}:C{R1},"Annual",G{R0}:G{R1},"Yes"))', "0")],
              note_text="Working days exclude weekends only. Add public holidays to the count by hand if your leave policy needs it.")


def performance_review_scorecard(path):
    build_log(path, "Review", "Performance Review Scorecard", "Score each employee from 1 to 5 on four criteria. The average and rating band calculate automatically",
              [("Employee", 20, "input", None), ("Role", 18, "input", None), ("Quality", 11, "input", "0"),
               ("Productivity", 13, "input", "0"), ("Teamwork", 12, "input", "0"), ("Development", 13, "input", "0"),
               ("Average", 11, '=IF(OR(B{r}="",COUNT(D{r}:G{r})=0),"",ROUND(AVERAGE(D{r}:G{r}),2))', "0.00"),
               ("Rating band", 16, '=IF(H{r}="","",IF(H{r}>=4.5,"Outstanding",IF(H{r}>=3.5,"Exceeds",IF(H{r}>=2.5,"Meets","Below"))))', None)],
              [("Ana", "Sales lead", 5, 4, 4, 5), ("Ben", "Warehouse", 3, 3, 4, 3), ("Chloe", "Support", 2, 3, 3, 2)],
              nrows=60,
              validations=[("D{R0}:G{R1}", ("whole", "1", "5"))],
              summary=[("Employees reviewed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Average rating", '=IF(COUNT(H{R0}:H{R1})=0,"",AVERAGE(H{R0}:H{R1}))', "0.00"),
                       ("Outstanding", '=COUNTIF(I{R0}:I{R1},"Outstanding")', "0"),
                       ("Below expectations", '=COUNTIF(I{R0}:I{R1},"Below")', "0")],
              note_text="Use the same criteria for everyone. Bands: 4.5 and above Outstanding, 3.5 Exceeds, 2.5 Meets, below 2.5 Below.")


def recruitment_candidate_tracker(path):
    build_log(path, "Candidates", "Recruitment Candidate Tracker", "Track each candidate through each stage of recruitment with their interview score. Days in process and active candidates calculate automatically",
              [("Candidate", 20, "input", None), ("Role", 18, "input", None), ("Source", 14, "input", None),
               ("Applied on", 13, "input", DATE), ("Stage", 13, "input", None), ("Interview score (1-5)", 14, "input", "0"),
               ("Days in process", 14, '=IF(OR(E{r}="",{RD}=""),"",{RD}-E{r})', "0")],
              [("Candidate A", "Sales assistant", "Website", D(2026, 11, 2), "Interview", 4),
               ("Candidate B", "Sales assistant", "Referral", D(2026, 10, 20), "Hired", 5),
               ("Candidate C", "Warehouse", "Job board", D(2026, 11, 9), "Screen", None)],
              nrows=150, report=("Report date", REPORT),
              validations=[("D{R0}:D{R1}", '"Website,Referral,Job board,Agency,Other"'),
                           ("F{R0}:F{R1}", '"Applied,Screen,Interview,Offer,Hired,Rejected"'),
                           ("G{R0}:G{R1}", ("whole", "1", "5"))],
              summary=[("Candidates", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Active", '=COUNTA(B{R0}:B{R1})-COUNTIF(F{R0}:F{R1},"Hired")-COUNTIF(F{R0}:F{R1},"Rejected")', "0"),
                       ("Hired", '=COUNTIF(F{R0}:F{R1},"Hired")', "0"),
                       ("Average interview score", '=IF(COUNT(G{R0}:G{R1})=0,"",AVERAGE(G{R0}:G{R1}))', "0.0")])


def shift_handover_log(path):
    build_log(path, "Handover", "Shift Handover Log", "Record what the next shift needs to know, with any action still open. Open actions are counted automatically",
              [("Date", 12, "input", DATE), ("Shift", 12, "input", None), ("Handed over by", 18, "input", None),
               ("Handed to", 18, "input", None), ("Issues or update", 36, "input", None),
               ("Action needed?", 14, "input", None), ("Resolved?", 12, "input", None), ("Notes", 26, "input", None)],
              [(D(2027, 1, 4), "Early", "Ana", "Ben", "Delivery van late", "Yes", "No", "Chase carrier by 10:00"),
               (D(2027, 1, 4), "Late", "Ben", "Chloe", "Stock count finished", "No", None, None)],
              nrows=150,
              validations=[("C{R0}:C{R1}", '"Early,Late,Night"'), ("G{R0}:G{R1}", '"Yes,No"'), ("H{R0}:H{R1}", '"Yes,No"')],
              summary=[("Handovers logged", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Actions needed", '=COUNTIF(G{R0}:G{R1},"Yes")', "0"),
                       ("Open actions", '=COUNTIFS(G{R0}:G{R1},"Yes",H{R0}:H{R1},"No")', "0")])
