"""Travel & Events templates 17-25: expense splitting, journal, destination scorecard, tickets, feedback, school trips, daily budget, vendors, countdown."""
import datetime as dt
from common import *
from tplkit import build_log

REPORT = dt.date(2026, 11, 17)
D = lambda y, m, d: dt.date(y, m, d)


def trip_expense_split(path):
    build_log(path, "Split", "Trip Expense Splitter", "Record what each person paid. Each share and balance calculate for an equal split. Positive balance means you are owed money",
              [("Person", 20, "input", None), ("Amount paid", 14, "input", MONEY),
               ("Share of costs", 14, '=IF(B{r}="","",SUM($C${R0}:$C${R1})/COUNTA($B${R0}:$B${R1}))', MONEY),
               ("Balance (paid - share)", 16, '=IF(B{r}="","",C{r}-D{r})', MONEY)],
              [("Ana", 240), ("Ben", 120), ("Chloe", 60)],
              nrows=12, totals=[1, 2, 3],
              summary=[("Total spent", "=SUM(C{R0}:C{R1})", MONEY),
                       ("Each person's share", '=IF(COUNTA(B{R0}:B{R1})=0,"",SUM(C{R0}:C{R1})/COUNTA(B{R0}:B{R1}))', MONEY)],
              note_text="Assumes an equal split. A negative balance means that person owes money to the group.")


def travel_journal(path):
    build_log(path, "Journal", "Travel Journal", "Log each day or place with a highlight and a rating from 1 to 5. The number of entries and average rating calculate automatically",
              [("Date", 12, "input", DATE), ("Place", 20, "input", None), ("Highlight", 28, "input", None),
               ("Rating (1-5)", 12, "input", "0"), ("Notes", 30, "input", None)],
              [(D(2027, 4, 3), "Lisbon", "Tram ride at sunset", 5, "Book the tram early"),
               (D(2027, 4, 5), "Sintra", "Palace gardens", 4, "Very crowded at noon")],
              nrows=40,
              validations=[("E{R0}:E{R1}", ("whole", "1", "5"))],
              summary=[("Entries", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Average rating", '=IF(COUNT(E{R0}:E{R1})=0,"",AVERAGE(E{R0}:E{R1}))', "0.0")])


def destination_scorecard(path):
    build_log(path, "Scores", "Destination Comparison Scorecard", "Score each destination from 1 (poor) to 5 (excellent) on each criterion. Weighted scores and ranks calculate from your weights",
              [("Destination", 20, "input", None), ("Cost", 10, "input", "0"), ("Weather", 10, "input", "0"),
               ("Travel time", 12, "input", "0"), ("Activities", 12, "input", "0"),
               ("Weighted score", 14, '=IF(B{r}="","",ROUND((N(C{r})*{IN0}+N(D{r})*{IN1}+N(E{r})*{IN2}+N(F{r})*{IN3})/SUM({IN0},{IN1},{IN2},{IN3}),2))', "0.00"),
               ("Rank", 10, '=IF(G{r}="","",RANK(G{r},$G${R0}:$G${R1},0))', "0")],
              [("Destination A", 4, 3, 2, 5), ("Destination B", 3, 5, 4, 3), ("Destination C", 5, 2, 3, 3)],
              nrows=10,
              validations=[("C{R0}:F{R1}", ("whole", "1", "5"))],
              inputs=[("Weight: cost", 3, "0"), ("Weight: weather", 2, "0"), ("Weight: travel time", 2, "0"), ("Weight: activities", 3, "0")],
              summary=[("Top choice", '=IF(COUNT(G{R0}:G{R1})=0,"",INDEX(B{R0}:B{R1},MATCH(MAX(G{R0}:G{R1}),G{R0}:G{R1},0)))', None),
                       ("Top score", '=IF(COUNT(G{R0}:G{R1})=0,"",MAX(G{R0}:G{R1}))', "0.00")],
              note_text="Change the weights above to match your priorities. Higher weights count for more in the score.")


def event_ticket_tracker(path):
    build_log(path, "Tickets", "Event Ticket Tracker", "Record each ticket order with its quantity, price and delivery status. Totals and undelivered tickets calculate automatically",
              [("Event", 22, "input", None), ("Seller", 18, "input", None), ("Ticket type", 16, "input", None),
               ("Quantity", 11, "input", "0"), ("Price each", 13, "input", MONEY),
               ("Total", 13, '=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r})', MONEY),
               ("Delivered?", 12, "input", None)],
              [("Summer Gala", "Box office", "General", 4, 25, "Yes"), ("Summer Gala", "Resale site", "VIP", 2, 60, "No")],
              nrows=20, totals=[3, 5],
              validations=[("H{R0}:H{R1}", '"Yes,No"')],
              summary=[("Total cost", "=SUM(G{R0}:G{R1})", MONEY),
                       ("Undelivered orders", '=COUNTIF(H{R0}:H{R1},"No")', "0")])


def event_feedback_summary(path):
    build_log(path, "Feedback", "Event Feedback Summary", "Enter how many people gave each score, from 1 to 5, for each question. Responses and averages calculate automatically",
              [("Question", 34, "input", None), ("1 star", 9, "input", "0"), ("2 stars", 9, "input", "0"),
               ("3 stars", 9, "input", "0"), ("4 stars", 9, "input", "0"), ("5 stars", 9, "input", "0"),
               ("Responses", 12, '=IF(B{r}="","",SUM(C{r}:G{r}))', "0"),
               ("Average", 11, '=IF(OR(B{r}="",N(H{r})=0),"",(C{r}*1+D{r}*2+E{r}*3+F{r}*4+G{r}*5)/H{r})', "0.00")],
              [("The venue was easy to find", 2, 5, 10, 20, 15), ("The schedule ran on time", 1, 3, 8, 18, 20),
               ("The food was good", 0, 2, 6, 14, 28)],
              nrows=12, totals=[1, 2, 3, 4, 5, 6],
              summary=[("Total responses", "=SUM(H{R0}:H{R1})", "0"),
                       ("Overall average", '=IF(SUM(H{R0}:H{R1})=0,"",(SUM(C{R0}:C{R1})*1+SUM(D{R0}:D{R1})*2+SUM(E{R0}:E{R1})*3+SUM(F{R0}:F{R1})*4+SUM(G{R0}:G{R1})*5)/SUM(H{R0}:H{R1}))', "0.00")],
              note_text="Count each person's score once per question. Use the same questions each time so results can be compared.")


def school_trip_tracker(path):
    build_log(path, "Trip", "School Trip Consent and Payment Tracker", "Track each participant's returned form and payments. Balances and outstanding forms calculate automatically",
              [("Participant", 22, "input", None), ("Form returned?", 14, "input", None),
               ("Payment due", 14, "input", MONEY), ("Paid", 14, "input", MONEY),
               ("Balance", 14, '=IF(B{r}="","",N(D{r})-N(E{r}))', MONEY),
               ("Status", 18, '=IF(B{r}="","",IF(C{r}<>"Yes","Form outstanding",IF(F{r}<=0,"Paid in full","Payment due")))', None)],
              [("Participant A", "Yes", 150, 150), ("Participant B", "Yes", 150, 100), ("Participant C", "No", 150, 0)],
              nrows=40, totals=[2, 3, 4],
              validations=[("C{R0}:C{R1}", '"Yes,No"')],
              summary=[("Participants", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Forms outstanding", '=COUNTIF(G{R0}:G{R1},"Form outstanding")', "0"),
                       ("Balance still to collect", "=SUM(F{R0}:F{R1})", MONEY)],
              note_text="Keep medical, dietary and emergency details out of this sheet and with the trip leader in a secure form.")


def daily_travel_budget(path):
    build_log(path, "Daily", "Daily Travel Spending Limit", "Set a spending limit for each day and record what you spend. Daily and running balances calculate automatically",
              [("Date", 12, "input", DATE), ("Daily limit", 13, "input", MONEY), ("Spent", 13, "input", MONEY),
               ("Left today", 13, '=IF(OR(C{r}="",D{r}=""),"",C{r}-D{r})', MONEY),
               ("Running balance", 15, '=IF(E{r}="","",SUM($E${R0}:E{r}))', MONEY)],
              [(D(2027, 4, 3), 80, 65), (D(2027, 4, 4), 80, 92), (D(2027, 4, 5), 80, 40)],
              nrows=21, totals=[1, 2, 3],
              summary=[("Total limits", "=SUM(C{R0}:C{R1})", MONEY),
                       ("Total spent", "=SUM(D{R0}:D{R1})", MONEY),
                       ("Days over limit", '=COUNTIF(E{R0}:E{R1},"<0")', "0")],
              note_text="A negative left-today figure means you went over that day's limit.")


def event_vendor_tracker(path):
    build_log(path, "Vendors", "Event Vendor Tracker", "Track each supplier's service, quote, deposit and contract status. The balance owed and the next action are shown for each vendor",
              [("Vendor", 20, "input", None), ("Service", 16, "input", None), ("Contact", 16, "input", None),
               ("Contract signed?", 13, "input", None), ("Quoted price", 13, "input", MONEY),
               ("Deposit paid", 13, "input", MONEY), ("Balance owed", 13, '=IF(B{r}="","",N(F{r})-N(G{r}))', MONEY),
               ("Next action", 28, "input", None)],
              [("Sound and light", "Entertainment", "Sam", "Yes", 900, 300, "Final timings due"),
               ("Party shop", "Decorations", "Priya", "No", 120, 0, "Send the colour scheme")],
              nrows=20, totals=[4, 5, 6],
              validations=[("C{R0}:C{R1}", '"Venue,Catering,Entertainment,Decorations,Equipment,Photography,Other"'), ("E{R0}:E{R1}", '"Yes,No"')],
              summary=[("Vendors booked", '=COUNTIF(E{R0}:E{R1},"Yes")', "0"),
                       ("Total quoted", "=SUM(F{R0}:F{R1})", MONEY),
                       ("Balance still to pay", "=SUM(H{R0}:H{R1})", MONEY)])


def trip_countdown_checklist(path):
    build_log(path, "Countdown", "Trip Countdown Checklist", "List each task before the trip with an owner and due date. Days left and a status flag calculate from the report date",
              [("Task", 30, "input", None), ("Owner", 14, "input", None), ("Due date", 13, "input", DATE),
               ("Done?", 10, "input", None),
               ("Days left", 11, '=IF(OR(D{r}="",E{r}="Yes"),"",D{r}-{RD})', "0"),
               ("Status", 16, '=IF(B{r}="","",IF(E{r}="Yes","Done",IF(D{r}="","No date",IF(F{r}<0,"Overdue",IF(F{r}<=7,"Due this week","Upcoming")))))', None)],
              [("Book flights", "Ana", D(2027, 1, 20), "Yes"), ("Confirm hotel", "Ben", D(2027, 2, 10), "No"),
               ("Renew passports", "Chloe", D(2026, 11, 20), "No")],
              nrows=40, report=("Report date", REPORT),
              validations=[("E{R0}:E{R1}", '"Yes,No"')],
              summary=[("Tasks", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Done", '=COUNTIF(G{R0}:G{R1},"Done")', "0"),
                       ("Overdue", '=COUNTIF(G{R0}:G{R1},"Overdue")', "0")])
