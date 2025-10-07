# TESTING DOCUMENTATION FOR JUNIOR DEVELOPERS

## Table of Contents
1. [Introduction to Software Testing](#introduction-to-software-testing)
2. [Why Testing Matters](#why-testing-matters)
3. [Types of Testing](#types-of-testing)
4. [Testing Tools & Environment](#testing-tools--environment)
5. [Complete Testing Checklist](#complete-testing-checklist)
6. [How to Test Each Feature](#how-to-test-each-feature)
7. [Edge Cases Explained](#edge-cases-explained)
8. [How to Report Bugs](#how-to-report-bugs)
9. [Best Practices](#best-practices)

---

## Introduction to Software Testing

**What is Software Testing?**
Software testing is the process of verifying that a software application works as expected. It involves:
- Running the application with different inputs
- Checking that outputs match expectations
- Finding bugs before users do
- Ensuring the application handles errors gracefully

**Definition: Bug**
A bug (also called a defect or issue) is any behavior in the software that doesn't match the intended design or causes problems for users.

**Definition: Test Case**
A test case is a specific scenario you test, including:
- **Input:** What you enter or click
- **Expected Output:** What should happen
- **Actual Output:** What actually happens
- **Pass/Fail:** Whether they match

---

## Why Testing Matters

### For Users:
- **Prevents Frustration:** Users don't encounter errors that make them lose data
- **Builds Trust:** Reliable software means users trust your application
- **Better Experience:** Smooth, bug-free interactions keep users happy

### For Developers:
- **Catches Bugs Early:** Finding bugs during testing is cheaper than fixing them in production
- **Prevents Regression:** Ensures new changes don't break existing features
- **Documentation:** Tests serve as examples of how features should work
- **Confidence:** You can deploy knowing the application works

### Real-World Example:
Imagine a banking app that doesn't test for negative numbers. A user accidentally enters "-$1000" and the app subtracts money instead of adding it! Testing would catch this.

---

## Types of Testing

### 1. **Manual Testing** (What We're Doing)
**Definition:** A human manually uses the application and checks if it works.

**Pros:**
- No coding required
- Can catch UX issues
- Flexible and exploratory

**Cons:**
- Time-consuming
- Can miss edge cases
- Not repeatable automatically

**When to Use:** Always do manual testing first to understand how the app feels to use.

---

### 2. **Automated Testing** (Future Enhancement)
**Definition:** Code that tests other code automatically.

**Types:**
- **Unit Tests:** Test individual functions (e.g., test `calculate_total()` function)
- **Integration Tests:** Test multiple components together (e.g., database + routes)
- **End-to-End Tests:** Simulate real user interactions (e.g., fill form, click submit, check database)

**Example Unit Test (Python):**
```python
def test_add_expense():
    result = add_expense('2025-01-01', 'Food', 50.0, 'Lunch')
    assert result > 0  # Should return an ID
    assert isinstance(result, int)  # ID should be an integer
```

**When to Use:** After manual testing confirms features work, write automated tests to prevent regression.

---

### 3. **Functional Testing** (What We're Focusing On)
**Definition:** Testing that each feature works according to requirements.

**Our Features to Test:**
- ✅ Add expense
- ✅ Edit expense
- ✅ Delete expense
- ✅ View all expenses
- ✅ Filter by category
- ✅ Filter by date range
- ✅ Export to CSV
- ✅ View analytics charts
- ✅ Manage budgets
- ✅ View dashboard statistics

---

### 4. **Edge Case Testing**
**Definition:** Testing extreme, unusual, or boundary conditions.

**Examples:**
- What if amount is $0?
- What if amount is $999,999,999?
- What if amount is negative?
- What if description is 1000 characters?
- What if date is in the year 1900?
- What if date is in the future?
- What if user submits empty form?
- What if user enters text in number field?

**Why Important:** Most bugs hide at the edges, not in normal use cases.

---

### 5. **Usability Testing**
**Definition:** Testing if the application is easy and pleasant to use.

**Questions to Ask:**
- Is it clear what each button does?
- Are error messages helpful?
- Is the layout intuitive?
- Does it work on mobile screens?
- Can keyboard-only users navigate?
- Are colors readable?

---

### 6. **Cross-Browser Testing**
**Definition:** Testing that the application works on different browsers.

**Browsers to Test:**
- ✅ Chrome/Edge (Chromium-based)
- ✅ Firefox
- ✅ Safari (if on Mac)

**Why Important:** Different browsers render CSS and JavaScript slightly differently.

---

## Testing Tools & Environment

### Browser Developer Tools (DevTools)

**How to Open:**
- **Windows/Linux:** Press `F12` or `Ctrl + Shift + I`
- **Mac:** Press `Cmd + Option + I`

**Key Tabs:**

#### 1. **Console Tab**
**What It Shows:** JavaScript errors, warnings, and console.log() messages

**What to Look For:**
- ❌ **Red errors:** JavaScript broke, feature might not work
- ⚠️ **Yellow warnings:** Non-critical issues
- 🔵 **Blue info:** Informational messages

**Example Error:**
```
Uncaught TypeError: Cannot read property 'value' of null
    at main.js:45
```
This means JavaScript tried to access an element that doesn't exist.

---

#### 2. **Network Tab**
**What It Shows:** All HTTP requests (page loads, form submissions, API calls)

**What to Look For:**
- ✅ **Status 200:** Request succeeded
- ❌ **Status 404:** File not found
- ❌ **Status 500:** Server error
- ⏱️ **Time:** How long requests take (slow = bad UX)

**How to Use:**
1. Open Network tab
2. Submit a form
3. See POST request to `/add`
4. Check status code (should be 200 or 302 redirect)
5. Check response (should not show error message)

---

#### 3. **Elements Tab**
**What It Shows:** HTML structure and CSS styles

**What to Look For:**
- Check if elements have correct classes
- Inspect CSS to see why styling looks wrong
- Verify form fields have correct `name` attributes

**How to Use:**
1. Right-click element
2. Choose "Inspect"
3. See HTML and CSS applied to that element

---

### Application Console (Terminal)

**What It Shows:** Flask server logs, Python errors, print statements

**What to Look For:**
```
127.0.0.1 - - [01/Oct/2025 12:34:56] "POST /add HTTP/1.1" 302 -
```
- IP address
- Timestamp
- HTTP method (POST)
- URL path (/add)
- Status code (302 = redirect, success!)

**Error Example:**
```
Traceback (most recent call last):
  File "app.py", line 123, in add_expense
    amount = float(request.form['amount'])
ValueError: could not convert string to float: 'abc'
```
This means someone entered text instead of a number.

---

### SQLite Database Viewer

**Option 1: DB Browser for SQLite (Recommended)**
- Free application: https://sqlitebrowser.org/
- Visual interface to see data
- Can run SQL queries manually

**Option 2: Python Script**
```python
import sqlite3
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM expenses")
rows = cursor.fetchall()
for row in rows:
    print(row)
```

**Why Important:** Verify data is actually saved correctly in database.

---

## Complete Testing Checklist

### Pre-Testing Setup
- [ ] Start the Flask application (`python app.py`)
- [ ] Open browser to `http://localhost:5000`
- [ ] Open Browser DevTools (F12)
- [ ] Open Console tab to watch for errors
- [ ] Have a notepad ready to document bugs

---

### Feature 1: Dashboard (index.html)

#### Test Case 1.1: View Dashboard Statistics
**Steps:**
1. Navigate to `http://localhost:5000`
2. Observe the stat cards at the top

**Expected Results:**
- ✅ "Total Expenses" shows sum of all expense amounts
- ✅ "This Month" shows sum of expenses from current month
- ✅ "Categories" shows count of unique categories with expenses
- ✅ "Avg/Day" shows reasonable average (total ÷ days)
- ✅ No JavaScript errors in console

**Edge Cases:**
- [ ] Test with zero expenses (should show $0.00, not error)
- [ ] Test with exactly 1 expense
- [ ] Test with 1000+ expenses (performance)

**Validation:**
- Check that calculations match manual calculation
- Verify currency formatting (always 2 decimals)

---

#### Test Case 1.2: Recent Expenses List
**Steps:**
1. Look at "Recent Expenses" section
2. Count number of expenses shown

**Expected Results:**
- ✅ Shows maximum 5 most recent expenses
- ✅ Sorted by date (newest first)
- ✅ Each expense shows date, category, amount, description
- ✅ "View All" button links to `/expenses`

**Edge Cases:**
- [ ] Test with 0 expenses (should show "No expenses yet" message)
- [ ] Test with exactly 5 expenses
- [ ] Test with 10 expenses (should still show only 5)

---

#### Test Case 1.3: Quick Actions Buttons
**Steps:**
1. Click "Add Expense" button
2. Verify redirects to `/add`
3. Go back
4. Click "View All Expenses" button
5. Verify redirects to `/expenses`

**Expected Results:**
- ✅ Buttons are clearly visible
- ✅ Hover effect works (color changes)
- ✅ Correct URLs
- ✅ Icons display properly

---

### Feature 2: Add Expense (add_expense.html)

#### Test Case 2.1: Valid Expense Submission
**Steps:**
1. Navigate to `/add`
2. Fill in form:
   - **Date:** 2025-10-01
   - **Category:** Food
   - **Amount:** 45.50
   - **Description:** Lunch at cafe
3. Click "Add Expense"

**Expected Results:**
- ✅ Success message appears: "Expense added successfully!"
- ✅ Redirects to dashboard
- ✅ New expense appears in Recent Expenses
- ✅ Total Expenses increases by $45.50
- ✅ Database contains new record

**Verification:**
- Check database: `SELECT * FROM expenses ORDER BY id DESC LIMIT 1`
- Verify all fields saved correctly
- Check `created_at` timestamp is accurate

---

#### Test Case 2.2: Empty Form Submission
**Steps:**
1. Navigate to `/add`
2. Leave all fields empty
3. Try to submit

**Expected Results:**
- ✅ HTML5 validation prevents submission
- ✅ Browser shows "Please fill out this field" message
- ✅ Red borders appear on empty required fields
- ✅ No data saved to database

**Why This Matters:** Client-side validation prevents unnecessary server requests.

---

#### Test Case 2.3: Invalid Amount Values
**Test Data:**

| Input | Expected Behavior |
|-------|------------------|
| `-50.00` | Rejected: "Amount must be at least 0.01" |
| `0` | Rejected: "Amount must be at least 0.01" |
| `0.001` | Rejected: Browser rounds to 0.01 (step="0.01") |
| `abc` | Rejected: HTML5 prevents entering letters |
| `$45.50` | Rejected: Dollar sign not allowed in number field |
| `999999999` | Accepted (but might need max limit) |
| `` (empty) | Rejected: Required field |

**Steps for Each:**
1. Enter test value in Amount field
2. Try to submit form
3. Verify error message or rejection

**Edge Case Discovery:**
- ❓ Should we have a maximum amount? (e.g., $1,000,000)
- ❓ What about very precise amounts like $45.999? (gets rounded)

---

#### Test Case 2.4: Invalid Date Values
**Test Data:**

| Input | Expected Behavior |
|-------|------------------|
| `2025-10-01` | ✅ Accepted (current date) |
| `2020-01-01` | ✅ Accepted (past date) |
| `2030-01-01` | ❓ Should future dates be allowed? |
| `1900-01-01` | ✅ Accepted but unusual |
| `` (empty) | ❌ Rejected: Required field |

**Edge Case to Consider:**
Should we prevent future dates? Many expense trackers do:
```javascript
// Could add to main.js
const dateInput = document.querySelector('input[type="date"]');
dateInput.max = new Date().toISOString().split('T')[0];  // Today's date
```

---

#### Test Case 2.5: Description Field Edge Cases
**Test Data:**

| Input | Expected Behavior |
|-------|------------------|
| `` (empty) | ✅ Accepted (optional field) |
| `A` | ✅ Accepted (1 character) |
| `Lorem ipsum dolor sit amet, consectetur adipiscing elit...` (500 chars) | ❓ Should have max length? |
| `<script>alert('XSS')</script>` | ✅ Jinja2 auto-escapes, safe |
| `Café naïve résumé` | ✅ UTF-8 characters work |
| `😀🎉💰` | ✅ Emojis should work |

**Security Test:**
1. Enter: `<b>Bold description</b>`
2. Submit and view in expense list
3. **Expected:** See literal text `<b>Bold description</b>` (not bold)
4. **Why:** Jinja2 auto-escapes HTML to prevent XSS attacks

**Definition: XSS (Cross-Site Scripting)**
A security vulnerability where attackers inject malicious JavaScript into web pages. Auto-escaping prevents this.

---

#### Test Case 2.6: Category Dropdown
**Steps:**
1. Click category dropdown
2. Verify all categories appear

**Expected Results:**
- ✅ All 8 categories present: Food, Transport, Entertainment, Bills, Shopping, Health, Education, Other
- ✅ Each has correct emoji icon
- ✅ Dropdown is keyboard-accessible (Tab to it, Arrow keys to select)
- ✅ Default selection is first category or placeholder

---

### Feature 3: View All Expenses (view_expenses.html)

#### Test Case 3.1: View All Expenses (No Filters)
**Steps:**
1. Navigate to `/expenses`
2. Observe expense table

**Expected Results:**
- ✅ All expenses displayed in table
- ✅ Sorted by date (newest first)
- ✅ Columns: Date, Category, Amount, Description, Actions
- ✅ Category shows colored badge with emoji
- ✅ Amount formatted with $ and 2 decimals
- ✅ Total sum displayed at bottom
- ✅ Edit and Delete buttons for each expense

**Performance Test:**
- [ ] Add 100 expenses, verify page loads in < 2 seconds
- [ ] Add 1000 expenses, check if pagination needed

---

#### Test Case 3.2: Filter by Category
**Steps:**
1. Select "Food" from category dropdown
2. Click "Apply Filters"

**Expected Results:**
- ✅ Only Food expenses shown
- ✅ Total updates to show Food total only
- ✅ URL updates: `/expenses?category=Food`
- ✅ Category dropdown still shows "Food" selected
- ✅ Other filter fields preserve their values

**Edge Cases:**
- [ ] Filter category with 0 expenses (should show "No expenses found")
- [ ] Select "All Categories" - should show everything

---

#### Test Case 3.3: Filter by Date Range
**Steps:**
1. Enter Start Date: `2025-09-01`
2. Enter End Date: `2025-09-30`
3. Click "Apply Filters"

**Expected Results:**
- ✅ Only September expenses shown
- ✅ Total updates correctly
- ✅ URL updates: `/expenses?start_date=2025-09-01&end_date=2025-09-30`
- ✅ Date fields preserve values

**Edge Cases:**
- [ ] Start date > End date (should show error or no results)
- [ ] Same start and end date (show expenses from that day)
- [ ] Date range with no expenses
- [ ] Only start date filled (show from start to now)
- [ ] Only end date filled (show from beginning to end)

---

#### Test Case 3.4: Quick Filter Buttons
**Steps:**
1. Click "This Month" button
2. Verify URL parameters
3. Check results

**Expected Results:**
- ✅ Filters to current month (Oct 1 - Oct 31, 2025)
- ✅ Date fields auto-fill
- ✅ Results update immediately

**Test All Quick Filters:**
- [ ] "This Month" - current month
- [ ] "Last 7 Days" - past week
- [ ] "Last 30 Days" - past month
- [ ] "This Year" - Jan 1 to Dec 31 current year
- [ ] "Clear Filters" - removes all filters

---

#### Test Case 3.5: Export to CSV
**Steps:**
1. Apply some filters (e.g., Food category)
2. Click "Export to CSV"

**Expected Results:**
- ✅ File downloads: `expenses_YYYY-MM-DD.csv`
- ✅ Opens in Excel/Google Sheets
- ✅ Contains only filtered expenses (not all expenses)
- ✅ Headers: Date, Category, Amount, Description
- ✅ Data matches what's displayed

**Edge Cases:**
- [ ] Export with 0 expenses (should create CSV with headers only)
- [ ] Export with special characters in description (properly escaped)
- [ ] Export with commas in description (wrapped in quotes)

**Example CSV Content:**
```csv
Date,Category,Amount,Description
2025-10-01,Food,45.50,"Lunch at cafe"
2025-09-30,Food,12.00,"Coffee, pastry"
```

---

### Feature 4: Edit Expense

#### Test Case 4.1: Edit Existing Expense
**Steps:**
1. Go to `/expenses`
2. Click "Edit" button on an expense
3. Verify form pre-fills with existing data
4. Change amount from $45.50 to $50.00
5. Click "Update Expense"

**Expected Results:**
- ✅ URL is `/edit/<id>` (e.g., `/edit/5`)
- ✅ Form shows existing values
- ✅ Page title says "Edit Expense"
- ✅ Button says "Update Expense"
- ✅ Success message: "Expense updated successfully!"
- ✅ Redirects to `/expenses`
- ✅ Updated expense shows new amount
- ✅ Database updated correctly

**Verification:**
```python
# Check database
SELECT * FROM expenses WHERE id = 5;
# amount should be 50.00, not 45.50
```

---

#### Test Case 4.2: Edit Non-Existent Expense
**Steps:**
1. Manually navigate to `/edit/99999` (ID that doesn't exist)

**Expected Results:**
- ✅ Shows error: "Expense not found"
- ✅ Redirects to `/expenses`
- ✅ No 500 error or crash

**Why This Matters:** Users might bookmark old URLs or manually type IDs.

---

### Feature 5: Delete Expense

#### Test Case 5.1: Delete with Confirmation
**Steps:**
1. Go to `/expenses`
2. Click "Delete" button on an expense
3. Verify JavaScript confirmation dialog appears
4. Click "OK" to confirm

**Expected Results:**
- ✅ Confirmation dialog says "Are you sure you want to delete this expense?"
- ✅ Expense removed from database
- ✅ Page updates (expense no longer visible)
- ✅ Total amount decreases
- ✅ Success message: "Expense deleted successfully!"

**JavaScript Check:**
```javascript
// In main.js, this code handles deletion
document.querySelectorAll('.delete-expense').forEach(button => {
    button.addEventListener('click', function(e) {
        if (!confirm('Are you sure?')) {
            e.preventDefault();  // Cancel if user clicks "Cancel"
        }
    });
});
```

---

#### Test Case 5.2: Delete Cancellation
**Steps:**
1. Click "Delete" button
2. Click "Cancel" in confirmation dialog

**Expected Results:**
- ✅ Expense is NOT deleted
- ✅ Stays on same page
- ✅ No changes to database

---

#### Test Case 5.3: Delete Non-Existent Expense
**Steps:**
1. Manually navigate to `/delete/99999`

**Expected Results:**
- ✅ Shows error: "Expense not found"
- ✅ Redirects gracefully
- ✅ No 500 error

---

### Feature 6: Analytics (analytics.html)

#### Test Case 6.1: Category Pie Chart
**Steps:**
1. Navigate to `/analytics`
2. Locate the pie chart

**Expected Results:**
- ✅ Chart renders without errors
- ✅ Each category shown as slice
- ✅ Colors match category colors
- ✅ Hover shows category name, amount, percentage
- ✅ Legend displays on right side
- ✅ No console errors

**Edge Cases:**
- [ ] With 0 expenses: Should show message "No data available"
- [ ] With 1 category: Pie chart is 100% one color
- [ ] With all 8 categories: All slices visible

**Visual Check:**
- Percentages add up to 100%
- Colors are distinct and readable
- Text is not cut off

---

#### Test Case 6.2: Spending Trend Line Chart
**Steps:**
1. Scroll to line chart
2. Observe trend over time

**Expected Results:**
- ✅ X-axis shows dates
- ✅ Y-axis shows dollar amounts
- ✅ Line connects daily totals
- ✅ Hover shows date and exact amount
- ✅ Responsive (resizes with window)

**Edge Cases:**
- [ ] With 1 day of data: Shows single point
- [ ] With 365 days: X-axis labels don't overlap
- [ ] With $0 days: Shows $0, not blank

---

#### Test Case 6.3: Monthly Bar Chart
**Steps:**
1. Scroll to bar chart
2. Check monthly comparisons

**Expected Results:**
- ✅ Bars for each month with expenses
- ✅ Height represents total spending
- ✅ Current month highlighted differently
- ✅ Hover shows month and amount

**Edge Cases:**
- [ ] First month using app: Only 1 bar
- [ ] Year with all 12 months: All bars visible

---

### Feature 7: Budget Management (budgets.html)

#### Test Case 7.1: Create New Budget
**Steps:**
1. Navigate to `/budgets`
2. Select category: "Food"
3. Enter limit: `500.00`
4. Click "Set Budget"

**Expected Results:**
- ✅ Success message: "Budget set successfully!"
- ✅ Budget appears in list below
- ✅ Progress bar shows current spending vs limit
- ✅ Database updated

**Verification:**
```python
SELECT * FROM budgets WHERE category = 'Food';
# limit should be 500.00
```

---

#### Test Case 7.2: Update Existing Budget
**Steps:**
1. Set Food budget to $500
2. Set Food budget again to $600

**Expected Results:**
- ✅ Previous budget is updated (not duplicated)
- ✅ Progress bar adjusts to new limit
- ✅ Message: "Budget updated successfully!"

**Database Check:**
```sql
SELECT COUNT(*) FROM budgets WHERE category = 'Food';
-- Should be 1, not 2
```

---

#### Test Case 7.3: Budget Progress Indicators
**Test Data:**
- Set Food budget: $100
- Add expenses:
  - $50 Food expense (50% used - Green)
  - $30 Food expense (80% used - Yellow)
  - $25 Food expense (105% used - Red)

**Expected Results:**

| Spent | Percentage | Color | Status Text |
|-------|-----------|-------|-------------|
| $50 | 50% | Green | On track |
| $80 | 80% | Yellow | Warning |
| $105 | 105% | Red | Over budget |

**Visual Check:**
- ✅ Progress bar color changes correctly
- ✅ Percentage displays accurately
- ✅ Bar doesn't exceed container width (capped at 100% visually)
- ✅ Over-budget amount shown: "Over by $5.00"

---

#### Test Case 7.4: Budget Pacing
**Explanation:** Budget pacing tells you if you're spending too fast.

**Formula:**
```
Expected spending = (Budget ÷ Days in month) × Days elapsed
Actual spending = Sum of expenses so far

If Actual > Expected: "Ahead of pace" (spending too fast)
If Actual < Expected: "Under pace" (doing well)
```

**Test:**
1. Set October Food budget: $310 (Oct has 31 days = $10/day)
2. Add $150 in Food expenses by Oct 15
3. Expected spending by Oct 15: $10 × 15 = $150
4. Check pacing message

**Expected Results:**
- ✅ Calculation shown: "$150 / $150 expected"
- ✅ Status: "On pace" (or within reasonable range)

---

### Feature 8: Form Validation & UX

#### Test Case 8.1: Real-Time Validation
**Steps:**
1. Go to `/add`
2. Focus on Amount field
3. Type `abc`
4. Tab to next field (blur event)

**Expected Results:**
- ✅ HTML5 prevents entering letters in number field
- ✅ Or: Error message appears: "Please enter a valid number"
- ✅ Red border around field
- ✅ Submit button stays disabled until fixed

---

#### Test Case 8.2: Loading States
**Steps:**
1. Fill out expense form
2. Click "Add Expense"
3. Observe button

**Expected Results:**
- ✅ Button text becomes loading spinner
- ✅ Button disabled (can't double-click)
- ✅ Cursor changes to "not-allowed"
- ✅ Loading class applied: `btn loading`

**CSS Implementation:**
```css
.btn.loading {
    color: transparent;  /* Hide text */
    pointer-events: none;
}
.btn.loading::after {
    content: '';
    /* Spinning circle appears */
}
```

---

#### Test Case 8.3: Error Messages Display
**Steps:**
1. Trigger a validation error
2. Check error message styling

**Expected Results:**
- ✅ Red background (#fee)
- ✅ Red text (#c00)
- ✅ Border and padding
- ✅ Icon or emoji (❌)
- ✅ Clear, actionable text
- ✅ Positioned near relevant field

**Good vs Bad Error Messages:**

| ❌ Bad | ✅ Good |
|-------|--------|
| "Error" | "Amount must be greater than $0" |
| "Invalid input" | "Please select a category" |
| "Failed" | "Date cannot be in the future" |

---

### Feature 9: Accessibility

#### Test Case 9.1: Keyboard Navigation
**Steps:**
1. Don't use mouse
2. Press Tab repeatedly
3. Try to complete entire flow: Dashboard → Add Expense → Submit

**Expected Results:**
- ✅ Tab moves through all interactive elements in logical order
- ✅ Links and buttons show focus outline (blue glow)
- ✅ Enter key activates buttons
- ✅ Arrow keys work in dropdowns
- ✅ No "keyboard traps" (can always Tab away)

**Accessibility Principle:**
Some users can't use a mouse (motor disabilities, blind users with screen readers). Keyboard access is essential.

---

#### Test Case 9.2: Screen Reader Testing
**Tools:**
- **Windows:** NVDA (free) or Narrator (built-in)
- **Mac:** VoiceOver (built-in, Cmd+F5)

**Steps:**
1. Turn on screen reader
2. Navigate to `/add`
3. Listen to form labels

**Expected Results:**
- ✅ Labels read aloud: "Date, required, edit text"
- ✅ Button purpose clear: "Add Expense, button"
- ✅ Error messages announced
- ✅ Success messages announced

**Check HTML:**
```html
<!-- Good: label associated with input -->
<label for="amount">Amount</label>
<input type="number" id="amount" name="amount" required>

<!-- Bad: no association -->
<div>Amount</div>
<input type="number" name="amount">
```

---

#### Test Case 9.3: Color Contrast
**Tool:** Browser extension "WCAG Color Contrast Checker"

**Steps:**
1. Check text on buttons (white on blue)
2. Run contrast checker

**Expected Results:**
- ✅ Ratio at least 4.5:1 for normal text
- ✅ Ratio at least 3:1 for large text (18pt+)
- ✅ Ratio at least 3:1 for interactive elements

**Why It Matters:** Low vision users need high contrast to read text.

**Our Colors:**
```css
/* Primary button */
background: #007bff;  /* Blue */
color: white;
/* Ratio: 8.59:1 ✅ Passes */

/* Success button */
background: #28a745;  /* Green */
color: white;
/* Ratio: 4.53:1 ✅ Passes */
```

---

#### Test Case 9.4: Reduced Motion
**Steps:**
1. Enable reduced motion:
   - **Windows:** Settings → Ease of Access → Display → Show animations
   - **Mac:** System Preferences → Accessibility → Display → Reduce motion
2. Reload page
3. Observe animations

**Expected Results:**
- ✅ No animations play (or instant)
- ✅ Transitions skip
- ✅ Loading spinners still visible (critical feedback)

**CSS Implementation:**
```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

**Why It Matters:** Vestibular disorders cause motion sickness from animations.

---

### Feature 10: Responsive Design

#### Test Case 10.1: Mobile View (375px width)
**Steps:**
1. Open DevTools (F12)
2. Click device toggle (Ctrl+Shift+M)
3. Select "iPhone SE" (375×667)
4. Navigate through all pages

**Expected Results:**
- ✅ No horizontal scrolling
- ✅ Text readable (minimum 16px)
- ✅ Buttons large enough to tap (minimum 44×44px)
- ✅ Navigation menu stacks vertically or hamburger
- ✅ Tables scroll or reformat for mobile
- ✅ Forms use full width

**Common Issues:**
- Text too small (zoom to read)
- Buttons too close together (hard to tap)
- Tables overflow screen
- Fixed-width containers break layout

---

#### Test Case 10.2: Tablet View (768px width)
**Device:** iPad (768×1024)

**Expected Results:**
- ✅ 2-column layouts where appropriate
- ✅ Charts resize correctly
- ✅ Navigation fits on one line

---

#### Test Case 10.3: Desktop View (1920px width)
**Expected Results:**
- ✅ Content doesn't stretch too wide (max-width: 1200px)
- ✅ Cards use grid layout (3-4 columns)
- ✅ White space balanced

---

#### Test Case 10.4: Zoom Testing
**Steps:**
1. Press Ctrl and + to zoom in
2. Zoom to 200%
3. Check readability

**Expected Results:**
- ✅ Text doesn't overflow containers
- ✅ Layout doesn't break
- ✅ Still usable at 200% zoom

**WCAG Requirement:** Must work up to 200% zoom.

---

### Feature 11: Performance

#### Test Case 11.1: Page Load Time
**Steps:**
1. Open DevTools → Network tab
2. Check "Disable cache"
3. Refresh page
4. Look at "Load" time at bottom

**Expected Results:**
- ✅ Dashboard loads in < 1 second
- ✅ Total page size < 1 MB
- ✅ No files over 500 KB

**Tools:**
- Chrome DevTools → Network → Load time
- Lighthouse report (F12 → Lighthouse tab)

---

#### Test Case 11.2: Large Dataset Performance
**Steps:**
1. Add 1000 test expenses:
```python
import random
from database import add_expense

categories = ['Food', 'Transport', 'Entertainment', 'Bills']
for i in range(1000):
    add_expense(
        date='2025-09-15',
        category=random.choice(categories),
        amount=round(random.uniform(5, 200), 2),
        description=f'Test expense {i}'
    )
```
2. Navigate to `/expenses`
3. Check load time

**Expected Results:**
- ✅ Loads in < 3 seconds
- ✅ Or: Pagination implemented if slow

**Optimization Ideas:**
- Add pagination (show 50 per page)
- Add database indexes
- Lazy-load images

---

### Feature 12: Security

#### Test Case 12.1: SQL Injection Prevention
**Attack Attempt:**
1. In description field, enter:
```
'; DROP TABLE expenses; --
```
2. Submit form

**Expected Results:**
- ✅ Form submits normally
- ✅ Description saved as literal text
- ✅ Database NOT affected
- ✅ No tables dropped

**Why It Works:**
```python
# BAD (vulnerable):
cursor.execute(f"INSERT INTO expenses (description) VALUES ('{description}')")
# Becomes: INSERT INTO expenses (description) VALUES (''; DROP TABLE expenses; --')
# Executes TWO statements!

# GOOD (safe):
cursor.execute("INSERT INTO expenses (description) VALUES (?)", (description,))
# Database treats entire input as single string value
```

---

#### Test Case 12.2: XSS Prevention
**Attack Attempt:**
1. Enter description: `<script>alert('Hacked!');</script>`
2. Submit and view expense

**Expected Results:**
- ✅ Alert does NOT pop up
- ✅ Literal text displayed: `<script>alert('Hacked!');</script>`
- ✅ HTML escaped: `&lt;script&gt;alert('Hacked!');&lt;/script&gt;`

**Why It Works:**
```html
<!-- Jinja2 auto-escapes by default -->
{{ expense.description }}
<!-- Becomes: -->
&lt;script&gt;alert('Hacked!');&lt;/script&gt;
<!-- Browser shows as text, doesn't execute -->
```

---

## Edge Cases Explained

### What Are Edge Cases?

**Definition:** Edge cases are unusual, extreme, or boundary conditions that might not be tested in normal use but can cause bugs.

**Example:**
- **Normal Case:** User enters $50 for lunch
- **Edge Case:** User enters $0.01 (minimum)
- **Edge Case:** User enters $999,999,999 (maximum)
- **Edge Case:** User enters negative number
- **Edge Case:** User leaves field empty

### Why Edge Cases Matter

**Real-World Example:**
In 1999, NASA's Mars Climate Orbiter crashed because one team used metric units and another used imperial. An edge case (unit mismatch) cost $327 million!

**In Our App:**
- If we don't test empty database, app might crash on first launch
- If we don't test long descriptions, text might overflow containers
- If we don't test future dates, users might accidentally track future expenses

### Common Edge Cases to Test

#### 1. **Empty States**
- Database with 0 expenses
- Form with all fields empty
- Filter that returns 0 results
- Category with no expenses

#### 2. **Boundary Values**
- Minimum: $0.01
- Maximum: $999,999,999
- Exactly 0
- Exactly 1
- Very large numbers

#### 3. **Data Type Mismatches**
- Text in number field
- Numbers in text field
- Special characters: `!@#$%^&*()`
- Unicode: `emoji, 中文, العربية`

#### 4. **Time-Based Edge Cases**
- First day of month
- Last day of month
- Leap year (Feb 29)
- Daylight saving time transitions
- Year 2038 problem (32-bit timestamp overflow)

#### 5. **Length Extremes**
- 1-character input
- 1000-character input
- Empty string
- Just whitespace: `"   "`

---

## How to Report Bugs

### Bug Report Template

Use this format in BUG_TRACKER.md:

```markdown
## Bug #XXX - [Short, Descriptive Title]

**Status:** 🔴 Open / 🟡 In Progress / 🟢 Fixed

**Severity:** Critical / High / Medium / Low

**Date Reported:** YYYY-MM-DD

**Reporter:** Your Name

### Description
Clear, concise description of what's wrong.

### Steps to Reproduce
1. Navigate to [page]
2. Click [button]
3. Enter [data]
4. Observe [result]

### Expected Behavior
What should happen.

### Actual Behavior
What actually happens.

### Screenshots
[Attach if applicable]

### Environment
- Browser: Chrome 118
- OS: Windows 11
- Screen size: 1920x1080

### Error Messages
```
[Paste exact error from console]
```

### Root Cause
[After investigation] The problem is caused by...

### Solution
[After fix] Fixed by changing...

### Code Changes
```python
# Before
old_code()

# After
new_code()
```

### Testing
- [ ] Verified fix works
- [ ] Tested edge cases
- [ ] No regression (other features still work)

### Prevention
How to avoid this type of bug in the future.
```

---

### Bug Severity Levels

**Critical:** App completely broken, data loss possible
- Example: Can't add expenses, database corrupted

**High:** Major feature broken, workaround exists
- Example: Charts don't load, but data visible in table

**Medium:** Minor feature broken, doesn't affect core functionality
- Example: Export CSV button doesn't work

**Low:** Cosmetic issue, typo, minor UX annoyance
- Example: Button color slightly off, typo in label

---

### Example Bug Report

```markdown
## Bug #002 - Negative Amounts Accepted in Expense Form

**Status:** 🟢 Fixed

**Severity:** High

**Date Reported:** 2025-10-01

### Description
Users can enter negative amounts (e.g., -$50) in the expense form, which creates nonsensical data.

### Steps to Reproduce
1. Navigate to `/add`
2. Enter amount: `-50.00`
3. Fill other fields
4. Click "Add Expense"
5. Form submits successfully

### Expected Behavior
Form should reject negative amounts and show error: "Amount must be positive"

### Actual Behavior
Negative amount accepted and saved to database

### Root Cause
HTML number input has no `min` attribute:
```html
<input type="number" name="amount" step="0.01">
```

### Solution
Added `min="0.01"` attribute:
```html
<input type="number" name="amount" step="0.01" min="0.01" required>
```

Also added server-side validation in app.py:
```python
amount = float(request.form['amount'])
if amount <= 0:
    flash('Amount must be positive', 'error')
    return redirect(url_for('add_expense'))
```

### Testing
- [x] Verified HTML5 validation prevents negative input
- [x] Tested with 0, -0.01, -100
- [x] Server-side validation catches direct POST requests
- [x] Existing positive amounts still work

### Prevention
Always validate on both client (UX) and server (security) sides.
```

---

## Best Practices

### 1. **Always Test on Real Data**
- Don't just test with perfect inputs
- Use realistic data: typos, varied lengths, special characters
- Test with your own expenses for 1-2 weeks

### 2. **Test Early and Often**
- Don't wait until the end to test
- Test each feature as you build it
- Fix bugs immediately (cheaper than later)

### 3. **Automate Repetitive Tests**
- If you test the same thing 5+ times, write a script
- Example: Script to add 100 random expenses for testing

### 4. **Test in Multiple Environments**
- Different browsers (Chrome, Firefox, Safari)
- Different OS (Windows, Mac, Linux)
- Different screen sizes
- With and without internet (if applicable)

### 5. **Use Version Control**
- Commit working code before making changes
- If tests fail after changes, you can revert

### 6. **Document Everything**
- Write down steps to reproduce bugs
- Keep test cases up to date
- Update documentation when features change

### 7. **Think Like a User**
- Users don't read instructions
- Users make typos
- Users click things twice
- Users use the app in unexpected ways

### 8. **Test Error Handling**
- What if database is locked?
- What if database file deleted?
- What if server runs out of disk space?
- What if internet connection drops mid-request?

---

## Testing Schedule

### During Development (Continuous)
- Test each feature as you build it
- Quick smoke test after every significant change

### Before Demo/Release (Comprehensive)
- Full checklist (all test cases above)
- Cross-browser testing
- Accessibility check
- Performance check

### After Bug Fixes (Regression)
- Re-test the fixed bug
- Test related features (make sure fix didn't break anything)
- Run full test suite if major change

---

## Tools Summary

| Tool | Purpose | How to Access |
|------|---------|---------------|
| Browser DevTools | Debug HTML/CSS/JS, network, performance | F12 or Ctrl+Shift+I |
| Console Tab | See JavaScript errors | DevTools → Console |
| Network Tab | See HTTP requests | DevTools → Network |
| Device Simulator | Test mobile views | DevTools → Ctrl+Shift+M |
| Lighthouse | Performance & accessibility audit | DevTools → Lighthouse |
| NVDA/VoiceOver | Screen reader testing | Free download / Built-in |
| DB Browser for SQLite | View database | https://sqlitebrowser.org/ |

---

## Next Steps

After completing this testing phase:

1. **Fix All Critical Bugs**
   - Anything that breaks core functionality
   - Data loss or corruption issues

2. **Fix High-Priority Bugs**
   - Major features broken
   - Security issues

3. **Consider Medium/Low Bugs**
   - Fix if time allows
   - Or document as "known issues"

4. **Update BUG_TRACKER.md**
   - Document all findings
   - Mark fixed bugs as resolved
   - Leave open bugs for future work

5. **Create Final Documentation**
   - Update README.md
   - Add setup instructions
   - List known limitations

6. **Prepare for Deployment**
   - Set secret key in production
   - Use production database
   - Configure environment variables

---

## Conclusion

Testing is not about finding zero bugs (impossible). Testing is about:
- **Understanding** your application's behavior
- **Finding** the most critical bugs before users do
- **Building confidence** that core features work
- **Learning** how users will actually use your app

> "Testing shows the presence, not the absence of bugs." - Edsger Dijkstra

Good luck with testing! Remember: every bug you find is a bug your users won't encounter. 🐛 → ✅

---

**End of Testing Documentation**

For questions, issues, or suggestions, update BUG_TRACKER.md with a new entry.
