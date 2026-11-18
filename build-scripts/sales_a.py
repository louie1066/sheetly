"""Sales, Marketing & Operations templates 1-8: social media, email, marketing ROI, leads, customers, commission, forecast, SEO."""
import datetime as dt
from common import *
from tplkit import build_log

REPORT = dt.date(2026, 11, 17)
D = lambda y, m, d: dt.date(y, m, d)


def social_media_calendar(path):
    build_log(path, "Calendar", "Social Media Content Calendar", "Plan posts by date and platform, then record likes and reach. Engagement rate calculates from likes and reach",
              [("Date", 12, "input", DATE), ("Platform", 14, "input", None), ("Post topic", 26, "input", None),
               ("Content type", 13, "input", None), ("Status", 13, "input", None),
               ("Likes", 10, "input", "#,##0"), ("Reach", 10, "input", "#,##0"),
               ("Engagement rate", 14, '=IF(OR(G{r}="",N(H{r})=0),"",G{r}/H{r})', "0.0%")],
              [(D(2027, 1, 4), "Instagram", "New product preview", "Image", "Posted", 320, 4100),
               (D(2027, 1, 6), "LinkedIn", "Behind the scenes", "Text", "Scheduled", None, None),
               (D(2027, 1, 8), "TikTok", "How-to clip", "Video", "Idea", None, None)],
              nrows=120, totals=[5, 6],
              validations=[("C{R0}:C{R1}", '"Instagram,Facebook,LinkedIn,TikTok,X,Email,Other"'),
                           ("E{R0}:E{R1}", '"Image,Video,Carousel,Text,Story"'),
                           ("F{R0}:F{R1}", '"Idea,Drafted,Scheduled,Posted"')],
              summary=[("Posts planned", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Posted", '=COUNTIF(F{R0}:F{R1},"Posted")', "0"),
                       ("Average engagement rate", '=IF(COUNT(I{R0}:I{R1})=0,"",AVERAGE(I{R0}:I{R1}))', "0.0%")])


def email_campaign_tracker(path):
    build_log(path, "Campaigns", "Email Campaign Tracker", "Record each campaign's sends, opens and clicks. Open and click rates calculate automatically",
              [("Campaign", 26, "input", None), ("Send date", 13, "input", DATE), ("Emails sent", 12, "input", "#,##0"),
               ("Opened", 11, "input", "#,##0"), ("Clicked", 11, "input", "#,##0"),
               ("Open rate", 11, '=IF(OR(D{r}="",N(D{r})=0,E{r}=""),"",E{r}/D{r})', "0.0%"),
               ("Click rate", 11, '=IF(OR(D{r}="",N(D{r})=0,F{r}=""),"",F{r}/D{r})', "0.0%")],
              [("Spring newsletter", D(2027, 3, 1), 2400, 960, 240), ("Product launch", D(2027, 3, 15), 2500, 1300, 390)],
              nrows=60, totals=[2, 3, 4],
              summary=[("Campaigns", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Average open rate", '=IF(COUNT(G{R0}:G{R1})=0,"",AVERAGE(G{R0}:G{R1}))', "0.0%"),
                       ("Average click rate", '=IF(COUNT(H{R0}:H{R1})=0,"",AVERAGE(H{R0}:H{R1}))', "0.0%")])


def marketing_budget_and_roi(path):
    build_log(path, "ROI", "Marketing Budget and ROI Tracker", "Compare each channel's budget and spend with the revenue it brought in. Return on investment calculates for each channel and overall",
              [("Channel", 22, "input", None), ("Budget", 14, "input", MONEY), ("Spend", 14, "input", MONEY),
               ("Revenue", 14, "input", MONEY),
               ("ROI", 12, '=IF(OR(D{r}="",N(D{r})=0,E{r}=""),"",(E{r}-D{r})/D{r})', "0%")],
              [("Search ads", 3000, 2850, 9400), ("Trade show", 2000, 2300, 3100), ("Social media", 1500, 1200, 2050)],
              nrows=20, totals=[1, 2, 3],
              summary=[("Total spend", "=SUM(D{R0}:D{R1})", MONEY),
                       ("Total revenue", "=SUM(E{R0}:E{R1})", MONEY),
                       ("Overall ROI", '=IF(SUM(D{R0}:D{R1})=0,"",(SUM(E{R0}:E{R1})-SUM(D{R0}:D{R1}))/SUM(D{R0}:D{R1}))', "0%")],
              note_text="ROI is (revenue minus spend) divided by spend. Revenue should come from tracked sales or codes for each channel.")


def lead_tracker(path):
    build_log(path, "Leads", "Lead Tracker", "Track each lead from first contact to sale, with its value and next follow-up. Open leads, pipeline value and days to follow-up calculate automatically",
              [("Lead name", 20, "input", None), ("Company", 20, "input", None), ("Source", 14, "input", None),
               ("Status", 13, "input", None), ("Value", 13, "input", MONEY), ("Next follow-up", 14, "input", DATE),
               ("Days to follow-up", 14, '=IF(OR(G{r}="",{RD}=""),"",G{r}-{RD})', "0")],
              [("Jordan Park", "Harbour Cafe", "Referral", "Proposal", 2400, D(2026, 11, 20)),
               ("Sam Lee", "Lee Designs", "Website", "Contacted", 900, D(2026, 11, 25)),
               ("Priya Shah", "Shah Retail", "Event", "Won", 3100, None)],
              nrows=120, totals=[4], report=("Report date", REPORT),
              validations=[("D{R0}:D{R1}", '"Website,Referral,Event,Social,Cold call,Other"'),
                           ("E{R0}:E{R1}", '"New,Contacted,Qualified,Proposal,Won,Lost"')],
              summary=[("Open leads", '=COUNTA(B{R0}:B{R1})-COUNTIF(E{R0}:E{R1},"Won")-COUNTIF(E{R0}:E{R1},"Lost")', "0"),
                       ("Open pipeline value", '=SUM(F{R0}:F{R1})-SUMIF(E{R0}:E{R1},"Won",F{R0}:F{R1})-SUMIF(E{R0}:E{R1},"Lost",F{R0}:F{R1})', MONEY),
                       ("Won", '=COUNTIF(E{R0}:E{R1},"Won")', "0")])


def customer_database(path):
    build_log(path, "Customers", "Customer Database", "Keep customer contacts, spend and tier in one list. Customer count, total spend and VIP count calculate automatically",
              [("Customer", 22, "input", None), ("Contact name", 18, "input", None), ("Email", 26, "input", None),
               ("Phone", 14, "input", None), ("Town or city", 14, "input", None), ("Customer since", 13, "input", DATE),
               ("Total spent", 13, "input", MONEY), ("Last order", 13, "input", DATE), ("Tier", 11, "input", None)],
              [("Harbour Cafe", "Jordan Park", "jordan@example.com", "555-0101", "Harbour", D(2025, 4, 2), 5400, D(2026, 10, 14), "Gold"),
               ("Lee Designs", "Sam Lee", "sam@example.com", "555-0102", "Old town", D(2026, 1, 9), 900, D(2026, 6, 3), "Standard")],
              nrows=300, totals=[6],
              validations=[("J{R0}:J{R1}", '"Standard,Gold,VIP"')],
              summary=[("Customers", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total customer spend", "=SUM(H{R0}:H{R1})", MONEY),
                       ("VIP customers", '=COUNTIF(J{R0}:J{R1},"VIP")', "0")])


def sales_commission_calculator(path):
    build_log(path, "Commission", "Sales Commission Calculator", "Enter each salesperson's sales and target. Commission pays the base rate up to target and the bonus rate above it",
              [("Salesperson", 20, "input", None), ("Sales", 14, "input", MONEY), ("Target", 14, "input", MONEY),
               ("Commission", 14, '=IF(C{r}="","",IF(C{r}<=D{r},C{r}*{IN0},D{r}*{IN0}+(C{r}-D{r})*{IN1}))', MONEY),
               ("Target met?", 12, '=IF(C{r}="","",IF(C{r}>=D{r},"Yes","No"))', None)],
              [("Ana", 12000, 10000), ("Ben", 8000, 10000), ("Chloe", 15000, 12000)],
              nrows=40, totals=[1, 3],
              inputs=[("Base commission rate", 0.05, "0.0%"), ("Bonus rate above target", 0.08, "0.0%")],
              summary=[("Total commission", "=SUM(E{R0}:E{R1})", MONEY),
                       ("Targets met", '=COUNTIF(F{R0}:F{R1},"Yes")', "0")],
              note_text="Change the rates above to match your commission plan. Sales and target are in the same currency.")


def monthly_sales_forecast(path):
    build_log(path, "Forecast", "Monthly Sales Forecast", "Enter the forecast for each month and record actual sales as they come in. Variance and percentage difference calculate automatically",
              [("Month", 13, "input", DATE), ("Forecast", 14, "input", MONEY), ("Actual", 14, "input", MONEY),
               ("Variance (actual - forecast)", 17, '=IF(OR(C{r}="",D{r}=""),"",D{r}-C{r})', MONEY),
               ("Variance %", 12, '=IF(OR(C{r}="",D{r}="",N(C{r})=0),"",E{r}/C{r})', "0.0%")],
              [(D(2027, 1, 1), 20000, 18500), (D(2027, 2, 1), 21000, 22500), (D(2027, 3, 1), 22000, None)],
              nrows=24, totals=[1, 2, 3],
              summary=[("Total forecast", "=SUM(C{R0}:C{R1})", MONEY),
                       ("Total actual", "=SUM(D{R0}:D{R1})", MONEY),
                       ("Months below forecast", '=COUNTIF(E{R0}:E{R1},"<0")', "0")],
              note_text="Totals only include months with an actual figure entered.")


def seo_keyword_tracker(path):
    build_log(path, "Keywords", "SEO Keyword Tracker", "Track each target keyword's page, monthly searches and search position. The places to gain against your target calculate automatically",
              [("Keyword", 24, "input", None), ("Page", 18, "input", None), ("Monthly searches", 15, "input", "#,##0"),
               ("Current position", 14, "input", "0"), ("Target position", 14, "input", "0"),
               ("Places to gain", 14, '=IF(OR(E{r}="",F{r}=""),"",E{r}-F{r})', "0"),
               ("Last checked", 13, "input", DATE)],
              [("running shoes", "/shoes", 5400, 4, 3, D(2026, 11, 10)), ("trail running", "/trail", 1200, 9, 5, D(2026, 11, 10)),
               ("running tips", "/blog/tips", 800, 3, 3, D(2026, 11, 3))],
              nrows=100, totals=[2],
              summary=[("Keywords tracked", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("On or above target", "=SUMPRODUCT((E{R0}:E{R1}<>\"\")*(F{R0}:F{R1}<>\"\")*(E{R0}:E{R1}<=F{R0}:F{R1}))", "0"),
                       ("Average position", '=IF(COUNT(E{R0}:E{R1})=0,"",AVERAGE(E{R0}:E{R1}))', "0.0")],
              note_text="Lower position numbers are better. Places to gain shows how many places the page needs to climb.")
