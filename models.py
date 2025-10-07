"""
MODELS.PY - Data Models and Business Logic
===========================================

PURPOSE:
This file defines the data structures (models) and business logic for our application.
It acts as a bridge between the raw database operations and the web application.

WHAT ARE MODELS?
Models represent the "things" in our application (Expenses, Budgets, etc.).
They define what data each "thing" has and what operations you can perform on them.

WHY SEPARATE MODELS FROM DATABASE?
- Abstraction: Application code doesn't need to know database details
- Validation: Ensure data is valid before it reaches the database
- Business Logic: Calculations and rules live here, not in database or web code
- Testing: Easier to test business rules in isolation

MODEL vs DATABASE:
- Database (database.py): How to store/retrieve data
- Models (this file): What the data means and how to work with it
- Application (app.py): How to present data to users

JUNIOR DEVELOPER NOTES:
This is an example of the "Model" in MVC (Model-View-Controller) architecture:
- Model (models.py): Data and business logic
- View (templates/*.html): How data is displayed
- Controller (app.py): Coordinates between models and views
"""

# ============================================================================
# IMPORTS
# ============================================================================

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

"""
IMPORT EXPLANATIONS:
- datetime, timedelta: Date/time handling
- typing: Type hints for better code documentation
- dataclasses: Decorator that auto-generates boilerplate code for classes
- enum: Creates named constants (more about this below)
"""

# ============================================================================
# ENUMS - Named Constants
# ============================================================================

class ExpenseCategory(Enum):
    """
    Defines all valid expense categories.

    WHAT IS AN ENUM?
    Enum (Enumeration) creates a set of named constants.
    Instead of using strings like 'Food & Dining' everywhere,
    we use ExpenseCategory.FOOD_DINING which is safer and prevents typos.

    WHY USE ENUMS?
    1. Prevents typos: ExpenseCategory.FOOD will error, 'Fodd' won't
    2. Autocomplete: Your IDE can suggest valid categories
    3. Single source of truth: Change category name in one place
    4. Type checking: Can't accidentally pass a number where category expected

    USAGE EXAMPLE:
        category = ExpenseCategory.FOOD_DINING
        print(category.value)  # Outputs: 'Food & Dining'
        print(category.color)  # Outputs: '#FF6B6B'
    """

    # Format: NAME = (display_value, color_code)
    FOOD_DINING = ('Food & Dining', '#FF6B6B')
    TRANSPORTATION = ('Transportation', '#4ECDC4')
    SHOPPING = ('Shopping', '#45B7D1')
    ENTERTAINMENT = ('Entertainment', '#FFA07A')
    BILLS_UTILITIES = ('Bills & Utilities', '#98D8C8')
    HEALTHCARE = ('Healthcare', '#F7DC6F')
    OTHER = ('Other', '#BDC3C7')

    """
    COLOR CODES:
    These are hexadecimal color codes (RGB format).
    Format: #RRGGBB where RR=Red, GG=Green, BB=Blue
    Example: #FF6B6B = High red, medium green/blue = reddish/coral color
    """

    def __init__(self, display_name: str, color: str):
        """
        Initializes each enum member with its display name and color.

        This runs automatically when enum is created.
        You don't call this directly.
        """
        self.display_name = display_name
        self.color = color

    @classmethod
    def get_all_categories(cls) -> List[Tuple[str, str]]:
        """
        Returns all categories as (name, color) tuples.

        @classmethod EXPLAINED:
        A class method is called on the class itself, not an instance.
        ExpenseCategory.get_all_categories() not expense.get_all_categories()

        Returns:
            List of (display_name, color) tuples

        Example Usage:
            categories = ExpenseCategory.get_all_categories()
            # [('Food & Dining', '#FF6B6B'), ('Transportation', '#4ECDC4'), ...]
        """
        return [(cat.display_name, cat.color) for cat in cls]

    @classmethod
    def get_by_name(cls, name: str) -> Optional['ExpenseCategory']:
        """
        Finds a category by its display name.

        Args:
            name: Display name like 'Food & Dining'

        Returns:
            ExpenseCategory member if found, None otherwise

        Example Usage:
            cat = ExpenseCategory.get_by_name('Food & Dining')
            if cat:
                print(f"Color: {cat.color}")
        """
        for category in cls:
            if category.display_name == name:
                return category
        return None

    @classmethod
    def get_category_dict(cls) -> Dict[str, str]:
        """
        Returns a dictionary mapping category names to colors.

        Returns:
            Dict mapping display names to color codes

        Example Usage:
            colors = ExpenseCategory.get_category_dict()
            food_color = colors['Food & Dining']  # '#FF6B6B'
        """
        return {cat.display_name: cat.color for cat in cls}


class IncomeSource(Enum):
    """
    Defines all valid income sources.

    INCOME SOURCES:
    Just like we categorize expenses, we categorize income by source.
    This helps analyze where money comes from and plan for the future.

    Each source has:
    - Name (programming reference)
    - Display name (what users see)
    - Color (for charts and visual displays)
    """
    SALARY = ('Salary', '#10B981')          # Green - steady income
    FREELANCE = ('Freelance', '#3B82F6')    # Blue - project-based
    BUSINESS = ('Business', '#8B5CF6')      # Purple - entrepreneurship
    INVESTMENT = ('Investment', '#F59E0B')  # Orange - passive income
    GIFT = ('Gift', '#EC4899')              # Pink - one-time gifts
    REFUND = ('Refund', '#6366F1')          # Indigo - money back
    BONUS = ('Bonus', '#14B8A6')            # Teal - extra compensation
    OTHER = ('Other', '#94A3B8')            # Gray - miscellaneous

    """
    WHY THESE SOURCES?
    - Salary: Most common - regular paycheck from employer
    - Freelance: Contract work, side gigs, 1099 income
    - Business: Self-employed income, business revenue
    - Investment: Dividends, interest, capital gains
    - Gift: Birthday money, wedding gifts, etc.
    - Refund: Tax refunds, purchase returns
    - Bonus: Work bonuses, performance pay
    - Other: Catch-all for unusual income

    COLOR CHOICES:
    - Green for salary (reliable, steady)
    - Blue for freelance (professional)
    - Purple for business (entrepreneurial)
    - Orange for investment (growth-oriented)
    - Pink for gifts (celebratory)
    """

    def __init__(self, display_name: str, color: str):
        """Initializes each enum member with display name and color."""
        self.display_name = display_name
        self.color = color

    @classmethod
    def get_all_sources(cls) -> List[Tuple[str, str]]:
        """
        Returns all income sources as (name, color) tuples.

        Returns:
            List of (display_name, color) tuples

        Example:
            sources = IncomeSource.get_all_sources()
            # [('Salary', '#10B981'), ('Freelance', '#3B82F6'), ...]
        """
        return [(source.display_name, source.color) for source in cls]

    @classmethod
    def get_by_name(cls, name: str) -> Optional['IncomeSource']:
        """
        Finds an income source by its display name.

        Args:
            name: Display name to search for

        Returns:
            IncomeSource enum member, or None if not found
        """
        for source in cls:
            if source.display_name == name:
                return source
        return None

    @classmethod
    def get_source_dict(cls) -> Dict[str, str]:
        """
        Returns dictionary mapping source names to colors.

        Returns:
            Dictionary: {source_name: color}

        Example:
            colors = IncomeSource.get_source_dict()
            salary_color = colors['Salary']  # '#10B981'
        """
        return {source.display_name: source.color for source in cls}


# ============================================================================
# DATA CLASSES - Structured Data
# ============================================================================

@dataclass
class Expense:
    """
    Represents a single expense record.

    WHAT IS @dataclass?
    A decorator that automatically creates __init__, __repr__, and other methods.
    Without @dataclass, we'd need to write all this boilerplate manually:

    class Expense:
        def __init__(self, id, date, category, amount, description, created_at):
            self.id = id
            self.date = date
            # ... etc

    With @dataclass, Python generates this code for us!

    ATTRIBUTES:
    - id: Unique identifier (None for new expenses not yet in database)
    - date: When expense occurred
    - category: Type of expense
    - amount: How much was spent
    - description: Optional notes
    - created_at: When record was created (None for new expenses)

    TYPE HINTS:
    The format "name: type" tells developers (and tools) what type each field should be.
    Optional[int] means "can be an integer or None"
    """

    id: Optional[int] = None
    date: str = ""
    category: str = ""
    amount: float = 0.0
    description: str = ""
    created_at: Optional[str] = None

    """
    DEFAULT VALUES:
    The = after the type hint provides a default value.
    This allows: expense = Expense() without passing any arguments.
    """

    def __post_init__(self):
        """
        Called automatically after __init__ by @dataclass.

        Use this for validation and data transformation after object is created.
        """
        # Validate amount is positive
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

        # If date not provided, use today
        if not self.date:
            self.date = datetime.now().strftime('%Y-%m-%d')

        """
        STRFTIME FORMAT CODES:
        %Y = 4-digit year (2025)
        %m = 2-digit month (10)
        %d = 2-digit day (01)
        Result: '2025-10-01'
        """

    def to_dict(self) -> Dict:
        """
        Converts the Expense object to a dictionary.

        WHY CONVERT TO DICT?
        - JSON serialization: Dictionaries easily convert to JSON for web APIs
        - Database operations: Our database functions expect dictionaries
        - Template rendering: Jinja2 templates work well with dictionaries

        Returns:
            Dictionary representation of the expense

        Example Usage:
            expense = Expense(id=1, date='2025-10-01', category='Food', amount=25.50)
            data = expense.to_dict()
            # {'id': 1, 'date': '2025-10-01', 'category': 'Food', ...}
        """
        return {
            'id': self.id,
            'date': self.date,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        """
        Creates an Expense object from a dictionary.

        This is the reverse of to_dict() - useful for creating objects
        from database results or JSON data.

        Args:
            data: Dictionary containing expense data

        Returns:
            New Expense object

        Example Usage:
            data = {'id': 1, 'date': '2025-10-01', 'category': 'Food', 'amount': 25.50}
            expense = Expense.from_dict(data)
            print(expense.amount)  # 25.50
        """
        return cls(
            id=data.get('id'),
            date=data.get('date', ''),
            category=data.get('category', ''),
            amount=data.get('amount', 0.0),
            description=data.get('description', ''),
            created_at=data.get('created_at')
        )

        """
        .get() METHOD:
        dict.get('key', default) returns the value if key exists, otherwise returns default.
        This prevents KeyError if a key is missing.

        data['date'] - Crashes if 'date' key doesn't exist
        data.get('date', '') - Returns empty string if 'date' key doesn't exist
        """

    def get_category_color(self) -> str:
        """
        Returns the color code for this expense's category.

        Returns:
            Hexadecimal color code (e.g., '#FF6B6B')

        Example Usage:
            expense = Expense(category='Food & Dining', amount=25.50)
            color = expense.get_category_color()  # '#FF6B6B'
        """
        category_enum = ExpenseCategory.get_by_name(self.category)
        return category_enum.color if category_enum else '#BDC3C7'  # Default to gray

    def formatted_amount(self) -> str:
        """
        Returns amount formatted as currency string.

        Returns:
            Amount formatted as $X.XX

        Example Usage:
            expense = Expense(amount=25.5)
            print(expense.formatted_amount())  # '$25.50'
        """
        return f"${self.amount:.2f}"

        """
        F-STRING FORMATTING:
        {self.amount:.2f}
        - .2f means "format as float with 2 decimal places"
        - 25.5 becomes '25.50'
        - 25.999 becomes '26.00' (rounds)
        """

    def is_recent(self, days: int = 7) -> bool:
        """
        Checks if expense is within the last N days.

        Args:
            days: Number of days to check (default 7)

        Returns:
            True if expense is within the last N days

        Example Usage:
            expense = Expense(date='2025-10-01', amount=25.50)
            if expense.is_recent(7):
                print("This is a recent expense")
        """
        try:
            expense_date = datetime.strptime(self.date, '%Y-%m-%d')
            days_ago = datetime.now() - timedelta(days=days)
            return expense_date >= days_ago

            """
            STRPTIME vs STRFTIME:
            - strptime: Parse string TO datetime object ('2025-10-01'  datetime)
            - strftime: Format datetime TO string (datetime  '2025-10-01')
            Think: p = parse, f = format

            TIMEDELTA:
            Represents a duration. timedelta(days=7) = 7 days
            We can subtract timedelta from datetime to go back in time
            """

        except ValueError:
            # If date format is invalid, consider it not recent
            return False


@dataclass
class Budget:
    """
    Represents a budget limit for a category.

    ATTRIBUTES:
    - id: Unique identifier
    - category: Which expense category this budget applies to
    - monthly_limit: Maximum allowed spending per month
    - created_at: When budget was created
    """

    id: Optional[int] = None
    category: str = ""
    monthly_limit: float = 0.0
    created_at: Optional[str] = None

    def __post_init__(self):
        """Validates budget data after initialization."""
        if self.monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than 0")

        if self.monthly_limit >= 10000000:  # Sanity check for very large budgets
            raise ValueError("Budget limit seems unreasonably large (>= $10,000,000). Please verify.")

    def to_dict(self) -> Dict:
        """Converts Budget object to dictionary."""
        return {
            'id': self.id,
            'category': self.category,
            'monthly_limit': self.monthly_limit,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Budget':
        """Creates Budget object from dictionary."""
        return cls(
            id=data.get('id'),
            category=data.get('category', ''),
            monthly_limit=data.get('monthly_limit', 0.0),
            created_at=data.get('created_at')
        )

    def formatted_limit(self) -> str:
        """Returns monthly limit formatted as currency."""
        return f"${self.monthly_limit:.2f}"


@dataclass
class Income:
    """
    Represents a single income record.

    WHAT IS INCOME?
    Income is money you receive (as opposed to expenses, which is money you spend).
    Tracking income helps you understand:
    - Total earnings
    - Income sources (where money comes from)
    - Income stability and trends
    - Savings rate (income - expenses)

    ATTRIBUTES:
    - id: Unique identifier for this income record
    - date: When income was received (YYYY-MM-DD format)
    - source: Where money came from (Salary, Freelance, etc.)
    - amount: How much was received (always positive)
    - description: Optional notes (e.g., "October paycheck")
    - created_at: When record was added to database

    Example:
        income = Income(
            id=1,
            date='2025-10-01',
            source='Salary',
            amount=5000.00,
            description='October paycheck'
        )
    """

    id: Optional[int] = None
    date: str = ""
    source: str = ""
    amount: float = 0.0
    description: str = ""
    created_at: Optional[str] = None

    def __post_init__(self):
        """
        Validates income data after initialization.

        POST_INIT:
        This special method runs automatically after __init__().
        Perfect place for validation logic!

        VALIDATION CHECKS:
        1. Amount must be positive (can't have negative income)
        2. Date defaults to today if not provided (consistent with Expense)
        3. Source must be valid
        """
        if self.amount < 0:
            raise ValueError("Income amount cannot be negative")

        # If date not provided, use today (consistent with Expense class)
        if not self.date:
            self.date = datetime.now().strftime('%Y-%m-%d')

        if not self.source:
            raise ValueError("Source is required")

    def to_dict(self) -> Dict:
        """
        Converts Income object to dictionary.

        WHY THIS IS USEFUL:
        - Easier to serialize (convert to JSON)
        - Compatible with database operations
        - Can be passed to templates

        Returns:
            Dictionary containing all income data
        """
        return {
            'id': self.id,
            'date': self.date,
            'source': self.source,
            'amount': self.amount,
            'description': self.description,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Income':
        """
        Creates Income object from dictionary.

        WHY CLASSMETHOD?
        @classmethod means this method belongs to the class, not an instance.
        Call it like: Income.from_dict(data)
        Not like: income_instance.from_dict(data)

        Args:
            data: Dictionary with income data (usually from database)

        Returns:
            New Income object

        Example:
            data = {'id': 1, 'date': '2025-10-01', 'source': 'Salary', ...}
            income = Income.from_dict(data)
        """
        return cls(
            id=data.get('id'),
            date=data.get('date', ''),
            source=data.get('source', ''),
            amount=data.get('amount', 0.0),
            description=data.get('description', ''),
            created_at=data.get('created_at')
        )

    def formatted_amount(self) -> str:
        """
        Returns amount formatted as currency.

        Returns:
            String like '$5,000.00'

        Example:
            income = Income(amount=5000.50)
            print(income.formatted_amount())  # '$5,000.50'
        """
        return f"${self.amount:,.2f}"

    def get_source_color(self) -> str:
        """
        Returns the color associated with this income source.

        Returns:
            Hex color code (e.g., '#10B981')

        Example:
            income = Income(source='Salary')
            color = income.get_source_color()  # '#10B981' (green)

        JUNIOR DEV NOTE:
        We look up the source in our IncomeSource enum to get its color.
        If source isn't found (maybe it's old data), we return gray as default.
        """
        source_enum = IncomeSource.get_by_name(self.source)
        return source_enum.color if source_enum else '#94A3B8'  # Default gray

    def get_month_year(self) -> str:
        """
        Extracts month and year from date.

        Returns:
            String like '2025-10' for grouping by month

        Example:
            income = Income(date='2025-10-15')
            month = income.get_month_year()  # '2025-10'

        WHY THIS IS USEFUL:
        When we want to see total income per month, we group by month-year.
        This method extracts that from the full date.
        """
        return self.date[:7] if self.date else ""  # Takes 'YYYY-MM' from 'YYYY-MM-DD'


# ============================================================================
# BUSINESS LOGIC - Calculations and Analysis
# ============================================================================

class ExpenseAnalyzer:
    """
    Provides analysis and calculation methods for expenses.

    WHY A SEPARATE CLASS?
    Business logic (calculations, analysis) should be separate from data models.
    This keeps models simple and makes logic reusable and testable.

    STATIC METHODS:
    Methods that don't need access to instance data (self).
    Called on the class itself: ExpenseAnalyzer.calculate_total(expenses)
    """

    @staticmethod
    def calculate_total(expenses: List[Expense]) -> float:
        """
        Calculates total amount from a list of expenses.

        Args:
            expenses: List of Expense objects

        Returns:
            Total amount spent

        Example Usage:
            expenses = [Expense(amount=25.50), Expense(amount=30.00)]
            total = ExpenseAnalyzer.calculate_total(expenses)  # 55.50
        """
        return sum(expense.amount for expense in expenses)

        """
        GENERATOR EXPRESSION:
        (expense.amount for expense in expenses)
        Similar to list comprehension but uses () instead of []
        More memory efficient for large datasets
        """

    @staticmethod
    def calculate_average(expenses: List[Expense]) -> float:
        """
        Calculates average expense amount.

        Args:
            expenses: List of Expense objects

        Returns:
            Average amount, or 0 if no expenses

        Example Usage:
            expenses = [Expense(amount=20), Expense(amount=30), Expense(amount=40)]
            avg = ExpenseAnalyzer.calculate_average(expenses)  # 30.0
        """
        if not expenses:
            return 0.0

        """
        GUARD CLAUSE:
        Check for empty list first to prevent division by zero.
        This is called a "guard clause" - handles edge case early.
        """

        total = ExpenseAnalyzer.calculate_total(expenses)
        return total / len(expenses)

    @staticmethod
    def group_by_category(expenses: List[Expense]) -> Dict[str, List[Expense]]:
        """
        Groups expenses by category.

        Args:
            expenses: List of Expense objects

        Returns:
            Dictionary mapping category names to lists of expenses

        Example Usage:
            expenses = [Expense(category='Food', amount=25), Expense(category='Food', amount=30)]
            grouped = ExpenseAnalyzer.group_by_category(expenses)
            # {'Food': [Expense(amount=25), Expense(amount=30)], ...}
        """
        grouped = {}

        for expense in expenses:
            if expense.category not in grouped:
                grouped[expense.category] = []
            grouped[expense.category].append(expense)

        return grouped

        """
        ALTERNATIVE USING defaultdict:
        from collections import defaultdict
        grouped = defaultdict(list)
        for expense in expenses:
            grouped[expense.category].append(expense)
        return dict(grouped)

        defaultdict automatically creates empty list if key doesn't exist.
        """

    @staticmethod
    def get_category_totals(expenses: List[Expense]) -> Dict[str, float]:
        """
        Calculates total spending per category.

        Args:
            expenses: List of Expense objects

        Returns:
            Dictionary mapping category names to total amounts

        Example Usage:
            expenses = [Expense(category='Food', amount=25), Expense(category='Food', amount=30)]
            totals = ExpenseAnalyzer.get_category_totals(expenses)
            # {'Food': 55.0, ...}
        """
        totals = {}

        for expense in expenses:
            if expense.category in totals:
                totals[expense.category] += expense.amount
            else:
                totals[expense.category] = expense.amount

        return totals

    @staticmethod
    def get_monthly_total(expenses: List[Expense], year: int, month: int) -> float:
        """
        Calculates total spending for a specific month.

        Args:
            expenses: List of Expense objects
            year: Year (e.g., 2025)
            month: Month number (1-12)

        Returns:
            Total amount spent in that month

        Example Usage:
            total = ExpenseAnalyzer.get_monthly_total(expenses, 2025, 10)
            print(f"October 2025 spending: ${total:.2f}")
        """
        # Filter expenses for specified month
        monthly_expenses = [
            exp for exp in expenses
            if exp.date.startswith(f"{year}-{month:02d}")
        ]

        """
        LIST COMPREHENSION WITH CONDITION:
        [item for item in list if condition]
        Only includes items where condition is True

        STRING FORMATTING:
        {month:02d} formats month as 2-digit number with leading zero
        1 becomes '01', 12 stays '12'
        """

        return ExpenseAnalyzer.calculate_total(monthly_expenses)

    @staticmethod
    def get_budget_status(expenses: List[Expense], budgets: List[Budget],
                          year: int, month: int) -> Dict[str, Dict]:
        """
        Compares actual spending to budgets for a specific month.

        This is complex business logic that combines data from multiple sources
        to provide useful information for the user.

        Args:
            expenses: List of all expenses
            budgets: List of all budgets
            year: Year to check
            month: Month to check (1-12)

        Returns:
            Dictionary mapping categories to status info:
            {
                'Food & Dining': {
                    'budget': 500.0,
                    'spent': 350.0,
                    'remaining': 150.0,
                    'percentage': 70.0,
                    'over_budget': False
                },
                ...
            }

        Example Usage:
            status = ExpenseAnalyzer.get_budget_status(expenses, budgets, 2025, 10)
            for category, info in status.items():
                print(f"{category}: {info['percentage']:.1f}% used")
        """
        result = {}

        # Filter expenses for the specified month
        month_expenses = [
            exp for exp in expenses
            if exp.date.startswith(f"{year}-{month:02d}")
        ]

        # Group expenses by category
        category_totals = ExpenseAnalyzer.get_category_totals(month_expenses)

        # Calculate status for each budget
        for budget in budgets:
            category = budget.category
            spent = category_totals.get(category, 0.0)
            remaining = budget.monthly_limit - spent
            percentage = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0

            """
            TERNARY OPERATOR FOR SAFE DIVISION:
            (spent / budget * 100) if budget > 0 else 0

            Prevents division by zero error if budget is 0.
            If budget is 0, percentage is set to 0.
            """

            result[category] = {
                'budget': budget.monthly_limit,
                'spent': spent,
                'remaining': remaining,
                'percentage': round(percentage, 1),  # Round to 1 decimal place
                'over_budget': spent > budget.monthly_limit
            }

        return result

    @staticmethod
    def get_spending_trend(expenses: List[Expense], months: int = 6) -> Dict[str, float]:
        """
        Calculates spending trend over the last N months.

        Args:
            expenses: List of Expense objects
            months: Number of months to analyze (default 6)

        Returns:
            Dictionary mapping month strings (YYYY-MM) to total amounts

        Example Usage:
            trend = ExpenseAnalyzer.get_spending_trend(expenses, months=3)
            # {'2025-08': 450.00, '2025-09': 525.00, '2025-10': 480.00}
        """
        trend = {}

        # Calculate date range using proper month arithmetic
        end_date = datetime.now()

        # Calculate start date by going back N months
        # Handle year/month boundaries correctly
        start_year = end_date.year
        start_month = end_date.month - months

        # Adjust for negative months (go back to previous year)
        while start_month <= 0:
            start_month += 12
            start_year -= 1

        start_date = end_date.replace(year=start_year, month=start_month)

        """
        PROPER MONTH CALCULATION:
        Instead of approximating with 30 days, we calculate exact months.
        This handles varying month lengths (28-31 days) and year boundaries correctly.
        Example: 6 months back from Oct 2025 = Apr 2025 (not ~180 days back)
        """

        for expense in expenses:
            try:
                expense_date = datetime.strptime(expense.date, '%Y-%m-%d')

                # Check if expense is within date range
                if start_date <= expense_date <= end_date:
                    # Get year-month string (e.g., '2025-10')
                    month_key = expense_date.strftime('%Y-%m')

                    if month_key in trend:
                        trend[month_key] += expense.amount
                    else:
                        trend[month_key] = expense.amount

            except ValueError:
                # Skip expenses with invalid dates
                continue

        # Sort by month (oldest to newest)
        return dict(sorted(trend.items()))

        """
        SORTING DICTIONARIES:
        dict.items() returns [(key1, value1), (key2, value2), ...]
        sorted() sorts these tuples by key (month string)
        dict() converts back to dictionary
        """


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_expense_data(date: str, category: str, amount: float,
                         description: str = "") -> Tuple[bool, str]:
    """
    Validates expense data before saving to database.

    VALIDATION IS CRITICAL:
    Never trust user input! Always validate data before storing in database.
    This prevents data corruption and security issues.

    Args:
        date: Date string to validate
        category: Category name to validate
        amount: Amount to validate
        description: Description to validate (optional)

    Returns:
        Tuple of (is_valid, error_message)
        - (True, "") if valid
        - (False, "error message") if invalid

    Example Usage:
        valid, error = validate_expense_data('2025-10-01', 'Food', 25.50)
        if valid:
            save_to_database()
        else:
            show_error_to_user(error)
    """

    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD (e.g., 2025-10-01)"

    # Validate category
    valid_categories = [cat.display_name for cat in ExpenseCategory]
    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"

    # Validate amount
    if amount <= 0:
        return False, "Amount must be greater than 0"

    if amount >= 10000000:  # Sanity check for very large amounts (>= to reject 10M and above)
        return False, "Amount seems unreasonably large (>= $10,000,000). Please verify."

    # Validate description length
    if len(description) > 500:
        return False, "Description too long. Maximum 500 characters."

    # All validations passed
    return True, ""

    """
    VALIDATION BEST PRACTICES:
    1. Check format (date, email, etc.)
    2. Check range (amount > 0, length < max)
    3. Check against allowed values (category in list)
    4. Return clear error messages that help user fix the problem
    5. Validate on both frontend (quick feedback) and backend (security)
    """


def format_currency(amount: float) -> str:
    """
    Formats a number as currency string.

    Args:
        amount: Number to format

    Returns:
        Formatted currency string

    Example Usage:
        formatted = format_currency(1234.5)  # '$1,234.50'
    """
    return f"${amount:,.2f}"

    """
    FORMATTING FLAGS:
    {amount:,.2f}
    - : starts format specification
    - , adds thousand separators (1234 becomes 1,234)
    - .2f formats as float with 2 decimal places
    """


def validate_income_data(date: str, source: str, amount: float,
                         description: str = "") -> Tuple[bool, str]:
    """
    Validates income data before saving to database.

    WHY VALIDATE INCOME DATA?
    Just like expenses, income data needs validation to ensure data quality.
    This prevents bad data from corrupting our financial records.

    VALIDATION RULES:
    1. Date must be in YYYY-MM-DD format (ISO 8601 standard)
    2. Source must be from the valid IncomeSource enum
    3. Amount must be positive and less than $10 million (sanity check)
    4. Description must be 500 characters or less

    Args:
        date: Date string to validate (YYYY-MM-DD format)
        source: Income source to validate (must match IncomeSource enum)
        amount: Amount to validate (must be positive)
        description: Description to validate (optional, max 500 chars)

    Returns:
        Tuple of (is_valid, error_message)
        - (True, "") if all validations pass
        - (False, "error message") if any validation fails

    Example Usage:
        valid, error = validate_income_data('2025-10-01', 'Salary', 5000.00)
        if valid:
            save_to_database()
        else:
            show_error_to_user(error)

    JUNIOR DEV NOTES:
    - Always validate on both frontend (UX) and backend (security)
    - Return clear, actionable error messages
    - Use tuple return (bool, str) pattern for validation functions
    - Keep validation logic separate from business logic
    """
    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
        # strptime = "string parse time" - converts string to datetime object
        # If parsing fails, raises ValueError
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD (e.g., 2025-10-01)"
        # Return tuple: (False, error_message) to indicate validation failed

    # Validate source is not empty
    if not source:
        return False, "Source is required"
        # Check for empty string before validating against enum

    # Validate source against enum
    valid_sources = [source.display_name for source in IncomeSource]
    # List comprehension: Extract display_name from each enum member
    # Result: ['Salary', 'Freelance', 'Business', 'Investment', 'Gift', 'Refund', 'Bonus', 'Other']

    if source not in valid_sources:
        return False, f"Invalid source. Must be one of: {', '.join(valid_sources)}"
        # f-string: Inserts list of valid sources into error message
        # ', '.join(): Converts list to comma-separated string

    # Validate amount (positive and reasonable)
    if amount <= 0:
        return False, "Amount must be greater than 0"
        # Negative or zero income doesn't make sense

    if amount >= 10000000:  # Sanity check for very large income
        return False, "Amount seems unreasonably large (>= $10,000,000). Please verify."
        # Prevents typos (e.g., $100,000,000 instead of $10,000)
        # Note: >= means 10M and above are rejected

    # Validate description length
    if len(description) > 500:
        return False, "Description too long. Maximum 500 characters."
        # Prevents database bloat and potential DoS attacks

    # All validations passed
    return True, ""
    # Return (True, "") indicates success with no error message


def get_date_range_description(start_date: str, end_date: str) -> str:
    """
    Returns a human-readable description of a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        Human-readable description

    Example Usage:
        desc = get_date_range_description('2025-10-01', '2025-10-31')
        # 'October 2025'
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        # If same month, return month name and year
        if start.year == end.year and start.month == end.month:
            return start.strftime('%B %Y')  # 'October 2025'

        # If same year, return month range
        if start.year == end.year:
            return f"{start.strftime('%B')} - {end.strftime('%B %Y')}"  # 'August - October 2025'

        # Different years
        return f"{start.strftime('%B %Y')} - {end.strftime('%B %Y')}"  # 'December 2024 - February 2025'

    except ValueError:
        return f"{start_date} to {end_date}"


# ============================================================================
# MAIN EXECUTION - FOR TESTING
# ============================================================================

if __name__ == '__main__':
    """
    Test code that runs when this file is executed directly.
    Demonstrates how to use the models and functions.
    """

    print(" Testing models.py...\n")

    # Test ExpenseCategory
    print(" Available Categories:")
    for name, color in ExpenseCategory.get_all_categories():
        print(f"  - {name}: {color}")

    # Test Expense model
    print("\n Creating sample expense:")
    expense = Expense(
        id=1,
        date='2025-10-01',
        category='Food & Dining',
        amount=25.50,
        description='Lunch at cafe'
    )
    print(f"  {expense.formatted_amount()} on {expense.category}")
    print(f"  Color: {expense.get_category_color()}")

    # Test ExpenseAnalyzer
    print("\n Testing expense analysis:")
    expenses = [
        Expense(date='2025-10-01', category='Food & Dining', amount=25.50),
        Expense(date='2025-10-02', category='Food & Dining', amount=30.00),
        Expense(date='2025-10-01', category='Transportation', amount=15.00),
    ]

    total = ExpenseAnalyzer.calculate_total(expenses)
    average = ExpenseAnalyzer.calculate_average(expenses)
    category_totals = ExpenseAnalyzer.get_category_totals(expenses)

    print(f"  Total: ${total:.2f}")
    print(f"  Average: ${average:.2f}")
    print(f"  By category: {category_totals}")

    # Test validation
    print("\n Testing validation:")
    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 25.50)
    print(f"  Valid data: {valid}")

    valid, error = validate_expense_data('invalid-date', 'Food & Dining', 25.50)
    print(f"  Invalid date: {valid} - {error}")

    print("\n All model tests complete!")
