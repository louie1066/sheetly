"""IT & Computing templates 1-8: asset register, licences, help desk, backups, IP planning, devices, refresh, sprints."""
import random
import datetime as dt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as L
from common import *

RNG = random.Random(404)
REPORT = dt.date(2026, 12, 1)


def asset_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Assets"
    setup_sheet(ws, "IT Asset Register", "Record each device. Age and totals calculate from the report date below the table", 9,
                [14, 14, 22, 14, 14, 14, 13, 12, 10])
    header_row(ws, 5, 2, ["Asset tag", "Type", "Make and model", "Location", "Assigned to", "Status",
                          "Purchase date", "Cost", "Age (years)"])
    types = ["Laptop", "Desktop", "Tablet", "Projector", "Server", "Switch"]
    for i in range(15):
        r = 6 + i
        t = types[i % len(types)]
        put(ws, r, 2, f"AT-{1001 + i}")
        put(ws, r, 3, t)
        put(ws, r, 4, f"Model {chr(65 + i % 5)}{100 + i}")
        put(ws, r, 5, f"Room {10 + i % 4}")
        put(ws, r, 6, f"Staff {chr(65 + i % 6)}")
        put(ws, r, 7, "Repair" if i == 4 else "In use")
        put(ws, r, 8, dt.date(2021 + i % 5, 1 + i % 12, 10), DATE)
        put(ws, r, 9, RNG.choice([450, 650, 900, 1200, 2400]), MONEY)
        put(ws, r, 10, f'=IF(H{r}="","",YEARFRAC(H{r},$C$23))', "0.0", "calc")
    validate(ws, "C6:C20", '"Laptop,Desktop,Tablet,Projector,Server,Switch,Other"')
    validate(ws, "G6:G20", '"In use,In storage,Repair,Retired"')
    label_value(ws, 23, "Report date", REPORT, DATE, "input")
    label_value(ws, 25, "Assets recorded", '=COUNTA(B6:B20)', "0", "summary")
    label_value(ws, 26, "Total cost", '=SUM(I6:I20)', MONEY, "summary")
    label_value(ws, 27, "Aged 5 years or more", '=COUNTIF(J6:J20,">=5")', "0", "summary")
    wb.save(path)


def licence_tracker(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Licences"
    setup_sheet(ws, "Software Licence Tracker", "Compare seats owned with seats used and see which licences need renewing", 9,
                [22, 16, 10, 10, 12, 13, 14, 18, 14])
    header_row(ws, 5, 2, ["Software", "Licence type", "Seats owned", "Seats used", "Seats free",
                          "Expiry date", "Days to expiry", "Status", "Annual cost"])
    items = [("Office suite", "Per user", 60, 55, 240), ("Coding IDE", "Per seat", 30, 32, 900),
             ("Antivirus", "Per device", 120, 104, 1500), ("Design tool", "Per user", 10, 6, 480),
             ("Database server", "Site", 1, 1, 2000), ("Video editor", "Per seat", 8, 8, 320)]
    for i, (name, typ, own, used, cost) in enumerate(items):
        r = 6 + i
        put(ws, r, 2, name)
        put(ws, r, 3, typ)
        put(ws, r, 4, own, "0")
        put(ws, r, 5, used, "0")
        put(ws, r, 6, f"=D{r}-E{r}", "0", "calc")
        put(ws, r, 7, dt.date(2026, 12, 15) + dt.timedelta(days=45 * i), DATE)
        put(ws, r, 8, f'=IF(G{r}="","",G{r}-$C$23)', "0", "calc")
        put(ws, r, 9, f'=IF(G{r}="","",IF(E{r}>D{r},"Over-allocated",IF(H{r}<0,"Expired",IF(H{r}<=60,"Renew soon","Current"))))',
            None, "calc")
        put(ws, r, 10, cost, MONEY)
    label_value(ws, 23, "Report date", REPORT, DATE, "input")
    label_value(ws, 25, "Total annual cost", '=SUM(J6:J20)', MONEY, "summary")
    label_value(ws, 26, "Over-allocated licences", '=COUNTIF(I6:I20,"Over-allocated")', "0", "summary")
    label_value(ws, 27, "Renew within 60 days", '=COUNTIF(I6:I20,"Renew soon")', "0", "summary")
    wb.save(path)


def help_desk(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tickets"
    setup_sheet(ws, "Help Desk Ticket Log", "Log each request. Hours to resolve and SLA breaches calculate automatically", 12,
                [12, 16, 16, 10, 16, 12, 14, 12, 14, 3, 10, 12])
    header_row(ws, 5, 2, ["Ticket ID", "Opened", "Closed", "Priority", "Category", "Status",
                          "Hours to resolve", "SLA hours", "SLA result"])
    header_row(ws, 5, 12, ["Priority", "SLA hours"])
    for i, (p, h) in enumerate([("High", 4), ("Medium", 24), ("Low", 72)]):
        put(ws, 6 + i, 12, p)
        put(ws, 6 + i, 13, h, "0")
    ws.column_dimensions["M"].width = 12
    cats = ["Hardware", "Software", "Network", "Account", "Printer", "Other"]
    for i in range(20):
        r = 6 + i
        opened = dt.datetime(2026, 11, 16, 8, 30) + dt.timedelta(hours=RNG.randint(0, 200))
        status = "Closed" if i < 14 else RNG.choice(["Open", "In progress"])
        closed = opened + dt.timedelta(hours=RNG.randint(1, 60)) if status == "Closed" else None
        put(ws, r, 2, f"T-{2001 + i}")
        put(ws, r, 3, opened, "dd/mm/yy hh:mm")
        put(ws, r, 4, closed, "dd/mm/yy hh:mm")
        put(ws, r, 5, RNG.choice(["High", "Medium", "Low"]))
        put(ws, r, 6, RNG.choice(cats))
        put(ws, r, 7, status)
        put(ws, r, 8, f'=IF(D{r}="","",ROUND((D{r}-C{r})*24,1))', "0.0", "calc")
        put(ws, r, 9, f'=IF(E{r}="","",IFERROR(VLOOKUP(E{r},$L$6:$M$8,2,FALSE),""))', "0", "calc")
        put(ws, r, 10, f'=IF(OR(H{r}="",I{r}=""),"",IF(H{r}>I{r},"Breached","Met"))', None, "calc")
    validate(ws, "E6:E25", '"High,Medium,Low"')
    validate(ws, "G6:G25", '"Open,In progress,Closed"')
    validate(ws, "F6:F25", '"Hardware,Software,Network,Account,Printer,Other"')
    label_value(ws, 27, "Open or in progress", '=COUNTIF(G6:G25,"Open")+COUNTIF(G6:G25,"In progress")', "0", "summary")
    label_value(ws, 28, "Average hours to resolve", '=IFERROR(AVERAGE(H6:H25),"")', "0.0", "summary")
    label_value(ws, 29, "SLA breaches", '=COUNTIF(J6:J25,"Breached")', "0", "summary")
    wb.save(path)


def backup_log(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Backups"
    setup_sheet(ws, "Server Backup Schedule Log", "Log each backup run. Duration and success rate per server calculate automatically", 13,
                [12, 14, 14, 10, 10, 12, 12, 10, 3, 16, 10, 12, 14])
    header_row(ws, 5, 2, ["Date", "Server", "Backup type", "Start", "End", "Duration (min)", "Status", "Data (GB)"])
    header_row(ws, 5, 11, ["Server", "Runs", "Successful", "Success rate"])
    servers = ["File server", "Web server", "Database server"]
    for i in range(30):
        r = 6 + i
        srv = servers[i % 3]
        start = dt.time(22, RNG.choice([0, 15, 30, 45]))
        mins = RNG.randint(20, 150)
        end_dt = dt.datetime(2026, 11, 1, start.hour, start.minute) + dt.timedelta(minutes=mins)
        put(ws, r, 2, dt.date(2026, 11, 1) + dt.timedelta(days=i // 3), DATE)
        put(ws, r, 3, srv)
        put(ws, r, 4, "Full" if i % 7 == 0 else "Incremental")
        put(ws, r, 5, start, "hh:mm")
        put(ws, r, 6, end_dt.time(), "hh:mm")
        put(ws, r, 7, f'=IF(OR(E{r}="",F{r}=""),"",ROUND(MOD(F{r}-E{r},1)*1440,0))', "0", "calc")
        put(ws, r, 8, "Failed" if i in (5, 17) else ("Partial" if i == 11 else "Success"))
        put(ws, r, 9, round(RNG.uniform(5, 80), 1), "0.0")
    validate(ws, "H6:H35", '"Success,Partial,Failed"')
    for i, s in enumerate(servers):
        r = 6 + i
        put(ws, r, 11, s)
        put(ws, r, 12, f'=COUNTIF($C$6:$C$35,K{r})', "0", "calc")
        put(ws, r, 13, f'=COUNTIFS($C$6:$C$35,K{r},$H$6:$H$35,"Success")', "0", "calc")
        put(ws, r, 14, f'=IFERROR(M{r}/L{r},"")', "0%", "calc")
    label_value(ws, 37, "Overall success rate", '=IFERROR(COUNTIF(H6:H35,"Success")/COUNTA(H6:H35),"")', "0%", "summary")
    ws.column_dimensions["B"].width = 12
    wb.save(path)


def ip_planner(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Subnets"
    setup_sheet(ws, "IP Address Planner", "Enter the hosts each department needs. Block size, prefix and spare addresses calculate automatically", 6,
                [22, 14, 16, 12, 14, 14])
    header_row(ws, 5, 2, ["Department", "Hosts needed", "Addresses in block", "Prefix", "Usable hosts", "Spare hosts"])
    depts = [("Administration", 25), ("Teaching", 60), ("Computing lab", 30), ("Library", 12),
             ("Guest Wi-Fi", 100), ("Servers", 10), ("Printers", 5)]
    for i, (d, h) in enumerate(depts):
        r = 6 + i
        put(ws, r, 2, d)
        put(ws, r, 3, h, "0")
        put(ws, r, 4, f"=2^ROUNDUP(LOG(C{r}+2,2),0)", "0", "calc")
        put(ws, r, 5, f"=32-LOG(D{r},2)", '"/"0', "calc")
        put(ws, r, 6, f"=D{r}-2", "0", "calc")
        put(ws, r, 7, f"=F{r}-C{r}", "0", "calc")
    label_value(ws, 15, "Total addresses in blocks", "=SUM(D6:D12)", "0", "summary")
    label_value(ws, 16, "Fits in one /24 (256 addresses)?", '=IF(C15<=256,"Yes","No, use a larger range")', None, "summary")
    put(ws, 17, 2, "Each block must start on a boundary of its own size when you assign real addresses. Check alignment by hand.",
        kind="label")
    wb.save(path)


def network_inventory(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Devices"
    setup_sheet(ws, "Network Device Inventory", "Record each network device. Warranty status compares with the report date", 8,
                [18, 16, 16, 14, 12, 13, 13, 16])
    header_row(ws, 5, 2, ["Device name", "Type", "IP address", "Location", "Firmware", "Last checked", "Warranty end", "Warranty status"])
    types = ["Core switch", "Router", "Access point", "Firewall", "Wireless controller"]
    for i in range(12):
        r = 6 + i
        put(ws, r, 2, f"NET-{i + 1:02d}")
        put(ws, r, 3, types[i % len(types)])
        put(ws, r, 4, f"10.0.{i % 4}.{10 + i}")
        put(ws, r, 5, f"Comms room {1 + i % 2}")
        put(ws, r, 6, f"v{4 + i % 3}.{RNG.randint(0, 9)}")
        put(ws, r, 7, dt.date(2026, 11, 2) + dt.timedelta(days=i), DATE)
        put(ws, r, 8, dt.date(2027, 1, 1) + dt.timedelta(days=120 * i), DATE)
        put(ws, r, 9, f'=IF(H{r}="","",IF(H{r}<$C$23,"Expired",IF(H{r}-$C$23<=180,"Expires soon","Covered")))', None, "calc")
    validate(ws, "C6:C20", '"Core switch,Router,Access point,Firewall,Wireless controller,Other"')
    label_value(ws, 23, "Report date", REPORT, DATE, "input")
    label_value(ws, 25, "Devices", '=COUNTA(B6:B20)', "0", "summary")
    label_value(ws, 26, "Warranty expired or expiring soon", '=COUNTIF(I6:I20,"Expired")+COUNTIF(I6:I20,"Expires soon")', "0", "summary")
    wb.save(path)


def hardware_refresh(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Refresh"
    setup_sheet(ws, "Hardware Refresh Planner", "Set each device's lifespan. Refresh dates and the budget needed in the next 12 months calculate automatically", 9,
                [16, 12, 14, 12, 14, 12, 22, 14, 3])
    header_row(ws, 5, 2, ["Device", "Type", "Purchase date", "Lifespan (years)", "Refresh due", "Age (years)", "Status", "Estimated cost"])
    types = ["Laptop", "Desktop", "Tablet", "Server"]
    for i in range(12):
        r = 6 + i
        put(ws, r, 2, f"HW-{i + 1:03d}")
        put(ws, r, 3, types[i % 4])
        put(ws, r, 4, dt.date(2019 + i % 6, 3 + i % 9, 1), DATE)
        put(ws, r, 5, 4 if types[i % 4] != "Server" else 5, "0")
        put(ws, r, 6, f'=IF(D{r}="","",EDATE(D{r},12*E{r}))', DATE, "calc")
        put(ws, r, 7, f'=IF(D{r}="","",($C$23-D{r})/365.25)', "0.0", "calc")
        put(ws, r, 8, f'=IF(F{r}="","",IF(F{r}<$C$23,"Overdue",IF(F{r}-$C$23<=365,"Due within 12 months","Later")))', None, "calc")
        put(ws, r, 9, RNG.choice([550, 700, 900, 3200]), MONEY)
    label_value(ws, 23, "Report date", REPORT, DATE, "input")
    label_value(ws, 25, "Overdue", '=COUNTIF(H6:H17,"Overdue")', "0", "summary")
    label_value(ws, 26, "Budget needed in next 12 months", '=SUMIF(H6:H17,"Overdue",I6:I17)+SUMIF(H6:H17,"Due within 12 months",I6:I17)',
                MONEY, "summary")
    wb.save(path)


def sprint_burndown(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sprint"
    setup_sheet(ws, "Sprint Backlog and Burndown", "Enter story points and status. Enter remaining points each day to compare with the ideal line", 10,
                [30, 10, 14, 14, 12, 3, 3, 8, 16, 16])
    header_row(ws, 5, 2, ["Task", "Points", "Assignee", "Status", "Points done"])
    header_row(ws, 5, 9, ["Day", "Ideal remaining", "Actual remaining"])
    tasks = [("Login page", 3, "Student A", "Done"), ("Quiz data model", 5, "Student B", "Done"),
             ("Score calculation", 2, "Student A", "Done"), ("Results table", 8, "Student C", "In progress"),
             ("Input validation", 5, "Student B", "Done"), ("Error messages", 3, "Student C", "In progress"),
             ("Teacher dashboard", 5, "Student A", "To do"), ("Export to CSV", 3, "Student B", "To do"),
             ("Unit tests", 2, "Student C", "To do"), ("Sprint review notes", 1, "Student A", "To do")]
    for i, (t, p, who, st) in enumerate(tasks):
        r = 6 + i
        put(ws, r, 2, t)
        put(ws, r, 3, p, "0")
        put(ws, r, 4, who)
        put(ws, r, 5, st)
        put(ws, r, 6, f'=IF(E{r}="Done",C{r},0)', "0", "calc")
    validate(ws, "E6:E15", '"To do,In progress,Done"')
    actual = [33, 30, 27, 22, 20, 16, 14, 10, 6, 0]
    for d in range(10):
        r = 6 + d
        put(ws, r, 9, d + 1, "0", "label")
        put(ws, r, 10, f"=$C$18*(1-I{r}/10)", "0.0", "calc")
        put(ws, r, 11, actual[d], "0")
    label_value(ws, 18, "Points committed", "=SUM(C6:C15)", "0", "summary")
    label_value(ws, 19, "Points done", "=SUM(F6:F15)", "0", "summary")
    label_value(ws, 20, "Points remaining", "=C18-C19", "0", "summary")
    wb.save(path)
