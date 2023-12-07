import pytest

from lib.solutions.CHK.checkout_solution import Checkout

# To update the tests for the new requirements, we need to consider the following changes introduced in ROUND 2:

# New Item E: Priced at 40 normally.
# New Offers:
# A: Additional offer of 5A for 200.
# E: Special offer of 2E get one B free.
# Policy Favoring Customers: Ensuring that the best possible offers are applied for the benefit of the customer.
# Combination of Offers: Offers can be combined without conflicts.
# Based on these, the updated test cases should cover:

# The new pricing and offers for items A and E.
# Scenarios where multiple offers, including the new ones, are applied together.
# Edge cases that involve the new item E and its offer, ensuring that the "2E get one B free" offer is correctly applied.
# The continued functionality of the original offers and prices for items B, C, and D.
# Here's how the test cases can be updated to reflect these changes:


class TestCheckout:
    @pytest.fixture
    def checkout_system(self):
        return Checkout()

    @pytest.mark.parametrize(
        "skus, expected",
        [
            ("ABCD", 115),
            ("AAAAA", 200),  # New offer for A
            ("", 0),
            ("AAAB", 160),
            ("AB", 80),
            ("EE", 80),  # New item E without offer
            ("EEB", 80),  # New offer for E (2E get B free)
            ("EEEEBB", 160),  # Applying E's offer twice
            ("ABCDE", 195),  # All items, including new E
        ],
    )
    def test_calculate_price_with_valid_inputs(self, checkout_system, skus, expected):
        assert checkout_system.calculate_price(skus) == expected

    @pytest.mark.parametrize(
        "skus, expected",
        [
            (None, -1),
            (123, -1),
            (["A", "B"], -1),
            ("EFG", -1),  # G is an invalid SKU
            ("A" * 1000, -1),  # Overly long strings, if treated as invalid
        ],
    )
    def test_calculate_price_with_breaking_inputs(
        self, checkout_system, skus, expected
    ):
        assert checkout_system.calculate_price(skus) == expected

