"""Generate the category page, the Most Downloaded page, the template catalogue and the download function.

Run from anywhere:  python3 /home/claude/build/build_site.py
"""
import json
import os
import re

SITE = "/home/claude/site"
PAGE_SIZE = 25

# ---------------------------------------------------------------- catalogue
CATEGORIES = {
    "personal-finance": "Personal Finance & Budgeting",
    "education": "Education & Classroom",
    "it-computing": "IT & Computing",
    "small-business": "Small Business & Invoicing",
    "project-management": "Project & Task Management",
    "health-fitness": "Health, Fitness & Wellbeing",
    "home-household": "Home & Household",
    "travel-events": "Travel & Events",
    "hobbies-creative-projects": "Hobbies & Creative Projects",
    "sales-marketing-operations": "Sales, Marketing & Operations",
}

CATEGORY_INTRO = {
    "personal-finance": "Free Excel templates for budgets, debt payoff, loans, savings and everyday money tracking. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "education": "Free Excel templates for gradebooks, registers, lesson and scheme planning, rubrics, mark sheets and classroom admin. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "it-computing": "Free Excel templates for IT asset registers, help desk and backup logs, network planning, sprint and bug tracking, and computing classroom practice. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "small-business": "Free Excel templates for invoices, quotes, cash flow, payroll, VAT, stock and pricing for small businesses. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "project-management": "Free Excel templates for Gantt charts, Kanban boards, project budgets, risk registers, RACI matrices, meeting and decision logs, and work planning. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "health-fitness": "Free Excel templates for workouts, meal and water logs, sleep, habits, body measurements and appointment reminders. Each file has a logo header, a How to use sheet, and formulas that calculate for you. They are records, not medical advice.",
    "home-household": "Free Excel templates for chore rotas, maintenance and cleaning schedules, household inventories, meal shopping, bills, garden planting, moving, vehicles and more. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "travel-events": "Free Excel templates for trip itineraries, travel budgets, packing, passports and visas, flights and hotels, event budgets, guest lists, run sheets, volunteers and wedding planning. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "hobbies-creative-projects": "Free Excel templates for photography logs, recipes and baking, brewing, knitting and yarn stashes, woodworking cut lists, sewing charts, collections, reading and film logs, games, music practice, writing and podcasts. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
    "sales-marketing-operations": "Free Excel templates for social media calendars, email and ad campaigns, marketing ROI, leads and customers, commission, sales forecasts, customer feedback, support tickets, warehouse picking, shipping, food costs, staff training, leave, reviews, recruitment and shift handovers. Each file has a logo header, a How to use sheet, and formulas that calculate for you.",
}

CATEGORY_DESC = {
    "personal-finance": "Free Excel templates for budgets, debt payoff, loans, savings and personal money tracking. CC BY 4.0.",
    "education": "Free Excel templates for gradebooks, attendance, marking, lesson planning and classroom admin. CC BY 4.0.",
    "it-computing": "Free Excel templates for IT asset registers, help desk logs, network planning, sprint tracking and computing practice. CC BY 4.0.",
    "small-business": "Free Excel templates for invoices, cash flow, payroll, VAT, stock and pricing for small businesses. CC BY 4.0.",
    "project-management": "Free Excel templates for Gantt charts, task lists, risk registers, RACI matrices, decision logs, OKRs and project status. CC BY 4.0.",
    "health-fitness": "Free Excel templates for workouts, meal and water logs, sleep, habits, readings and appointments. Records only, not medical advice. CC BY 4.0.",
    "home-household": "Free Excel templates for chores, maintenance, inventories, shopping, bills, garden planting, moving and vehicle upkeep. CC BY 4.0.",
    "travel-events": "Free Excel templates for trip planning, travel budgets, documents, event budgets, guest lists, weddings and volunteer rotas. CC BY 4.0.",
    "hobbies-creative-projects": "Free Excel templates for photography, recipes, brewing, knitting, woodworking, collections, reading, games, music, writing and podcasts. CC BY 4.0.",
    "sales-marketing-operations": "Free Excel templates for marketing, sales pipelines, customer feedback, support tickets, warehouse picking, shipping, food costs and staff records. CC BY 4.0.",
}

TEMPLATES = [
    ("monthly-household-budget-planner", "Monthly Household Budget", "Plan income and spending each month, then compare planned against actual."),
    ("zero-based-budget", "Zero-Based Budget", "Give every pound a job until nothing is left unassigned."),
    ("envelope-budgeting-tracker", "Envelope Budgeting Tracker", "Fixed envelopes for each spending area, with what is left at a glance."),
    ("expense-tracker", "Expense Tracker", "Log each spend and see totals by category on a summary sheet."),
    ("income-vs-expenses-summary", "Income vs Expenses Summary", "A twelve-month view of income, spending, net result and savings rate."),
    ("debt-snowball-calculator", "Debt Snowball Calculator", "Clear the smallest debts first while paying minimums on the rest."),
    ("debt-avalanche-calculator", "Debt Avalanche Calculator", "Clear the highest-rate debt first to reduce total interest."),
    ("loan-amortisation-schedule", "Loan Amortisation Schedule", "Monthly repayments split into interest and principal, with the balance over time."),
    ("mortgage-repayment-calculator", "Mortgage Repayment Calculator", "Estimate monthly repayments, total interest and total cost of a home loan."),
    ("car-loan-comparison", "Car Loan Comparison", "Compare up to three car finance offers by total cost."),
    ("savings-goal-tracker", "Savings Goal Tracker", "Log deposits and track progress towards a savings target."),
    ("emergency-fund-calculator", "Emergency Fund Calculator", "Work out your emergency fund target from essential monthly costs."),
    ("net-worth-tracker", "Net Worth Tracker", "Record assets and liabilities to see your net worth over time."),
    ("subscription-cost-tracker", "Subscription Cost Tracker", "See what recurring subscriptions cost per month and per year."),
    ("bill-payment-calendar", "Bill Payment Calendar", "Track due days, amounts and which bills are paid this month."),
    ("annual-cash-flow-forecast", "Annual Cash-Flow Forecast", "Forecast your bank balance month by month and spot the low point."),
    ("credit-card-payoff-planner", "Credit Card Payoff Planner", "See how long a card balance takes to clear and the interest you will pay."),
    ("retirement-savings-projection", "Retirement Savings Projection", "Project how savings could grow from today until retirement age."),
    ("compound-interest-calculator", "Compound Interest Calculator", "See how a starting amount and regular saving grow with interest."),
    ("sinking-funds-planner", "Sinking Funds Planner", "Set aside a fixed amount each month for costs that come once a year."),
    ("tax-estimate-calculator", "Tax Estimate Calculator", "Estimate income tax using progressive bands. Check your local rules."),
    ("freelancer-income-tracker", "Freelancer Income Tracker", "Log work and payments, and set aside money for tax automatically."),
    ("price-comparison-sheet", "Price Comparison Sheet", "Compare prices per unit to find the best value across options."),
    ("weekly-grocery-budget", "Weekly Grocery Budget", "Track weekly food spending against a set budget."),
    ("holiday-gift-budget", "Holiday Gift Budget", "Plan gifts within a budget and record what you actually spend."),
    ("gradebook-weighted-averages", "Gradebook with Weighted Averages", "Enter marks and weights to get each student's weighted percentage and grade."),
    ("attendance-register", "Attendance Register", "Record present, late, absent and authorised codes, with attendance % per student."),
    ("seating-plan-generator", "Seating Plan Generator", "Type names in list order and see them placed on a classroom grid."),
    ("lesson-plan-template", "Lesson Plan Template", "Plan objectives, stages and timings, and check that the lesson fits."),
    ("scheme-of-work-planner", "Scheme of Work Planner", "Plan lessons week by week and track how many have been taught."),
    ("termly-timetable", "Termly Timetable", "Build a weekly timetable and count lessons per subject automatically."),
    ("rubric-scoring-sheet", "Rubric Scoring Sheet", "Score work against weighted criteria on a 1 to 4 scale."),
    ("mark-sheet-grade-boundaries", "Mark Sheet with Grade Boundaries", "Convert marks to grades using your own boundary table, with pass or fail."),
    ("assessment-tracker-learning-objective", "Assessment Tracker by Learning Objective", "Track each student against learning objectives as not yet, developing or secure."),
    ("student-progress-tracker", "Student Progress Tracker", "Follow test results over time and flag students who need support or stretch."),
    ("homework-tracker", "Homework Tracker", "Log on-time, late and missing homework for each student and task."),
    ("behaviour-points-log", "Behaviour Points Log", "Log positive and negative points, with totals for each student."),
    ("parent-contact-log", "Parent Contact Log", "Record contacts with parents and carers, and track open follow-ups."),
    ("class-roster", "Class Roster", "Keep a simple class list with tutor groups and counts for each group."),
    ("reading-log", "Reading Log", "Record books read, pages and dates, with days taken and pages per day."),
    ("quiz-score-analyser", "Quiz Score Analyser", "See each student's score and how hard each question was for the class."),
    ("exam-timetable-planner", "Exam Timetable Planner", "Plan exam dates, times and rooms, and flag students with two exams on one day."),
    ("revision-schedule", "Revision Schedule", "Plan revision hours by topic and track hours done and left."),
    ("student-project-tracker", "Student Project Tracker", "Track project milestones, due dates and overdue work."),
    ("lab-equipment-booking", "Lab Equipment Booking", "Book rooms and equipment by period, and flag clashes and over-booked stock."),
    ("classroom-budget-tracker", "Classroom Budget Tracker", "Set category budgets and log spending against them."),
    ("club-signup-sheet", "Club Sign-up Sheet", "Count first-choice sign-ups per club and see spaces left."),
    ("group-work-rotation-planner", "Group-Work Rotation Planner", "Rotate students through groups each round and check the group sizes."),
    ("report-card-comment-bank", "Report Card Comment Bank", "Build report comments from a bank of coded phrases, with word counts."),
    ("course-completion-checklist", "Course Completion Checklist", "Track course items by unit and see percent complete."),
    ("it-asset-register", "IT Asset Register", "Track devices by type, location and cost, and flag older equipment."),
    ("software-licence-tracker", "Software Licence Tracker", "Compare licences owned with seats used and see renewals coming up."),
    ("help-desk-ticket-log", "Help Desk Ticket Log", "Log support tickets and check resolution times against priority targets."),
    ("server-backup-log", "Server Backup Schedule Log", "Log backup runs and see the success rate for each server."),
    ("ip-address-planner", "IP Address Planner", "Work out subnet block sizes and prefixes for each department's hosts."),
    ("network-device-inventory", "Network Device Inventory", "Record network devices and track warranty expiry dates."),
    ("hardware-refresh-planner", "Hardware Refresh Planner", "Plan replacement dates for devices and the budget needed to replace them."),
    ("sprint-backlog-burndown", "Sprint Backlog and Burndown", "Track sprint tasks and compare remaining points with the ideal burndown line."),
    ("bug-tracker", "Bug Tracker", "Log bugs by severity and status, and see how long each has been open."),
    ("test-case-log", "Test Case Log", "Record tests with expected and actual results, and calculate the pass rate."),
    ("code-review-checklist", "Code Review Checklist", "Review code files against a checklist and see the pass rate for each file."),
    ("website-traffic-summary", "Website Traffic Summary", "Track monthly visits and page views, with changes and the busiest month."),
    ("cloud-cost-estimator", "Cloud Cost Estimator", "Estimate monthly and yearly cloud costs, with a contingency allowance."),
    ("uptime-incident-log", "Uptime and Incident Log", "Log outages and calculate downtime and uptime for the month."),
    ("change-request-log", "Change Request Log", "Track change requests through approval and delivery, and flag overdue work."),
    ("data-cleansing-checklist", "Data Cleansing Checklist", "Work through data clean-up steps and record rows changed at each step."),
    ("data-dictionary-template", "Data Dictionary Template", "Document each field's type, format and rules, and check for gaps."),
    ("api-endpoint-documentation", "API Endpoint Documentation", "Document each API endpoint's method, authentication and responses."),
    ("release-checklist", "Release Checklist", "Track each release task by stage, from build to review."),
    ("computer-lab-booking-maintenance", "Computer Lab Booking and Maintenance Log", "Log lab bookings and maintenance tasks, with costs and tasks due soon."),
    ("printer-consumables-tracker", "Printer and Consumables Tracker", "Track toner levels, reorder points and the cost per printed page."),
    ("new-device-onboarding-checklist", "New-Device Onboarding Checklist", "Track each new device through the onboarding steps to completion."),
    ("binary-hex-conversion-practice", "Binary and Hexadecimal Conversion Practice", "Practise decimal, binary and hex conversions with automatic checking."),
    ("algorithm-trace-table", "Algorithm Trace Table", "Trace a short program step by step and check the final value."),
    ("program-testing-record", "Program Testing Record", "Record test inputs and outputs for a function, with pass or fail for each test."),
    ("invoice-generator", "Invoice Generator", "Create an invoice with line items, VAT and the balance still due."),
    ("quote-estimate-template", "Quote and Estimate Template", "Price a job with line items, a discount and VAT, with a validity date."),
    ("purchase-order-log", "Purchase Order Log", "Track purchase orders from approval to delivery and see open order values."),
    ("accounts-receivable-aging-report", "Accounts Receivable Aging Report", "See which client invoices are unpaid and how long they are overdue."),
    ("accounts-payable-tracker", "Accounts Payable Tracker", "Track supplier bills, what is paid, and what is due soon or overdue."),
    ("profit-and-loss-statement", "Profit and Loss Statement", "Enter income and costs to see gross, operating and net profit."),
    ("cash-flow-forecast", "Cash Flow Forecast", "Forecast monthly cash in and out, and find the lowest cash point."),
    ("break-even-analysis", "Break-even Analysis", "Find the sales volume that covers your costs and the profit at planned sales."),
    ("inventory-stock-count-sheet", "Inventory Stock Count Sheet", "Compare system stock with physical counts and value the differences."),
    ("reorder-level-calculator", "Reorder Level Calculator", "Work out when to reorder each item from sales rate, lead time and safety stock."),
    ("payroll-calculator", "Payroll Calculator", "Work out tax, contributions and net pay, using example rates you can replace."),
    ("timesheet-overtime", "Timesheet with Overtime", "Record weekly hours and calculate regular hours, overtime and gross pay."),
    ("mileage-log", "Mileage Log", "Log business journeys and calculate mileage claims at your rate."),
    ("expense-claim-form", "Expense Claim Form", "Itemise expenses and flag any line that is missing a receipt."),
    ("petty-cash-register", "Petty Cash Register", "Track petty cash in and out with a running balance and a cash count check."),
    ("vat-sales-tax-calculator", "VAT and Sales Tax Calculator", "Calculate VAT and gross totals for each item at its own rate."),
    ("product-pricing-margin-calculator", "Product Pricing and Margin Calculator", "Set selling prices from markups and see margins and target prices."),
    ("client-contact-list", "Client Contact List", "Keep client details and see who needs a follow-up call."),
    ("sales-pipeline-tracker", "Sales Pipeline Tracker", "Track deals by stage, with weighted values for your open pipeline."),
    ("supplier-comparison", "Supplier Comparison", "Compare supplier prices for each item and see the cheapest overall."),
    ("business-plan-projections", "Business Plan Financial Projections", "Project three years of revenue, costs and profit from your assumptions."),
    ("asset-depreciation-schedule", "Asset Depreciation Schedule", "Calculate straight-line depreciation by year for each asset."),
    ("shift-rota", "Shift Rota", "Plan shifts for each person and see hours and cover per shift."),
    ("stock-valuation-fifo-lifo", "Stock Valuation (FIFO and LIFO)", "Value cost of sales and remaining stock with FIFO and LIFO side by side."),
    ("refunds-returns-log", "Refunds and Returns Log", "Log refunds and returns with reasons, status and totals."),
    ("gantt-chart", "Gantt Chart", "Plan tasks on a weekly timeline that shades the weeks each task is active."),
    ("kanban-board", "Kanban Board", "Track cards across columns, with work-in-progress limits and due-date flags."),
    ("project-budget-tracker", "Project Budget Tracker", "Compare budget, spend and commitments to forecast the final cost."),
    ("task-list-priorities", "Task List with Priorities", "List tasks by priority and status, with days left and overdue flags."),
    ("milestone-tracker", "Milestone Tracker", "Compare target and forecast dates for each milestone and see the slip."),
    ("risk-register", "Risk Register", "Score each risk by likelihood and impact, and rate it High, Medium or Low."),
    ("raci-matrix", "RACI Matrix", "Show who does, approves, is consulted and is informed for each activity."),
    ("meeting-agenda-minutes-log", "Meeting Agenda and Minutes Log", "Log each meeting’s attendance, decisions and actions, with totals."),
    ("action-items-tracker", "Action Items Tracker", "Track actions from meetings to completion and see which are overdue."),
    ("resource-allocation-planner", "Resource Allocation Planner", "Compare hours planned for each person with their weekly capacity."),
    ("time-tracking-by-project", "Time Tracking by Project", "Log hours against each project and see billable time at a glance."),
    ("project-status-dashboard", "Project Status Dashboard", "Give each project a Green, Amber or Red health rating with a progress chart."),
    ("weekly-team-status-report", "Weekly Team Status Report", "Collect each person’s progress, plans, blockers and confidence for the week."),
    ("decision-log", "Decision Log", "Record decisions, the options considered, and when each one needs review."),
    ("stakeholder-register", "Stakeholder Register", "Map stakeholders by interest and influence, and plan how to engage each one."),
    ("change-control-log", "Change Control Log", "Track change requests, their effort and schedule impact, and approved totals."),
    ("work-breakdown-structure", "Work Breakdown Structure", "Split the project into phases and work packages, with hour estimates."),
    ("capacity-planning-sheet", "Capacity Planning Sheet", "Compare each role’s weekly capacity with demand and flag shortfalls."),
    ("vendor-evaluation-scorecard", "Vendor Evaluation Scorecard", "Weight each criterion, score each vendor, and rank the results."),
    ("lessons-learned-log", "Lessons Learned Log", "Record what happened, the lesson and the action, with totals by category."),
    ("okr-tracker", "OKR Tracker", "Track each key result’s progress from start to target, with confidence."),
    ("personal-goal-tracker", "Personal Goal Tracker", "Track milestones for each personal goal, with days left and status."),
    ("event-run-sheet", "Event Run Sheet", "Plan the timings of an event, with finish times and total run time."),
    ("document-version-register", "Document Version Register", "Track every version of a document, who reviewed it, and what changed."),
    ("onboarding-task-checklist", "Onboarding Task Checklist", "Set a start date and give each onboarding task a due date and status."),
    ("workout-log", "Workout Log", "Log each exercise with sets, reps and weight, and see the total volume."),
    ("running-training-plan", "Running Training Plan", "Plan each week's runs, log what you ran, and compare distance with plan."),
    ("weight-tracker", "Weight Tracker", "Track your weight over time and see the change since your first entry."),
    ("calorie-and-macro-tracker", "Calorie and Macro Tracker", "Log foods with energy, protein, carbohydrate and fat, and see the totals."),
    ("meal-planner", "Meal Planner", "Plan breakfast, lunch, dinner and snacks for the week, with prep time."),
    ("water-intake-tracker", "Water Intake Tracker", "Log cups of water each day and see millilitres and averages."),
    ("sleep-log", "Sleep Log", "Record bedtime, wake time and how rested you felt, with hours slept."),
    ("habit-tracker", "Habit Tracker", "Mark each habit by day, and see days done against your weekly target."),
    ("daily-reflection-journal", "Daily Reflection Journal", "A private daily record of highlights, challenges and gratitude."),
    ("medication-reminder-schedule", "Medication Reminder Schedule", "List medicines, times and refill dates, with days left before each refill."),
    ("blood-pressure-log", "Blood Pressure Log", "Record readings and check them against the limits your doctor gives you."),
    ("blood-glucose-log", "Blood Glucose Log", "Record readings and check them against the range your clinician gives you."),
    ("step-count-tracker", "Step Count Tracker", "Log daily steps against your own goal and see your averages."),
    ("body-measurement-tracker", "Body Measurement Tracker", "Track chest, waist, hips, arm and thigh measurements over time."),
    ("strength-progression-chart", "Strength Progression Chart", "Log lifts and see the estimated one-rep max and your best so far."),
    ("cycling-log", "Cycling Log", "Log rides with distance, time and elevation, and see average speed."),
    ("recipe-nutrition-calculator", "Recipe Nutrition Calculator", "Work out energy and macronutrients per serving from ingredient values."),
    ("baby-feeding-and-nappy-log", "Baby Feeding and Nappy Log", "Log feeds and nappies with their times, and see daily totals."),
    ("childcare-schedule", "Childcare Schedule", "Plan who looks after the children each day, with hours booked."),
    ("symptom-diary", "Symptom Diary", "Record symptoms, severity and what was happening, to share at appointments."),
    ("stretching-routine-planner", "Stretching Routine Planner", "Plan stretches with hold times and sets, and see the routine length."),
    ("team-sports-stats-tracker", "Team Sports Stats Tracker", "Record goals, assists and minutes for each player, with goals per 90 minutes."),
    ("annual-health-check-reminders", "Annual Health Check Reminders", "Track check-up dates and see which are overdue or due soon."),
    ("gym-membership-cost-tracker", "Gym Membership Cost Tracker", "Track monthly fees and visits, and see the cost per visit."),
    ("screen-time-log", "Screen Time Log", "Log screen time by device and purpose, with hours calculated."),
    ("chore-rota", "Chore Rota", "Assign each chore to a person and day, with minutes and progress."),
    ("home-maintenance-schedule", "Home Maintenance Schedule", "Track when each home job was last done and when it is next due."),
    ("household-inventory-insurance", "Household Inventory for Insurance", "List valuable items with replacement values and receipts for insurance records."),
    ("pantry-inventory", "Pantry Inventory", "Track what is in the cupboard, fridge and freezer, with use-by dates and reorder levels."),
    ("meal-plan-shopping-list", "Meal Plan and Shopping List", "Turn each planned meal into a shopping list, grouped by aisle."),
    ("cleaning-schedule", "Cleaning Schedule", "Plan daily, weekly and monthly cleaning, with next due dates and overdue tasks."),
    ("garden-planting-planner", "Garden Planting Planner", "Plan sowing and harvest windows for each crop and see which stage it is at."),
    ("home-energy-usage-tracker", "Home Energy Usage Tracker", "Log meter readings to see electricity and gas used between readings, with costs."),
    ("utility-bill-comparison", "Utility Bill Comparison", "Compare tariffs by estimated monthly cost and see which is cheapest."),
    ("moving-checklist", "Moving Checklist", "Track every task before a move, with owners, due dates and overdue items."),
    ("home-renovation-budget", "Home Renovation Budget", "Compare quotes with actual costs room by room, with a contingency allowance."),
    ("paint-materials-calculator", "Paint and Materials Calculator", "Work out wall area, paint litres and tins from each room's size."),
    ("wardrobe-inventory", "Wardrobe Inventory", "List clothes with price, times worn and cost per wear."),
    ("pet-care-log", "Pet Care Log", "Record feeding, walks, vet visits and costs for each pet."),
    ("plant-watering-schedule", "Plant Watering Schedule", "See when each houseplant needs watering next."),
    ("birthday-anniversary-reminders", "Birthday and Anniversary Reminder List", "Track birthdays and anniversaries and see how many days until each one."),
    ("warranty-tracker", "Warranty Tracker", "Record warranties with end dates, days left and expiry flags."),
    ("smart-home-device-list", "Smart Home Device List", "List connected devices and flag any whose software has not been checked recently."),
    ("packing-list", "Packing List", "List what to pack, which bag it goes in, and track progress as you go."),
    ("car-maintenance-log", "Car Maintenance Log", "Log each job on the car with its mileage, cost and next due mileage."),
    ("fuel-economy-tracker", "Fuel Economy Tracker", "Track fill-ups to see distance, cost and litres per 100 km."),
    ("vehicle-service-schedule", "Vehicle Service Schedule", "See how far each service is from due, based on the current odometer."),
    ("recipe-scaling-calculator", "Recipe Scaling Calculator", "Scale a recipe up or down to the number of servings you need."),
    ("house-sitting-instructions", "House-Sitting Instructions Sheet", "Give a house-sitter one clear sheet of tasks, locations and contacts."),
    ("emergency-contacts-list", "Emergency Contacts List", "Keep the people and services to call in an emergency in one printable list."),
    ("trip-itinerary-planner", "Trip Itinerary Planner", "Plan each day's activities with times, places, booking references and costs."),
    ("travel-budget", "Travel Budget", "Set a budget for each travel category and track what you actually spend."),
    ("currency-conversion-log", "Currency Conversion Log", "Log foreign spending with the rate you were charged, including any card fee."),
    ("travel-packing-checklist", "Travel Packing Checklist", "Record what each person packs, which bag it goes in, and check the total weight against your allowance."),
    ("flight-and-hotel-comparison", "Flight and Hotel Comparison", "Compare flight and hotel options on total cost, cost per night and rank."),
    ("road-trip-fuel-calculator", "Road Trip Fuel Cost Calculator", "Work out fuel needed and cost for each leg, then share the total between travellers."),
    ("event-budget-planner", "Event Budget Planner", "Estimate each event cost and compare it with what you actually paid."),
    ("wedding-budget-planner", "Wedding Budget Planner", "Track each supplier's estimate, deposit and balance, with a contingency allowance."),
    ("passport-and-document-tracker", "Passport and Document Tracker", "Record travel documents with expiry dates and flag any that need renewing."),
    ("visa-and-entry-requirements-tracker", "Visa and Entry Requirements Tracker", "Track each destination's entry requirement and application deadline."),
    ("travel-insurance-comparison", "Travel Insurance Comparison", "Compare policies by premium, cover limit and excess, with cost per day."),
    ("event-guest-list", "Event Guest List", "Track invitations, RSVPs and plus-ones to get a confirmed guest count."),
    ("event-run-sheet", "Event Run Sheet", "Plan the event timeline with start times, lengths, owners and an overall finish time."),
    ("wedding-seating-planner", "Wedding Seating Planner", "See how many seats are free at each table and flag any that are over capacity."),
    ("event-volunteer-roster", "Event Volunteer Roster", "Schedule volunteers by role and shift, and record hours and check-ins."),
    ("travel-time-and-layover-planner", "Travel Time and Layover Planner", "Work out the real elapsed time of each journey, allowing for time zone changes."),
    ("trip-expense-splitter", "Trip Expense Splitter", "Record who paid what and see each person's balance for an equal split."),
    ("travel-journal", "Travel Journal", "Log each place with a highlight, notes and a rating, with an average rating."),
    ("destination-comparison-scorecard", "Destination Comparison Scorecard", "Score destinations on cost, weather, travel time and activities using your own weights."),
    ("event-ticket-tracker", "Event Ticket Tracker", "Track ticket orders, their total cost and whether they have been delivered."),
    ("event-feedback-summary", "Event Feedback Summary", "Count feedback scores for each question and see the average for each."),
    ("school-trip-consent-and-payment-tracker", "School Trip Consent and Payment Tracker", "Track returned forms and payments for each participant, with balances to collect."),
    ("daily-travel-spending-limit", "Daily Travel Spending Limit", "Set a limit for each day of a trip and track the running balance."),
    ("event-vendor-tracker", "Event Vendor Tracker", "Track each supplier's quote, deposit, contract status and balance owed."),
    ("trip-countdown-checklist", "Trip Countdown Checklist", "List tasks to finish before a trip, with owners, due dates and overdue flags."),
    ("photography-shot-log", "Photography Shot Log", "Log each shot with its lens and settings, and mark your keepers."),
    ("recipe-book-cost-per-serving", "Recipe Book with Cost per Serving", "Price each recipe's ingredients and see the cost per serving."),
    ("baking-ratio-calculator", "Baking Ratio Calculator", "Work out baker's percentages and scale a dough recipe to any flour weight."),
    ("home-brewing-log", "Home Brewing Log", "Record each batch's gravity readings and see its alcohol by volume."),
    ("knitting-pattern-row-counter", "Knitting Pattern Row Counter", "Track rows done against your pattern, with rows left and progress."),
    ("model-railway-inventory", "Model Railway Inventory", "Catalogue locomotives, rolling stock and scenery by scale and condition."),
    ("book-reading-tracker", "Book Reading Tracker", "Log each book with its dates, pages and rating, and see your totals."),
    ("film-watch-log", "Film Watch Log", "Log films and episodes with where you watched them and how you rated them."),
    ("board-game-score-tracker", "Board Game Score Tracker", "Record scores for each game session and mark the winners."),
    ("fantasy-league-points-calculator", "Fantasy League Points Calculator", "Turn weekly player stats into points using your league's rules."),
    ("music-practice-log", "Music Practice Log", "Log each practice session with its focus and tempo, and see total practice time."),
    ("song-chord-planner", "Song Chord Planner", "Plan the chords and strumming for each section of a song."),
    ("art-supply-inventory", "Art Supply Inventory", "Track paints, brushes and paper, with stock value and reorder alerts."),
    ("seed-library-tracker", "Seed Library Tracker", "Track seed varieties, packets and germination rates, and flag old seed to test."),
    ("fishing-catch-log", "Fishing Catch Log", "Log each catch with its size, weight and whether you released it."),
    ("bird-watching-log", "Bird Watching Log", "Record each sighting with its count and behaviour, and count the species seen."),
    ("stamp-and-coin-collection-tracker", "Stamp and Coin Collection Tracker", "Record each item with its condition, what you paid and its current value."),
    ("video-game-backlog-tracker", "Video Game Backlog Tracker", "Track your game backlog by status, priority and hours played."),
    ("podcast-episode-planner", "Podcast Episode Planner", "Plan episodes from idea to publishing, with days left until each release."),
    ("writing-word-count-tracker", "Writing Word Count Tracker", "Log daily words for each project and see whether you met your goal."),
    ("novel-chapter-outline-planner", "Novel Chapter Outline Planner", "Outline each chapter with its word target and see progress across the book."),
    ("yarn-stash-inventory", "Yarn Stash Inventory", "Catalogue your yarn by weight, skeins and metres, and link it to a planned project."),
    ("woodworking-cut-list", "Woodworking Cut List", "List each part to cut with its size, quantity and the face area of board it needs."),
    ("sewing-measurement-chart", "Sewing Measurement Chart", "Compare pattern sizes with your measurements and see the ease in each size."),
    ("vinyl-record-catalogue", "Vinyl Record Catalogue", "Catalogue your records by format, label, condition and price paid."),
    ("social-media-content-calendar", "Social Media Content Calendar", "Plan posts by date and platform, then record likes and reach to see engagement."),
    ("email-campaign-tracker", "Email Campaign Tracker", "Track sends, opens and clicks for each email campaign."),
    ("marketing-budget-and-roi-tracker", "Marketing Budget and ROI Tracker", "Compare each channel's budget and spend with the revenue it brought in."),
    ("lead-tracker", "Lead Tracker", "Track each lead from first contact to sale, with its value and next follow-up."),
    ("customer-database", "Customer Database", "Keep customer contacts, spend and tier in one list."),
    ("sales-commission-calculator", "Sales Commission Calculator", "Work out commission with a base rate up to target and a bonus rate above it."),
    ("monthly-sales-forecast", "Monthly Sales Forecast", "Compare each month's forecast with actual sales and see the variance."),
    ("seo-keyword-tracker", "SEO Keyword Tracker", "Track target keywords, their pages and search positions against your goals."),
    ("ad-spend-tracker", "Ad Spend Tracker", "Log ad spend, impressions and clicks, with cost per click and click-through rate."),
    ("customer-feedback-summary", "Customer Feedback Summary", "Count positive, neutral and negative comments for each topic."),
    ("net-promoter-score-tracker", "Net Promoter Score Tracker", "Record 0 to 10 scores and calculate your Net Promoter Score."),
    ("customer-churn-analysis", "Customer Churn Analysis", "Track customers gained and lost each month and see the churn rate."),
    ("competitor-comparison-matrix", "Competitor Comparison Matrix", "Rate features for your business and competitors, and see who leads on each."),
    ("swot-analysis", "SWOT Analysis", "List strengths, weaknesses, opportunities and threats with actions and owners."),
    ("event-attendance-tracker", "Event Attendance Tracker", "Track registrations, attendance, leads and cost for each event."),
    ("support-ticket-sla-tracker", "Support Ticket SLA Tracker", "Check whether each support ticket was resolved within its target time."),
    ("warehouse-picking-list", "Warehouse Picking List", "List order lines to pick and flag any that come up short."),
    ("order-fulfilment-tracker", "Order Fulfilment Tracker", "Track each order from order date to dispatch, and flag late shipments."),
    ("shipping-cost-calculator", "Shipping Cost Calculator", "Estimate shipping costs from parcel weight, parcel count and your rates."),
    ("restaurant-food-cost-calculator", "Restaurant Food Cost Calculator", "Work out food cost percentage and gross profit for each dish."),
    ("staff-training-log", "Staff Training Log", "Record training courses and certificate expiry dates, with renewals flagged."),
    ("employee-leave-tracker", "Employee Leave Tracker", "Log leave requests, count working days and see annual leave remaining."),
    ("performance-review-scorecard", "Performance Review Scorecard", "Score staff on four criteria and see each average and rating band."),
    ("recruitment-candidate-tracker", "Recruitment Candidate Tracker", "Track candidates through each recruitment stage with interview scores."),
    ("shift-handover-log", "Shift Handover Log", "Pass on issues and open actions between shifts, and count what is still unresolved."),
]

# Groups for the category pages: (heading, [slugs]) per category.
PF_GROUPS = [
    ("Budgeting", ["monthly-household-budget-planner", "zero-based-budget", "envelope-budgeting-tracker",
                   "expense-tracker", "income-vs-expenses-summary", "weekly-grocery-budget"]),
    ("Debt and loans", ["debt-snowball-calculator", "debt-avalanche-calculator", "loan-amortisation-schedule",
                        "mortgage-repayment-calculator", "car-loan-comparison", "credit-card-payoff-planner"]),
    ("Savings and planning", ["savings-goal-tracker", "emergency-fund-calculator", "compound-interest-calculator",
                              "retirement-savings-projection", "sinking-funds-planner", "annual-cash-flow-forecast"]),
    ("Money tracking", ["net-worth-tracker", "subscription-cost-tracker", "bill-payment-calendar",
                        "freelancer-income-tracker", "price-comparison-sheet", "holiday-gift-budget",
                        "tax-estimate-calculator"]),
]

EDU_GROUPS = [
    ("Marks and grades", ["gradebook-weighted-averages", "rubric-scoring-sheet", "mark-sheet-grade-boundaries",
                          "assessment-tracker-learning-objective", "student-progress-tracker", "quiz-score-analyser"]),
    ("Attendance and behaviour", ["attendance-register", "homework-tracker", "behaviour-points-log",
                                  "parent-contact-log", "class-roster", "seating-plan-generator"]),
    ("Planning and timetables", ["lesson-plan-template", "scheme-of-work-planner", "termly-timetable",
                                 "exam-timetable-planner", "revision-schedule", "reading-log"]),
    ("Projects, clubs and admin", ["student-project-tracker", "group-work-rotation-planner", "club-signup-sheet",
                                   "lab-equipment-booking", "classroom-budget-tracker", "report-card-comment-bank",
                                   "course-completion-checklist"]),
]

IT_GROUPS = [
    ("Assets and inventory", ["it-asset-register", "software-licence-tracker", "network-device-inventory",
                              "hardware-refresh-planner", "printer-consumables-tracker", "new-device-onboarding-checklist"]),
    ("Support and operations", ["help-desk-ticket-log", "server-backup-log", "uptime-incident-log", "change-request-log",
                                "ip-address-planner", "cloud-cost-estimator", "website-traffic-summary"]),
    ("Software development", ["sprint-backlog-burndown", "bug-tracker", "test-case-log", "code-review-checklist",
                              "release-checklist", "api-endpoint-documentation", "program-testing-record"]),
    ("Data and classroom practice", ["data-cleansing-checklist", "data-dictionary-template", "binary-hex-conversion-practice",
                                     "algorithm-trace-table", "computer-lab-booking-maintenance"]),
]

SB_GROUPS = [
    ("Invoicing and sales", ["invoice-generator", "quote-estimate-template", "accounts-receivable-aging-report",
                             "sales-pipeline-tracker", "client-contact-list", "refunds-returns-log"]),
    ("Money in and out", ["purchase-order-log", "accounts-payable-tracker", "petty-cash-register",
                          "expense-claim-form", "mileage-log", "vat-sales-tax-calculator"]),
    ("Reporting and planning", ["profit-and-loss-statement", "cash-flow-forecast", "break-even-analysis",
                                "business-plan-projections", "asset-depreciation-schedule", "product-pricing-margin-calculator"]),
    ("Stock, staff and suppliers", ["inventory-stock-count-sheet", "reorder-level-calculator", "stock-valuation-fifo-lifo",
                                    "payroll-calculator", "timesheet-overtime", "shift-rota", "supplier-comparison"]),
]

PM_GROUPS = [
    ("Planning and scope", ["gantt-chart", "work-breakdown-structure", "milestone-tracker", "project-budget-tracker",
                            "resource-allocation-planner", "capacity-planning-sheet"]),
    ("Tasks and tracking", ["kanban-board", "task-list-priorities", "action-items-tracker", "time-tracking-by-project",
                            "project-status-dashboard", "weekly-team-status-report"]),
    ("Risk, decisions and people", ["risk-register", "decision-log", "stakeholder-register", "raci-matrix",
                                    "change-control-log", "meeting-agenda-minutes-log"]),
    ("Review and improvement", ["vendor-evaluation-scorecard", "lessons-learned-log", "okr-tracker", "document-version-register",
                                "onboarding-task-checklist", "event-run-sheet", "personal-goal-tracker"]),
]

HEALTH_GROUPS = [
    ("Exercise and movement", ["workout-log", "running-training-plan", "strength-progression-chart", "cycling-log", "stretching-routine-planner", "team-sports-stats-tracker", "step-count-tracker"]),
    ("Food, water and sleep", ["calorie-and-macro-tracker", "meal-planner", "recipe-nutrition-calculator", "water-intake-tracker", "sleep-log"]),
    ("Body and health records", ["weight-tracker", "body-measurement-tracker", "blood-pressure-log", "blood-glucose-log", "medication-reminder-schedule", "symptom-diary", "annual-health-check-reminders"]),
    ("Habits and family life", ["habit-tracker", "daily-reflection-journal", "screen-time-log", "gym-membership-cost-tracker", "baby-feeding-and-nappy-log", "childcare-schedule"]),
]

HOME_GROUPS = [
    ("Household admin", ["chore-rota", "home-maintenance-schedule", "cleaning-schedule", "moving-checklist", "household-inventory-insurance", "warranty-tracker", "emergency-contacts-list", "house-sitting-instructions"]),
    ("Food and kitchen", ["pantry-inventory", "meal-plan-shopping-list", "recipe-scaling-calculator"]),
    ("Home and garden", ["home-renovation-budget", "paint-materials-calculator", "garden-planting-planner", "plant-watering-schedule", "smart-home-device-list"]),
    ("Bills and energy", ["home-energy-usage-tracker", "utility-bill-comparison"]),
    ("Belongings and people", ["wardrobe-inventory", "pet-care-log", "birthday-anniversary-reminders", "packing-list"]),
    ("Vehicles", ["car-maintenance-log", "fuel-economy-tracker", "vehicle-service-schedule"]),
]

TRAVEL_GROUPS = [
    ("Trip planning", ["trip-itinerary-planner", "travel-packing-checklist", "trip-countdown-checklist", "travel-time-and-layover-planner", "passport-and-document-tracker", "visa-and-entry-requirements-tracker"]),
    ("Travel money", ["travel-budget", "daily-travel-spending-limit", "currency-conversion-log", "trip-expense-splitter", "travel-insurance-comparison"]),
    ("Getting there and staying", ["flight-and-hotel-comparison", "road-trip-fuel-calculator", "destination-comparison-scorecard", "travel-journal"]),
    ("Events and weddings", ["event-budget-planner", "wedding-budget-planner", "event-guest-list", "wedding-seating-planner", "event-run-sheet", "event-volunteer-roster", "event-vendor-tracker", "event-ticket-tracker", "event-feedback-summary"]),
    ("Groups and schools", ["school-trip-consent-and-payment-tracker"]),
]

HOBBIES_GROUPS = [
    ("Food and drink", ["recipe-book-cost-per-serving", "baking-ratio-calculator", "home-brewing-log"]),
    ("Making and crafts", ["knitting-pattern-row-counter", "yarn-stash-inventory", "woodworking-cut-list", "sewing-measurement-chart", "art-supply-inventory"]),
    ("Collections", ["model-railway-inventory", "stamp-and-coin-collection-tracker", "vinyl-record-catalogue"]),
    ("Reading, film and games", ["book-reading-tracker", "film-watch-log", "video-game-backlog-tracker", "board-game-score-tracker", "fantasy-league-points-calculator"]),
    ("Music, writing and outdoors", ["music-practice-log", "song-chord-planner", "writing-word-count-tracker", "novel-chapter-outline-planner", "podcast-episode-planner", "photography-shot-log", "fishing-catch-log", "bird-watching-log", "seed-library-tracker"]),
]

SALES_GROUPS = [
    ("Social and marketing", ["social-media-content-calendar", "email-campaign-tracker", "marketing-budget-and-roi-tracker", "seo-keyword-tracker", "ad-spend-tracker", "event-attendance-tracker"]),
    ("Sales and leads", ["lead-tracker", "customer-database", "sales-commission-calculator", "monthly-sales-forecast"]),
    ("Customers", ["customer-feedback-summary", "net-promoter-score-tracker", "customer-churn-analysis", "competitor-comparison-matrix", "swot-analysis", "support-ticket-sla-tracker"]),
    ("Operations and stock", ["warehouse-picking-list", "order-fulfilment-tracker", "shipping-cost-calculator", "restaurant-food-cost-calculator"]),
    ("Team and staff", ["staff-training-log", "employee-leave-tracker", "performance-review-scorecard", "recruitment-candidate-tracker", "shift-handover-log"]),
]

GROUPS_BY_CAT = {"personal-finance": PF_GROUPS, "education": EDU_GROUPS, "it-computing": IT_GROUPS, "small-business": SB_GROUPS,
                 "project-management": PM_GROUPS, "health-fitness": HEALTH_GROUPS, "home-household": HOME_GROUPS, "travel-events": TRAVEL_GROUPS, "hobbies-creative-projects": HOBBIES_GROUPS, "sales-marketing-operations": SALES_GROUPS}
CAT_OF = {slug: cat for cat, groups in GROUPS_BY_CAT.items() for _, slugs in groups for slug in slugs}
assert sorted(s for groups in GROUPS_BY_CAT.values() for _, slugs in groups for s in slugs) == \
    sorted(slug for slug, _, _ in TEMPLATES), "groups must cover every template exactly once"

# ---------------------------------------------------------------- shared shell
index_html = open(f"{SITE}/index.html", encoding="utf-8").read()
script = re.search(r"<script>(.*?)</script>", index_html, re.S).group(1)
header = re.search(r"<header .*?</header>", index_html, re.S).group(0)
footer = re.search(r"<footer .*?</footer>", index_html, re.S).group(0)


def fix_links(html, prefix):
    """prefix is '../' for pages in a subfolder, '' for pages at the site root."""
    if not prefix:
        return html.replace('href="#categories"', 'href="index.html#categories"')
    html = html.replace('href="categories/', 'href="')
    html = re.sub(r'(href|action)="(index\.html|all\.html|about\.html|privacy\.html|terms\.html|licence\.html|contact\.html|popular\.html|search\.html)"',
                  lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"', html)
    return html.replace('href="#categories"', f'href="{prefix}index.html#categories"')


def page(title, description, body, prefix, extra_script=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{prefix}css/style.css">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

{fix_links(header, prefix)}

{body}

{fix_links(footer, prefix)}

<script>{script}</script>
{extra_script}
</body>
</html>
"""


def card(slug, name, desc, tint):
    return f"""      <li class="tpl-card {tint}">
        <h3>{name}</h3>
        <p>{desc}</p>
        <p class="dl-count" data-count-slug="{slug}">Downloads: loading&hellip;</p>
        <a class="dl" href="../downloads/{CAT_OF[slug]}/{slug}.xlsx" aria-label="Download {name} (Excel file)">Download .xlsx</a>
      </li>"""


# ---------------------------------------------------------------- category pages
TINTS = ["tint-lavender", "tint-mint", "tint-blue", "tint-peach", "tint-cream"]
by_slug = {slug: (name, desc) for slug, name, desc in TEMPLATES}
os.makedirs(f"{SITE}/categories", exist_ok=True)


def build_category(cat, groups):
    sections, n = [], 0
    for g, (heading, slugs) in enumerate(groups):
        cards = []
        for slug in slugs:
            name, desc = by_slug[slug]
            cards.append(card(slug, name, desc, TINTS[n % len(TINTS)]))
            n += 1
        sections.append(f"""  <section class="tpl-group" aria-labelledby="g{g}">
    <h2 class="group-title" id="g{g}">{heading}</h2>
    <ul class="tpl-grid">
{chr(10).join(cards)}
    </ul>
  </section>""")

    name = CATEGORIES[cat]
    cat_body = f"""<main id="main">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> &rsaquo; {name}</nav>
  <h1 class="page-title">{name}</h1>
  <p class="page-intro">{CATEGORY_INTRO[cat]}</p>

{chr(10).join(sections)}

  <div class="note">
    <strong>Free to use, adapt and share.</strong> Every template is licensed under <a href="../licence.html">CC BY 4.0</a>. All example figures are generic. Replace them with your own.
  </div>
</main>"""
    title = name.replace("&", "&amp;") + " Templates | Sheetly"
    open(f"{SITE}/categories/{cat}.html", "w", encoding="utf-8").write(
        page(title, CATEGORY_DESC[cat], cat_body, "../",
             '<script src="../js/downloads.js" data-root="../" defer></script>'))


for cat, groups in GROUPS_BY_CAT.items():
    build_category(cat, groups)
print("built category pages:", ", ".join(GROUPS_BY_CAT))

# ---------------------------------------------------------------- most downloaded page
popular_body = f"""<main id="main">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; Most downloaded</nav>
  <h1 class="page-title">Most downloaded templates</h1>
  <p class="page-intro">The templates people download most, across all categories. Ranked by total downloads, {PAGE_SIZE} per page.</p>
  <p id="countsStatus" class="brand-note" role="status"></p>
  <ol class="rank-list" id="rankList"></ol>
  <nav class="pager" id="pager" aria-label="Pages of templates"></nav>
</main>"""

os.makedirs(SITE, exist_ok=True)
open(f"{SITE}/popular.html", "w", encoding="utf-8").write(
    page("Most Downloaded Templates | Sheetly",
         "The most downloaded free spreadsheet templates, ranked by total downloads.",
         popular_body, "", '<script src="js/downloads.js" data-root="" defer></script>'))

# ---------------------------------------------------------------- search page (all templates)
search_body = """<main id="main">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; Search</nav>
  <h1 class="page-title">Search templates</h1>
  <p class="page-intro">Search all {n} free templates by name, purpose or category.</p>
  <form class="search-form" action="search.html" method="get" role="search">
    <label class="sr-only" for="searchPageInput">Search templates</label>
    <input id="searchPageInput" name="q" type="search" placeholder="Try budget, timetable or invoice" autocomplete="off">
  </form>
  <p class="search-status" id="searchStatus" role="status" aria-live="polite"></p>
  <ul class="tpl-grid" id="searchResults"></ul>
</main>""".replace("{n}", str(len(TEMPLATES)))
open(f"{SITE}/search.html", "w", encoding="utf-8").write(
    page("Search Templates | Sheetly",
         "Search all free spreadsheet templates by name, purpose or category.",
         search_body, "", '<script src="js/search.js" defer></script>'))

# ---------------------------------------------------------------- site map page
def site_map_categories():
    sections = []
    for cat, groups in GROUPS_BY_CAT.items():
        items = []
        for _, slugs in groups:
            for slug in slugs:
                name = by_slug[slug][0].replace("&", "&amp;")
                items.append(f'          <li><a href="downloads/{CAT_OF[slug]}/{slug}.xlsx">{name}</a></li>')
        cat_name = CATEGORIES[cat].replace("&", "&amp;")
        sections.append(f"""      <section class="sitemap-cat" aria-labelledby="sm-{cat}">
        <h3 id="sm-{cat}"><a href="categories/{cat}.html">{cat_name}</a></h3>
        <ul class="sitemap-list">
{chr(10).join(items)}
        </ul>
      </section>""")
    return chr(10).join(sections)


sitemap_body = f"""<main id="main">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; Site map</nav>
  <h1 class="page-title">Site map</h1>
  <p class="page-intro">Every page on Sheetly, and every free template listed by category.</p>

  <section class="sitemap-section" aria-labelledby="sm-pages">
    <h2 class="group-title" id="sm-pages">Pages</h2>
    <ul class="sitemap-list">
      <li><a href="index.html">Home</a></li>
      <li><a href="search.html">Search templates</a></li>
      <li><a href="popular.html">Most downloaded</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="contact.html">Contact us</a></li>
      <li><a href="licence.html">Licence (CC BY 4.0)</a></li>
      <li><a href="privacy.html">Privacy Policy</a></li>
      <li><a href="terms.html">Terms of Use</a></li>
      <li><a href="sitemap.html">Site map</a></li>
    </ul>
  </section>

  <section class="sitemap-section" aria-labelledby="sm-cats">
    <h2 class="group-title" id="sm-cats">Templates by category</h2>
{site_map_categories()}
  </section>
</main>"""
open(f"{SITE}/sitemap.html", "w", encoding="utf-8").write(
    page("Site map | Sheetly",
         "A list of every page on Sheetly and every free spreadsheet template, by category.",
         sitemap_body, ""))

# ---------------------------------------------------------------- all templates page (alphabetical)
def all_templates_sections():
    sections = []
    for cat in sorted(GROUPS_BY_CAT, key=lambda c: CATEGORIES[c].lower()):
        names = sorted((by_slug[slug][0], slug) for _, slugs in GROUPS_BY_CAT[cat] for slug in slugs)
        items = [f'          <li><a href="downloads/{CAT_OF[slug]}/{slug}.xlsx">{name.replace("&", "&amp;")}</a></li>'
                 for name, slug in names]
        cat_name = CATEGORIES[cat].replace("&", "&amp;")
        sections.append(f"""      <section class="sitemap-cat" aria-labelledby="all-{cat}">
        <h3 id="all-{cat}"><a href="categories/{cat}.html">{cat_name}</a></h3>
        <ul class="sitemap-list">
{chr(10).join(items)}
        </ul>
      </section>""")
    return chr(10).join(sections)


all_body = f"""<main id="main">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; All templates</nav>
  <h1 class="page-title">All templates</h1>
  <p class="page-intro">Every free template, listed alphabetically by category, then by name.</p>
{all_templates_sections()}
</main>"""
open(f"{SITE}/all.html", "w", encoding="utf-8").write(
    page("All templates | Sheetly",
         "Every free spreadsheet template, listed alphabetically by category and by name.",
         all_body, ""))

# ---------------------------------------------------------------- catalogue data for the page script
catalogue = [{"slug": slug, "name": name, "description": desc, "category": CAT_OF[slug],
              "categoryName": CATEGORIES[CAT_OF[slug]], "file": f"downloads/{CAT_OF[slug]}/{slug}.xlsx"}
             for slug, name, desc in TEMPLATES]
os.makedirs(f"{SITE}/data", exist_ok=True)
json.dump({"pageSize": PAGE_SIZE, "templates": catalogue},
          open(f"{SITE}/data/templates.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# ---------------------------------------------------------------- download function (Cloudflare Pages)
slug_map = ",\n  ".join(f'"{slug}": "{CAT_OF[slug]}"' for slug, _, _ in TEMPLATES)
fn = f"""// Cloudflare Pages Function: GET /api/download/:slug
// Counts the download, then redirects to the .xlsx file.
// Needs a KV namespace bound as DOWNLOADS (Pages > Settings > Bindings).
// Generated by build_site.py. Edit the generator, not this file.

const TEMPLATES = {{
  {slug_map}
}};

export async function onRequestGet({{ params, env, request }}) {{
  const slug = params.slug;
  const category = TEMPLATES[slug];
  if (!category) {{
    return new Response("Template not found", {{ status: 404 }});
  }}

  const key = `dl:${{slug}}`;
  const current = parseInt((await env.DOWNLOADS.get(key)) || "0", 10);
  await env.DOWNLOADS.put(key, String(current + 1));

  const file = new URL(`/downloads/${{category}}/${{slug}}.xlsx`, request.url);
  return Response.redirect(file.toString(), 302);
}}
"""
# Cloudflare Pages expects the functions folder next to the site folder, not inside it
FUNCTIONS = os.path.join(os.path.dirname(SITE), "functions")
os.makedirs(f"{FUNCTIONS}/api/download", exist_ok=True)
open(f"{FUNCTIONS}/api/download/[slug].js", "w", encoding="utf-8").write(fn)

print(f"built category page, popular page, {len(catalogue)} catalogue entries, download function")

# ---------------------------------------------------------------- footer pages (site root)
CONTACT_EMAIL = "hello@sheetly.example"

def prose(title, intro, sections, updated="16 November 2026"):
    parts = [f'<h1 class="page-title">{title}</h1>', f'<p class="page-intro">{intro}</p>']
    for heading, paras in sections:
        parts.append(f'<h2 class="prose-h">{heading}</h2>')
        parts.extend(f"<p>{p}</p>" for p in paras)
    parts.append(f'<p class="brand-note">Last updated: {updated}</p>')
    return '<main id="main">\n  <div class="prose">\n  ' + "\n  ".join(parts) + "\n  </div>\n</main>"

about_body = prose(
    "About Sheetly",
    "Sheetly is a free library of practical spreadsheet templates for money, school, work and everyday life. Every template is designed to be opened, understood and used straight away.",
    [
        ("Why Sheetly exists", [
            "Good spreadsheets save time, but building one from scratch is slow and easy to get wrong. Sheetly gives you a clear starting point, so you can spend your time on your own figures instead of on layout and formulas.",
            "The idea grew out of classroom work. Teachers, students and families often need the same handful of tools: a budget, a gradebook, a timetable, a loan calculator. Sheetly collects those and makes them free to use.",
        ]),
        ("What is included", [
            "Sheetly is organised into categories, so you can find what you need quickly: Personal Finance and Budgeting, Education and Classroom, IT and Computing, Small Business and Invoicing, Project and Task Management, Health, Fitness and Wellbeing, Home and Household, Travel and Events, Hobbies and Creative Projects, and Sales, Marketing and Operations.",
            "Each category has its own page, grouped by topic. The Personal Finance category, for example, covers budgets, debt payoff, loans, savings and everyday money tracking.",
            "The Most downloaded page shows which templates people use most, so you can see what others find useful.",
        ]),
        ("How every template is built", [
            "Each workbook has the Sheetly logo in the corner, a clear title band, and a How to use sheet that explains what to type and what to read. Input cells are cream and formula cells are left unshaded, so you always know where to type.",
            "Formulas calculate automatically. Before a template is released, every workbook is recalculated to check for errors, and example results are checked by hand against independent calculations.",
            "All example data is generic and made up. Nothing is based on real people, students or customers.",
        ]),
        ("Who it is for", [
            "Teachers and students who need gradebooks, registers, timetables and revision planners.",
            "Families and individuals who want to plan budgets, track spending, pay down debt or save for a goal.",
            "Freelancers and small business owners who need invoices, timesheets, stock sheets and simple profit reports.",
            "Anyone who prefers a clear, ready-made tool to a blank page.",
        ]),
        ("Our principles", [
            "Free: every template is free, with no paywall and no account needed.",
            "Practical: templates focus on real tasks, not theory. Each one should be useful the first time you open it.",
            "Clear: clean layouts, plain labels and colours that make inputs and results easy to find.",
            "Private: the site does not ask for personal details. See the <a href=\"privacy.html\">Privacy Policy</a> for what is stored.",
            "Accessible: pages adapt to phones, tablets, laptops and desktops, and work in light or dark mode.",
        ]),
        ("Sharing and credit", [
            "All templates are licensed under <a href=\"licence.html\">CC BY 4.0</a>. You can use, adapt and share them, including for commercial purposes, as long as you credit the author and say if you have made changes.",
        ]),
        ("Important to know", [
            "Templates are tools for planning and organising. Calculations such as tax, loan and payoff estimates are approximations. Check important decisions with a qualified professional or your local authority. See the <a href=\"terms.html\">Terms of Use</a> for details.",
        ]),
        ("About the author", [
            "Sheetly is created and maintained by Mark, a teacher of computing and ICT who builds learning resources and everyday planning tools.",
        ]),
        ("Get in touch", [
            "Have a question, a template request or feedback? Visit the <a href=\"contact.html\">Contact us</a> page, or email <a href=\"mailto:" + CONTACT_EMAIL + "\">" + CONTACT_EMAIL + "</a>. Suggestions for new templates are always welcome.",
        ]),
    ])

privacy_body = prose(
    "Privacy Policy",
    "This policy explains what information Sheetly handles and why. Sheetly does not ask you to create an account.",
    [
        ("Information we collect", [
            "Sheetly does not collect your name, address or payment details. Browsing the site does not require signing in.",
            "When you download a template, Sheetly adds one to a total count for that template. The count does not record who downloaded it.",
            "If you send a message through the contact form, the form opens your email app with the message already written. Sheetly receives your message only when you send it from your email app.",
        ]),
        ("Cookies and local storage", [
            "Sheetly does not use advertising or tracking cookies. It stores one setting in your browser, your light or dark mode choice, so the site remembers it on your next visit. You can clear this at any time in your browser settings.",
        ]),
        ("Hosting", [
            "The site is hosted by a third-party web host, which may keep standard server logs such as IP address, time and page requested, under its own privacy policy.",
        ]),
        ("Your choices", [
            "To ask what information we hold about you, or to ask for it to be removed, email <a href=\"mailto:" + CONTACT_EMAIL + "\">" + CONTACT_EMAIL + "</a>.",
        ]),
    ])

terms_body = prose(
    "Terms of Use",
    "By using Sheetly you agree to these terms. Please read them before downloading any template.",
    [
        ("Licence", [
            "Templates are licensed under <a href=\"licence.html\">Creative Commons Attribution 4.0 (CC BY 4.0)</a>. You must credit the author and indicate whether you changed the file.",
        ]),
        ("Example data", [
            "All example figures are generic and made up. Do not treat them as real results or advice.",
        ]),
        ("No guarantee", [
            "Templates are provided as is, without warranty of any kind. Calculations such as tax, loan and payoff estimates are for planning only. Check important figures with a qualified professional or your local authority.",
        ]),
        ("Limitation of liability", [
            "Sheetly and its author are not liable for any loss arising from using a template, including loss of data or money.",
        ]),
        ("Changes", [
            "These terms may change. The date at the bottom of this page shows when they were last updated.",
        ]),
    ])

licence_body = prose(
    "Licence",
    "Sheetly templates are shared under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).",
    [
        ("What you can do", [
            "You are free to share (copy and redistribute the file in any medium or format) and to adapt it (remix, transform and build on it) for any purpose, including commercially.",
        ]),
        ("What you must do", [
            "Give appropriate credit: name the author, Mark, and Sheetly, and link to the licence. Indicate if you made changes. Do not suggest the author endorses your use.",
        ]),
        ("Full licence text", [
            "Read the full licence at <a href=\"https://creativecommons.org/licenses/by/4.0/\">creativecommons.org/licenses/by/4.0</a>.",
        ]),
    ])

contact_body = f"""<main id="main">
  <div class="prose">
    <h1 class="page-title">Contact us</h1>
    <p class="page-intro">Questions, feedback or a template request? Send a message below, or email us directly at <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
  </div>

  <form class="contact-form" id="contactForm" novalidate>
    <div class="field">
      <label for="cName">Your name</label>
      <input id="cName" name="name" type="text" autocomplete="name" required maxlength="100">
    </div>
    <div class="field">
      <label for="cEmail">Your email</label>
      <input id="cEmail" name="email" type="email" autocomplete="email" required maxlength="200">
    </div>
    <div class="field">
      <label for="cTopic">Topic</label>
      <select id="cTopic" name="topic" required>
        <option value="">Choose a topic</option>
        <option>General question</option>
        <option>Template request</option>
        <option>Report a problem with a template</option>
        <option>Licence or permission</option>
        <option>Other</option>
      </select>
    </div>
    <div class="field">
      <label for="cMessage">Message</label>
      <textarea id="cMessage" name="message" rows="6" required maxlength="2000"></textarea>
    </div>
    <button class="btn" type="submit">Send message</button>
    <p class="form-note" id="formStatus" role="status" aria-live="polite">
      Sending opens your email app with your message ready to send to {CONTACT_EMAIL}.
    </p>
  </form>
</main>"""

for name, title, desc, body, extra in [
    ("about", "About | Sheetly", "About Sheetly and its free spreadsheet templates.", about_body, ""),
    ("privacy", "Privacy Policy | Sheetly", "How Sheetly handles information and cookies.", privacy_body, ""),
    ("terms", "Terms of Use | Sheetly", "Terms for using Sheetly templates.", terms_body, ""),
    ("licence", "Licence | Sheetly", "Sheetly templates are shared under CC BY 4.0.", licence_body, ""),
    ("contact", "Contact us | Sheetly", "Contact Sheetly with a question or template request.", contact_body,
     '<script src="js/contact.js" defer></script>'),
]:
    open(f"{SITE}/{name}.html", "w", encoding="utf-8").write(page(title, desc, body, "", extra))

# Contact address in the footer (same made-up address everywhere)
idx = open(f"{SITE}/index.html", encoding="utf-8").read()
idx = idx.replace("mailto:hello@example.com", f"mailto:{CONTACT_EMAIL}").replace(">hello@example.com<", f">{CONTACT_EMAIL}<")
open(f"{SITE}/index.html", "w", encoding="utf-8").write(idx)
print("built footer pages")
