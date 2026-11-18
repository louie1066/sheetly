"""Hobbies & Creative Projects templates 9-16: games, fantasy league, practice, chords, art supplies, seeds, fishing, birds."""
import datetime as dt
from common import *
from tplkit import build_log

D = lambda y, m, d: dt.date(y, m, d)
T = lambda h, m: dt.time(h, m)


def board_game_score_tracker(path):
    build_log(path, "Scores", "Board Game Score Tracker", "Record each player's score for each game session. The winner of each game is marked automatically",
              [("Game", 20, "input", None), ("Date", 12, "input", DATE), ("Player", 16, "input", None),
               ("Score", 10, "input", "0"),
               ("Winner?", 12, '=IF(OR(B{r}="",E{r}=""),"",IF(E{r}=_xlfn.MAXIFS($E${R0}:$E${R1},$B${R0}:$B${R1},B{r}),"Winner",""))', None)],
              [("Catan", D(2027, 1, 5), "Ana", 8), ("Catan", D(2027, 1, 5), "Ben", 10), ("Chess night", D(2027, 1, 12), "Chloe", 3)],
              nrows=100,
              summary=[("Scores recorded", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Wins", '=COUNTIF(F{R0}:F{R1},"Winner")', "0"),
                       ("Highest score", '=IF(COUNT(E{R0}:E{R1})=0,"",MAX(E{R0}:E{R1}))', "0")],
              note_text="The winner is the highest score for that game. Ties show more than one winner.")


def fantasy_league_points(path):
    build_log(path, "Points", "Fantasy League Points Calculator", "Enter each player's weekly stats. Points calculate from the scoring rules set above the table",
              [("Player", 18, "input", None), ("Week", 8, "input", "0"), ("Goals", 9, "input", "0"),
               ("Assists", 9, "input", "0"), ("Yellow cards", 12, "input", "0"),
               ("Points", 10, '=IF(B{r}="","",N(D{r})*{IN0}+N(E{r})*{IN1}+N(F{r})*{IN2})', "0")],
              [("Ana", 1, 2, 1, 0), ("Ben", 1, 0, 2, 1), ("Chloe", 1, 1, 0, 0)],
              nrows=100, totals=[2, 3, 4, 5],
              inputs=[("Points per goal", 4, "0"), ("Points per assist", 3, "0"), ("Points per yellow card", -1, "0")],
              summary=[("Top scorer on points", '=IF(COUNT(G{R0}:G{R1})=0,"",INDEX(B{R0}:B{R1},MATCH(MAX(G{R0}:G{R1}),G{R0}:G{R1},0)))', None),
                       ("Top points", '=IF(COUNT(G{R0}:G{R1})=0,"",MAX(G{R0}:G{R1}))', "0")],
              note_text="Change the points above to match your league rules. Negative values take points away.")


def music_practice_log(path):
    build_log(path, "Practice", "Music Practice Log", "Log each practice session with its focus, tempo and whether you reached your goal. Total minutes and hours calculate automatically",
              [("Date", 12, "input", DATE), ("Piece or exercise", 24, "input", None), ("Instrument", 14, "input", None),
               ("Minutes", 10, "input", "0"), ("Focus", 16, "input", None), ("Tempo (bpm)", 11, "input", "0"),
               ("Goal reached?", 13, "input", None), ("Notes", 26, "input", None)],
              [(D(2027, 1, 4), "Scale of C major", "Piano", 25, "Technique", 80, "Yes", "Hands separate"),
               (D(2027, 1, 6), "Prelude in G", "Piano", 40, "Repertoire", 60, "No", "Left hand stumbles")],
              nrows=120, totals=[3],
              validations=[("F{R0}:F{R1}", '"Technique,Repertoire,Sight-reading,Theory,Other"'), ("H{R0}:H{R1}", '"Yes,No"')],
              summary=[("Sessions", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Total minutes", "=SUM(E{R0}:E{R1})", "#,##0"),
                       ("Total hours", "=SUM(E{R0}:E{R1})/60", "0.0")])


def song_chord_planner(path):
    build_log(path, "Chords", "Song Chord Planner", "Plan the chords for each section of a song with beats and strumming. The key and total beats calculate for the song",
              [("Section", 14, "input", None), ("Chord", 12, "input", None), ("Beats", 10, "input", "0"),
               ("Strumming pattern", 22, "input", None), ("Notes", 26, "input", None)],
              [("Verse", "C", 4, "Down, down, up", None), ("Verse", "Am", 4, "Down, down, up", None),
               ("Chorus", "F", 4, "Down-up pattern", "Build dynamics")],
              nrows=40, totals=[2],
              validations=[("B{R0}:B{R1}", '"Intro,Verse,Pre-chorus,Chorus,Bridge,Outro"')],
              inputs=[("Song key", "C major", None)],
              summary=[("Song key", "={IN0}", None),
                       ("Chords planned", "=COUNTA(C{R0}:C{R1})", "0"),
                       ("Total beats", "=SUM(D{R0}:D{R1})", "0")],
              note_text="Set the song's key above the table. Use one row per chord change.")


def art_supply_inventory(path):
    build_log(path, "Supplies", "Art Supply Inventory", "Record each art supply with its quantity and cost. Stock value and reorder alerts calculate automatically",
              [("Item", 22, "input", None), ("Brand", 14, "input", None), ("Type", 14, "input", None),
               ("Colour or size", 14, "input", None), ("Quantity", 10, "input", "0"), ("Cost each", 12, "input", MONEY),
               ("Stock value", 13, '=IF(OR(F{r}="",G{r}=""),"",F{r}*G{r})', MONEY),
               ("Reorder at", 11, "input", "0"),
               ("Status", 13, '=IF(OR(F{r}="",I{r}=""),"",IF(F{r}<=N(I{r}),"Reorder","OK"))', None)],
              [("Acrylic paint", "Brand A", "Paint", "White 200ml", 2, 6.50, 1),
               ("Sketch paper", "Brand B", "Paper", "A4, 120gsm", 0, 8.00, 2),
               ("Round brush", "Brand C", "Brush", "Size 6", 3, 4.00, 1)],
              nrows=80, totals=[6],
              validations=[("D{R0}:D{R1}", '"Paint,Pencil,Brush,Paper,Canvas,Other"')],
              summary=[("Items", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Total stock value", "=SUM(H{R0}:H{R1})", MONEY),
                       ("Need reordering", '=COUNTIF(J{R0}:J{R1},"Reorder")', "0")])


def seed_library_tracker(path):
    build_log(path, "Seeds", "Seed Library Tracker", "Record each seed variety with its packets, harvest year and germination rate. Seeds to test before sowing are flagged",
              [("Variety", 22, "input", None), ("Type", 14, "input", None), ("Year harvested", 13, "input", "0"),
               ("Packets", 10, "input", "0"), ("Germination rate", 14, "input", "0%"),
               ("Sowing status", 16, '=IF(F{r}="","",IF(F{r}>=0.7,"Good",IF(F{r}>=0.5,"Fair","Test first")))', None),
               ("Notes", 26, "input", None)],
              [("Tomato, Gardener's Red", "Vegetable", 2026, 3, 0.85, "Sow in March"),
               ("Basil, Sweet", "Herb", 2024, 2, 0.45, "Test before sowing"),
               ("Sunflower, Dwarf", "Flower", 2025, 5, 0.70, None)],
              nrows=100, totals=[3],
              validations=[("C{R0}:C{R1}", '"Vegetable,Herb,Flower,Other"')],
              summary=[("Varieties", "=COUNTA(B{R0}:B{R1})", "0"),
                       ("Packets in stock", "=SUM(E{R0}:E{R1})", "0"),
                       ("Test before sowing", '=COUNTIF(G{R0}:G{R1},"Test first")', "0")],
              note_text="Germination falls as seed ages. Test older seed on a damp paper towel before sowing.")


def fishing_catch_log(path):
    build_log(path, "Catches", "Fishing Catch Log", "Log each catch with its date, location, size and whether you released it. Totals and records calculate automatically",
              [("Date", 12, "input", DATE), ("Location", 20, "input", None), ("Species", 16, "input", None),
               ("Length (cm)", 12, "input", "0.0"), ("Weight (kg)", 12, "input", "0.00"),
               ("Method", 14, "input", None), ("Released?", 11, "input", None), ("Notes", 26, "input", None)],
              [(D(2027, 3, 3), "Lake North", "Perch", 22.5, 0.35, "Spinner", "Yes", "Calm morning"),
               (D(2027, 3, 10), "River bend", "Trout", 34.0, 0.80, "Fly", "No", None)],
              nrows=100,
              validations=[("H{R0}:H{R1}", '"Yes,No"')],
              summary=[("Catches", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Released", '=COUNTIF(H{R0}:H{R1},"Yes")', "0"),
                       ("Longest (cm)", '=IF(COUNT(E{R0}:E{R1})=0,"",MAX(E{R0}:E{R1}))', "0.0"),
                       ("Heaviest (kg)", '=IF(COUNT(F{R0}:F{R1})=0,"",MAX(F{R0}:F{R1}))', "0.00")])


def bird_watching_log(path):
    build_log(path, "Sightings", "Bird Watching Log", "Record each sighting with the count and behaviour. Total birds and the number of different species calculate automatically",
              [("Date", 12, "input", DATE), ("Location", 20, "input", None), ("Species", 18, "input", None),
               ("Count", 9, "input", "0"), ("Behaviour", 18, "input", None), ("Time", 9, "input", "hh:mm"),
               ("Weather", 14, "input", None), ("Notes", 26, "input", None)],
              [(D(2027, 2, 6), "Park pond", "Mallard", 6, "Feeding", T(8, 15), "Clear", None),
               (D(2027, 2, 6), "Park pond", "Heron", 1, "Hunting", T(8, 40), "Clear", "By the reeds")],
              nrows=150,
              summary=[("Sightings", "=COUNTA(D{R0}:D{R1})", "0"),
                       ("Total birds counted", "=SUM(E{R0}:E{R1})", "0"),
                       ("Different species", '=SUMPRODUCT((D{R0}:D{R1}<>"")/COUNTIF(D{R0}:D{R1},D{R0}:D{R1}&""))', "0")])
