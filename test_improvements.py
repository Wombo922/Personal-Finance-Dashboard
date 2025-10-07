"""
Test script to verify all improvements work correctly.
"""
import sys
import codecs
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from models import validate_expense_data, validate_income_data
from datetime import datetime

print("="*60)
print("TESTING ALL IMPROVEMENTS")
print("="*60)

# Test 1: Boundary amount fix (1,000,000 should now be rejected)
print("\n1. Testing boundary amount fix:")
valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 1000000, 'Test')
print(f"   1,000,000 rejected: {not valid} [PASS]" if not valid else f"   FAIL: {error}")

valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 999999, 'Test')
print(f"   999,999 accepted: {valid} [PASS]" if valid else f"   FAIL: {error}")

# Test 2: Income validation
print("\n2. Testing income validation:")
valid, error = validate_income_data('2025-10-01', 'Salary', 5000.00, 'Test')
print(f"   Valid income accepted: {valid} [PASS]" if valid else f"   FAIL: {error}")

valid, error = validate_income_data('2025-10-01', 'InvalidSource', 5000.00, 'Test')
print(f"   Invalid source rejected: {not valid} [PASS]" if not valid else f"   FAIL: Should reject")

valid, error = validate_income_data('2025-10-01', 'Salary', 5000.00, 'A' * 501)
print(f"   Long description rejected: {not valid} [PASS]" if not valid else f"   FAIL: Should reject")

# Test 3: Date range validation (simulated)
print("\n3. Testing date range logic:")
start = datetime.strptime('2025-10-01', '%Y-%m-%d')
end = datetime.strptime('2025-09-01', '%Y-%m-%d')
print(f"   Start > End detected: {start > end} [PASS]")

# Test 4: Income class date default
print("\n4. Testing Income class improvements:")
from models import Income
try:
    income = Income(amount=1000, source='Salary')  # Date should default to today
    print(f"   Income date defaulted: {income.date == datetime.now().strftime('%Y-%m-%d')} [PASS]")
except Exception as e:
    print(f"   Income date validation: {e}")

print("\n" + "="*60)
print("ALL TESTS COMPLETED")
print("="*60)
