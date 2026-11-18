"""Sales, Marketing & Operations templates 9-16: ad spend, feedback, NPS, churn, competitors, SWOT, events, support SLAs."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda y, m, d: dt.date(y, m, d)
DT = lambda y, m, d, h, mi: dt.datetime(y, m, d, h, mi)


def ad_spend_tracker(path):
    build_log(path, "Ad spend", "Ad Spend Tracker", "Log each campaign's spend, impressions and clicks. Cost per click and click-through rate calculate automatically",
              [("Platform", 14, "input", None), ("Campaign", 22, "input", None), ("Start date", 12, "input", DATE),
               ("Spend", 13, "input", MONEY), ("Impressions", 13, "input", "#,##0"), ("Clicks", 11, "input", "#,##0"),
               ("Cost per click", 13, '=IF(OR(G{r}="",N(G{r})=0,E{r}=""),"",E{r}/G{r})', MONEY),
               ("Click-through rate", 14, '=IF(OR(F{r}="",N(F{r})=0,G{r}=""),"",G{r}/F{r})', "0.00%")],
              [("Search", "Brand terms", D(2027, 1, 4), 300, 12000, 540), ("Social", "Spring offer", D(2027, 1, 10), 250, 48000, 610)],
              nrows=120, totals=[3, 4, 5],
              validations=[("B{R0}:B{R1}", '"Search,Social,Display,Video,Email,Other"')],
              summary=[("Total spend", "=SUM(E{R0}:E{R1})", MONEY),
                       ("Total clicks", "=SUM(G{R0}:G{R1})", "#,##0"),
                       ("Overall cost per click", '=IF(SUM(G{R0}:G{R1})=0,"",SUM(E{R0}:E{R1})/SUM(G{R0}:G{R1}))', MONEY)])


def customer_feedback_summary(path):
    build_log(path, "Feedback", "Customer Feedback Summary", "Count positive, neutral and negative comments for each topic. Totals and the positive share calculate automatically",
              [("Topic", 26, "input", None), ("Positive", 12, "input", "0"), ("Neutral", 12, "input", "0"),
               ("Negative", 12, "input", "0"),
               ("Total comments", 14, '=IF(B{r}="","",SUM(C{r}:E{r}))', "0"),
               ("Positive share", 14, '=IF(OR(B{r}="",N(F{r})=0),"",C{r}/F{r})', "0%")],
              [("Delivery speed", 14, 5, 6), ("Product quality", 22, 3, 1), ("Customer service", 9, 2, 4)],
              nrows=40, totals=[1, 2, 3, 4],
              summary=[("Total comments", "=SUM(F{R0}:F{R1})", "0"),
                       ("Overall positive share", '=IF(SUM(F{R0}:F{R1})=0,"",SUM(C{R0}:C{R1})/SUM(F{R0}:F{R1}))', "0%")])


def net_promoter_score_tracker(path):
    build_log(path, "Scores", "Net Promoter Score Tracker", "Record each 0 to 10 score. Scores of 9 to 10 are promoters and 0 to 6 are detractors. The Net Promoter Score calculates from the totals",
              [("Date", 12, "input", DATE), ("Customer", 22, "input", None), ("Score (0-10)", 12, "input", "0"),
               ("Group", 14, '=IF(D{r}="","",IF(D{r}>=9,"Promoter",IF(D{r}>=7,"Passive","Detractor")))', None)],
              [(D(2027, 2, 1), "Harbour Cafe", 10), (D(2027, 2, 2), "Lee Designs", 7), (D(2027, 2, 3), "Shah Retail", 4)],
              nrows=300,
              validations=[("D{R0}:D{R1}", ("whole", "0", "10"))],
              summary=[("Responses", "=COUNT(D{R0}:D{R1})", "0"),
                       ("Promoters", '=COUNTIF(E{R0}:E{R1},"Promoter")', "0"),
                       ("Detractors", '=COUNTIF(E{R0}:E{R1},"Detractor")', "0"),
                       ("Net Promoter Score", '=IF(COUNT(D{R0}:D{R1})=0,"",ROUND((COUNTIF(E{R0}:E{R1},"Promoter")-COUNTIF(E{R0}:E{R1},"Detractor"))/COUNT(D{R0}:D{R1})*100,0))', "0")],
              note_text="Net Promoter Score is the percentage of promoters minus the percentage of detractors, from -100 to 100.")


def customer_churn_analysis(path):
    build_log(path, "Churn", "Customer Churn Analysis", "Record each month's starting customers, new customers and lost customers. Churn rate and the closing count calculate automatically",
              [("Month", 13, "input", DATE), ("Customers at start", 16, "input", "#,##0"), ("New customers", 14, "input", "#,##0"),
               ("Lost customers", 14, "input", "#,##0"),
               ("Customers at end", 15, '=IF(OR(C{r}="",D{r}="",E{r}=""),"",C{r}+D{r}-E{r})', "#,##0"),
               ("Churn rate", 12, '=IF(OR(C{r}="",N(C{r})=0,E{r}=""),"",E{r}/C{r})', "0.0%")],
              [(D(2026, 8, 1), 500, 40, 20), (D(2026, 9, 1), 520, 35, 30), (D(2026, 10, 1), 525, 30, 25)],
              nrows=36, totals=[2, 3],
              summary=[("Average monthly churn", '=IF(COUNT(G{R0}:G{R1})=0,"",AVERAGE(G{R0}:G{R1}))', "0.0%"),
                       ("Customers lost (total)", "=SUM(E{R0}:E{R1})", "#,##0"),
                       ("Net change in customers", "=SUM(D{R0}:D{R1})-SUM(E{R0}:E{R1})", "#,##0")])


def competitor_comparison_matrix(path):
    build_log(path, "Matrix", "Competitor Comparison Matrix", "Rate each feature from 1 (weak) to 5 (strong) for your business and each competitor. Totals and the strongest business on each feature calculate automatically",
              [("Feature", 26, "input", None), ("Our business", 14, "input", "0"), ("Competitor A", 14, "input", "0"),
               ("Competitor B", 14, "input", "0"), ("Competitor C", 14, "input", "0"),
               ("Best in class", 16, '=IF(COUNT(C{r}:F{r})=0,"",INDEX($C$5:$F$5,MATCH(MAX(C{r}:F{r}),C{r}:F{r},0)))', None)],
              [("Price", 4, 3, 5, 2), ("Delivery speed", 3, 4, 4, 5), ("Customer support", 5, 3, 2, 3)],
              nrows=25, totals=[1, 2, 3, 4],
              validations=[("C{R0}:F{R1}", ("whole", "1", "5"))],
              summary=[("Total: our business", "=SUM(C{R0}:C{R1})", "0"),
                       ("Total: Competitor A", "=SUM(D{R0}:D{R1})", "0"),
                       ("Total: Competitor B", "=SUM(E{R0}:E{R1})", "0"),
                       ("Total: Competitor C", "=SUM(F{R0}:F{R1})", "0")],
              note_text="Rate every feature on the same scale. Totals show overall strength, but the best-in-class column shows where each one leads.")


def swot_analysis(path):
    build_log(path, "SWOT", "SWOT Analysis", "List each strength, weakness, opportunity and threat with its impact, the action to take and who owns it. Counts by category calculate automatically",
              [("Category", 16, "input", None), ("Point", 40, "input", None), ("Impact", 12, "input", None),
               ("Action", 32, "input", None), ("Owner", 16, "input", None)],
              [("Strength", "Loyal repeat customers", "High", "Ask for referrals", "Sam"),
               ("Weakness", "Limited weekend staffing", "Medium", "Plan a weekend rota", "Priya"),
               ("Opportunity", "Growing local demand", "High", "Test a second site", None),
               ("Threat", "New competitor opening nearby", "Medium", "Review pricing", None)],
              nrows=40,
              validations=[("B{R0}:B{R1}", '"Strength,Weakness,Opportunity,Threat"'), ("D{R0}:D{R1}", '"High,Medium,Low"')],
              summary=[("Strengths", '=COUNTIF(B{R0}:B{R1},"Strength")', "0"),
                       ("Weaknesses", '=COUNTIF(B{R0}:B{R1},"Weakness")', "0"),
                       ("Opportunities", '=COUNTIF(B{R0}:B{R1},"Opportunity")', "0"),
                       ("Threats", '=COUNTIF(B{R0}:B{R1},"Threat")', "0"),
                       ("High-impact points", '=COUNTIF(D{R0}:D{R1},"High")', "0")])


def event_attendance_tracker(path):
    build_log(path, "Events", "Event Attendance Tracker", "Record registrations, attendance, leads and cost for each event. Attendance rate and cost per lead calculate automatically",
              [("Event", 22, "input", None), ("Date", 12, "input", DATE), ("Registered", 12, "input", "#,##0"),
               ("Attended", 11, "input", "#,##0"),
               ("Attendance rate", 13, '=IF(OR(D{r}="",N(D{r})=0,E{r}=""),"",E{r}/D{r})', "0%"),
               ("Leads captured", 13, "input", "#,##0"), ("Cost", 13, "input", MONEY),
               ("Cost per lead", 13, '=IF(OR(H{r}="",N(G{r})=0),"",H{r}/G{r})', MONEY)],
              [("Spring trade fair", D(2027, 3, 12), 300, 210, 45, 2800), ("Webinar", D(2027, 4, 2), 150, 96, 22, 350)],
              nrows=60, totals=[2, 3, 5, 6],
              summary=[("Events", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total leads", "=SUM(G{R0}:G{R1})", "#,##0"),
                       ("Overall cost per lead", '=IF(SUM(G{R0}:G{R1})=0,"",SUM(H{R0}:H{R1})/SUM(G{R0}:G{R1}))', MONEY)])


def support_ticket_sla_tracker(path):
    build_log(path, "Tickets", "Support Ticket SLA Tracker", "Log when each ticket opened and was resolved, with its target time. Hours taken and whether the target was met calculate automatically",
              [("Ticket ID", 14, "input", None), ("Opened", 17, "input", "dd/mm/yyyy hh:mm"),
               ("Resolved", 17, "input", "dd/mm/yyyy hh:mm"), ("Target (hours)", 13, "input", "0"),
               ("Hours taken", 12, '=IF(OR(C{r}="",D{r}=""),"",ROUND((D{r}-C{r})*24,1))', "0.0"),
               ("Within target?", 14, '=IF(F{r}="","",IF(F{r}<=E{r},"Yes","No"))', None)],
              [("T-1001", DT(2027, 1, 4, 9, 0), DT(2027, 1, 4, 13, 30), 8), ("T-1002", DT(2027, 1, 4, 10, 0), DT(2027, 1, 6, 9, 0), 24),
               ("T-1003", DT(2027, 1, 5, 14, 0), None, 8)],
              nrows=150,
              summary=[("Tickets", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Within target", '=COUNTIF(G{R0}:G{R1},"Yes")', "0"),
                       ("Missed target", '=COUNTIF(G{R0}:G{R1},"No")', "0"),
                       ("Target met (%)", '=IF(COUNTIF(G{R0}:G{R1},"Yes")+COUNTIF(G{R0}:G{R1},"No")=0,"",COUNTIF(G{R0}:G{R1},"Yes")/(COUNTIF(G{R0}:G{R1},"Yes")+COUNTIF(G{R0}:G{R1},"No")))', "0%")],
              note_text="Enter the target in hours for each ticket. Tickets without a resolved time are left blank until they are closed.")
