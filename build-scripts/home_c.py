"""Home & Household templates 17-25: warranties, smart home, packing, car and vehicle logs, recipe scaling, house-sitting, contacts."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda m, d: dt.date(2026, m, d)
REPORT = dt.date(2026, 12, 1)


def warranty_tracker(path):
    build_log(path, "Warranties", "Warranty Tracker", "Record each purchase with its warranty length. Expiry date and days left calculate from the report date",
              [("Item", 22, "input", None), ("Make and model", 20, "input", None), ("Serial number", 16, "input", None),
               ("Purchase date", 13, "input", DATE), ("Warranty (months)", 12, "input", "0"),
               ("Warranty ends", 13, '=IF(OR(E{r}="",F{r}=""),"",EDATE(E{r},F{r}))', DATE),
               ("Days left", 11, '=IF(G{r}="","",G{r}-{RD})', "0"),
               ("Status", 14, '=IF(H{r}="","",IF(H{r}<0,"Expired",IF(H{r}<=60,"Expiring soon","In warranty")))', None)],
              [("Washing machine", "Brand X WM-200", "SN-0001", D(3, 5), 24), ("Laptop", "Brand Y 14", "SN-0002", D(10, 20), 12),
               ("Fridge freezer", "Brand Z FF-3", "SN-0003", D(1, 15), 24)],
              nrows=40, report=("Report date", REPORT),
              summary=[("Items listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("In warranty", '=COUNTIF(I{R0}:I{R1},"In warranty")', "0"),
                       ("Expiring within 60 days", '=COUNTIF(I{R0}:I{R1},"Expiring soon")', "0"),
                       ("Expired", '=COUNTIF(I{R0}:I{R1},"Expired")', "0")],
              note_text="Keep receipts with this list. Some warranties need registration within a set time of purchase.")


def smart_home_devices(path):
    build_log(path, "Devices", "Smart Home Device List", "List each connected device, how it connects and when its software was last updated. Devices needing an update check are flagged",
              [("Device", 22, "input", None), ("Room", 14, "input", None), ("Brand and model", 20, "input", None),
               ("Connection", 14, "input", None), ("App or hub", 18, "input", None), ("Software last updated", 14, "input", DATE),
               ("Update check", 15, '=IF(G{r}="","",IF({RD}-G{r}>90,"Update check","Recent"))', None)],
              [("Video doorbell", "Front door", "Brand D2", "Wi-Fi", "Doorbell app", D(10, 1)),
               ("Thermostat", "Hall", "Brand T5", "Wi-Fi", "Heating app", D(8, 15)),
               ("Smart plug", "Lounge", "Brand P1", "Zigbee", "Hub A", D(11, 2))],
              nrows=25, report=("Report date", REPORT),
              validations=[("E{R0}:E{R1}", '"Wi-Fi,Bluetooth,Zigbee,Z-Wave,Other"')],
              summary=[("Devices listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Need an update check", '=COUNTIF(H{R0}:H{R1},"Update check")', "0")],
              note_text="Store account passwords in a password manager, not in this sheet.")


def packing_list(path):
    build_log(path, "Packing", "Packing List", "List what you need to take, the bag it goes in and whether it is packed. The progress summary updates as you tick items off",
              [("Item", 30, "input", None), ("Category", 16, "input", None), ("Quantity", 10, "input", "0"),
               ("Bag", 14, "input", None), ("Packed?", 10, "input", None)],
              [("Passport", "Documents", 1, "Daypack", "Yes"), ("Phone charger", "Electronics", 1, "Carry-on", "No"),
               ("T-shirts", "Clothes", 5, "Suitcase", "No"), ("Toothbrush", "Toiletries", 1, "Carry-on", "Yes")],
              nrows=50,
              validations=[("C{R0}:C{R1}", '"Clothes,Toiletries,Documents,Electronics,Health,Other"'),
                           ("E{R0}:E{R1}", '"Suitcase,Carry-on,Daypack,Other"'),
                           ("F{R0}:F{R1}", '"Yes,No"')],
              summary=[("Items listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Packed", '=COUNTIF(F{R0}:F{R1},"Yes")', "0"),
                       ("Still to pack", '=COUNTA(B{R0}:B{R1})-COUNTIF(F{R0}:F{R1},"Yes")', "0")])


def car_maintenance(path):
    build_log(path, "Log", "Car Maintenance Log", "Record each job on the car with its odometer reading, cost and when the next one is due",
              [("Date", 12, "input", DATE), ("Odometer reading", 14, "input", "#,##0"), ("Job", 26, "input", None),
               ("Done by", 16, "input", None), ("Cost", 12, "input", MONEY), ("Next due at", 14, "input", "#,##0"),
               ("Notes", 26, "input", None)],
              [(D(9, 3), 38200, "Full service", "Garage", 240.00, 48200, None),
               (D(10, 14), 40650, "Front brake pads", "Garage", 135.50, None, "Discs still good"),
               (D(11, 9), 41900, "Tyre pressure check and top-up", "Me", 0, None, None)],
              nrows=30, totals=[4],
              validations=[("E{R0}:E{R1}", '"Me,Garage,Friend,Other"')],
              summary=[("Jobs logged", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Total spent", "=SUM(F{R0}:F{R1})", MONEY),
                       ("Latest odometer reading", '=IF(COUNT(C{R0}:C{R1})=0,"",MAX(C{R0}:C{R1}))', "#,##0")])


def fuel_economy(path):
    build_log(path, "Fuel", "Fuel Economy Tracker", "Record each fill-up with the odometer reading. Distance since the last fill, cost and litres per 100 km calculate automatically",
              [("Date", 12, "input", DATE), ("Odometer (km)", 14, "input", "#,##0"), ("Litres added", 12, "input", "0.00"),
               ("Price per litre", 13, "input", "0.000"),
               ("Distance since last fill (km)", 17, '=IF(OR(C{r}="",N(C{p})=0),"",C{r}-C{p})', "#,##0"),
               ("Fuel cost", 12, '=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r})', MONEY),
               ("Litres per 100 km", 14, '=IF(OR(F{r}="",N(F{r})=0),"",D{r}/F{r}*100)', "0.0")],
              [(D(10, 2), 41000, 38.5, 1.499), (D(10, 18), 41420, 41.0, 1.529), (D(11, 4), 41880, 36.2, 1.549)],
              nrows=40, totals=[2, 5],
              summary=[("Overall litres per 100 km", '=IFERROR(SUMIF(F{R0}:F{R1},">0",D{R0}:D{R1})/SUM(F{R0}:F{R1})*100,"")', "0.0"),
                       ("Total fuel cost", "=SUM(G{R0}:G{R1})", MONEY)],
              note_text="Distances use the odometer units you enter (km here). Fill up to the same level each time for accurate figures.")


def vehicle_service(path):
    build_log(path, "Services", "Vehicle Service Schedule", "Record the service interval and the odometer reading at the last service. Remaining distance calculates from the current reading above the table",
              [("Vehicle", 18, "input", None), ("Service item", 26, "input", None), ("Every (km)", 12, "input", "#,##0"),
               ("Last done at (km)", 15, "input", "#,##0"),
               ("Next due at (km)", 15, '=IF(OR(D{r}="",E{r}=""),"",E{r}+D{r})', "#,##0"),
               ("Remaining (km)", 14, '=IF(F{r}="","",F{r}-{IN0})', "#,##0;[Red]-#,##0"),
               ("Status", 13, '=IF(G{r}="","",IF(G{r}<0,"Overdue",IF(G{r}<=1000,"Due soon","OK")))', None)],
              [("Family car", "Engine oil and filter", 10000, 38000), ("Family car", "Cabin filter", 20000, 30000),
               ("Family car", "Brake fluid", 40000, 1000)],
              nrows=15,
              inputs=[("Current odometer reading (km)", 42000, "#,##0")],
              summary=[("Services listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Overdue", '=COUNTIF(H{R0}:H{R1},"Overdue")', "0"),
                       ("Due within 1,000 km", '=COUNTIF(H{R0}:H{R1},"Due soon")', "0")],
              note_text="Use the service intervals in your handbook. 'Due soon' means within 1,000 km of the next service.")


def recipe_scaling(path):
    build_log(path, "Scale", "Recipe Scaling Calculator", "Enter the original servings and the number you want. Each ingredient is scaled in proportion",
              [("Ingredient", 26, "input", None), ("Original amount", 15, "input", "0.0"), ("Unit", 12, "input", None),
               ("Scaled amount", 15, '=IF(OR(C{r}="",N({IN0})=0),"",C{r}*N({IN1})/{IN0})', "0.0")],
              [("Plain flour", 250, "g"), ("Butter", 125, "g"), ("Eggs", 2, "large"), ("Milk", 150, "ml")],
              nrows=25,
              inputs=[("Original servings", 4, "0"), ("New servings", 6, "0")],
              summary=[("Scale factor", '=IFERROR({IN1}/{IN0},"")', "0.00")],
              note_text="Scaling is simple proportion. Baking times, seasoning and small quantities such as eggs may need adjusting by testing.")


def house_sitting(path):
    build_log(path, "Instructions", "House-Sitting Instructions Sheet", "Give the house-sitter one clear sheet: what to do, where things are and who to call",
              [("Topic", 20, "input", None), ("Instruction", 44, "input", None), ("Location", 18, "input", None),
               ("Contact if needed", 20, "input", None), ("Notes", 26, "input", None)],
              [("Bins", "Put out the green bin on Tuesday evening", "Under the stairs", "Neighbour", None),
               ("Heating", "Keep the thermostat at 15 degrees", "Hall", "Me", "Do not change the timer"),
               ("Plants", "Water the kitchen plants every 3 days", "Kitchen windowsill", None, None),
               ("Post", "Collect post from the mat each morning", "Front door", None, None)],
              nrows=25,
              summary=[("Instructions listed", "=COUNTA(B{R0}:B{R1})", "0")],
              note_text="Replace the example details with your own. Add door codes and alarm details only on a copy you hand over in person.")


def emergency_contacts(path):
    build_log(path, "Contacts", "Emergency Contacts List", "Keep the people and services to call in an emergency in one place. Print a copy and keep it where others can find it",
              [("Name or service", 24, "input", None), ("Relationship or role", 20, "input", None),
               ("Phone", 16, "input", None), ("Email", 26, "input", None), ("Address", 28, "input", None),
               ("Notes", 26, "input", None)],
              [("Example neighbour", "Neighbour", "000 000 0000", None, None, "Has a spare key"),
               ("Example relative", "Family", "000 000 0000", None, None, None),
               ("Example GP surgery", "Doctor", "000 000 0000", None, None, None)],
              nrows=20,
              summary=[("Contacts listed", "=COUNTA(B{R0}:B{R1})", "0")],
              note_text="Replace the examples with real details. Check the list once a year. For emergencies, call your local emergency number.")
