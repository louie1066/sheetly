"""Build the personal finance, education, IT & computing, small business and project management templates (125) into the site downloads folders."""
import os, sys
from openpyxl import Workbook
import common
from common import how_to_sheet
import finance_a as A, finance_b as B, finance_c as C
import education_a as EA, education_b as EB, education_c as EC
import it_a as IA, it_b as IB, it_c as IC
import sb_a as SA, sb_b as SB, sb_c as SC
import pm_a as PA, pm_b as PB, pm_c as PC
import sales_a, sales_b, sales_c
import hobby_a, hobby_b, hobby_c
import travel_a, travel_b, travel_c
import home_a, home_b, home_c
import hw_a, hw_b, hw_c

OUT = "/home/claude/site/downloads/personal-finance"
EDU_OUT = "/home/claude/site/downloads/education"
IT_OUT = "/home/claude/site/downloads/it-computing"
SB_OUT = "/home/claude/site/downloads/small-business"
PM_OUT = "/home/claude/site/downloads/project-management"
SALES_OUT = "/home/claude/site/downloads/sales-marketing-operations"
os.makedirs(SALES_OUT, exist_ok=True)
HOBBIES_OUT = "/home/claude/site/downloads/hobbies-creative-projects"
os.makedirs(HOBBIES_OUT, exist_ok=True)
TRAVEL_OUT = "/home/claude/site/downloads/travel-events"
os.makedirs(TRAVEL_OUT, exist_ok=True)
HOME_OUT = "/home/claude/site/downloads/home-household"
os.makedirs(HOME_OUT, exist_ok=True)
HEALTH_OUT = "/home/claude/site/downloads/health-fitness"
os.makedirs(HEALTH_OUT, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
os.makedirs(EDU_OUT, exist_ok=True)
os.makedirs(IT_OUT, exist_ok=True)
os.makedirs(SB_OUT, exist_ok=True)
os.makedirs(PM_OUT, exist_ok=True)

TEMPLATES = [
    ("monthly-household-budget-planner", "Monthly Household Budget", A.monthly_budget, "Enter planned and actual amounts for each income source and expense category."),
    ("zero-based-budget", "Zero-Based Budget", A.zero_based, "Enter income, then assign every amount until Left to assign is zero."),
    ("envelope-budgeting-tracker", "Envelope Budgeting Tracker", A.envelope, "Set each envelope's monthly allocation and record spending as it happens."),
    ("expense-tracker", "Expense Tracker", A.expense_tracker, "Log each expense on the Expenses sheet. Use the category names listed on the Summary sheet."),
    ("income-vs-expenses-summary", "Income vs Expenses Summary", A.income_vs_expenses, "Enter monthly income and expenses. The net, cumulative and savings rate columns calculate automatically."),
    ("debt-snowball-calculator", "Debt Snowball Calculator", A.snowball, "Enter each debt, its rate and minimum payment. The extra payment goes to the priority-1 debt."),
    ("debt-avalanche-calculator", "Debt Avalanche Calculator", A.avalanche, "Enter each debt, its rate and minimum payment. The extra payment goes to the highest-rate debt."),
    ("loan-amortisation-schedule", "Loan Amortisation Schedule", A.amortisation, "Enter the loan amount, annual rate and term. The schedule shows each payment split into interest and principal."),
    ("mortgage-repayment-calculator", "Mortgage Repayment Calculator", B.mortgage, "Enter the property price, deposit, rate and term to estimate repayments and total cost."),
    ("car-loan-comparison", "Car Loan Comparison", B.car_loan, "Enter up to three offers. The total paid and lowest-cost offer calculate automatically."),
    ("savings-goal-tracker", "Savings Goal Tracker", B.savings_goal, "Set your goal and monthly plan, then log each deposit in the table."),
    ("emergency-fund-calculator", "Emergency Fund Calculator", B.emergency_fund, "List essential monthly costs and choose months of cover to find your target."),
    ("net-worth-tracker", "Net Worth Tracker", B.net_worth, "Record assets and liabilities on the same date each month to track net worth."),
    ("subscription-cost-tracker", "Subscription Cost Tracker", B.subscriptions, "Enter each subscription and its billing cycle. Monthly and yearly costs calculate automatically."),
    ("bill-payment-calendar", "Bill Payment Calendar", B.bill_calendar, "List each bill with its due day. Mark it Yes or No each month using the drop-down."),
    ("annual-cash-flow-forecast", "Annual Cash-Flow Forecast", B.cash_flow, "Enter your opening balance and expected income and expenses for each month."),
    ("credit-card-payoff-planner", "Credit Card Payoff Planner", B.card_payoff, "Enter the balance, APR and monthly payment to see how long payoff takes."),
    ("retirement-savings-projection", "Retirement Savings Projection", C.retirement, "Enter your age, retirement age, savings and growth rate to project your balance."),
    ("compound-interest-calculator", "Compound Interest Calculator", C.compound, "Enter a starting amount, monthly saving, rate and years to see growth."),
    ("sinking-funds-planner", "Sinking Funds Planner", C.sinking_funds, "List costs that come up later. The monthly set-aside shows how much to save each month."),
    ("tax-estimate-calculator", "Tax Estimate Calculator", C.tax_estimate, "Enter income, allowance and tax bands. Check rates against your local tax authority."),
    ("freelancer-income-tracker", "Freelancer Income Tracker", C.freelancer, "Log each piece of work with hours, rate and payment status. Tax set-aside calculates automatically."),
    ("price-comparison-sheet", "Price Comparison Sheet", C.price_compare, "Enter each option's price and quantity. The Best flag marks the lowest price per unit."),
    ("weekly-grocery-budget", "Weekly Grocery Budget", C.weekly_grocery, "Set your weekly budget and enter what you spend each week."),
    ("holiday-gift-budget", "Holiday Gift Budget", C.gift_budget, "Plan each gift with a limit, then record the actual cost."),
]

EDU_TEMPLATES = [
    ("gradebook-weighted-averages", "Gradebook with Weighted Averages", EA.gradebook, "Enter marks for each assessment, then set the maximum marks and weights in rows 6 and 7."),
    ("attendance-register", "Attendance Register", EA.attendance, "Enter P, L, A or E for each student each day, using the drop-down list."),
    ("seating-plan-generator", "Seating Plan Generator", EA.seating, "Type student names in list order. The grid fills in seat by seat, left to right, row by row."),
    ("lesson-plan-template", "Lesson Plan Template", EA.lesson_plan, "Fill in the lesson details, then list each stage with its minutes. Time left shows whether the plan fits."),
    ("scheme-of-work-planner", "Scheme of Work Planner", EA.scheme_of_work, "Enter planned and taught lessons for each week. Lessons left and status update automatically."),
    ("termly-timetable", "Termly Timetable", EA.timetable, "Pick a subject for each period from the Subjects list. Lesson counts per subject update automatically."),
    ("rubric-scoring-sheet", "Rubric Scoring Sheet", EA.rubric, "Set the weights in row 6, then score each criterion from 1 to 4 for each student."),
    ("mark-sheet-grade-boundaries", "Mark Sheet with Grade Boundaries", EA.mark_sheet, "Enter each mark and its total. Grades come from the boundary table on the right."),
    ("assessment-tracker-learning-objective", "Assessment Tracker by Learning Objective", EB.assessment_objectives, "Score each student 0, 1 or 2 for each objective. Secure counts update automatically."),
    ("student-progress-tracker", "Student Progress Tracker", EB.student_progress, "Enter test percentages, then set the Support and Stretch thresholds to flag students."),
    ("homework-tracker", "Homework Tracker", EB.homework, "Set due dates in row 6, then mark each student Y, L or N for each task."),
    ("behaviour-points-log", "Behaviour Points Log", EB.behaviour_points, "Log points on the Log sheet. Totals by student appear on the Summary sheet."),
    ("parent-contact-log", "Parent Contact Log", EB.parent_contact, "Log each contact on the Log sheet. Open follow-ups are counted on the Summary sheet."),
    ("class-roster", "Class Roster", EB.class_roster, "Enter student details and tutor groups. Totals per tutor group update automatically."),
    ("reading-log", "Reading Log", EB.reading_log, "Log each book with its pages and dates. Days taken and pages per day calculate automatically."),
    ("quiz-score-analyser", "Quiz Score Analyser", EB.quiz_analyser, "Enter 1 for each correct answer and 0 for each incorrect answer. Difficulty updates automatically."),
    ("exam-timetable-planner", "Exam Timetable Planner", EB.exam_timetable, "Enter the date, start time and length of each exam. Check the same-day warnings."),
    ("revision-schedule", "Revision Schedule", EC.revision_schedule, "Enter planned and completed hours for each topic. Hours left and % complete calculate automatically."),
    ("student-project-tracker", "Student Project Tracker", EC.project_tracker, "Set the report date, then enter due and completion dates. Status updates automatically."),
    ("lab-equipment-booking", "Lab Equipment Booking", EC.lab_booking, "Book a room and equipment for each period. The check column flags room clashes and over-booked stock."),
    ("classroom-budget-tracker", "Classroom Budget Tracker", EC.classroom_budget, "Set budgets on the Budget sheet and log purchases on the Spending sheet."),
    ("club-signup-sheet", "Club Sign-up Sheet", EC.club_signup, "Enter each student's first and second choice. Spaces left and status update automatically."),
    ("group-work-rotation-planner", "Group-Work Rotation Planner", EC.group_rotation, "Enter the number of groups, then list students in order. Group numbers for each round calculate automatically."),
    ("report-card-comment-bank", "Report Card Comment Bank", EC.report_comments, "Edit comments on the Comment bank sheet. Choose codes for each student on the Report sheet."),
    ("course-completion-checklist", "Course Completion Checklist", EC.course_checklist, "Mark each item Yes or No. Section progress updates automatically."),
]

IT_TEMPLATES = [
    ("it-asset-register", "IT Asset Register", IA.asset_register, "Enter each device's tag, type, location and cost. Age calculates from the report date."),
    ("software-licence-tracker", "Software Licence Tracker", IA.licence_tracker, "Enter seats owned and used, and expiry dates. Over-allocated and expiring licences are flagged."),
    ("help-desk-ticket-log", "Help Desk Ticket Log", IA.help_desk, "Log each ticket with its priority. Hours to resolve and SLA breaches calculate automatically."),
    ("server-backup-log", "Server Backup Schedule Log", IA.backup_log, "Log each backup run with its start and end times. Duration and success rates calculate automatically."),
    ("ip-address-planner", "IP Address Planner", IA.ip_planner, "Enter the hosts each department needs. Block size, prefix and spare addresses calculate automatically."),
    ("network-device-inventory", "Network Device Inventory", IA.network_inventory, "Record each device and its warranty end date. Warranty status compares with the report date."),
    ("hardware-refresh-planner", "Hardware Refresh Planner", IA.hardware_refresh, "Enter purchase dates and lifespans. Refresh dates and the budget needed in the next 12 months calculate automatically."),
    ("sprint-backlog-burndown", "Sprint Backlog and Burndown", IA.sprint_burndown, "Enter story points and status, then log remaining points each day to compare with the ideal line."),
    ("bug-tracker", "Bug Tracker", IB.bug_tracker, "Log each bug with severity and status. Days open calculate from the report date."),
    ("test-case-log", "Test Case Log", IB.test_cases, "Record each test's expected and actual result. The pass rate calculates automatically."),
    ("code-review-checklist", "Code Review Checklist", IB.code_review, "Mark each check Pass, Fail or N/A for each file. The pass rate calculates automatically."),
    ("website-traffic-summary", "Website Traffic Summary", IB.traffic_summary, "Enter monthly visits and page views. Ratios, changes and the busiest month calculate automatically."),
    ("cloud-cost-estimator", "Cloud Cost Estimator", IB.cloud_cost, "Enter quantities, unit prices and hours for each service. Monthly and yearly costs calculate automatically."),
    ("uptime-incident-log", "Uptime and Incident Log", IB.uptime_log, "Log each outage with its start and end. Downtime and uptime for the month calculate automatically."),
    ("change-request-log", "Change Request Log", IB.change_requests, "Log each change with its impact and approval. Days to deliver and overdue changes are counted."),
    ("data-cleansing-checklist", "Data Cleansing Checklist", IB.data_cleansing, "Work through the steps in order and record how many rows each step changed."),
    ("data-dictionary-template", "Data Dictionary Template", IB.data_dictionary, "Describe each field, its type and whether it is required. Completeness is checked automatically."),
    ("api-endpoint-documentation", "API Endpoint Documentation", IC.api_docs, "Document each endpoint's method, authentication, parameters and responses."),
    ("release-checklist", "Release Checklist", IC.release_checklist, "Set the version, then tick each task. Progress by stage calculates automatically."),
    ("computer-lab-booking-maintenance", "Computer Lab Booking and Maintenance Log", IC.lab_maintenance, "Log lab bookings and maintenance tasks. Costs and tasks due in the next 30 days calculate automatically."),
    ("printer-consumables-tracker", "Printer and Consumables Tracker", IC.printers, "Enter toner levels and cartridge costs. Reorder flags and cost per page calculate automatically."),
    ("new-device-onboarding-checklist", "New-Device Onboarding Checklist", IC.onboarding, "Mark each onboarding step Yes as it is done. Completion for each device calculates automatically."),
    ("binary-hex-conversion-practice", "Binary and Hexadecimal Conversion Practice", IC.binary_hex, "Type your answers as text. Each answer is checked automatically."),
    ("algorithm-trace-table", "Algorithm Trace Table", IC.algorithm_trace, "Trace the program by hand, filling in n and total at each step. The final total is checked."),
    ("program-testing-record", "Program Testing Record", IC.program_testing, "Record each test's input, expected and actual output. Pass or fail calculates automatically."),
]

SB_TEMPLATES = [
    ("invoice-generator", "Invoice Generator", SA.invoice, "Enter your details and line items. Subtotal, VAT and the balance due calculate automatically."),
    ("quote-estimate-template", "Quote and Estimate Template", SA.quote, "Enter the work and prices. Discount, VAT and the quote total calculate automatically."),
    ("purchase-order-log", "Purchase Order Log", SA.purchase_orders, "Log each order and its status. Totals and the value of open orders calculate automatically."),
    ("accounts-receivable-aging-report", "Accounts Receivable Aging Report", SA.receivables, "Enter unpaid invoices and the report date. Days overdue and age buckets calculate automatically."),
    ("accounts-payable-tracker", "Accounts Payable Tracker", SA.payables, "Log supplier bills and payments. Days to due and payment status calculate from the report date."),
    ("profit-and-loss-statement", "Profit and Loss Statement", SA.profit_and_loss, "Enter income and costs. Gross profit, operating profit and net profit calculate automatically."),
    ("cash-flow-forecast", "Cash Flow Forecast", SA.cash_flow, "Enter opening cash and expected money in and out each month. Closing balances carry forward."),
    ("break-even-analysis", "Break-even Analysis", SA.break_even, "Enter fixed costs, price and variable cost. The break-even point and profit at planned sales calculate automatically."),
    ("inventory-stock-count-sheet", "Inventory Stock Count Sheet", SB.inventory_count, "Enter the system and counted figures. Differences and their value calculate automatically."),
    ("reorder-level-calculator", "Reorder Level Calculator", SB.reorder_level, "Enter sales rate, lead time and safety stock. The reorder level and action calculate automatically."),
    ("payroll-calculator", "Payroll Calculator", SB.payroll, "Enter gross pay. Tax, contributions and net pay calculate from the example rates at the top. Replace them with your local rates."),
    ("timesheet-overtime", "Timesheet with Overtime", SB.timesheet, "Enter daily hours. Regular hours, overtime and gross pay calculate automatically."),
    ("mileage-log", "Mileage Log", SB.mileage, "Log each business journey. Claim amounts calculate from the rate per kilometre."),
    ("expense-claim-form", "Expense Claim Form", SB.expense_claim, "Itemise each expense. Lines without a receipt are flagged automatically."),
    ("petty-cash-register", "Petty Cash Register", SB.petty_cash, "Log money in and out. The running balance and the cash count check calculate automatically."),
    ("vat-sales-tax-calculator", "VAT and Sales Tax Calculator", SB.vat_calculator, "Enter net amounts and each item's rate. VAT and gross totals calculate automatically."),
    ("product-pricing-margin-calculator", "Product Pricing and Margin Calculator", SB.pricing_margin, "Enter cost and markup. Selling price, margin and the price for your target margin calculate automatically."),
    ("client-contact-list", "Client Contact List", SC.client_list, "Keep one row per client. Days since last contact and follow-ups calculate from the report date."),
    ("sales-pipeline-tracker", "Sales Pipeline Tracker", SC.sales_pipeline, "Log each deal and its stage. Probability and weighted value calculate from the stage table."),
    ("supplier-comparison", "Supplier Comparison", SC.supplier_comparison, "Enter each supplier's unit prices. The cheapest supplier and yearly totals calculate automatically."),
    ("business-plan-projections", "Business Plan Financial Projections", SC.business_plan, "Enter Year 1 and your growth and cost assumptions. Years 2 and 3 calculate from them."),
    ("asset-depreciation-schedule", "Asset Depreciation Schedule", SC.asset_depreciation, "Enter cost, salvage value and useful life. Straight-line depreciation for five years calculates automatically."),
    ("shift-rota", "Shift Rota", SC.shift_rota, "Enter a shift code for each person each day. Hours and cover per shift calculate automatically."),
    ("stock-valuation-fifo-lifo", "Stock Valuation (FIFO and LIFO)", SC.stock_valuation, "Enter purchase batches and units sold. Cost of sales and stock value calculate both ways."),
    ("refunds-returns-log", "Refunds and Returns Log", SC.refunds_log, "Log each refund or return with its reason and status. Totals calculate automatically."),
]

PM_TEMPLATES = [
    ("gantt-chart", "Gantt Chart", PA.gantt_chart, "Enter each task’s start and end date and its owner. Bars shade the weeks each task runs."),
    ("kanban-board", "Kanban Board", PA.kanban_board, "Log each card and set its column and due date. Days to due and the WIP check calculate automatically."),
    ("project-budget-tracker", "Project Budget Tracker", PA.project_budget, "Enter the budget, actual spend and commitments for each cost line. Forecast and variance calculate automatically."),
    ("task-list-priorities", "Task List with Priorities", PA.task_list, "Enter each task with its priority, status and due date. Days left and flags calculate from the report date."),
    ("milestone-tracker", "Milestone Tracker", PA.milestone_tracker, "Enter target and forecast dates for each milestone. Slip and the rating calculate automatically."),
    ("risk-register", "Risk Register", PA.risk_register, "Describe each risk and score its likelihood and impact from 1 to 5. The score and rating calculate automatically."),
    ("raci-matrix", "RACI Matrix", PA.raci_matrix, "List activities and set R, A, C or I for each role. The check flags any activity without exactly one A."),
    ("meeting-agenda-minutes-log", "Meeting Agenda and Minutes Log", PA.meeting_log, "Log each meeting’s date, chair, attendance and outcomes. Totals and averages calculate below the log."),
    ("action-items-tracker", "Action Items Tracker", PB.action_items, "Record each action with its owner and due date. Days overdue calculate from the report date."),
    ("resource-allocation-planner", "Resource Allocation Planner", PB.resource_allocation, "Enter each person’s capacity and hours per project. Utilisation and over-allocation flags calculate automatically."),
    ("time-tracking-by-project", "Time Tracking by Project", PB.time_tracking, "Log hours against a project each day. Billable hours and the project summary calculate automatically."),
    ("project-status-dashboard", "Project Status Dashboard", PB.project_dashboard, "Enter budget, spend and planned and actual progress. The health rating and chart update automatically."),
    ("weekly-team-status-report", "Weekly Team Status Report", PB.weekly_status, "Enter each team member’s progress, plans, blockers and confidence. RAG totals calculate below the table."),
    ("decision-log", "Decision Log", PB.decision_log, "Record each decision with its options and review date. Reviews due calculate from the report date."),
    ("stakeholder-register", "Stakeholder Register", PB.stakeholder_register, "Rate each stakeholder’s interest and influence, then set current and desired stance. Approach and gap calculate automatically."),
    ("change-control-log", "Change Control Log", PB.change_control, "Log each change with its effort and schedule impact. Approved impact adds up in the running total."),
    ("work-breakdown-structure", "Work Breakdown Structure", PC.work_breakdown, "Enter WBS codes such as 1, 1.1 and 1.2. Level calculates from the code and estimates total the work packages."),
    ("capacity-planning-sheet", "Capacity Planning Sheet", PC.capacity_planning, "Enter headcount, hours and four weeks of demand for each role. Capacity, peak demand and gaps calculate automatically."),
    ("vendor-evaluation-scorecard", "Vendor Evaluation Scorecard", PC.vendor_scorecard, "Set the criteria weights and score each vendor from 1 to 5. Weighted scores, ranks and the top vendor calculate automatically."),
    ("lessons-learned-log", "Lessons Learned Log", PC.lessons_learned, "Record what happened, the lesson and the next action. Totals by category calculate below the log."),
    ("okr-tracker", "OKR Tracker", PC.okr_tracker, "Enter each key result’s start value, target and current value. Progress and status calculate automatically."),
    ("personal-goal-tracker", "Personal Goal Tracker", PC.personal_goals, "Enter each goal’s milestones and how many are done. Percent complete, days left and status calculate automatically."),
    ("event-run-sheet", "Event Run Sheet", PC.event_run_sheet, "Enter each item’s start time and length. Finish times and the event timings calculate automatically."),
    ("document-version-register", "Document Version Register", PC.document_versions, "Log each version of a document with its author, status and approver. Totals calculate below the register."),
    ("onboarding-task-checklist", "Onboarding Task Checklist", PC.onboarding_checklist, "Set the start date and give each task a day offset. Due dates and completion rate calculate automatically."),
]

HEALTH_TEMPLATES = [
    ("workout-log", "Workout Log", hw_a.workout_log, "Enter the date, exercise, sets, reps and weight for each set. Volume calculates for each line."),
    ("running-training-plan", "Running Training Plan", hw_a.running_plan, "Enter the planned and actual distance for each run. Differences and completion calculate automatically."),
    ("weight-tracker", "Weight Tracker", hw_a.weight_tracker, "Enter the date and weight each time you weigh yourself. Change since the first entry calculates automatically."),
    ("calorie-and-macro-tracker", "Calorie and Macro Tracker", hw_a.calorie_macro, "Enter each food with its values from the label. Totals calculate for each entry."),
    ("meal-planner", "Meal Planner", hw_a.meal_planner, "Enter each day's meals and prep time. The totals and planned days calculate at the foot of the sheet."),
    ("water-intake-tracker", "Water Intake Tracker", hw_a.water_intake, "Enter the number of cups each day. Millilitres and totals calculate automatically."),
    ("sleep-log", "Sleep Log", hw_a.sleep_log, "Enter bedtime, wake time and a rested score from 1 to 5. Hours slept calculate automatically."),
    ("habit-tracker", "Habit Tracker", hw_a.habit_tracker, "Enter each habit and its weekly target, then choose Yes or No for each day."),
    ("daily-reflection-journal", "Daily Reflection Journal", hw_b.daily_reflection, "Write a short entry each day. Nothing is calculated, so keep it as simple as you like."),
    ("medication-reminder-schedule", "Medication Reminder Schedule", hw_b.medication_schedule, "Enter each medicine as written on its label, its time and refill date. Days to refill calculate from the report date."),
    ("blood-pressure-log", "Blood Pressure Log", hw_b.blood_pressure, "Enter your limits above the table, then log each reading. Each reading is checked against your limits."),
    ("blood-glucose-log", "Blood Glucose Log", hw_b.blood_glucose, "Enter your range above the table, then log each reading in the units your meter shows."),
    ("step-count-tracker", "Step Count Tracker", hw_b.step_count, "Set your daily goal above the table, then enter the steps for each day."),
    ("body-measurement-tracker", "Body Measurement Tracker", hw_b.body_measurements, "Measure in the same places each time and enter the results. Waist change calculates automatically."),
    ("strength-progression-chart", "Strength Progression Chart", hw_b.strength_progression, "Enter each lift's exercise, weight and reps. The estimate and best-so-far values calculate automatically."),
    ("cycling-log", "Cycling Log", hw_b.cycling_log, "Enter distance, moving time and elevation for each ride. Average speed calculates automatically."),
    ("recipe-nutrition-calculator", "Recipe Nutrition Calculator", hw_c.recipe_nutrition, "Enter each ingredient's grams and its values per 100 g, and the number of servings above the table."),
    ("baby-feeding-and-nappy-log", "Baby Feeding and Nappy Log", hw_c.baby_log, "Enter each feed or nappy with its time. Totals calculate in the summary."),
    ("childcare-schedule", "Childcare Schedule", hw_c.childcare_schedule, "Enter each day's slot, carer and times. Hours calculate for each slot."),
    ("symptom-diary", "Symptom Diary", hw_c.symptom_diary, "Enter when a symptom happened, how severe it was from 0 to 10, and what was going on."),
    ("stretching-routine-planner", "Stretching Routine Planner", hw_c.stretching_planner, "Enter each stretch with its hold time and sets. Time per stretch and the routine total calculate automatically."),
    ("team-sports-stats-tracker", "Team Sports Stats Tracker", hw_c.sports_stats, "Enter each player's stats for a match. Goals per 90 minutes calculate for each line."),
    ("annual-health-check-reminders", "Annual Health Check Reminders", hw_c.health_check_reminders, "Enter each check-up and its next due date. Days until due and status calculate from the report date."),
    ("gym-membership-cost-tracker", "Gym Membership Cost Tracker", hw_c.gym_cost, "Enter each month's fees, extras and number of visits. Total spend and cost per visit calculate automatically."),
    ("screen-time-log", "Screen Time Log", hw_c.screen_time, "Enter the date, device or app, minutes and category for each session. Hours calculate for each entry."),
]

HOME_TEMPLATES = [
    ("chore-rota", "Chore Rota", home_a.chore_rota, "Enter each chore with who does it, when, how often and roughly how long it takes."),
    ("home-maintenance-schedule", "Home Maintenance Schedule", home_a.maintenance_schedule, "Enter each job, when it was last done and how often it repeats. Next due and status calculate automatically."),
    ("household-inventory-insurance", "Household Inventory for Insurance", home_a.inventory_for_insurance, "Enter each item, its price and replacement value, and whether you kept a receipt or photo."),
    ("pantry-inventory", "Pantry Inventory", home_a.pantry_inventory, "Enter each item, its quantity, use-by date and reorder level. Status and days to use-by calculate automatically."),
    ("meal-plan-shopping-list", "Meal Plan and Shopping List", home_a.meal_plan_shopping, "Enter each meal's ingredients with quantity and aisle. Tick them off as you shop."),
    ("cleaning-schedule", "Cleaning Schedule", home_a.cleaning_schedule, "Enter each area and task with its frequency and last date. Next due and status calculate from the report date."),
    ("garden-planting-planner", "Garden Planting Planner", home_a.garden_planner, "Enter the sowing and harvest windows, spacing and row length for each crop. Plants per row and stage calculate automatically."),
    ("home-energy-usage-tracker", "Home Energy Usage Tracker", home_a.energy_tracker, "Enter each meter reading. Use since the last reading calculates automatically; add your tariff rates for costs."),
    ("utility-bill-comparison", "Utility Bill Comparison", home_b.utility_comparison, "Enter each tariff's standing charge, unit rate and your expected monthly use. Costs and ranks calculate automatically."),
    ("moving-checklist", "Moving Checklist", home_b.moving_checklist, "List each task with its owner, due date and status. Days left calculate from the report date."),
    ("home-renovation-budget", "Home Renovation Budget", home_b.renovation_budget, "Enter each quote and actual cost by room, and set your contingency above the table."),
    ("paint-materials-calculator", "Paint and Materials Calculator", home_b.paint_calculator, "Set the coverage and tin size above the table, then enter each room's dimensions and openings."),
    ("wardrobe-inventory", "Wardrobe Inventory", home_b.wardrobe_inventory, "Enter each item with its price and how many times you have worn it. Cost per wear calculates automatically."),
    ("pet-care-log", "Pet Care Log", home_b.pet_care_log, "Enter each pet's activity, details and cost. Totals and vet visits calculate in the summary."),
    ("plant-watering-schedule", "Plant Watering Schedule", home_b.plant_watering, "Enter how often each plant needs water and when it was last watered. Next watering and status calculate automatically."),
    ("birthday-anniversary-reminders", "Birthday and Anniversary Reminder List", home_b.birthday_reminders, "Enter each date by day and month. Days until the next one calculate from the report date."),
    ("warranty-tracker", "Warranty Tracker", home_c.warranty_tracker, "Enter each purchase date and warranty length. Expiry date, days left and status calculate automatically."),
    ("smart-home-device-list", "Smart Home Device List", home_c.smart_home_devices, "Enter each device with its room, connection and last update date. Devices needing a check are flagged."),
    ("packing-list", "Packing List", home_c.packing_list, "Enter each item, its quantity and bag, then mark it Yes when packed."),
    ("car-maintenance-log", "Car Maintenance Log", home_c.car_maintenance, "Enter each job with the odometer reading and cost. Total spent and the latest reading calculate automatically."),
    ("fuel-economy-tracker", "Fuel Economy Tracker", home_c.fuel_economy, "Enter each fill-up's odometer reading, litres and price. Distance, cost and economy calculate automatically."),
    ("vehicle-service-schedule", "Vehicle Service Schedule", home_c.vehicle_service, "Set the current odometer reading above the table, then enter each service interval and last reading."),
    ("recipe-scaling-calculator", "Recipe Scaling Calculator", home_c.recipe_scaling, "Enter the original and new servings above the table, then each ingredient's original amount."),
    ("house-sitting-instructions", "House-Sitting Instructions Sheet", home_c.house_sitting, "Write one instruction per row, with where things are and who to contact."),
    ("emergency-contacts-list", "Emergency Contacts List", home_c.emergency_contacts, "Enter each contact with their role, phone, email and address. Print a copy and keep it handy."),
]

TRAVEL_TEMPLATES = [
    ("trip-itinerary-planner", "Trip Itinerary Planner", travel_a.itinerary, "Enter each activity with its day, time, place and cost. The number of activities and total cost calculate automatically."),
    ("travel-budget", "Travel Budget", travel_a.travel_budget, "Enter each item's budget and actual spend. Amount left and status calculate automatically."),
    ("currency-conversion-log", "Currency Conversion Log", travel_a.currency_log, "Enter each foreign amount, currency and the rate charged. Home currency amounts and fees calculate automatically."),
    ("travel-packing-checklist", "Travel Packing Checklist", travel_a.travel_packing, "Enter each item, traveller, bag and weight. Set your baggage allowance above the table to see if you are over."),
    ("flight-and-hotel-comparison", "Flight and Hotel Comparison", travel_a.flight_hotel_comparison, "Enter each option's price, taxes and number of nights or journeys. Totals and ranks calculate automatically."),
    ("road-trip-fuel-calculator", "Road Trip Fuel Cost Calculator", travel_a.road_trip_fuel, "Enter each leg's distance, fuel use and price per litre. Set the number of people sharing the cost above the table."),
    ("event-budget-planner", "Event Budget Planner", travel_a.event_budget, "Enter each item's estimate and actual cost. Differences and over-estimate flags calculate automatically."),
    ("wedding-budget-planner", "Wedding Budget Planner", travel_a.wedding_budget, "Enter each item's priority, estimate and deposit. Balances and the budget with contingency calculate automatically."),
    ("passport-and-document-tracker", "Passport and Document Tracker", travel_b.passport_tracker, "Enter each traveller's document and expiry date. Days left and status calculate from the report date."),
    ("visa-and-entry-requirements-tracker", "Visa and Entry Requirements Tracker", travel_b.visa_tracker, "Enter each country, its requirement and deadline. Days to deadline and status calculate from the report date."),
    ("travel-insurance-comparison", "Travel Insurance Comparison", travel_b.insurance_comparison, "Enter each policy's premium, cover limit, excess and days covered. Cost per day and rank calculate automatically."),
    ("event-guest-list", "Event Guest List", travel_b.event_guest_list, "Enter each guest, their group, RSVP and plus-ones. Confirmed party size and totals calculate automatically."),
    ("event-run-sheet", "Event Run Sheet", travel_b.event_run_sheet, "Enter each slot's start time, length in minutes and owner. End times and the finish time calculate automatically."),
    ("wedding-seating-planner", "Wedding Seating Planner", travel_b.seating_planner, "Enter each table's seats and the number of guests placed there. Free seats and status calculate automatically."),
    ("event-volunteer-roster", "Event Volunteer Roster", travel_b.volunteer_roster, "Enter each volunteer's role, shift and hours. Booked hours and check-in counts calculate automatically."),
    ("travel-time-and-layover-planner", "Travel Time and Layover Planner", travel_b.travel_time_planner, "Enter each leg's departure and arrival in local time, plus the time zone change. Elapsed hours calculate automatically."),
    ("trip-expense-splitter", "Trip Expense Splitter", travel_c.trip_expense_split, "Enter each person and what they paid. Each share and balance calculate automatically."),
    ("travel-journal", "Travel Journal", travel_c.travel_journal, "Enter the date, place, highlight, a rating from 1 to 5 and notes."),
    ("destination-comparison-scorecard", "Destination Comparison Scorecard", travel_c.destination_scorecard, "Score each destination from 1 to 5 and set the weights above the table. Weighted scores and ranks calculate automatically."),
    ("event-ticket-tracker", "Event Ticket Tracker", travel_c.event_ticket_tracker, "Enter each order with its quantity, price each and delivery status. Totals calculate automatically."),
    ("event-feedback-summary", "Event Feedback Summary", travel_c.event_feedback_summary, "Enter how many people gave each star rating for each question. Responses and averages calculate automatically."),
    ("school-trip-consent-and-payment-tracker", "School Trip Consent and Payment Tracker", travel_c.school_trip_tracker, "Enter each participant, whether their form is returned, the amount due and the amount paid."),
    ("daily-travel-spending-limit", "Daily Travel Spending Limit", travel_c.daily_travel_budget, "Enter each date, its limit and what you spent. Left for the day and the running balance calculate automatically."),
    ("event-vendor-tracker", "Event Vendor Tracker", travel_c.event_vendor_tracker, "Enter each vendor's service, contact, quote and deposit. Balance owed calculates automatically."),
    ("trip-countdown-checklist", "Trip Countdown Checklist", travel_c.trip_countdown_checklist, "Enter each task, owner and due date, then mark it Yes when done. Days left and status calculate from the report date."),
]

HOBBIES_TEMPLATES = [
    ("photography-shot-log", "Photography Shot Log", hobby_a.photography_shot_log, "Enter the date, subject, lens, settings, rating and whether it is a keeper. Keeper count and average rating calculate automatically."),
    ("recipe-book-cost-per-serving", "Recipe Book with Cost per Serving", hobby_a.recipe_cost_per_serving, "Enter the servings above the table, then each ingredient with its quantity and price per unit. Cost per serving calculates automatically."),
    ("baking-ratio-calculator", "Baking Ratio Calculator", hobby_a.baking_ratio_calculator, "Enter flour in the first row and the other ingredients below it. Set the target flour weight above the table to scale the recipe."),
    ("home-brewing-log", "Home Brewing Log", hobby_a.home_brewing_log, "Enter each batch's original and final gravity. ABV calculates automatically."),
    ("knitting-pattern-row-counter", "Knitting Pattern Row Counter", hobby_a.knitting_row_counter, "Enter the rows in your pattern, then update rows done after each session. Rows left and progress calculate automatically."),
    ("model-railway-inventory", "Model Railway Inventory", hobby_a.model_railway_inventory, "Enter each item with its scale, type, condition and price. Total cost and items needing repair calculate automatically."),
    ("book-reading-tracker", "Book Reading Tracker", hobby_a.book_reading_tracker, "Enter the title, dates, pages and rating. Days to finish and totals calculate automatically."),
    ("film-watch-log", "Film Watch Log", hobby_a.film_watch_log, "Enter each title, the date watched, format, rating and whether you would rewatch it."),
    ("board-game-score-tracker", "Board Game Score Tracker", hobby_b.board_game_score_tracker, "Enter the game, date, player and score for each player. The winner of each game is marked automatically."),
    ("fantasy-league-points-calculator", "Fantasy League Points Calculator", hobby_b.fantasy_league_points, "Set the points per goal, assist and yellow card above the table. Enter each player's stats and points calculate automatically."),
    ("music-practice-log", "Music Practice Log", hobby_b.music_practice_log, "Enter the date, piece, minutes, focus, tempo and whether you reached your goal. Totals calculate automatically."),
    ("song-chord-planner", "Song Chord Planner", hobby_b.song_chord_planner, "Set the song's key above the table, then enter each section, chord, beats and strumming pattern."),
    ("art-supply-inventory", "Art Supply Inventory", hobby_b.art_supply_inventory, "Enter each item with its quantity, cost and reorder level. Stock value and reorder status calculate automatically."),
    ("seed-library-tracker", "Seed Library Tracker", hobby_b.seed_library_tracker, "Enter each variety, year harvested, packets and germination rate. Seeds to test before sowing are flagged automatically."),
    ("fishing-catch-log", "Fishing Catch Log", hobby_b.fishing_catch_log, "Enter the date, location, species, length, weight and method. Catch count and records calculate automatically."),
    ("bird-watching-log", "Bird Watching Log", hobby_b.bird_watching_log, "Enter the date, location, species, count and behaviour for each sighting. Totals and species count calculate automatically."),
    ("stamp-and-coin-collection-tracker", "Stamp and Coin Collection Tracker", hobby_c.stamp_coin_collection, "Enter each item with its condition, purchase price and current value. Gains and losses calculate automatically."),
    ("video-game-backlog-tracker", "Video Game Backlog Tracker", hobby_c.video_game_backlog_tracker, "Enter each game with its platform, status, hours played and priority. Counts and total hours calculate automatically."),
    ("podcast-episode-planner", "Podcast Episode Planner", hobby_c.podcast_episode_planner, "Enter each episode's dates, status and guest. Days to publish calculate from the report date."),
    ("writing-word-count-tracker", "Writing Word Count Tracker", hobby_c.writing_word_count_tracker, "Set your daily word goal above the table, then enter the date, project and words written each day."),
    ("novel-chapter-outline-planner", "Novel Chapter Outline Planner", hobby_c.novel_chapter_outline_planner, "Enter each chapter's title, summary, target and words written. Progress calculates automatically."),
    ("yarn-stash-inventory", "Yarn Stash Inventory", hobby_c.yarn_stash_inventory, "Enter each yarn with its skeins and metres per skein. Total metres calculate automatically."),
    ("woodworking-cut-list", "Woodworking Cut List", hobby_c.woodworking_cut_list, "Enter each part's quantity, length, width and thickness in millimetres. Face area calculates automatically."),
    ("sewing-measurement-chart", "Sewing Measurement Chart", hobby_c.sewing_measurement_chart, "Enter your measurements above the table, then each pattern size's bust, waist and hip. Ease calculates automatically."),
    ("vinyl-record-catalogue", "Vinyl Record Catalogue", hobby_c.vinyl_record_catalogue, "Enter each record's artist, album, year, format, label, price and condition. Totals calculate automatically."),
]

SALES_TEMPLATES = [
    ("social-media-content-calendar", "Social Media Content Calendar", sales_a.social_media_calendar, "Enter each post's date, platform, topic, type and status. Engagement rate calculates from likes and reach."),
    ("email-campaign-tracker", "Email Campaign Tracker", sales_a.email_campaign_tracker, "Enter each campaign's send date, emails sent, opened and clicked. Open and click rates calculate automatically."),
    ("marketing-budget-and-roi-tracker", "Marketing Budget and ROI Tracker", sales_a.marketing_budget_and_roi, "Enter each channel's budget, spend and revenue. Return on investment calculates for each channel and overall."),
    ("lead-tracker", "Lead Tracker", sales_a.lead_tracker, "Enter each lead's source, status, value and follow-up date. Open leads, pipeline value and days to follow-up calculate automatically."),
    ("customer-database", "Customer Database", sales_a.customer_database, "Enter each customer's contact details, total spend, last order and tier."),
    ("sales-commission-calculator", "Sales Commission Calculator", sales_a.sales_commission_calculator, "Set the commission rates above the table, then enter each salesperson's sales and target."),
    ("monthly-sales-forecast", "Monthly Sales Forecast", sales_a.monthly_sales_forecast, "Enter each month's forecast and actual sales as they come in. Variance calculates automatically."),
    ("seo-keyword-tracker", "SEO Keyword Tracker", sales_a.seo_keyword_tracker, "Enter each keyword, its page, monthly searches, current position and target. Places to gain calculate automatically."),
    ("ad-spend-tracker", "Ad Spend Tracker", sales_b.ad_spend_tracker, "Enter each campaign's platform, spend, impressions and clicks. Cost per click and click-through rate calculate automatically."),
    ("customer-feedback-summary", "Customer Feedback Summary", sales_b.customer_feedback_summary, "Enter the number of positive, neutral and negative comments for each topic. Totals and positive share calculate automatically."),
    ("net-promoter-score-tracker", "Net Promoter Score Tracker", sales_b.net_promoter_score_tracker, "Enter each score from 0 to 10. Each response is grouped automatically, and the score calculates from the totals."),
    ("customer-churn-analysis", "Customer Churn Analysis", sales_b.customer_churn_analysis, "Enter each month's starting customers, new customers and lost customers. Closing count and churn rate calculate automatically."),
    ("competitor-comparison-matrix", "Competitor Comparison Matrix", sales_b.competitor_comparison_matrix, "Rate each feature from 1 to 5 for your business and each competitor. Totals and the best in class calculate automatically."),
    ("swot-analysis", "SWOT Analysis", sales_b.swot_analysis, "Enter each point with its category, impact, action and owner. Counts by category calculate automatically."),
    ("event-attendance-tracker", "Event Attendance Tracker", sales_b.event_attendance_tracker, "Enter each event's registrations, attendance, leads captured and cost. Attendance rate and cost per lead calculate automatically."),
    ("support-ticket-sla-tracker", "Support Ticket SLA Tracker", sales_b.support_ticket_sla_tracker, "Enter when each ticket opened and was resolved, and its target in hours. Hours taken and whether the target was met calculate automatically."),
    ("warehouse-picking-list", "Warehouse Picking List", sales_c.warehouse_picking_list, "Enter each order line with its location, quantity ordered and quantity picked. Short lines are flagged automatically."),
    ("order-fulfilment-tracker", "Order Fulfilment Tracker", sales_c.order_fulfilment_tracker, "Set your target days to ship above the table, then enter each order's dates, carrier and tracking number."),
    ("shipping-cost-calculator", "Shipping Cost Calculator", sales_c.shipping_cost_calculator, "Set your fees and rates above the table, then enter each destination, parcel weight and number of parcels."),
    ("restaurant-food-cost-calculator", "Restaurant Food Cost Calculator", sales_c.restaurant_food_cost_calculator, "Set your target food cost above the table, then enter each dish's ingredient cost and menu price."),
    ("staff-training-log", "Staff Training Log", sales_c.staff_training_log, "Enter each course with its date, hours and certificate expiry date. Days to expiry and status calculate from the report date."),
    ("employee-leave-tracker", "Employee Leave Tracker", sales_c.employee_leave_tracker, "Set the annual leave allowance above the table, then enter each request's dates and approval. Working days calculate automatically."),
    ("performance-review-scorecard", "Performance Review Scorecard", sales_c.performance_review_scorecard, "Enter a 1 to 5 score for each criterion. The average and rating band calculate automatically."),
    ("recruitment-candidate-tracker", "Recruitment Candidate Tracker", sales_c.recruitment_candidate_tracker, "Enter each candidate's role, source, stage and interview score. Days in process and active candidates calculate from the report date."),
    ("shift-handover-log", "Shift Handover Log", sales_c.shift_handover_log, "Enter each handover's date, shift, people, issues and whether action is needed. Open actions are counted automatically."),
]

_orig_save = Workbook.save
CURRENT = {}

def _save_with_howto(self, path):
    if "How to use" not in self.sheetnames:
        how_to_sheet(self, "How to use", CURRENT["title"], [
            CURRENT["step"],
            "Only type in cream cells. White and coloured cells are formulas that update automatically.",
            "Read the mint summary boxes for your key results.",
        ])
    self.active = 0
    self.calculation.fullCalcOnLoad = True
    _orig_save(self, path)

Workbook.save = _save_with_howto

if __name__ == "__main__":
    only = sys.argv[1:]
    jobs = [(OUT, t) for t in TEMPLATES] + [(EDU_OUT, t) for t in EDU_TEMPLATES] + [(IT_OUT, t) for t in IT_TEMPLATES] + [(SB_OUT, t) for t in SB_TEMPLATES] + [(PM_OUT, t) for t in PM_TEMPLATES]
    jobs += [(HEALTH_OUT, t) for t in HEALTH_TEMPLATES]
    jobs += [(HOME_OUT, t) for t in HOME_TEMPLATES]
    jobs += [(TRAVEL_OUT, t) for t in TRAVEL_TEMPLATES]
    jobs += [(HOBBIES_OUT, t) for t in HOBBIES_TEMPLATES]
    jobs += [(SALES_OUT, t) for t in SALES_TEMPLATES]
    for out_dir, (slug, title, fn, step) in jobs:
        if only and slug not in only:
            continue
        CURRENT.update(title=title, step=step)
        path = os.path.join(out_dir, slug + ".xlsx")
        fn(path)
        print("built", slug)
