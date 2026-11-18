"""Hobbies & Creative Projects templates 1-8: photography, recipes, baking, brewing, knitting, model railways, reading, films."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda y, m, d: dt.date(y, m, d)


def photography_shot_log(path):
    build_log(path, "Shots", "Photography Shot Log", "Log each shot with its settings and rating. Keeper count and average rating calculate automatically",
              [("Date", 12, "input", DATE), ("Subject", 22, "input", None), ("Lens", 14, "input", None),
               ("Aperture", 10, "input", None), ("Shutter", 10, "input", None), ("ISO", 9, "input", "0"),
               ("Rating (1-5)", 12, "input", "0"), ("Keeper?", 10, "input", None)],
              [(D(2027, 3, 1), "Harbour at dawn", "35mm prime", "f/8", "1/125", 200, 4, "Yes"),
               (D(2027, 3, 2), "Street market", "35mm prime", "f/2.8", "1/250", 400, 3, "No")],
              nrows=60,
              validations=[("H{R0}:H{R1}", ("whole", "1", "5")), ("I{R0}:I{R1}", '"Yes,No"')],
              summary=[("Shots logged", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Keepers", '=COUNTIF(I{R0}:I{R1},"Yes")', "0"),
                       ("Average rating", '=IF(COUNT(H{R0}:H{R1})=0,"",AVERAGE(H{R0}:H{R1}))', "0.0")])


def recipe_cost_per_serving(path):
    build_log(path, "Recipe", "Recipe Book with Cost per Serving", "List each ingredient with its quantity and price per unit. Line costs and the cost per serving calculate automatically",
              [("Recipe", 20, "input", None), ("Ingredient", 20, "input", None), ("Quantity", 11, "input", "0.00"),
               ("Unit", 10, "input", None), ("Price per unit", 13, "input", "0.0000"),
               ("Line cost", 13, '=IF(OR(D{r}="",F{r}=""),"",D{r}*F{r})', MONEY)],
              [("Banana bread", "Flour", 300, "g", 0.0030), ("Banana bread", "Bananas", 3, "each", 0.40),
               ("Banana bread", "Sugar", 150, "g", 0.0025)],
              nrows=40, totals=[5],
              inputs=[("Servings", 6, "0")],
              summary=[("Total ingredient cost", "=SUM(G{R0}:G{R1})", MONEY),
                       ("Cost per serving", '=IF(N({IN0})=0,"",SUM(G{R0}:G{R1})/{IN0})', MONEY)],
              note_text="Enter each price for the same unit as the quantity, for example price per gram with quantity in grams.")


def baking_ratio_calculator(path):
    build_log(path, "Ratios", "Baking Ratio Calculator", "Enter each ingredient's weight with flour in the first row. Baker's percentages and scaled weights calculate automatically",
              [("Ingredient", 20, "input", None), ("Weight (g)", 13, "input", "0.0"),
               ("Baker's %", 12, '=IF(OR(C{r}="",N($C${R0})=0),"",C{r}/$C${R0})', "0.0%"),
               ("Scaled weight (g)", 16, '=IF(D{r}="","",D{r}*{IN0})', "0.0")],
              [("Flour", 500), ("Water", 350), ("Salt", 10), ("Yeast", 5)],
              nrows=20,
              inputs=[("Target flour weight (g)", 800, "0")],
              summary=[("Hydration (water / flour)", '=IF(N($C${R0})=0,"",SUMIF(B{R0}:B{R1},"Water",C{R0}:C{R1})/$C${R0})', "0.0%"),
                       ("Total scaled dough weight (g)", "=SUM(E{R0}:E{R1})", "0.0")],
              note_text="Put the flour in the first row. Baker's percentages compare each ingredient with the flour weight.")


def home_brewing_log(path):
    build_log(path, "Batches", "Home Brewing Log", "Record each batch's gravity readings. Alcohol by volume calculates from the original and final gravity",
              [("Batch", 12, "input", None), ("Brew date", 13, "input", DATE), ("Style", 18, "input", None),
               ("Original gravity", 12, "input", "0.000"), ("Final gravity", 12, "input", "0.000"),
               ("ABV (%)", 10, '=IF(OR(E{r}="",F{r}=""),"",ROUND((E{r}-F{r})*131.25,1))', "0.0"),
               ("Bottled on", 13, "input", DATE), ("Notes", 26, "input", None)],
              [("Batch 01", D(2027, 2, 1), "Pale ale", 1.050, 1.010, D(2027, 2, 15), "Dry hopped"),
               ("Batch 02", D(2027, 3, 1), "Stout", 1.062, 1.018, None, None)],
              nrows=30,
              summary=[("Batches", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Batches bottled", "=COUNT(H{R0}:H{R1})", "0"),
                       ("Average ABV (%)", '=IF(COUNT(G{R0}:G{R1})=0,"",AVERAGE(G{R0}:G{R1}))', "0.0")],
              note_text="ABV uses the standard formula: (original gravity - final gravity) x 131.25.")


def knitting_row_counter(path):
    build_log(path, "Projects", "Knitting Pattern Row Counter", "Update rows done after each session. Rows left and progress calculate from the rows in your pattern",
              [("Project", 20, "input", None), ("Pattern", 20, "input", None), ("Date", 12, "input", DATE),
               ("Rows done", 11, "input", "0"), ("Rows in pattern", 14, "input", "0"),
               ("Rows left", 11, '=IF(OR(E{r}="",F{r}=""),"",MAX(0,F{r}-E{r}))', "0"),
               ("Progress", 11, '=IF(OR(E{r}="",N(F{r})=0),"",MIN(1,E{r}/F{r}))', "0%")],
              [("Winter scarf", "Ribbed scarf", D(2027, 1, 10), 120, 300), ("Hat", "Beanie, 2 sizes", D(2027, 1, 12), 40, 90)],
              nrows=20,
              summary=[("Projects", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Average progress", '=IF(COUNT(H{R0}:H{R1})=0,"",AVERAGE(H{R0}:H{R1}))', "0%")],
              note_text="Use the row counter on your pattern or a stitch marker to keep rows done accurate.")


def model_railway_inventory(path):
    build_log(path, "Inventory", "Model Railway Inventory", "Record each item with its scale, type, condition and price. Total cost and repair needs calculate automatically",
              [("Item", 24, "input", None), ("Scale", 10, "input", None), ("Type", 14, "input", None),
               ("Maker", 16, "input", None), ("Purchase price", 14, "input", MONEY),
               ("Condition", 14, "input", None), ("Running?", 11, "input", None)],
              [("Class 66 locomotive", "OO", "Loco", "Maker A", 145, "Good", "Yes"),
               ("Goods wagon", "OO", "Wagon", "Maker B", 18, "Needs repair", "No"),
               ("Station building", "N", "Building", "Maker C", 30, "Fair", "No")],
              nrows=60, totals=[4],
              validations=[("C{R0}:C{R1}", '"OO,HO,N,TT,Z,O,G,Other"'),
                           ("D{R0}:D{R1}", '"Loco,Wagon,Coach,Track,Building,Scenery,Other"'),
                           ("G{R0}:G{R1}", '"Good,Fair,Needs repair"'), ("H{R0}:H{R1}", '"Yes,No"')],
              summary=[("Items", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total purchase cost", "=SUM(F{R0}:F{R1})", MONEY),
                       ("Items needing repair", '=COUNTIF(G{R0}:G{R1},"Needs repair")', "0")])


def book_reading_tracker(path):
    build_log(path, "Books", "Book Reading Tracker", "Log each book with its dates, pages and rating. Days to finish and totals calculate automatically",
              [("Title", 26, "input", None), ("Author", 18, "input", None), ("Genre", 14, "input", None),
               ("Started", 12, "input", DATE), ("Finished", 12, "input", DATE), ("Pages", 10, "input", "0"),
               ("Days to finish", 12, '=IF(OR(E{r}="",F{r}=""),"",F{r}-E{r})', "0"),
               ("Rating (1-5)", 12, "input", "0")],
              [("The Lighthouse Keeper", "A. Writer", "Fiction", D(2027, 1, 2), D(2027, 1, 20), 320, 4)],
              nrows=60, totals=[5],
              validations=[("I{R0}:I{R1}", ("whole", "1", "5"))],
              summary=[("Books finished", "=COUNT(F{R0}:F{R1})", "0"),
                       ("Pages read", "=SUM(G{R0}:G{R1})", "#,##0"),
                       ("Average rating", '=IF(COUNT(I{R0}:I{R1})=0,"",AVERAGE(I{R0}:I{R1}))', "0.0")])


def film_watch_log(path):
    build_log(path, "Films", "Film Watch Log", "Log each film or episode with where you watched it and your rating. Totals and averages calculate automatically",
              [("Title", 26, "input", None), ("Year", 9, "input", "0"), ("Genre", 14, "input", None),
               ("Date watched", 13, "input", DATE), ("Format", 14, "input", None),
               ("Rating (1-5)", 12, "input", "0"), ("Rewatch?", 11, "input", None), ("Notes", 26, "input", None)],
              [("City Lights Story", 2019, "Drama", D(2027, 2, 14), "Streaming", 4, "Yes", "Watched with friends"),
               ("Second Feature", 2023, "Comedy", D(2027, 2, 20), "Cinema", 3, "No", None)],
              nrows=80,
              validations=[("F{R0}:F{R1}", '"Cinema,Streaming,Disc,Other"'), ("G{R0}:G{R1}", ("whole", "1", "5")),
                           ("H{R0}:H{R1}", '"Yes,No"')],
              summary=[("Films watched", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Average rating", '=IF(COUNT(G{R0}:G{R1})=0,"",AVERAGE(G{R0}:G{R1}))', "0.0"),
                       ("Would rewatch", '=COUNTIF(H{R0}:H{R1},"Yes")', "0")])
