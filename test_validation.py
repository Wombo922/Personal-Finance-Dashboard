"""
TEST_VALIDATION.PY - Automated Validation Testing Script
========================================================

PURPOSE:
This script systematically tests the validation functions in models.py
to ensure all edge cases are handled properly.

JUNIOR DEVELOPER NOTES:
- Automated testing saves time (run script instead of manual testing)
- Each test case has clear expected behavior
- Tests help prevent regression (new changes breaking old features)

HOW TO RUN:
    python test_validation.py

EXPECTED OUTPUT:
    All tests should pass. If any fail, a bug was discovered!
"""

# Import our validation function
from models import validate_expense_data
from datetime import datetime, timedelta
import sys

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def test_valid_data():
    """Test that valid data passes validation."""
    print("\n" + "="*60)
    print("TEST 1: Valid Data")
    print("="*60)

    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 25.50, 'Lunch')

    if valid and error == "":
        print("✅ PASS: Valid data accepted")
    else:
        print(f"❌ FAIL: Valid data rejected with error: {error}")

    return valid


def test_negative_amount():
    """Test that negative amounts are rejected."""
    print("\n" + "="*60)
    print("TEST 2: Negative Amount")
    print("="*60)

    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', -50.00, 'Test')

    if not valid and "greater than 0" in error:
        print(f"✅ PASS: Negative amount rejected with: {error}")
        return True
    else:
        print(f"❌ FAIL: Negative amount should be rejected")
        return False


def test_zero_amount():
    """Test that zero amount is rejected."""
    print("\n" + "="*60)
    print("TEST 3: Zero Amount")
    print("="*60)

    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 0, 'Test')

    if not valid and "greater than 0" in error:
        print(f"✅ PASS: Zero amount rejected with: {error}")
        return True
    else:
        print(f"❌ FAIL: Zero amount should be rejected")
        return False


def test_tiny_amount():
    """Test that very small amounts (0.01) are accepted."""
    print("\n" + "="*60)
    print("TEST 4: Tiny Amount ($0.01)")
    print("="*60)

    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 0.01, 'Test')

    if valid:
        print("✅ PASS: Tiny amount ($0.01) accepted")
        return True
    else:
        print(f"❌ FAIL: Tiny amount rejected with: {error}")
        return False


def test_huge_amount():
    """Test that unreasonably large amounts are rejected."""
    print("\n" + "="*60)
    print("TEST 5: Huge Amount ($2,000,000)")
    print("="*60)

    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 2000000, 'Test')

    if not valid and "unreasonably large" in error:
        print(f"✅ PASS: Huge amount rejected with: {error}")
        return True
    else:
        print(f"❌ FAIL: Huge amount should be rejected")
        return False


def test_invalid_date_format():
    """Test that invalid date formats are rejected."""
    print("\n" + "="*60)
    print("TEST 6: Invalid Date Format")
    print("="*60)

    valid, error = validate_expense_data('10/01/2025', 'Food & Dining', 25.50, 'Test')

    if not valid and "date format" in error.lower():
        print(f"✅ PASS: Invalid date format rejected with: {error}")
        return True
    else:
        print(f"❌ FAIL: Invalid date format should be rejected")
        return False


def test_invalid_category():
    """Test that invalid categories are rejected."""
    print("\n" + "="*60)
    print("TEST 7: Invalid Category")
    print("="*60)

    valid, error = validate_expense_data('2025-10-01', 'InvalidCategory', 25.50, 'Test')

    if not valid and "category" in error.lower():
        print(f"✅ PASS: Invalid category rejected with: {error}")
        return True
    else:
        print(f"❌ FAIL: Invalid category should be rejected")
        return False


def test_long_description():
    """Test that descriptions over 500 characters are rejected."""
    print("\n" + "="*60)
    print("TEST 8: Long Description (501 characters)")
    print("="*60)

    long_desc = "A" * 501  # 501 characters
    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 25.50, long_desc)

    if not valid and "500 characters" in error:
        print(f"✅ PASS: Long description rejected with: {error}")
        return True
    else:
        print(f"❌ FAIL: Long description should be rejected")
        return False


def test_empty_description():
    """Test that empty description is allowed (optional field)."""
    print("\n" + "="*60)
    print("TEST 9: Empty Description")
    print("="*60)

    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 25.50, '')

    if valid:
        print("✅ PASS: Empty description accepted (optional field)")
        return True
    else:
        print(f"❌ FAIL: Empty description should be allowed: {error}")
        return False


def test_special_characters_description():
    """Test that special characters in description are handled."""
    print("\n" + "="*60)
    print("TEST 10: Special Characters in Description")
    print("="*60)

    special_desc = "Café with <script>alert('XSS')</script> & friends 😀"
    valid, error = validate_expense_data('2025-10-01', 'Food & Dining', 25.50, special_desc)

    if valid:
        print("✅ PASS: Special characters accepted")
        print(f"   Note: Jinja2 will auto-escape HTML tags for security")
        return True
    else:
        print(f"❌ FAIL: Special characters should be allowed: {error}")
        return False


def test_past_date():
    """Test that past dates are accepted."""
    print("\n" + "="*60)
    print("TEST 11: Past Date (2020-01-01)")
    print("="*60)

    valid, error = validate_expense_data('2020-01-01', 'Food & Dining', 25.50, 'Old expense')

    if valid:
        print("✅ PASS: Past date accepted")
        return True
    else:
        print(f"❌ FAIL: Past date rejected with: {error}")
        return False


def test_future_date():
    """Test if future dates are accepted (potential improvement area)."""
    print("\n" + "="*60)
    print("TEST 12: Future Date (1 year from now)")
    print("="*60)

    future = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    valid, error = validate_expense_data(future, 'Food & Dining', 25.50, 'Future expense')

    if valid:
        print("⚠️  WARNING: Future date accepted")
        print("   Consider: Should we prevent future-dated expenses?")
        print("   Many expense trackers only allow past/present dates.")
        return True
    else:
        print(f"✅ PASS: Future date rejected with: {error}")
        return True


def test_boundary_amounts():
    """Test amounts at exact boundaries."""
    print("\n" + "="*60)
    print("TEST 13: Boundary Amounts")
    print("="*60)

    tests = [
        (0.01, True, "Minimum valid amount"),
        (999999, True, "Just under limit"),
        (1000000, False, "At limit (1M and above rejected)"),
        (1000001, False, "Just over limit"),
    ]

    all_passed = True
    for amount, should_pass, desc in tests:
        valid, error = validate_expense_data('2025-10-01', 'Food & Dining', amount, 'Test')

        if valid == should_pass:
            print(f"  ✅ {desc}: ${amount:,} - {'Accepted' if valid else 'Rejected'}")
        else:
            print(f"  ❌ {desc}: ${amount:,} - Unexpected result")
            all_passed = False

    return all_passed


def run_all_tests():
    """Run all validation tests and print summary."""
    print("\n" + "#"*60)
    print("# EXPENSE VALIDATION TEST SUITE")
    print("#"*60)
    print("\nThis script tests all edge cases for expense validation.")
    print("Each test verifies that the validation function correctly")
    print("accepts valid data and rejects invalid data.")

    # Run all tests
    tests = [
        test_valid_data,
        test_negative_amount,
        test_zero_amount,
        test_tiny_amount,
        test_huge_amount,
        test_invalid_date_format,
        test_invalid_category,
        test_long_description,
        test_empty_description,
        test_special_characters_description,
        test_past_date,
        test_future_date,
        test_boundary_amounts,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test.__name__}: {e}")
            results.append(False)

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100

    print(f"\nTests Passed: {passed}/{total} ({percentage:.1f}%)")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("Validation is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED")
        print("Review failures above and fix validation logic.")

    print("\n" + "="*60)


if __name__ == "__main__":
    """
    MAIN ENTRY POINT:
    When you run 'python test_validation.py', this block executes.
    __name__ == "__main__" is True only when script is run directly,
    not when imported as a module.
    """
    run_all_tests()
