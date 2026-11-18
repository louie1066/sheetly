"""Travel & Events templates 1-8: itinerary, travel budget, currency log, travel packing, flight and hotel comparison, road trip fuel, event budget, wedding budget."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda m, d: dt.date(2027, m, d)
T = lambda h, m: dt.time(h, m)


def itinerary(path):
    build_log(path, "Itinerary", "Trip Itinerary Planner", "Plan each day's activities with times, places and booking references. Costs total at the foot of the sheet",
              [("Day", 12, "input", DATE), ("Time", 9, "input", "hh:mm"), ("Activity", 30, "input", None),
               ("Place", 20, "input", None), ("Booking reference", 16, "input", None), ("Cost", 12, "input", MONEY),
               ("Notes", 26, "input", None)],
              [(D(4, 3), T(9, 0), "Flight to Lisbon", "Airport", "ABC123", 180, "Check in online 24 hours before"),
               (D(4, 3), T(14, 30), "Check in to hotel", "Alfama", "HTL-552", 0, None),
               (D(4, 4), T(9, 30), "Walking tour", "Old town", "TOUR-9", 25, "Meet at the square"),
               (D(4, 5), T(10, 0), "Day trip to Sintra", "Sintra", None, 45, "Book the palace slot")],
              nrows=40, totals=[5],
              summary=[("Activities listed", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Total planned cost", "=SUM(G{R0}:G{R1})", MONEY)])


def travel_budget(path):
    build_log(path, "Budget", "Travel Budget", "Set a budget for each category and record what you actually spend. Remaining amounts and status calculate automatically",
              [("Category", 16, "input", None), ("Item", 26, "input", None), ("Budget", 13, "input", MONEY),
               ("Actual spent", 13, "input", MONEY),
               ("Left (budget - spent)", 16, '=IF(OR(D{r}="",E{r}=""),"",D{r}-E{r})', MONEY),
               ("Status", 15, '=IF(D{r}="","",IF(E{r}="","Not yet spent",IF(E{r}>D{r},"Over budget","Within budget")))', None)],
              [("Transport", "Flights", 480, 462), ("Accommodation", "Hotel, 4 nights", 620, 620),
               ("Food", "Restaurants and snacks", 250, 190), ("Activities", "Tours and tickets", 200, 235),
               ("Insurance", "Travel insurance", 60, None)],
              nrows=30, totals=[2, 3, 4],
              validations=[("B{R0}:B{R1}", '"Transport,Accommodation,Food,Activities,Insurance,Other"')],
              summary=[("Total budget", "=SUM(D{R0}:D{R1})", MONEY),
                       ("Total spent", "=SUM(E{R0}:E{R1})", MONEY),
                       ("Left to spend", "=SUM(D{R0}:D{R1})-SUM(E{R0}:E{R1})", MONEY)],
              note_text="Enter amounts in one currency. Use the currency log for spending made abroad.")


def currency_log(path):
    build_log(path, "Spending", "Currency Conversion Log", "Log each foreign spend with the rate you were charged. The home currency amount and any card fee calculate automatically",
              [("Date", 12, "input", DATE), ("Place", 22, "input", None), ("Amount (foreign)", 14, "input", "#,##0.00"),
               ("Currency code", 11, "input", None), ("Rate (home per 1 foreign)", 15, "input", "0.0000"),
               ("Home amount", 14, '=IF(OR(D{r}="",F{r}=""),"",D{r}*F{r})', MONEY),
               ("Card fee (%)", 11, "input", "0.0%"),
               ("Total with fee", 14, '=IF(G{r}="","",G{r}*(1+N(H{r})))', MONEY)],
              [(D(4, 3), "Cafe", 12.50, "EUR", 1.0850, 0.0), (D(4, 4), "Taxi", 35.00, "EUR", 1.0850, 0.0),
               (D(4, 6), "Market", 22.00, "EUR", 1.0820, 0.02)],
              nrows=40, totals=[5, 7],
              summary=[("Total including fees (home currency)", "=SUM(I{R0}:I{R1})", MONEY),
                       ("Card fees paid", "=SUM(I{R0}:I{R1})-SUM(G{R0}:G{R1})", MONEY)],
              note_text="Rates change daily. Use the rate on your card or bank statement, not the rate on this sheet.")


def travel_packing(path):
    build_log(path, "Packing", "Travel Packing Checklist", "List what each person packs, which bag it goes in and its weight. The total weight is checked against your baggage allowance",
              [("Item", 26, "input", None), ("Traveller", 14, "input", None), ("Bag", 14, "input", None),
               ("Weight (kg)", 12, "input", "0.0"), ("Packed?", 10, "input", None)],
              [("Passports", "Ana", "Hand luggage", 0.1, "Yes"), ("Walking shoes", "Ana", "Suitcase", 1.2, "No"),
               ("Jackets (2)", "Ben", "Suitcase", 1.6, "No"), ("Medicines", "Ben", "Hand luggage", 0.3, "Yes"),
               ("Phone chargers", "Chloe", "Hand luggage", 0.4, "No")],
              nrows=60, totals=[3],
              validations=[("D{R0}:D{R1}", '"Suitcase,Hand luggage,Daypack,Other"'), ("F{R0}:F{R1}", '"Yes,No"')],
              inputs=[("Baggage allowance per bag (kg)", 23, "0.0")],
              summary=[("Items listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Packed", '=COUNTIF(F{R0}:F{R1},"Yes")', "0"),
                       ("Total weight (kg)", "=SUM(E{R0}:E{R1})", "0.0"),
                       ("Over allowance by (kg, if one bag)", '=IF({IN0}="","Enter your allowance above",MAX(0,SUM(E{R0}:E{R1})-{IN0}))', "0.0")],
              note_text="Check your airline's allowance for each bag and fare. The check above assumes one bag.")


def flight_hotel_comparison(path):
    build_log(path, "Compare", "Flight and Hotel Comparison", "Compare flight and hotel options on total cost. Cost per night and the rank calculate automatically",
              [("Option", 22, "input", None), ("Type", 12, "input", None), ("Base price", 13, "input", MONEY),
               ("Taxes and fees", 13, "input", MONEY),
               ("Total cost", 13, '=IF(D{r}="","",N(D{r})+N(E{r}))', MONEY),
               ("Nights or journeys", 13, "input", "0"),
               ("Cost per night or journey", 16, '=IF(OR(F{r}="",N(G{r})=0),"",F{r}/G{r})', MONEY),
               ("Rank (1 = cheapest)", 12, '=IF(F{r}="","",RANK(F{r},$F${R0}:$F${R1},1))', "0")],
              [("Airline A, direct", "Flight", 320, 45, 2), ("Airline B, one stop", "Flight", 265, 60, 2),
               ("Hotel Central", "Hotel", 480, 36, 4), ("Guesthouse Park", "Hotel", 420, 28, 4)],
              nrows=10,
              validations=[("C{R0}:C{R1}", '"Flight,Hotel,Train,Bus,Other"')],
              summary=[("Cheapest option", '=IFERROR(INDEX($B${R0}:$B${R1},MATCH(MIN($F${R0}:$F${R1}),$F${R0}:$F${R1},0)),"")', None),
                       ("Cheapest total cost", '=IF(COUNT($F${R0}:$F${R1})=0,"",MIN($F${R0}:$F${R1}))', MONEY)],
              note_text="Compare like with like: include baggage, transfers and cancellation terms before deciding.")


def road_trip_fuel(path):
    build_log(path, "Trip", "Road Trip Fuel Cost Calculator", "Enter each leg's distance, fuel use and price. Litres and cost calculate, and the cost is shared across the people you enter",
              [("Leg", 16, "input", None), ("From", 16, "input", None), ("To", 16, "input", None),
               ("Distance (km)", 13, "input", "#,##0"), ("Fuel use (litres per 100 km)", 16, "input", "0.0"),
               ("Litres needed", 13, '=IF(OR(E{r}="",F{r}=""),"",E{r}*F{r}/100)', "0.0"),
               ("Price per litre", 13, "input", "0.000"),
               ("Fuel cost", 13, '=IF(OR(G{r}="",H{r}=""),"",G{r}*H{r})', MONEY)],
              [("Leg 1", "Home", "Coast", 310, 6.8, 1.52), ("Leg 2", "Coast", "Mountains", 240, 7.2, 1.59),
               ("Leg 3", "Mountains", "Home", 380, 6.8, 1.55)],
              nrows=20, totals=[3, 5, 7],
              inputs=[("Number of people sharing the cost", 4, "0")],
              summary=[("Cost per person", '=IF(N({IN0})=0,"",SUM(I{R0}:I{R1})/{IN0})', MONEY),
                       ("Total distance (km)", "=SUM(E{R0}:E{R1})", "#,##0")])


def event_budget(path):
    build_log(path, "Budget", "Event Budget Planner", "Estimate each cost for an event and record the actual amount paid. Differences and totals calculate automatically",
              [("Category", 16, "input", None), ("Item", 26, "input", None), ("Supplier", 18, "input", None),
               ("Estimate", 13, "input", MONEY), ("Actual", 13, "input", MONEY),
               ("Difference (estimate - actual)", 17, '=IF(OR(E{r}="",F{r}=""),"",E{r}-F{r})', MONEY),
               ("Status", 16, '=IF(E{r}="","",IF(F{r}="","Not yet paid",IF(F{r}>E{r},"Over estimate","Within estimate")))', None)],
              [("Venue", "Hall hire", "Community centre", 800, 800), ("Catering", "Buffet for 60", "Local caterer", 900, 940),
               ("Entertainment", "DJ", "Sound and light", 350, None), ("Decorations", "Balloons and banners", "Party shop", 120, 95)],
              nrows=30, totals=[3, 4, 5],
              validations=[("B{R0}:B{R1}", '"Venue,Catering,Entertainment,Decorations,Equipment,Marketing,Staff,Other"')],
              summary=[("Total estimate", "=SUM(E{R0}:E{R1})", MONEY),
                       ("Total actual", "=SUM(F{R0}:F{R1})", MONEY),
                       ("Items over estimate", '=COUNTIF(H{R0}:H{R1},"Over estimate")', "0")])


def wedding_budget(path):
    build_log(path, "Budget", "Wedding Budget Planner", "Track each supplier with its estimate, deposit and balance. Priorities, balances and the contingency calculate automatically",
              [("Area", 16, "input", None), ("Item", 26, "input", None), ("Priority", 14, "input", None),
               ("Estimate", 13, "input", MONEY), ("Deposit paid", 13, "input", MONEY),
               ("Balance due", 13, '=IF(E{r}="","",E{r}-N(F{r}))', MONEY),
               ("Paid in full?", 13, "input", None)],
              [("Venue", "Reception hall", "Essential", 4200, 1000, "No"), ("Catering", "Three-course dinner", "Essential", 5400, 1500, "No"),
               ("Photography", "Eight hours", "Essential", 1800, 1800, "Yes"), ("Flowers", "Table centres", "Nice to have", 450, 0, "No"),
               ("Music", "Band for the evening", "Nice to have", 900, 300, "No")],
              nrows=30, totals=[3, 4, 5],
              validations=[("D{R0}:D{R1}", '"Essential,Nice to have"'), ("H{R0}:H{R1}", '"Yes,No"')],
              inputs=[("Contingency allowance (%)", 0.10, "0%")],
              summary=[("Essential items total", '=SUMIF(D{R0}:D{R1},"Essential",E{R0}:E{R1})', MONEY),
                       ("Total estimate", "=SUM(E{R0}:E{R1})", MONEY),
                       ("Budget including contingency", "=SUM(E{R0}:E{R1})*(1+{IN0})", MONEY),
                       ("Balance still to pay", "=SUM(G{R0}:G{R1})", MONEY)])
