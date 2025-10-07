"""
APP.PY - Main Flask Application
================================

PURPOSE:
This is the heart of our web application. It handles HTTP requests from users'
browsers and returns HTML pages as responses.

WHAT IS FLASK?
Flask is a Python web framework that makes it easy to build web applications.
It handles the complex parts of web development (routing, requests, responses)
so we can focus on our application logic.

WHAT IS A WEB FRAMEWORK?
Think of it as a toolkit that handles common web development tasks:
- Routing: Which function handles which URL?
- Request handling: What data did the user send?
- Response generation: What HTML/data to send back?
- Template rendering: How to create HTML with dynamic data?

HOW DOES A WEB APP WORK?
1. User types URL in browser (e.g., localhost:5000/add)
2. Browser sends HTTP request to our Flask app
3. Flask routes request to correct function based on URL
4. Function processes request (maybe reads database, validates data)
5. Function returns response (usually HTML page)
6. Browser displays the HTML to user

JUNIOR DEVELOPER NOTES:
- Routes are like addresses: @app.route('/home') handles requests to /home
- Methods determine request type: GET (retrieve data) vs POST (submit data)
- Templates are HTML files with placeholders for dynamic data
- Flash messages are temporary messages shown to users (success/error alerts)
"""

# ============================================================================
# IMPORTS - Loading Required Libraries
# ============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import os

# Import our custom modules
import database
from models import (
    Expense, Budget, Income, ExpenseCategory, IncomeSource, ExpenseAnalyzer,
    validate_expense_data, validate_income_data, format_currency, get_date_range_description
)

"""
IMPORT EXPLANATIONS:

FROM FLASK:
- Flask: The main application class
- render_template: Converts HTML templates to final HTML with data
- request: Contains data from user's browser (form data, URL parameters)
- redirect: Sends user to a different page
- url_for: Generates URLs for routes (better than hardcoding URLs)
- flash: Creates temporary messages to show users
- jsonify: Converts Python dictionaries to JSON (for AJAX requests)

FROM DATETIME:
- datetime: Work with dates and times
- timedelta: Represent time durations (e.g., 7 days ago)

FROM OS:
- os: Operating system functions (we'll use for environment variables)

FROM OUR MODULES:
- database: Our database operations (add_expense, get_all_expenses, etc.)
- models: Our data models and business logic
"""

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

app = Flask(__name__)

"""
FLASK(__name__):
__name__ is a special Python variable that equals the module name.
When running app.py directly, __name__ == '__main__'
Flask uses this to know where to look for templates and static files.
"""

# Secret key for session management and flash messages
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

"""
SECRET KEY EXPLANATION:
Flask needs a secret key to encrypt session data and flash messages.
This prevents users from tampering with cookies.

os.environ.get('SECRET_KEY', default):
- First tries to get SECRET_KEY from environment variables (for production)
- If not found, uses 'dev-secret-key-change-in-production' (for development)

SECURITY NOTE:
In production, ALWAYS set a real secret key as an environment variable!
Never commit real secret keys to version control (Git).

To set environment variable:
Windows: set SECRET_KEY=your-random-secret-key
Mac/Linux: export SECRET_KEY=your-random-secret-key
"""

# Configuration settings
app.config['DATABASE_NAME'] = 'finance.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

"""
FLASK CONFIGURATION:
app.config is a dictionary storing configuration values.

MAX_CONTENT_LENGTH:
Limits upload size to prevent users from crashing server with huge uploads.
16 * 1024 * 1024 = 16 megabytes (1024 bytes = 1 KB, 1024 KB = 1 MB)
"""

# ============================================================================
# INITIALIZATION
# ============================================================================

# Initialize database on app startup
try:
    database.init_db()
    print(" Database initialized successfully")
except Exception as e:
    print(f" Database initialization failed: {e}")

"""
APP STARTUP CODE:
This runs once when the application starts.
We initialize the database to ensure tables exist before handling requests.

TRY/EXCEPT:
Catches initialization errors so app doesn't crash on startup.
Prints clear error message to help with debugging.
"""

# ============================================================================
# TEMPLATE FILTERS - Custom Functions for Jinja2 Templates
# ============================================================================

@app.template_filter('currency')
def currency_filter(value):
    """
    Formats numbers as currency in templates.

    TEMPLATE FILTERS:
    Filters transform values in templates.
    Usage in template: {{ amount|currency }}
    This calls currency_filter(amount)

    Args:
        value: Number to format

    Returns:
        Formatted currency string (e.g., '$1,234.56')

    Example in Template:
        {{ 1234.56|currency }} renders as '$1,234.56'
    """
    try:
        return format_currency(float(value))
    except (ValueError, TypeError):
        return '$0.00'  # Return default if conversion fails


@app.template_filter('date_format')
def date_format_filter(date_str, format='%B %d, %Y'):
    """
    Formats date strings in templates.

    Args:
        date_str: Date string in YYYY-MM-DD format
        format: strftime format string

    Returns:
        Formatted date string

    Example in Template:
        {{ '2025-10-01'|date_format }} renders as 'October 01, 2025'
        {{ '2025-10-01'|date_format('%m/%d/%Y') }} renders as '10/01/2025'
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime(format)
    except (ValueError, TypeError):
        return date_str  # Return original if parsing fails


# ============================================================================
# CONTEXT PROCESSORS - Variables Available in All Templates
# ============================================================================

@app.context_processor
def inject_categories():
    """
    Makes expense categories and income sources available to all templates.

    CONTEXT PROCESSORS:
    Functions decorated with @app.context_processor run before rendering any template.
    They return a dictionary of variables that become available in ALL templates.

    This means every template can access 'categories' and 'income_sources' without us passing them explicitly.

    Returns:
        Dict with variables to inject into template context

    Usage in Templates:
        {% for category in categories %}
            <option>{{ category }}</option>
        {% endfor %}

        {% for source in income_sources %}
            <option>{{ source }}</option>
        {% endfor %}
    """
    return {
        'categories': ExpenseCategory.get_all_categories(),
        'category_colors': ExpenseCategory.get_category_dict(),
        'income_sources': IncomeSource.get_all_sources(),
        'income_source_colors': IncomeSource.get_source_dict(),
        'current_year': datetime.now().year
    }

    """
    INJECTED VARIABLES:
    - categories: List of expense category names (for dropdowns)
    - category_colors: Dict mapping expense categories to colors (for styling)
    - income_sources: List of income source names (for dropdowns)
    - income_source_colors: Dict mapping income sources to colors (for styling)
    - current_year: Current year (for copyright notices, date pickers, etc.)

    JUNIOR DEV NOTE:
    By adding these to the context processor, we don't have to pass them
    manually to every single template. They're automatically available!
    """


# ============================================================================
# ROUTES - URL Handlers
# ============================================================================

# ----------------------------------------------------------------------------
# HOME PAGE
# ----------------------------------------------------------------------------

@app.route('/')
def index():
    """
    Displays the home page with financial overview.

    UPDATED DASHBOARD:
    Now shows both income and expenses for complete financial picture.
    Key metrics:
    - Total income
    - Total expenses
    - Net savings (income - expenses)
    - Savings rate (savings / income as percentage)

    ROUTE DECORATOR:
    @app.route('/') means "when user visits the root URL, call this function"

    Returns:
        Rendered HTML template with financial data

    Template: templates/index.html
    """

    # Get all expenses from database
    expense_dicts = database.get_all_expenses()
    expenses = [Expense.from_dict(exp) for exp in expense_dicts]

    # Get all income from database
    income_dicts = database.get_all_income()
    income_records = [Income.from_dict(inc) for inc in income_dicts]

    """
    COMPLETE FINANCIAL PICTURE:
    We now fetch both expenses AND income.
    This lets us show:
    - How much money is coming IN (income)
    - How much money is going OUT (expenses)
    - The difference (savings or deficit)
    """

    # Calculate expense statistics
    total_expenses_count = len(expenses)
    total_expenses_amount = ExpenseAnalyzer.calculate_total(expenses)
    category_totals = ExpenseAnalyzer.get_category_totals(expenses)

    # Calculate income statistics
    total_income_count = len(income_records)
    total_income_amount = sum(inc.amount for inc in income_records)

    # Calculate net savings and savings rate
    net_savings = total_income_amount - total_expenses_amount
    # Net savings = money left over after expenses
    # Positive = saving money ✓
    # Negative = spending more than earning (deficit) ✗

    # Calculate savings rate with better handling of negative savings
    """
    SAVINGS RATE CALCULATION:
    Savings Rate = (Net Savings / Total Income) × 100

    Example:
    - Income: $5000
    - Expenses: $3500
    - Net Savings: $1500
    - Savings Rate: ($1500 / $5000) × 100 = 30%

    Financial experts recommend 20% minimum savings rate.
    """
    if total_income_amount > 0:
        savings_rate = (net_savings / total_income_amount * 100)

        # Flag if running a deficit (spending more than earning)
        is_deficit = net_savings < 0
        # is_deficit flag lets template display "DEFICIT" instead of negative percentage
        # Better UX: "20% Deficit" vs "-20% Savings Rate"

    else:
        # No income recorded - can't calculate savings rate
        savings_rate = 0
        is_deficit = False
        # Prevents division by zero error

    """
    FINANCIAL CALCULATIONS:

    NET SAVINGS:
    Income - Expenses = Savings
    $5000 - $3500 = $1500 saved

    SAVINGS RATE:
    (Savings / Income) * 100 = Percentage saved
    ($1500 / $5000) * 100 = 30% savings rate

    WHY SAVINGS RATE MATTERS:
    Financial experts recommend saving 20% of income.
    Savings rate is more important than absolute amount:
    - 30% of $3000 = $900 (better than)
    - 10% of $5000 = $500

    EDGE CASE:
    If income is $0, we can't divide (would cause error).
    That's why we check: if total_income_amount > 0
    Otherwise savings rate defaults to 0.
    """

    # Get recent transactions (5 expenses + 5 income)
    recent_expenses = expenses[:5] if expenses else []
    recent_income = income_records[:5] if income_records else []

    """
    RECENT ACTIVITY:
    Show last 5 expenses and last 5 income for quick overview.
    User can click through to see full lists.
    """

    # Render template with data
    return render_template(
        'index.html',
        expenses=recent_expenses,
        total_expenses=total_expenses_count,
        total_expenses_amount=total_expenses_amount,
        category_totals=category_totals,
        income_records=recent_income,
        total_income=total_income_count,
        total_income_amount=total_income_amount,
        net_savings=net_savings,
        savings_rate=savings_rate,
        is_deficit=is_deficit
    )

    """
    TEMPLATE VARIABLES:
    All these variables become available in index.html:
    - expenses: Last 5 expense records
    - total_expenses: Count of all expenses
    - total_expenses_amount: Sum of all expenses
    - category_totals: Spending by category
    - income_records: Last 5 income records
    - total_income: Count of all income
    - total_income_amount: Sum of all income
    - net_savings: Income - Expenses
    - savings_rate: Percentage of income saved
    """

    """
    RENDER_TEMPLATE:
    1. Loads templates/index.html
    2. Replaces placeholders with our data
    3. Returns final HTML to browser

    Variables passed become available in template:
    {{ expenses }}, {{ total_amount }}, etc.
    """


# ----------------------------------------------------------------------------
# ADD EXPENSE
# ----------------------------------------------------------------------------

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    """
    Handles expense addition form.

    TWO HTTP METHODS:
    - GET: User requests the form (viewing the page)
    - POST: User submits the form (sending data)

    FORM WORKFLOW:
    1. User visits /add (GET)  Show empty form
    2. User fills form and clicks submit  Browser sends POST to /add
    3. We validate data
    4. If valid  Save to database and redirect
    5. If invalid  Show form again with error message

    Returns:
        GET: Rendered form template
        POST: Redirect to home page (on success) or form with errors
    """

    if request.method == 'POST':
        """
        REQUEST.METHOD:
        Browser tells us what type of request this is.
        POST means user submitted a form.
        """

        # Get form data
        date = request.form.get('date', '')
        category = request.form.get('category', '')
        amount_str = request.form.get('amount', '0')
        description = request.form.get('description', '')

        """
        REQUEST.FORM:
        Dictionary containing form data.
        Keys match the 'name' attribute of HTML form inputs.

        <input name="amount">  request.form.get('amount')

        .get(key, default):
        Returns value if key exists, otherwise returns default.
        This prevents KeyError if field is missing.
        """

        # Convert amount to float
        try:
            amount = float(amount_str)
        except ValueError:
            flash('Amount must be a valid number', 'error')
            return redirect(url_for('add_expense'))

        """
        TYPE CONVERSION WITH ERROR HANDLING:
        User input comes as strings. We need to convert '25.50' to 25.50
        If conversion fails (user entered 'abc'), catch error and show message.

        FLASH:
        flash(message, category) creates a temporary message.
        'error' category styles message as error (red)
        Other categories: 'success', 'warning', 'info'

        URL_FOR:
        url_for('add_expense') generates URL for add_expense function.
        Better than hardcoding '/add' because if we change route, URL updates automatically.
        """

        # Validate data
        is_valid, error_message = validate_expense_data(date, category, amount, description)

        if not is_valid:
            flash(error_message, 'error')
            return redirect(url_for('add_expense'))

        """
        VALIDATION:
        Always validate before saving to database!
        Our validate_expense_data function checks:
        - Date format is correct
        - Category is valid
        - Amount is positive
        - Description isn't too long
        """

        # Save to database
        try:
            expense_id = database.add_expense(date, category, amount, description)
            flash(f'Expense added successfully! (ID: {expense_id})', 'success')
            return redirect(url_for('index'))

            """
            SUCCESS PATH:
            1. Save to database
            2. Show success message
            3. Redirect to home page (shows new expense)

            POST-REDIRECT-GET PATTERN:
            After successful POST, always redirect.
            This prevents duplicate submissions if user refreshes page.
            """

        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'error')
            return redirect(url_for('add_expense'))

            """
            ERROR HANDLING:
            If database operation fails, show error and return to form.
            User can try again without losing their data.
            """

    # GET request - show the form
    # Note: categories already available via context processor
    return render_template('add_expense.html')

    """
    GET REQUEST:
    User is viewing the page, not submitting data.
    Show them a blank form to fill out.

    PASSING CATEGORIES:
    Template needs list of valid categories to populate dropdown.
    ExpenseCategory.get_all_categories() returns all category names.
    list() converts to list format that Jinja2 can iterate over.
    """


# ----------------------------------------------------------------------------
# VIEW ALL EXPENSES
# ----------------------------------------------------------------------------

@app.route('/expenses')
def view_expenses():
    """
    Displays all expenses with filtering options.

    URL PARAMETERS:
    Users can filter by adding URL parameters:
    /expenses?category=Food&start_date=2025-10-01

    Returns:
        Rendered template with filtered expenses
    """

    # Get filter parameters from URL
    category_filter = request.args.get('category', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    """
    REQUEST.ARGS:
    Dictionary containing URL parameters (query string).
    /expenses?category=Food  request.args.get('category') = 'Food'

    REQUEST.FORM vs REQUEST.ARGS:
    - request.form: Data from POST forms (body of request)
    - request.args: Data from URL parameters (query string)
    """

    # Fetch expenses based on filters
    if category_filter:
        # Filter by category (e.g., show only "Food & Dining" expenses)
        expense_dicts = database.get_expenses_by_category(category_filter)

    elif start_date and end_date:
        # Validate date range before querying database
        """
        DATE RANGE VALIDATION:
        Users can manipulate URL parameters, so we must validate:
        1. Dates are in correct format (YYYY-MM-DD)
        2. Start date comes before (or equals) end date

        Without validation: start_date='2025-12-01', end_date='2025-01-01'
        would return no results and confuse the user.
        """
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')

            if start_dt > end_dt:
                # Dates are backwards - show error and fall back to all expenses
                flash('Start date must be before or equal to end date', 'error')
                expense_dicts = database.get_all_expenses()
            else:
                # Valid date range - fetch filtered expenses
                expense_dicts = database.get_expenses_by_date_range(start_date, end_date)

        except ValueError:
            # Invalid date format (e.g., '2025-13-45' or 'not-a-date')
            flash('Invalid date format', 'error')
            expense_dicts = database.get_all_expenses()

    else:
        # No filters applied - show all expenses
        expense_dicts = database.get_all_expenses()

    """
    CONDITIONAL FILTERING:
    Check what filters user applied and call appropriate database function.
    If no filters, get all expenses.
    """

    # Convert to Expense objects
    expenses = [Expense.from_dict(exp) for exp in expense_dicts]

    # Calculate statistics for filtered data
    total_amount = ExpenseAnalyzer.calculate_total(expenses)
    category_totals = ExpenseAnalyzer.get_category_totals(expenses)

    return render_template(
        'view_expenses.html',
        expenses=expenses,
        total_amount=total_amount,
        category_totals=category_totals,
        category_filter=category_filter,
        start_date=start_date,
        end_date=end_date,
        now=datetime.now(),
        timedelta=timedelta
        # Note: categories already available via context processor
    )

    """
    PASSING DATA TO TEMPLATE:

    expenses: Filtered list of Expense objects to display
    total_amount: Sum of all filtered expenses (for statistics)
    category_totals: Dictionary of spending by category
    category_filter: Current category filter (to pre-select dropdown)
    start_date/end_date: Current date filters (to pre-fill date inputs)
    now: Current datetime object (for quick filter buttons like "This Month")
    timedelta: timedelta class (so template can calculate date ranges)
    categories: List of all available categories (for dropdown options)

    WHY PASS 'now' AND 'timedelta'?
    The template has "Quick Filter" buttons (This Month, Last 7 Days, etc.)
    that need to calculate date ranges. By passing these objects, the
    template can do calculations like: now.replace(day=1) for first day
    of current month, or (now - timedelta(days=7)) for 7 days ago.

    ALTERNATIVE APPROACH:
    Could calculate these dates in Python and pass them as strings,
    but passing the objects allows template to be more flexible.
    """


# ----------------------------------------------------------------------------
# EDIT EXPENSE
# ----------------------------------------------------------------------------

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """
    Handles expense editing.

    URL PARAMETER:
    <int:expense_id> means this part of URL is captured as an integer.
    /edit/5 calls edit_expense(5)
    /edit/abc returns 404 error (not an integer)

    Args:
        expense_id: ID of expense to edit (from URL)

    Returns:
        GET: Form pre-filled with expense data
        POST: Redirect after successful update
    """

    # Get expense from database
    expense_dict = database.get_expense_by_id(expense_id)

    if not expense_dict:
        flash(f'Expense {expense_id} not found', 'error')
        return redirect(url_for('index'))

    """
    ERROR HANDLING:
    If expense doesn't exist (user typed wrong ID, or expense was deleted),
    show error and redirect to home page.

    ALWAYS VALIDATE:
    Never assume data exists. Always check and handle missing data gracefully.
    """

    expense = Expense.from_dict(expense_dict)

    if request.method == 'POST':
        # Get updated data from form
        date = request.form.get('date', '')
        category = request.form.get('category', '')
        amount_str = request.form.get('amount', '0')
        description = request.form.get('description', '')

        # Convert and validate
        try:
            amount = float(amount_str)
        except ValueError:
            flash('Amount must be a valid number', 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))

        is_valid, error_message = validate_expense_data(date, category, amount, description)

        if not is_valid:
            flash(error_message, 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))

        # Update database
        try:
            success = database.update_expense(expense_id, date, category, amount, description)

            if success:
                flash('Expense updated successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Failed to update expense', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))

        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))

    # GET request - show form with current data
    return render_template(
        'add_expense.html',
        expense=expense,
        edit_mode=True
        # Note: categories already available via context processor
    )

    """
    TEMPLATE REUSE:
    We reuse add_expense.html for editing by passing expense and edit_mode.

    PARAMETERS PASSED:
    - expense: Current expense data to pre-fill form
    - edit_mode: Boolean flag (True) so template knows we're editing
    - categories: List of all valid categories for dropdown

    Template can check if edit_mode=True and:
    - Pre-fill form with expense data
    - Change submit button text to "Update" instead of "Add"
    - Change form action URL

    This is DRY (Don't Repeat Yourself) - one template for add and edit.
    """


# ----------------------------------------------------------------------------
# DELETE EXPENSE
# ----------------------------------------------------------------------------

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense_route(expense_id):
    """
    Deletes an expense.

    SECURITY NOTE:
    Only accepts POST requests, not GET.
    This prevents accidental deletions from clicking links or browser prefetching.

    DELETE CONFIRMATION:
    Frontend should show JavaScript confirmation before submitting this request.

    Args:
        expense_id: ID of expense to delete

    Returns:
        Redirect to home page
    """

    try:
        success = database.delete_expense(expense_id)

        if success:
            flash('Expense deleted successfully!', 'success')
        else:
            flash(f'Expense {expense_id} not found', 'error')

    except Exception as e:
        flash(f'Error deleting expense: {str(e)}', 'error')

    return redirect(url_for('index'))

    """
    ALWAYS REDIRECT AFTER DELETE:
    Prevents user from resubmitting delete request if they refresh page.

    FUNCTION NAME:
    Named delete_expense_route (not delete_expense) to avoid naming conflict
    with database.delete_expense function.
    """


# ----------------------------------------------------------------------------
# BUDGET MANAGEMENT
# ----------------------------------------------------------------------------

@app.route('/budgets', methods=['GET', 'POST'])
def manage_budgets():
    """
    Handles budget viewing and setting.

    Returns:
        GET: Budget management page
        POST: Redirect after setting budget
    """

    if request.method == 'POST':
        category = request.form.get('category', '')
        limit_str = request.form.get('monthly_limit', '0')

        try:
            monthly_limit = float(limit_str)

            if monthly_limit <= 0:
                flash('Budget limit must be greater than 0', 'error')
                return redirect(url_for('manage_budgets'))

            success = database.set_budget(category, monthly_limit)

            if success:
                flash(f'Budget set for {category}: {format_currency(monthly_limit)}/month', 'success')
            else:
                flash('Failed to set budget', 'error')

        except ValueError:
            flash('Budget limit must be a valid number', 'error')

        return redirect(url_for('manage_budgets'))

    # GET request - show budgets page
    budget_dicts = database.get_all_budgets()
    budgets = [Budget.from_dict(b) for b in budget_dicts]

    # Get current month expenses for budget comparison
    now = datetime.now()
    expense_dicts = database.get_all_expenses()
    expenses = [Expense.from_dict(exp) for exp in expense_dicts]

    # Calculate budget status
    budget_status = ExpenseAnalyzer.get_budget_status(
        expenses, budgets, now.year, now.month
    )

    """
    BUDGET STATUS:
    Shows how much of each budget has been used this month.
    ExpenseAnalyzer.get_budget_status calculates:
    - Amount spent vs budget limit
    - Percentage used
    - Whether over budget
    """

    return render_template(
        'budgets.html',
        budgets=budgets,
        budget_status=budget_status,
        current_month=now.strftime('%B %Y'),
        now=now
        # Note: categories and category_colors already available via context processor
    )

    """
    TEMPLATE DATA:
    - budgets: All budget records from database
    - budget_status: Calculated spending vs limits for current month
    - current_month: Formatted month name (e.g., "October 2025")
    - categories: List of all expense categories for dropdown
    - category_colors: Dictionary mapping categories to colors
    - now: Current datetime for pacing calculations
    """


# ----------------------------------------------------------------------------
# ANALYTICS & REPORTS
# ----------------------------------------------------------------------------

@app.route('/analytics')
def analytics():
    """
    Displays spending analytics and visualizations.

    This page shows:
    - Category breakdown pie chart
    - Spending trend line chart
    - Monthly comparisons
    - Summary statistics

    Returns:
        Rendered analytics template with chart data
    """

    # Get all expenses
    expense_dicts = database.get_all_expenses()
    expenses = [Expense.from_dict(exp) for exp in expense_dicts]

    if not expenses:
        flash('No expenses to analyze yet. Add some expenses first!', 'info')
        return redirect(url_for('index'))

    # Calculate category totals for pie chart
    category_totals = ExpenseAnalyzer.get_category_totals(expenses)

    # Get spending trend for line chart
    spending_trend = ExpenseAnalyzer.get_spending_trend(expenses, months=6)

    """
    CHART DATA:
    We prepare data in Python and pass to template.
    Template uses JavaScript (Chart.js) to render visual charts.

    Data format for Chart.js:
    - Labels: ['Food', 'Transport', ...]
    - Data: [250.50, 100.00, ...]
    - Colors: ['#FF6B6B', '#4ECDC4', ...]
    """

    # Prepare chart data
    category_labels = list(category_totals.keys())
    category_values = list(category_totals.values())
    category_colors_map = ExpenseCategory.get_category_dict()
    category_colors = [category_colors_map.get(cat, '#BDC3C7') for cat in category_labels]

    """
    LIST COMPREHENSION WITH GET:
    [category_colors_map.get(cat, default) for cat in category_labels]

    For each category, look up its color. If not found, use gray (#BDC3C7).
    """

    # Prepare trend data
    trend_labels = list(spending_trend.keys())
    trend_values = list(spending_trend.values())

    # Calculate summary statistics
    total_spent = ExpenseAnalyzer.calculate_total(expenses)
    average_expense = ExpenseAnalyzer.calculate_average(expenses)

    # Get current month spending
    now = datetime.now()
    current_month_total = ExpenseAnalyzer.get_monthly_total(expenses, now.year, now.month)

    return render_template(
        'analytics.html',
        category_labels=category_labels,
        category_values=category_values,
        category_colors=category_colors,
        trend_labels=trend_labels,
        trend_values=trend_values,
        total_spent=total_spent,
        average_expense=average_expense,
        current_month_total=current_month_total
    )


# ----------------------------------------------------------------------------
# EXPORT DATA
# ----------------------------------------------------------------------------

@app.route('/export')
def export_csv():
    """
    Exports all expenses to CSV file.

    CSV (Comma-Separated Values) format can be opened in Excel, Google Sheets, etc.

    Returns:
        CSV file download
    """
    import csv
    from io import StringIO
    from flask import make_response

    """
    ADDITIONAL IMPORTS:
    Imported inside function since only needed here.
    - csv: Module for reading/writing CSV files
    - StringIO: Creates a file-like object in memory (no disk write needed)
    - make_response: Creates custom HTTP response
    """

    # Get all expenses
    expense_dicts = database.get_all_expenses()

    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)

    """
    STRING IO:
    StringIO creates a file-like object that writes to memory instead of disk.
    Faster and simpler than creating temporary files.
    """

    # Write header row
    writer.writerow(['ID', 'Date', 'Category', 'Amount', 'Description', 'Created At'])

    # Write expense rows
    for expense in expense_dicts:
        writer.writerow([
            expense['id'],
            expense['date'],
            expense['category'],
            expense['amount'],
            expense['description'],
            expense['created_at']
        ])

    """
    CSV FORMAT:
    Each writerow() creates one line in CSV file:
    ID,Date,Category,Amount,Description,Created At
    1,2025-10-01,Food & Dining,25.50,Lunch,2025-10-01 10:30:00
    """

    # Create response
    output.seek(0)  # Move to start of StringIO object

    """
    SEEK(0):
    After writing, we're at the end of the file.
    seek(0) moves back to the beginning so we can read it.
    """

    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=expenses_{datetime.now().strftime("%Y%m%d")}.csv'

    """
    HTTP HEADERS:
    - Content-Type: Tells browser what kind of file this is
    - Content-Disposition: Tells browser to download (not display) file
    - filename: What to name the downloaded file

    Result: File downloads as expenses_20251001.csv
    """

    return response


# ============================================================================
# INCOME TRACKING ROUTES
# ============================================================================

@app.route('/income')
def view_income():
    """
    Displays all income records.

    INCOME TRACKING:
    Just like we have a page for viewing expenses, we need one for income.
    This shows all money coming IN (as opposed to going OUT).

    WHY TRACK INCOME?
    - See total earnings over time
    - Understand income sources (where money comes from)
    - Calculate net worth (income - expenses)
    - Track savings rate

    Returns:
        Rendered template with all income records

    JUNIOR DEV NOTES:
    - Similar structure to view_expenses route
    - Could add filtering later (by source, date range, etc.)
    - For now, showing all income sorted by date
    """
    # Get all income from database
    income_dicts = database.get_all_income()

    # Convert dictionaries to Income objects
    income_records = [Income.from_dict(inc) for inc in income_dicts]

    # Calculate total income
    total_income = sum(inc.amount for inc in income_records)

    # Count total records
    total_records = len(income_records)

    # Get income by source (for statistics)
    income_by_source = {}
    for inc in income_records:
        source = inc.source
        if source in income_by_source:
            income_by_source[source] += inc.amount
        else:
            income_by_source[source] = inc.amount

    """
    GROUPING BY SOURCE:
    We loop through all income and group by source.
    This shows how much came from each source (Salary, Freelance, etc.)

    Example result:
    {
        'Salary': 15000.00,
        'Freelance': 3500.00,
        'Gift': 500.00
    }
    """

    return render_template(
        'view_income.html',
        income_records=income_records,
        total_income=total_income,
        total_records=total_records,
        income_by_source=income_by_source
    )


@app.route('/income/add', methods=['GET', 'POST'])
def add_income():
    """
    Handles adding new income records.

    TWO REQUEST TYPES:
    - GET: Show the add income form (empty)
    - POST: Process the submitted form data

    Returns:
        GET: Rendered form template
        POST: Redirect to income list with success message

    JUNIOR DEV NOTES:
    - Almost identical to add_expense() but for income
    - Same pattern: GET shows form, POST processes it
    - Validates data before saving to database
    """
    if request.method == 'POST':
        # Get form data
        date = request.form.get('date', '')
        source = request.form.get('source', '')
        amount_str = request.form.get('amount', '0')
        description = request.form.get('description', '')

        # Convert amount to float
        try:
            amount = float(amount_str)
        except ValueError:
            flash('Amount must be a valid number', 'error')
            return redirect(url_for('add_income'))

        # Validate data using new validation function
        is_valid, error_message = validate_income_data(date, source, amount, description)

        if not is_valid:
            flash(error_message, 'error')
            return redirect(url_for('add_income'))

        """
        VALIDATION:
        We check:
        1. Date is provided
        2. Source is selected
        3. Amount is positive (can't have negative income!)

        This prevents bad data from getting into the database.
        """

        # Save to database
        try:
            income_id = database.add_income(date, source, amount, description)
            flash(f'Income added successfully! (ID: {income_id})', 'success')
            return redirect(url_for('view_income'))

        except Exception as e:
            flash(f'Error adding income: {str(e)}', 'error')
            return redirect(url_for('add_income'))

    # GET request - show the form
    return render_template('add_income.html')


@app.route('/income/edit/<int:income_id>', methods=['GET', 'POST'])
def edit_income(income_id):
    """
    Handles editing existing income records.

    Args:
        income_id: ID of income record to edit (from URL)

    Returns:
        GET: Form pre-filled with income data
        POST: Redirect after successful update

    JUNIOR DEV NOTES:
    - Similar to edit_expense() but for income
    - Loads existing data on GET to pre-fill form
    - Updates database on POST
    """
    # Get income from database
    income_dict = database.get_income_by_id(income_id)

    if not income_dict:
        flash(f'Income record {income_id} not found', 'error')
        return redirect(url_for('view_income'))

    income = Income.from_dict(income_dict)

    if request.method == 'POST':
        # Get updated data from form
        date = request.form.get('date', '')
        source = request.form.get('source', '')
        amount_str = request.form.get('amount', '0')
        description = request.form.get('description', '')

        # Convert and validate
        try:
            amount = float(amount_str)
        except ValueError:
            flash('Amount must be a valid number', 'error')
            return redirect(url_for('edit_income', income_id=income_id))

        # Validate data using validation function
        is_valid, error_message = validate_income_data(date, source, amount, description)

        if not is_valid:
            flash(error_message, 'error')
            return redirect(url_for('edit_income', income_id=income_id))

        # Update database
        try:
            success = database.update_income(income_id, date, source, amount, description)

            if success:
                flash('Income updated successfully!', 'success')
                return redirect(url_for('view_income'))
            else:
                flash('Failed to update income', 'error')
                return redirect(url_for('edit_income', income_id=income_id))

        except Exception as e:
            flash(f'Error updating income: {str(e)}', 'error')
            return redirect(url_for('edit_income', income_id=income_id))

    # GET request - show form with current data
    return render_template(
        'add_income.html',
        income=income,
        edit_mode=True
    )

    """
    TEMPLATE REUSE:
    We reuse add_income.html for editing by passing:
    - income: Current income data to pre-fill form
    - edit_mode: Boolean flag so template knows we're editing

    This is DRY (Don't Repeat Yourself) - one template for add and edit!
    """


@app.route('/income/delete/<int:income_id>', methods=['POST'])
def delete_income_route(income_id):
    """
    Deletes an income record.

    SECURITY:
    Only accepts POST requests (not GET) to prevent accidental deletions.
    Frontend should show confirmation dialog before submitting.

    Args:
        income_id: ID of income record to delete

    Returns:
        Redirect to income list page

    JUNIOR DEV NOTES:
    - Named delete_income_route to avoid conflict with database.delete_income()
    - Always use POST for destructive actions (delete, update)
    - GET requests should be read-only (safe to call multiple times)
    """
    try:
        success = database.delete_income(income_id)

        if success:
            flash('Income deleted successfully!', 'success')
        else:
            flash(f'Income record {income_id} not found', 'error')

    except Exception as e:
        flash(f'Error deleting income: {str(e)}', 'error')

    return redirect(url_for('view_income'))


# ============================================================================
# API ENDPOINTS (For AJAX Requests)
# ============================================================================

@app.route('/api/category-totals')
def api_category_totals():
    """
    Returns category totals as JSON.

    API ENDPOINTS:
    These routes return JSON data instead of HTML.
    Used by JavaScript to fetch data without reloading page (AJAX).

    Returns:
        JSON response with category totals
    """

    category_totals = database.get_category_totals()

    """
    JSONIFY:
    Converts Python dictionary to JSON string and sets correct Content-Type header.
    {'Food': 250.50} becomes '{"Food": 250.50}'
    """

    return jsonify(category_totals)


@app.route('/api/monthly-trend/<int:months>')
def api_monthly_trend(months):
    """
    Returns spending trend data as JSON.

    Args:
        months: Number of months to include

    Returns:
        JSON response with monthly totals
    """

    expense_dicts = database.get_all_expenses()
    expenses = [Expense.from_dict(exp) for exp in expense_dicts]

    trend = ExpenseAnalyzer.get_spending_trend(expenses, months=months)

    return jsonify(trend)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 errors (page not found).

    ERROR HANDLERS:
    Special functions that run when specific errors occur.
    Instead of showing Flask's default error page, we show our custom page.

    Args:
        error: Error object (automatically passed by Flask)

    Returns:
        Custom 404 error page with 404 status code
    """
    return render_template('error.html',
                          error_code=404,
                          error_message='Page not found'), 404

    """
    RETURN TUPLE:
    (template, status_code)
    - template: HTML to show
    - 404: HTTP status code (tells browser this is an error)

    Common status codes:
    - 200: OK (success)
    - 404: Not Found
    - 500: Internal Server Error
    - 403: Forbidden
    """


@app.errorhandler(500)
def internal_error(error):
    """
    Handles 500 errors (internal server errors).

    These occur when Python code raises an unhandled exception.
    """
    return render_template('error.html',
                          error_code=500,
                          error_message='Internal server error'), 500


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    """
    This code runs when you execute: python app.py

    It starts the Flask development server.
    """

    print("\n" + "="*50)
    print(" Starting Personal Finance Dashboard")
    print("="*50)
    print(f" Database: {app.config['DATABASE_NAME']}")
    print(f" Server: http://localhost:5000")
    print(f" Debug Mode: True (Development)")
    print("="*50 + "\n")

    """
    STARTUP MESSAGE:
    Shows important information when server starts.
    Helps developers know configuration and where to access the app.
    """

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )

    """
    APP.RUN OPTIONS:

    debug=True:
    - Shows detailed error pages when something breaks
    - Auto-reloads server when code changes (no need to restart)
    - NEVER use in production! Security risk.

    host='0.0.0.0':
    - Makes server accessible from other devices on network
    - localhost = only accessible from your computer
    - 0.0.0.0 = accessible from any computer on your network

    port=5000:
    - Which port to run on
    - Access at http://localhost:5000
    - If 5000 is busy, try 5001, 8000, 8080, etc.

    TO RUN:
    1. Open terminal in project folder
    2. Activate virtual environment: venv\\Scripts\\activate (Windows)
    3. Run: python app.py
    4. Open browser to http://localhost:5000
    5. Press Ctrl+C to stop server
    """
