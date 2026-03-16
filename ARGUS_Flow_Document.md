# ARGUS — Productivity Intelligence
## Complete Application Flow

---

## Manager Flow

### Screen 1: Login

The login screen has two tabs — Manager and Employee. Managers enter their email and password. Employees enter only their email. The selected role determines which dashboard the user sees.

**[Screenshot: Login page with Manager tab selected]**

---

### Screen 2: Manager Dashboard — Overview

The manager's main view. At the top, four stat cards show the total employee count, the team's average score, the top performer (name and score), and the person who needs the most support (lowest score).

Below the stats, a Category Averages section shows bar charts for the four scoring dimensions: Task Completion, Timeliness, Communication, and Engagement. This gives managers a quick read on where the team is strong and where it is falling behind.

**[Screenshot: Manager dashboard showing the four stat cards and category average bars]**

---

### Screen 3: Team Leaderboard

Below the category averages, a Team Scores table lists every employee with their individual scores across all four categories plus an overall score. Each score cell is color-coded:

- Green for Excellent (80+)
- Yellow for Good (60-79)
- Orange for Average (40-59)
- Red for Needs Work (below 40)

A trend arrow next to each employee shows whether their performance is improving, declining, or stable. Clicking any row navigates to that employee's detailed view.

**[Screenshot: Team leaderboard table with color-coded scores and trend arrows]**

---

### Screen 4: Employee Detail — Score and Breakdown

Clicking an employee from the leaderboard opens their detail page. The top section shows two things side by side:

- A large circular score gauge displaying their overall productivity score with a color-coded label (Excellent, Good, Average, Needs Work)
- A score breakdown with four horizontal progress bars showing Task Completion (40% weight), Timeliness (25%), Communication (20%), and Engagement (15%)

**[Screenshot: Employee detail page showing the score gauge and breakdown bars]**

---

### Screen 5: Employee Detail — AI Recommendations

Below the score breakdown, ARGUS displays AI-generated recommendations for the employee. Each advice card shows an actionable insight with a priority level (High, Medium, Low) color-coded in red, orange, or green. Categories include Focus, Time Management, Communication, and Engagement.

These recommendations are generated based on the employee's actual performance data across ECHO and HERA.

**[Screenshot: AI recommendation cards with priority badges and category labels]**

---

### Screen 6: Employee Detail — Score History

At the bottom of the detail page, a score history table shows how the employee's scores have changed over time. Each row includes the date and scores for all four categories plus the overall score. A collapsible Raw Metrics section shows the underlying data used for the calculations.

**[Screenshot: Score history table showing trends over multiple dates]**

---

## Employee Flow

### Screen 7: Employee Login

Employees select the "Employee" tab on the login page and enter only their email address. They are taken to their personal score page.

**[Screenshot: Login page with Employee tab selected]**

---

### Screen 8: My Score — Personal Dashboard

The employee sees their own productivity score in the same format as the manager's view — a score gauge and breakdown bars. But they also get an exclusive section: "How is my score calculated?" which expands to show the exact formula:

- Task Completion (40%) — completion rate and priority-weighted output from HERA
- Timeliness (25%) — on-time delivery rate for tasks with deadlines
- Communication (20%) — email suggestion acceptance rate from ECHO
- Engagement (15%) — notification read and action rate from ECHO

A note at the bottom states: "All data is sourced transparently. No subjective factors."

**[Screenshot: My Score page showing the score gauge, breakdown, and expanded formula explanation]**

---

### Screen 9: My Score — Recommendations

Below the formula section, employees see their personalized AI recommendations. Unlike the manager's view, employees can dismiss recommendations that they have already acted on or find irrelevant. Dismissed cards are removed from the list.

**[Screenshot: Recommendation cards with dismiss (X) buttons]**

---

### Screen 10: My Score — History and Raw Data

At the bottom, employees can view their score history table and expand a Raw Data section to see exactly what metrics were used in their calculations. This supports the transparency principle — employees can verify that their scores are based on objective, measurable data.

**[Screenshot: Score history table and expanded raw data section]**

---

### Cross-Module Connections

- Task completion and timeliness data comes from HERA (task status transitions, deadline adherence)
- Communication scores come from ECHO (how often employees accept, modify, or reject AI-suggested replies)
- Engagement scores come from ECHO (notification read rates, action rates on alerts)
- ARGUS pulls this data through cross-service APIs, calculates weighted scores, and generates AI recommendations
- Managers use ARGUS insights to make informed decisions about task assignments in HERA
