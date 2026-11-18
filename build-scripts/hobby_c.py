"""Hobbies & Creative Projects templates 17-25: collections, backlog, podcasts, writing, novels, yarn, woodwork, sewing, vinyl."""
import datetime as dt
from common import *
from tplkit import build_log

REPORT = dt.date(2026, 11, 17)
D = lambda y, m, d: dt.date(y, m, d)


def stamp_coin_collection(path):
    build_log(path, "Collection", "Stamp and Coin Collection Tracker", "Record each item with its condition, purchase price and current value. Gains or losses calculate automatically",
              [("Item", 24, "input", None), ("Type", 12, "input", None), ("Country", 14, "input", None),
               ("Year", 9, "input", "0"), ("Condition", 13, "input", None), ("Purchase price", 14, "input", MONEY),
               ("Current value", 14, "input", MONEY),
               ("Gain or (loss)", 14, '=IF(OR(G{r}="",H{r}=""),"",H{r}-G{r})', MONEY)],
              [("Penny Black replica", "Stamp", "UK", 1840, "Good", 12.00, 15.00),
               ("Silver crown", "Coin", "UK", 1935, "Fair", 20.00, 18.50)],
              nrows=100, totals=[5, 6, 7],
              validations=[("C{R0}:C{R1}", '"Stamp,Coin,Note,Other"'), ("F{R0}:F{R1}", '"Mint,Good,Fair,Poor"')],
              summary=[("Items", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Collection value", "=SUM(H{R0}:H{R1})", MONEY),
                       ("Total gain or (loss)", "=SUM(I{R0}:I{R1})", MONEY)],
              note_text="Current values are estimates. Check a catalogue or dealer before insuring or selling items.")


def video_game_backlog_tracker(path):
    build_log(path, "Backlog", "Video Game Backlog Tracker", "Track each game's platform, status, hours played and priority. Counts of unplayed and finished games calculate automatically",
              [("Title", 26, "input", None), ("Platform", 14, "input", None), ("Genre", 14, "input", None),
               ("Status", 14, "input", None), ("Hours played", 12, "input", "0.0"),
               ("Priority", 11, "input", None), ("Date added", 13, "input", DATE)],
              [("Star Harbour", "Console A", "Adventure", "Playing", 12.5, "High", D(2026, 10, 1)),
               ("Puzzle game", "PC", "Puzzle", "Not started", 0, "Low", D(2026, 11, 2)),
               ("Racing game", "Console B", "Racing", "Finished", 30, "Medium", D(2026, 8, 20))],
              nrows=100, totals=[4],
              validations=[("C{R0}:C{R1}", '"Console A,Console B,PC,Mobile,Other"'),
                           ("E{R0}:E{R1}", '"Not started,Playing,Finished,Dropped"'),
                           ("G{R0}:G{R1}", '"High,Medium,Low"')],
              summary=[("Not started", '=COUNTIF(E{R0}:E{R1},"Not started")', "0"),
                       ("Finished", '=COUNTIF(E{R0}:E{R1},"Finished")', "0"),
                       ("Total hours played", "=SUM(F{R0}:F{R1})", "0.0")])


def podcast_episode_planner(path):
    build_log(path, "Episodes", "Podcast Episode Planner", "Plan each episode from idea to publication. Days until publishing calculate from the report date",
              [("Episode", 10, "input", "0"), ("Title", 26, "input", None), ("Topic", 18, "input", None),
               ("Recording date", 13, "input", DATE), ("Publish date", 13, "input", DATE), ("Status", 14, "input", None),
               ("Guest", 16, "input", None),
               ("Days to publish", 13, '=IF(OR(F{r}="",{RD}=""),"",F{r}-{RD})', "0")],
              [(1, "Welcome episode", "Introductions", D(2026, 12, 1), D(2026, 12, 8), "Scripted", None),
               (2, "Tools I use", "Productivity", D(2026, 12, 15), D(2026, 12, 22), "Idea", "Sam Lee")],
              nrows=60, report=("Report date", REPORT),
              validations=[("G{R0}:G{R1}", '"Idea,Scripted,Recorded,Edited,Published"')],
              summary=[("Episodes", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Published", '=COUNTIF(G{R0}:G{R1},"Published")', "0"),
                       ("Next publish in (days)", '=IF(COUNTIF(I{R0}:I{R1},">=0")=0,"",_xlfn.MINIFS(I{R0}:I{R1},I{R0}:I{R1},">=0"))', "0")])


def writing_word_count_tracker(path):
    build_log(path, "Words", "Writing Word Count Tracker", "Log words written each day for each project. Project totals and days that met your goal calculate automatically",
              [("Date", 12, "input", DATE), ("Project", 22, "input", None), ("Words written", 14, "input", "#,##0"),
               ("Project total", 14, '=IF(OR(C{r}="",D{r}=""),"",SUMIF($C${R0}:$C${R1},C{r},$D${R0}:$D${R1}))', "#,##0"),
               ("Goal met?", 12, '=IF(D{r}="","",IF(D{r}>={IN0},"Yes","No"))', None)],
              [(D(2027, 1, 4), "Short stories", 620), (D(2027, 1, 5), "Short stories", 310), (D(2027, 1, 5), "Blog", 200)],
              nrows=200, totals=[2],
              inputs=[("Daily word goal", 500, "#,##0")],
              summary=[("Words written", "=SUM(D{R0}:D{R1})", "#,##0"),
                       ("Days goal met", '=COUNTIF(F{R0}:F{R1},"Yes")', "0"),
                       ("Entries logged", "=COUNT(B{R0}:B{R1})", "0")])


def novel_chapter_outline_planner(path):
    build_log(path, "Chapters", "Novel Chapter Outline Planner", "Outline each chapter with its target and words written. Progress and overall completion calculate automatically",
              [("Chapter", 10, "input", "0"), ("Title", 22, "input", None), ("Summary", 36, "input", None),
               ("Target words", 13, "input", "#,##0"), ("Words written", 13, "input", "#,##0"),
               ("Progress", 11, '=IF(OR(E{r}="",N(E{r})=0),"",MIN(1,N(F{r})/E{r}))', "0%"),
               ("Stage", 13, "input", None)],
              [(1, "The arrival", "Protagonist reaches the city", 3000, 3150, "Revised"),
               (2, "First clue", "A letter turns up", 2500, 800, "Draft")],
              nrows=40, totals=[4, 5],
              validations=[("H{R0}:H{R1}", '"Idea,Outline,Draft,Revised,Final"')],
              summary=[("Chapters", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Words written", "=SUM(F{R0}:F{R1})", "#,##0"),
                       ("Overall progress", '=IF(SUM(E{R0}:E{R1})=0,"",SUM(F{R0}:F{R1})/SUM(E{R0}:E{R1}))', "0%")])


def yarn_stash_inventory(path):
    build_log(path, "Stash", "Yarn Stash Inventory", "Record each yarn with its weight, skeins and metres per skein. Total metres and the project you planned it for are shown",
              [("Yarn name", 20, "input", None), ("Brand", 14, "input", None), ("Fibre", 14, "input", None),
               ("Colour", 14, "input", None), ("Weight", 12, "input", None), ("Skeins", 10, "input", "0"),
               ("Metres per skein", 13, "input", "0"),
               ("Total metres", 13, '=IF(OR(G{r}="",H{r}=""),"",G{r}*H{r})', "#,##0"),
               ("Planned project", 22, "input", None)],
              [("Merino sport", "Brand A", "Merino", "Forest green", "Fingering", 4, 400, "Winter scarf"),
               ("Cotton DK", "Brand B", "Cotton", "Cream", "DK", 2, 210, None)],
              nrows=80, totals=[5, 7],
              validations=[("F{R0}:F{R1}", '"Lace,Fingering,DK,Aran,Chunky"')],
              summary=[("Yarn types", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total skeins", "=SUM(G{R0}:G{R1})", "0"),
                       ("Total metres", "=SUM(I{R0}:I{R1})", "#,##0")])


def woodworking_cut_list(path):
    build_log(path, "Cut list", "Woodworking Cut List", "List each part with its quantity and size in millimetres. Face area and total area calculate automatically. Add saw kerf to the lengths yourself",
              [("Part", 22, "input", None), ("Qty", 8, "input", "0"), ("Length (mm)", 13, "input", "#,##0"),
               ("Width (mm)", 13, "input", "#,##0"), ("Thickness (mm)", 13, "input", "0"), ("Board", 16, "input", None),
               ("Face area (m²)", 13, '=IF(OR(C{r}="",D{r}="",E{r}=""),"",C{r}*D{r}*E{r}/1000000)', "0.000")],
              [("Side panel", 2, 720, 300, 18, "Plywood sheet"), ("Shelf", 3, 600, 280, 18, "Plywood sheet"),
               ("Back panel", 1, 720, 600, 6, "Hardboard")],
              nrows=40, totals=[1, 6],
              summary=[("Pieces to cut", "=SUM(C{R0}:C{R1})", "0"),
                       ("Total face area (m²)", "=SUM(H{R0}:H{R1})", "0.000")],
              note_text="Face area is the length times the width for each piece, multiplied by the quantity.")


def sewing_measurement_chart(path):
    build_log(path, "Sizes", "Sewing Measurement Chart", "Compare each pattern size with your body measurements. The ease shows the room the pattern allows, in centimetres",
              [("Size", 10, "input", None), ("Bust (cm)", 12, "input", "0.0"), ("Waist (cm)", 12, "input", "0.0"),
               ("Hip (cm)", 12, "input", "0.0"),
               ("Bust ease", 12, '=IF(OR(C{r}="",{IN0}=""),"",C{r}-{IN0})', "0.0"),
               ("Waist ease", 12, '=IF(OR(D{r}="",{IN1}=""),"",D{r}-{IN1})', "0.0"),
               ("Hip ease", 12, '=IF(OR(E{r}="",{IN2}=""),"",E{r}-{IN2})', "0.0")],
              [("S", 86, 68, 92), ("M", 90, 72, 96), ("L", 94, 76, 100)],
              nrows=12,
              inputs=[("My bust (cm)", 90, "0.0"), ("My waist (cm)", 72, "0.0"), ("My hip (cm)", 96, "0.0")],
              summary=[("Sizes listed", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Sizes with 0 to 10 cm bust ease", '=COUNTIFS(F{R0}:F{R1},">=0",F{R0}:F{R1},"<=10")', "0")],
              note_text="Use a soft tape measure over light clothing. Ease is the pattern measurement minus your measurement.")


def vinyl_record_catalogue(path):
    build_log(path, "Records", "Vinyl Record Catalogue", "Catalogue each record with its format, label, condition and price. Total and average cost calculate automatically",
              [("Artist", 20, "input", None), ("Album", 22, "input", None), ("Year", 9, "input", "0"),
               ("Format", 12, "input", None), ("Label", 16, "input", None), ("Price paid", 13, "input", MONEY),
               ("Condition", 12, "input", None), ("Date bought", 13, "input", DATE)],
              [("The Blue Vessels", "First album", 1979, "LP", "Label A", 22.00, "VG+", D(2026, 9, 5)),
               ("Harbour Quartet", "Live recording", 1985, "12in", "Label B", 15.50, "VG", D(2026, 10, 12))],
              nrows=300, totals=[5],
              validations=[("E{R0}:E{R1}", '"LP,7in,12in,Box set,Other"'), ("H{R0}:H{R1}", '"Mint,VG+,VG,Good,Fair"')],
              summary=[("Records", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Total paid", "=SUM(G{R0}:G{R1})", MONEY),
                       ("Average price", '=IF(COUNT(G{R0}:G{R1})=0,"",AVERAGE(G{R0}:G{R1}))', MONEY)])
