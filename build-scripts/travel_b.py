"""Travel & Events templates 9-16: passports, visas, insurance, guest list, run sheet, seating, volunteers, layover times."""
import datetime as dt
from common import *
from tplkit import build_log

REPORT = dt.date(2026, 11, 17)
D = lambda y, m, d: dt.date(y, m, d)
DT = lambda y, m, d, h, mi: dt.datetime(y, m, d, h, mi)
T = lambda h, m: dt.time(h, m)


def passport_tracker(path):
    build_log(path, "Documents", "Passport and Document Tracker", "Record each travel document with its expiry date. Days left and a status flag calculate from the report date",
              [("Traveller", 16, "input", None), ("Document", 18, "input", None), ("Issue date", 13, "input", DATE),
               ("Expiry date", 13, "input", DATE),
               ("Days left", 11, '=IF(E{r}="","",E{r}-{RD})', "0"),
               ("Status", 16, '=IF(E{r}="","",IF(E{r}<{RD},"Expired",IF(E{r}-{RD}<=183,"Renew soon","Valid")))', None)],
              [("Ana", "Passport", D(2021, 6, 1), D(2026, 9, 30)), ("Ben", "Passport", D(2019, 2, 14), D(2027, 3, 1)),
               ("Chloe", "Driving licence", D(2020, 8, 5), D(2030, 8, 4))],
              nrows=20, report=("Report date", REPORT),
              summary=[("Documents listed", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Expired", '=COUNTIF(G{R0}:G{R1},"Expired")', "0"),
                       ("Renew soon (within about 6 months)", '=COUNTIF(G{R0}:G{R1},"Renew soon")', "0")],
              note_text="Many countries require a passport to be valid for a set period after your return date. Check the rule for each destination.")


def visa_tracker(path):
    build_log(path, "Entry", "Visa and Entry Requirements Tracker", "Track each destination's entry requirement and application deadline. Days to deadline and status calculate automatically",
              [("Country", 18, "input", None), ("Entry requirement", 18, "input", None), ("Application deadline", 16, "input", DATE),
               ("Submitted?", 12, "input", None),
               ("Days to deadline", 14, '=IF(OR(D{r}="",C{r}="No visa"),"",D{r}-{RD})', "0"),
               ("Status", 16, '=IF(B{r}="","",IF(C{r}="No visa","Not needed",IF(E{r}="Yes","Submitted",IF(AND(F{r}<>"",N(F{r})<0),"Overdue","To do"))))', None)],
              [("Country A", "Visa", D(2027, 1, 15), "No"), ("Country B", "No visa", None, "No"),
               ("Country C", "eVisa", D(2027, 3, 1), "Yes")],
              nrows=20, report=("Report date", REPORT),
              validations=[("C{R0}:C{R1}", '"Visa,eVisa,Visa on arrival,No visa,Other"'), ("E{R0}:E{R1}", '"Yes,No"')],
              summary=[("Countries listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("To do", '=COUNTIF(G{R0}:G{R1},"To do")', "0"),
                       ("Overdue", '=COUNTIF(G{R0}:G{R1},"Overdue")', "0")],
              note_text="Check official government sites for current entry rules. This sheet only tracks your own deadlines.")


def insurance_comparison(path):
    build_log(path, "Compare", "Travel Insurance Comparison", "Compare policies by premium, cover limit and excess. Cost per day and the cheapest option calculate automatically",
              [("Provider", 18, "input", None), ("Policy", 16, "input", None), ("Premium", 13, "input", MONEY),
               ("Cover limit", 14, "input", MONEY), ("Excess", 12, "input", MONEY), ("Days covered", 12, "input", "0"),
               ("Cost per day", 13, '=IF(OR(D{r}="",N(G{r})=0),"",D{r}/G{r})', MONEY),
               ("Rank (1 = cheapest per day)", 16, '=IF(H{r}="","",RANK(H{r},$H${R0}:$H${R1},1))', "0")],
              [("Provider A", "Basic", 42, 500000, 100, 10), ("Provider B", "Standard", 65, 1000000, 50, 10),
               ("Provider C", "Premium", 90, 2000000, 0, 10)],
              nrows=8,
              summary=[("Cheapest per day", '=IF(COUNT(H{R0}:H{R1})=0,"",INDEX(B{R0}:B{R1},MATCH(MIN(H{R0}:H{R1}),H{R0}:H{R1},0)))', None),
                       ("Lowest cost per day", '=IF(COUNT(H{R0}:H{R1})=0,"",MIN(H{R0}:H{R1}))', MONEY)],
              note_text="Compare the cover limits and exclusions, not only the price. Check the policy wording before you buy.")


def event_guest_list(path):
    build_log(path, "Guests", "Event Guest List", "Track each invitation, RSVP and any plus-ones. The confirmed party size calculates automatically",
              [("Guest", 20, "input", None), ("Group", 14, "input", None), ("RSVP", 12, "input", None),
               ("Plus-ones", 10, "input", "0"),
               ("Confirmed party size", 15, '=IF(B{r}="","",IF(D{r}="Yes",1+N(E{r}),0))', "0"),
               ("Table", 12, "input", None)],
              [("Sam Lee", "Friend", "Yes", 1, "Table 2"), ("Priya Shah", "Family", "Maybe", 0, None),
               ("Tom Reed", "Colleague", "No", 0, None)],
              nrows=50, totals=[4],
              validations=[("C{R0}:C{R1}", '"Family,Friend,Colleague,Partner,Other"'), ("D{R0}:D{R1}", '"Yes,No,Maybe"')],
              summary=[("Invitations sent", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Confirmed guests", "=SUM(F{R0}:F{R1})", "0"),
                       ("Still to reply (Maybe)", '=COUNTIF(D{R0}:D{R1},"Maybe")', "0"),
                       ("Declined", '=COUNTIF(D{R0}:D{R1},"No")', "0")],
              note_text="Confirmed party size counts the guest plus any plus-ones when the RSVP is Yes.")


def event_run_sheet(path):
    build_log(path, "Run sheet", "Event Run Sheet", "Plan the event timeline. Each slot's end time and the finish time calculate from the start time and length",
              [("Start", 10, "input", "hh:mm"), ("Minutes", 10, "input", "0"),
               ("Ends", 10, '=IF(OR(B{r}="",C{r}=""),"",B{r}+C{r}/1440)', "hh:mm"),
               ("Activity", 30, "input", None), ("Owner", 16, "input", None), ("Notes", 26, "input", None)],
              [(T(9, 0), 30, "Doors open and registration", "Front desk", "Event notes"), (T(9, 30), 45, "Opening talk", "Main hall", None),
               (T(10, 15), 60, "Workshop session", "Room 2", "Bring extension leads")],
              nrows=25, totals=[1],
              summary=[("Slots planned", "=COUNTA(E{R0}:E{R1})", "0"),
                       ("Finish time", '=IF(COUNT(D{R0}:D{R1})=0,"",MAX(D{R0}:D{R1}))', "hh:mm")],
              note_text="Give each slot one owner so everyone knows who to ask.")


def seating_planner(path):
    build_log(path, "Seating", "Wedding Seating Planner", "Enter each table's seats and the guests placed there. Free seats and over-capacity flags calculate automatically",
              [("Table", 14, "input", None), ("Seats", 10, "input", "0"), ("Guests seated", 14, "input", "0"),
               ("Seats free", 12, '=IF(B{r}="","",N(C{r})-N(D{r}))', "0"),
               ("Status", 16, '=IF(B{r}="","",IF(N(D{r})>N(C{r}),"Over capacity",IF(N(D{r})=N(C{r}),"Full","Seats free")))', None)],
              [("Table 1", 8, 8), ("Table 2", 8, 6), ("Table 3", 6, 7)],
              nrows=20, totals=[1, 2, 3],
              summary=[("Total seats", "=SUM(C{R0}:C{R1})", "0"),
                       ("Guests placed", "=SUM(D{R0}:D{R1})", "0"),
                       ("Tables over capacity", '=COUNTIF(F{R0}:F{R1},"Over capacity")', "0")],
              note_text="Enter a count of guests per table. Change the table names to suit your room layout.")


def volunteer_roster(path):
    build_log(path, "Roster", "Event Volunteer Roster", "Schedule volunteers by role and shift, record hours and check-in. Total hours and check-ins calculate automatically",
              [("Volunteer", 20, "input", None), ("Role", 16, "input", None), ("Shift date", 13, "input", DATE),
               ("Start", 10, "input", "hh:mm"), ("Hours", 10, "input", "0.0"), ("Checked in?", 12, "input", None)],
              [("Ana", "Registration", D(2027, 4, 3), T(8, 30), 4.0, "Yes"), ("Ben", "Stewarding", D(2027, 4, 3), T(12, 0), 3.0, "No"),
               ("Chloe", "Catering", D(2027, 4, 4), T(9, 0), 5.0, "No")],
              nrows=40, totals=[4],
              validations=[("C{R0}:C{R1}", '"Setup,Registration,Stewarding,Catering,Clear-up,Other"'), ("G{R0}:G{R1}", '"Yes,No"')],
              summary=[("Shifts booked", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Checked in", '=COUNTIF(G{R0}:G{R1},"Yes")', "0"),
                       ("Hours booked", "=SUM(F{R0}:F{R1})", "0.0")])


def travel_time_planner(path):
    build_log(path, "Journeys", "Travel Time and Layover Planner", "Enter each leg's departure and arrival in local time, plus the time zone change. Elapsed hours calculate automatically",
              [("Leg", 16, "input", None), ("Departs (local)", 17, "input", "dd/mm/yyyy hh:mm"),
               ("Arrives (local)", 17, "input", "dd/mm/yyyy hh:mm"), ("Time zone change (hours ahead)", 16, "input", "0.0"),
               ("Elapsed hours", 13, '=IF(OR(C{r}="",D{r}=""),"",ROUND((D{r}-C{r})*24-N(E{r}),2))', "0.00"),
               ("Notes", 26, "input", None)],
              [("Outbound", DT(2027, 4, 3, 9, 0), DT(2027, 4, 3, 13, 30), 1.0, "Direct"),
               ("Connection", DT(2027, 4, 3, 14, 0), DT(2027, 4, 3, 15, 10), 0.0, "Layover at gate"),
               ("Return", DT(2027, 4, 10, 18, 0), DT(2027, 4, 10, 21, 45), -1.0, None)],
              nrows=12, totals=[4],
              summary=[("Total elapsed hours", "=SUM(F{R0}:F{R1})", "0.00")],
              note_text="Time zone change is positive when you move ahead and negative when you move back.")
