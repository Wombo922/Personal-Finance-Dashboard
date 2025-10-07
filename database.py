"""
DATABASE.PY - Database Management Module
=========================================

PURPOSE:
This file handles all database operations for the Personal Finance Dashboard.
It creates, reads, updates, and deletes (CRUD) data from our SQLite database.

WHAT IS A DATABASE?
A database is like a smart filing cabinet that stores information in an organized way.
Instead of keeping data in variables (which disappear when the program stops),
databases save information permanently on your computer's hard drive.

WHAT IS SQLite?
SQLite is a lightweight database that stores everything in a single file (finance.db).
Unlike other databases (MySQL, PostgreSQL), it doesn't need a separate server running.
Perfect for small to medium applications like ours!

WHY SEPARATE DATABASE OPERATIONS?
- Separation of Concerns: Keeps database logic separate from web logic
- Reusability: These functions can be used anywhere in our app
- Maintainability: If we change databases later, we only update this file
- Testing: Easier to test database operations in isolation

JUNIOR DEVELOPER NOTES:
- Always close database connections when done (prevents file locks)
- Use parameterized queries (?) to prevent SQL injection attacks
- Handle errors gracefully with try/except blocks
- Document what each function does and returns
"""

# ============================================================================
# IMPORTS - External Libraries We Need
# ============================================================================

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple

"""
IMPORT EXPLANATIONS:
- sqlite3: Python's built-in library for SQLite databases
- datetime: Handles dates and times (for created_at timestamps)
- typing: Helps us specify what type of data functions expect/return
  - List: A list of items (e.g., List[Dict] = list of dictionaries)
  - Dict: A dictionary/object (e.g., {"key": "value"})
  - Optional: Value can be the specified type OR None
  - Tuple: An immutable list (can't be changed after creation)
"""

# ============================================================================
# CONSTANTS - Values That Never Change
# ============================================================================

DATABASE_NAME = 'finance.db'

"""
WHY USE CONSTANTS?
If we ever need to rename the database file, we only change it here.
All functions reference DATABASE_NAME, so they'll automatically use the new name.
Convention: Constants are written in UPPERCASE_WITH_UNDERSCORES
"""

# ============================================================================
# DATABASE CONNECTION FUNCTION
# ============================================================================

def get_db_connection():
    """
    Establishes a connection to the SQLite database.

    WHAT IS A DATABASE CONNECTION?
    Think of it like opening a file - you need to "open" the database before
    reading or writing to it. The connection object lets you execute SQL commands.

    WHAT IS ROW_FACTORY?
    By default, SQLite returns data as tuples: (1, 'Food', 25.50)
    With Row factory, we get dictionaries: {'id': 1, 'category': 'Food', 'amount': 25.50}
    Dictionaries are easier to work with because we access values by name, not position.

    Returns:
        sqlite3.Connection: A connection object to interact with the database

    Example Usage:
        conn = get_db_connection()
        # Do database operations here
        conn.close()

    BEST PRACTICE: Always close connections when done!
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries instead of tuples
    return conn


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """
    Initializes the database by creating all necessary tables.

    WHEN TO CALL THIS:
    Run this function once when you first set up the application.
    It's safe to run multiple times - it won't overwrite existing data
    because we use "IF NOT EXISTS" in the CREATE TABLE statements.

    TABLES CREATED:
    1. expenses - Stores individual expense records
    2. budgets - Stores monthly budget limits by category (added in Week 2)

    SQL KEYWORDS EXPLAINED:
    - CREATE TABLE IF NOT EXISTS: Only creates table if it doesn't already exist
    - INTEGER PRIMARY KEY AUTOINCREMENT: Unique ID that auto-increments (1, 2, 3...)
    - TEXT: Stores text/strings of any length
    - REAL: Stores decimal numbers (floats)
    - NOT NULL: This field is required, can't be empty
    - DEFAULT CURRENT_TIMESTAMP: Automatically sets to current date/time when row created
    - UNIQUE: No two rows can have the same value in this column

    Returns:
        None

    Raises:
        sqlite3.Error: If there's a problem creating the database
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        """
        WHAT IS A CURSOR?
        A cursor is like a pointer that executes SQL commands and fetches results.
        Think of it as a pen that writes to/reads from the database.
        """

        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        """
        EXPENSES TABLE STRUCTURE:
        - id: Unique identifier for each expense (auto-generated)
        - date: When the expense occurred (format: YYYY-MM-DD)
        - category: Type of expense (Food, Transport, etc.)
        - amount: How much money was spent (decimal number)
        - description: Optional notes about the expense
        - created_at: When this record was added to database (auto-generated)
        """

        # Create budgets table (we'll use this in Week 2)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                monthly_limit REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        """
        BUDGETS TABLE STRUCTURE:
        - id: Unique identifier for each budget (auto-generated)
        - category: Must be unique - only one budget per category
        - monthly_limit: Maximum amount to spend in this category per month
        - created_at: When this budget was created (auto-generated)
        """

        # Create income table for tracking earnings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                source TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        """
        INCOME TABLE STRUCTURE:
        - id: Unique identifier for each income record (auto-generated)
        - date: When the income was received (format: YYYY-MM-DD)
        - source: Where the money came from (Salary, Freelance, Gift, Investment, etc.)
        - amount: How much money was received (decimal number)
        - description: Optional notes about the income (e.g., "Monthly salary - January")
        - created_at: When this record was added to database (auto-generated)

        WHY SEPARATE INCOME TABLE?
        We could add a "type" field to expenses, but separating income has benefits:
        1. Clearer data model - income and expenses are fundamentally different
        2. Different categories - income sources vs expense categories
        3. Easier queries - don't need WHERE type='income' everywhere
        4. Future flexibility - income might need different fields later
        """

        conn.commit()  # Save changes to database
        conn.close()   # Close connection

        print(f"Database initialized successfully: {DATABASE_NAME}")

        """
        WHAT IS COMMIT?
        Changes to the database aren't saved until you call commit().
        This is like clicking "Save" - if your program crashes before commit(),
        no changes are saved (which is actually a safety feature!).
        """

    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        raise  # Re-raise the error so calling code knows something went wrong

    """
    ERROR HANDLING:
    The try/except block catches database errors so the program doesn't crash.
    We print a friendly error message and raise the error again so the caller
    knows something went wrong and can handle it appropriately.
    """


# ============================================================================
# CREATE OPERATIONS (Adding New Data)
# ============================================================================

def add_expense(date: str, category: str, amount: float, description: str = "") -> int:
    """
    Adds a new expense record to the database.

    FUNCTION PARAMETERS EXPLAINED:
    - date (str): The date of the expense in 'YYYY-MM-DD' format
    - category (str): The expense category (e.g., 'Food & Dining')
    - amount (float): The amount spent (e.g., 25.50)
    - description (str, optional): Optional notes about the expense. Defaults to empty string.

    THE -> int MEANS:
    This function returns an integer (the ID of the newly created expense)

    Args:
        date: Date in ISO format (YYYY-MM-DD)
        category: Category name from predefined list
        amount: Expense amount (must be positive)
        description: Optional description of the expense

    Returns:
        int: The ID of the newly created expense record

    Raises:
        sqlite3.Error: If database operation fails
        ValueError: If amount is negative or zero

    Example Usage:
        expense_id = add_expense('2025-10-01', 'Food & Dining', 25.50, 'Lunch at cafe')
        print(f"Created expense with ID: {expense_id}")

    SQL INJECTION PREVENTION:
    Notice we use ? placeholders instead of f-strings or string concatenation.
    This prevents SQL injection attacks where malicious users could manipulate queries.

    WRONG (Vulnerable): f"INSERT INTO expenses VALUES ('{date}', '{category}'...)"
    RIGHT (Safe): "INSERT INTO expenses VALUES (?, ?, ...)", (date, category, ...)
    """

    # Validate input data
    if amount <= 0:
        raise ValueError("Amount must be positive")

    """
    INPUT VALIDATION:
    Always validate data BEFORE putting it in the database.
    This prevents bad data from corrupting your database.
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new expense
        cursor.execute('''
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, description))

        """
        THE ? PLACEHOLDERS:
        Each ? is replaced by the corresponding value in the tuple (date, category, amount, description)
        sqlite3 automatically escapes special characters, preventing SQL injection.
        """

        expense_id = cursor.lastrowid  # Get the ID of the row we just inserted

        """
        LASTROWID:
        After inserting a row, lastrowid gives us the auto-generated ID.
        This is useful for confirming the operation succeeded and for referencing this expense later.
        """

        conn.commit()
        conn.close()

        return expense_id

    except sqlite3.Error as e:
        print(f"Error adding expense: {e}")
        raise


def set_budget(category: str, monthly_limit: float) -> bool:
    """
    Sets or updates a monthly budget limit for a specific category.

    UPSERT OPERATION:
    This function checks if budget exists:
    - If budget doesn't exist: create new budget
    - If budget exists: update only the monthly_limit (preserves created_at)

    Args:
        category: The expense category to set budget for
        monthly_limit: Maximum amount allowed per month

    Returns:
        bool: True if operation succeeded, False otherwise

    Example Usage:
        if set_budget('Food & Dining', 500.00):
            print("Budget set successfully")
    """

    if monthly_limit <= 0:
        raise ValueError("Budget limit must be positive")

    if monthly_limit >= 10000000:
        raise ValueError("Budget limit seems unreasonably large (>= $10,000,000). Please verify.")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if budget exists
        cursor.execute('SELECT id FROM budgets WHERE category = ?', (category,))
        existing = cursor.fetchone()

        if existing:
            # Update existing budget (preserves created_at)
            cursor.execute('''
                UPDATE budgets
                SET monthly_limit = ?
                WHERE category = ?
            ''', (monthly_limit, category))
        else:
            # Insert new budget
            cursor.execute('''
                INSERT INTO budgets (category, monthly_limit)
                VALUES (?, ?)
            ''', (category, monthly_limit))

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error as e:
        print(f" Error setting budget: {e}")
        return False


# ============================================================================
# READ OPERATIONS (Getting Data)
# ============================================================================

def get_all_expenses() -> List[Dict]:
    """
    Retrieves all expenses from the database, sorted by date (newest first).

    RETURN TYPE EXPLAINED:
    List[Dict] means this returns a list of dictionaries.
    Example: [
        {'id': 1, 'date': '2025-10-01', 'category': 'Food', 'amount': 25.50, ...},
        {'id': 2, 'date': '2025-09-30', 'category': 'Transport', 'amount': 15.00, ...}
    ]

    Returns:
        List[Dict]: List of expense dictionaries, each containing:
            - id (int): Expense unique identifier
            - date (str): Expense date
            - category (str): Expense category
            - amount (float): Expense amount
            - description (str): Expense description
            - created_at (str): Timestamp when record was created

    Example Usage:
        expenses = get_all_expenses()
        for expense in expenses:
            print(f"{expense['date']}: ${expense['amount']} on {expense['category']}")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM expenses
            ORDER BY date DESC, created_at DESC
        ''')

        """
        SQL SELECT EXPLAINED:
        - SELECT *: Get all columns from the table
        - FROM expenses: From the expenses table
        - ORDER BY date DESC: Sort by date, newest first (DESC = descending)
        - created_at DESC: If same date, show most recently added first
        """

        expenses = cursor.fetchall()

        """
        FETCHALL vs FETCHONE:
        - fetchall(): Returns all matching rows as a list
        - fetchone(): Returns only the first matching row
        - fetchmany(n): Returns n matching rows
        """

        conn.close()

        # Convert Row objects to dictionaries for easier use
        return [dict(expense) for expense in expenses]

        """
        LIST COMPREHENSION:
        [dict(expense) for expense in expenses]
        This is shorthand for:

        result = []
        for expense in expenses:
            result.append(dict(expense))
        return result

        It converts each Row object to a regular Python dictionary.
        """

    except sqlite3.Error as e:
        print(f" Error getting expenses: {e}")
        return []  # Return empty list on error


def get_expense_by_id(expense_id: int) -> Optional[Dict]:
    """
    Retrieves a single expense by its ID.

    OPTIONAL TYPE:
    Optional[Dict] means this function returns either a Dictionary OR None.
    We return None if no expense with that ID exists.

    Args:
        expense_id: The unique ID of the expense to retrieve

    Returns:
        Optional[Dict]: Expense dictionary if found, None if not found

    Example Usage:
        expense = get_expense_by_id(5)
        if expense:
            print(f"Found: {expense['description']}")
        else:
            print("Expense not found")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM expenses
            WHERE id = ?
        ''', (expense_id,))

        """
        THE COMMA IN (expense_id,):
        Python needs a comma to distinguish a tuple from a parenthesized expression.
        (expense_id) is just the number with parentheses
        (expense_id,) is a tuple containing one element
        The execute() method expects a tuple, even with just one value!
        """

        expense = cursor.fetchone()
        conn.close()

        return dict(expense) if expense else None

        """
        TERNARY OPERATOR:
        "X if condition else Y" is shorthand for:

        if expense:
            return dict(expense)
        else:
            return None
        """

    except sqlite3.Error as e:
        print(f" Error getting expense by ID: {e}")
        return None


def get_expenses_by_category(category: str) -> List[Dict]:
    """
    Retrieves all expenses for a specific category.

    Args:
        category: The category to filter by

    Returns:
        List[Dict]: List of expenses in the specified category

    Example Usage:
        food_expenses = get_expenses_by_category('Food & Dining')
        total = sum(exp['amount'] for exp in food_expenses)
        print(f"Total food spending: ${total:.2f}")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM expenses
            WHERE category = ?
            ORDER BY date DESC
        ''', (category,))

        expenses = cursor.fetchall()
        conn.close()

        return [dict(expense) for expense in expenses]

    except sqlite3.Error as e:
        print(f" Error getting expenses by category: {e}")
        return []


def get_expenses_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    Retrieves expenses within a specified date range (inclusive).

    DATE RANGE QUERIES:
    BETWEEN operator includes both start_date and end_date.
    Dates should be in 'YYYY-MM-DD' format for proper comparison.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        List[Dict]: List of expenses within the date range

    Example Usage:
        # Get all expenses in October 2025
        oct_expenses = get_expenses_by_date_range('2025-10-01', '2025-10-31')
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        ''', (start_date, end_date))

        expenses = cursor.fetchall()
        conn.close()

        return [dict(expense) for expense in expenses]

    except sqlite3.Error as e:
        print(f" Error getting expenses by date range: {e}")
        return []


def get_category_totals() -> Dict[str, float]:
    """
    Calculates total spending for each category.

    SQL AGGREGATION:
    GROUP BY groups rows with the same category together.
    SUM(amount) adds up all amounts in each group.
    This is very efficient - database does the math instead of Python!

    Returns:
        Dict[str, float]: Dictionary mapping category names to total amounts
        Example: {'Food & Dining': 250.50, 'Transportation': 85.00}

    Example Usage:
        totals = get_category_totals()
        for category, amount in totals.items():
            print(f"{category}: ${amount:.2f}")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')

        """
        SQL AGGREGATE FUNCTIONS:
        - SUM(column): Adds up all values
        - COUNT(column): Counts number of rows
        - AVG(column): Calculates average
        - MAX(column): Finds maximum value
        - MIN(column): Finds minimum value

        AS keyword creates an alias (nickname) for the result column
        """

        results = cursor.fetchall()
        conn.close()

        # Convert list of rows to dictionary
        return {row['category']: row['total'] for row in results}

        """
        DICTIONARY COMPREHENSION:
        {key: value for item in list}
        This creates a dictionary from the query results.
        """

    except sqlite3.Error as e:
        print(f" Error getting category totals: {e}")
        return {}


def get_budget(category: str) -> Optional[Dict]:
    """
    Retrieves budget information for a specific category.

    Args:
        category: Category name to get budget for

    Returns:
        Optional[Dict]: Budget dictionary if exists, None otherwise

    Example Usage:
        budget = get_budget('Food & Dining')
        if budget:
            print(f"Monthly limit: ${budget['monthly_limit']}")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM budgets
            WHERE category = ?
        ''', (category,))

        budget = cursor.fetchone()
        conn.close()

        return dict(budget) if budget else None

    except sqlite3.Error as e:
        print(f" Error getting budget: {e}")
        return None


def get_all_budgets() -> List[Dict]:
    """
    Retrieves all budget records.

    Returns:
        List[Dict]: List of all budget dictionaries
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM budgets ORDER BY category')

        budgets = cursor.fetchall()
        conn.close()

        return [dict(budget) for budget in budgets]

    except sqlite3.Error as e:
        print(f" Error getting budgets: {e}")
        return []


# ============================================================================
# UPDATE OPERATIONS (Modifying Existing Data)
# ============================================================================

def update_expense(expense_id: int, date: str, category: str,
                  amount: float, description: str = "") -> bool:
    """
    Updates an existing expense record.

    WHY RETURN BOOL?
    Returning True/False lets the caller know if update succeeded.
    This is simpler than returning the updated record or raising exceptions.

    Args:
        expense_id: ID of expense to update
        date: New date value
        category: New category value
        amount: New amount value
        description: New description value

    Returns:
        bool: True if update succeeded, False otherwise

    Example Usage:
        success = update_expense(5, '2025-10-01', 'Food & Dining', 30.00, 'Dinner')
        if success:
            print("Expense updated!")
        else:
            print("Update failed - expense may not exist")
    """

    if amount <= 0:
        raise ValueError("Amount must be positive")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE expenses
            SET date = ?, category = ?, amount = ?, description = ?
            WHERE id = ?
        ''', (date, category, amount, description, expense_id))

        """
        UPDATE STATEMENT:
        - UPDATE expenses: Which table to modify
        - SET: Which columns to change and their new values
        - WHERE id = ?: Only update rows matching this condition (VERY IMPORTANT!)

        WITHOUT WHERE CLAUSE:
        If you forget WHERE, ALL rows get updated! Always include WHERE for updates/deletes.
        """

        rows_affected = cursor.rowcount

        """
        ROWCOUNT:
        Tells us how many rows were changed.
        - 0 means no rows matched (expense_id doesn't exist)
        - 1 means one row updated (success!)
        - >1 would be unexpected for ID updates (IDs should be unique)
        """

        conn.commit()
        conn.close()

        return rows_affected > 0

    except sqlite3.Error as e:
        print(f" Error updating expense: {e}")
        return False


# ============================================================================
# DELETE OPERATIONS (Removing Data)
# ============================================================================

def delete_expense(expense_id: int) -> bool:
    """
    Deletes an expense record from the database.

    DANGER WARNING:
    DELETE operations are permanent! There's no "undo" button.
    Always confirm with users before deleting data.
    Consider "soft deletes" (marking as deleted instead) for important data.

    Args:
        expense_id: ID of expense to delete

    Returns:
        bool: True if deletion succeeded, False otherwise

    Example Usage:
        if delete_expense(5):
            print("Expense deleted successfully")
        else:
            print("Delete failed - expense may not exist")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM expenses
            WHERE id = ?
        ''', (expense_id,))

        """
        DELETE STATEMENT:
        - DELETE FROM expenses: Which table to delete from
        - WHERE id = ?: Only delete rows matching this condition

        CRITICAL: Always include WHERE clause!
        "DELETE FROM expenses" without WHERE deletes EVERYTHING!
        """

        rows_affected = cursor.rowcount

        conn.commit()
        conn.close()

        return rows_affected > 0

    except sqlite3.Error as e:
        print(f" Error deleting expense: {e}")
        return False


def delete_budget(category: str) -> bool:
    """
    Deletes a budget for a specific category.

    Args:
        category: Category to remove budget for

    Returns:
        bool: True if deletion succeeded, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM budgets
            WHERE category = ?
        ''', (category,))

        rows_affected = cursor.rowcount

        conn.commit()
        conn.close()

        return rows_affected > 0

    except sqlite3.Error as e:
        print(f" Error deleting budget: {e}")
        return False


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_database_stats() -> Dict[str, int]:
    """
    Returns statistics about the database contents.

    UTILITY FUNCTIONS:
    These are helpful functions that provide useful information
    but aren't core CRUD operations. Good for debugging and dashboards!

    Returns:
        Dict[str, int]: Dictionary containing:
            - total_expenses: Number of expense records
            - total_budgets: Number of budget records
            - earliest_date: Earliest expense date
            - latest_date: Latest expense date

    Example Usage:
        stats = get_database_stats()
        print(f"Database contains {stats['total_expenses']} expenses")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Count expenses
        cursor.execute('SELECT COUNT(*) as count FROM expenses')
        expense_count = cursor.fetchone()['count']

        # Count budgets
        cursor.execute('SELECT COUNT(*) as count FROM budgets')
        budget_count = cursor.fetchone()['count']

        # Get date range
        cursor.execute('SELECT MIN(date) as earliest, MAX(date) as latest FROM expenses')
        date_range = cursor.fetchone()

        conn.close()

        return {
            'total_expenses': expense_count,
            'total_budgets': budget_count,
            'earliest_date': date_range['earliest'],
            'latest_date': date_range['latest']
        }

    except sqlite3.Error as e:
        print(f" Error getting database stats: {e}")
        return {
            'total_expenses': 0,
            'total_budgets': 0,
            'earliest_date': None,
            'latest_date': None
        }


# ============================================================================
# INCOME MANAGEMENT FUNCTIONS
# ============================================================================

def add_income(date: str, source: str, amount: float, description: str = '') -> int:
    """
    Adds a new income record to the database.

    WHAT IS INCOME TRACKING?
    Just like we track expenses, we should track money coming IN.
    This helps calculate net worth, savings rate, and overall financial health.

    Args:
        date: Date income was received (YYYY-MM-DD format)
        source: Where money came from (Salary, Freelance, Gift, Investment, etc.)
        amount: Amount received (positive decimal number)
        description: Optional notes about the income

    Returns:
        int: The ID of the newly created income record

    Raises:
        ValueError: If validation fails

    Example:
        income_id = add_income('2025-10-01', 'Salary', 5000.00, 'October paycheck')
        # Returns: 1 (or next available ID)

    JUNIOR DEV NOTES:
    - Similar to add_expense(), but for income instead
    - Income amount should always be positive
    - Common sources: Salary, Freelance, Business, Investment, Gift, Refund
    """
    # Validate input data
    """
    INPUT VALIDATION EXPLAINED:
    We validate BEFORE touching the database to prevent bad data.
    This is called "defensive programming" - assume all input is malicious.
    """

    if not date:
        raise ValueError("Date is required")
        # Empty string, None, or missing - reject it

    if not source:
        raise ValueError("Source is required")
        # Source tells us where money came from (Salary, Freelance, etc.)

    if amount <= 0:
        raise ValueError("Amount must be positive")
        # Can't have negative or zero income - doesn't make sense!

    if len(description) > 500:
        raise ValueError("Description too long. Maximum 500 characters.")
        # Prevent database bloat and potential attacks (e.g., storing 1GB of text)

    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
        # strptime: "string parse time" - converts string to datetime
        # If format wrong, raises ValueError
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
        # Re-raise with clearer message for user

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO income (date, source, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, source, amount, description))

        conn.commit()
        income_id = cursor.lastrowid  # Get the ID of the record we just inserted
        conn.close()

        return income_id

    except sqlite3.Error as e:
        print(f"Error adding income: {e}")
        raise


def get_all_income() -> List[Dict]:
    """
    Retrieves all income records from the database.

    Returns:
        List of dictionaries, each containing an income record
        Sorted by date (newest first)

    Example Return Value:
        [
            {'id': 2, 'date': '2025-10-01', 'source': 'Salary', 'amount': 5000.00, ...},
            {'id': 1, 'date': '2025-09-15', 'source': 'Freelance', 'amount': 1500.00, ...}
        ]
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM income ORDER BY date DESC, id DESC')
        income_records = cursor.fetchall()
        conn.close()

        # Convert Row objects to dictionaries
        return [dict(record) for record in income_records]

    except sqlite3.Error as e:
        print(f"Error fetching income: {e}")
        return []


def get_income_by_id(income_id: int) -> Optional[Dict]:
    """
    Retrieves a single income record by its ID.

    Args:
        income_id: The ID of the income record to fetch

    Returns:
        Dictionary containing income data, or None if not found

    Example:
        income = get_income_by_id(5)
        if income:
            print(f"Income: ${income['amount']} from {income['source']}")
        else:
            print("Income not found")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM income WHERE id = ?', (income_id,))
        income_record = cursor.fetchone()
        conn.close()

        return dict(income_record) if income_record else None

    except sqlite3.Error as e:
        print(f"Error fetching income: {e}")
        return None


def update_income(income_id: int, date: str, source: str, amount: float, description: str) -> bool:
    """
    Updates an existing income record.

    Args:
        income_id: ID of income record to update
        date: New date
        source: New source
        amount: New amount
        description: New description

    Returns:
        True if update successful, False otherwise

    Raises:
        ValueError: If validation fails
    """
    # Validate input data (same as add_income)
    """
    WHY VALIDATE ON UPDATE?
    User might bypass frontend validation by editing HTTP requests.
    Always validate on backend - never trust client input!
    """

    if not date:
        raise ValueError("Date is required")

    if not source:
        raise ValueError("Source is required")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    if len(description) > 500:
        raise ValueError("Description too long. Maximum 500 characters.")

    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE income
            SET date = ?, source = ?, amount = ?, description = ?
            WHERE id = ?
        ''', (date, source, amount, description, income_id))

        """
        UPDATE QUERY EXPLAINED:
        - UPDATE income: Which table to modify
        - SET ...: Which columns to change and their new values
        - WHERE id = ?: CRITICAL! Only update this specific record
        - Without WHERE: Would update ALL records (disaster!)
        - ? placeholders: Prevent SQL injection attacks
        """

        conn.commit()
        success = cursor.rowcount > 0  # rowcount tells us how many rows were affected
        conn.close()

        return success

    except sqlite3.Error as e:
        print(f"Error updating income: {e}")
        return False


def delete_income(income_id: int) -> bool:
    """
    Deletes an income record from the database.

    Args:
        income_id: ID of income record to delete

    Returns:
        True if deletion successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM income WHERE id = ?', (income_id,))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        return success

    except sqlite3.Error as e:
        print(f"Error deleting income: {e}")
        return False


def get_income_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    Retrieves income records within a specific date range.

    Args:
        start_date: Start of date range (YYYY-MM-DD)
        end_date: End of date range (YYYY-MM-DD)

    Returns:
        List of income dictionaries within the date range
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM income
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        ''', (start_date, end_date))

        income_records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in income_records]

    except sqlite3.Error as e:
        print(f"Error fetching income by date range: {e}")
        return []


def get_total_income(start_date: str = None, end_date: str = None) -> float:
    """
    Calculates total income, optionally within a date range.

    Args:
        start_date: Optional start date (YYYY-MM-DD)
        end_date: Optional end date (YYYY-MM-DD)

    Returns:
        Total income amount

    Example:
        # Get all-time income
        total = get_total_income()

        # Get October 2025 income
        total = get_total_income('2025-10-01', '2025-10-31')

    JUNIOR DEV NOTES:
    - SUM() is a SQL aggregate function that adds up all values
    - COALESCE() returns the first non-NULL value (handles case where no income exists)
    - If start_date/end_date not provided, calculates total for all time
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if start_date and end_date:
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) as total
                FROM income
                WHERE date BETWEEN ? AND ?
            ''', (start_date, end_date))
        else:
            cursor.execute('SELECT COALESCE(SUM(amount), 0) as total FROM income')

        result = cursor.fetchone()
        conn.close()

        return float(result['total'])

    except sqlite3.Error as e:
        print(f"Error calculating total income: {e}")
        return 0.0


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    """
    This code only runs if you execute this file directly (python database.py).
    It won't run when this file is imported as a module in other files.

    TESTING YOUR DATABASE:
    Run this file directly to initialize the database and test basic operations.
    """

    print("Initializing database...")
    init_db()

    print("\nDatabase statistics:")
    stats = get_database_stats()
    for key, value in stats.items():
        print(f"  - {key}: {value}")

    print("\nDatabase module ready to use!")
    print(f"Database file: {DATABASE_NAME}")

    """
    TO TEST THIS FILE:
    1. Open terminal in project folder
    2. Run: python database.py
    3. You should see the success messages above
    4. Check that finance.db file was created
    """
