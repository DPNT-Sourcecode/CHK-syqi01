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
    def checkout(self):
        return Checkout()

    # Tests for valid inputs
    def test_ABCD(self, checkout):
        assert checkout.calculate_price("ABCD") == 115

    def test_AAAA(self, checkout):
        assert checkout.calculate_price("AAAA") == 180

    def test_empty_string(self, checkout):
        assert checkout.calculate_price("") == 0

    def test_AAAB(self, checkout):
        assert checkout.calculate_price("AAAB") == 160

    def test_AB(self, checkout):
        assert checkout.calculate_price("AB") == 80

    def test_EE(self, checkout):
        assert checkout.calculate_price("EE") == 80

    def test_EEB(self, checkout):
        assert checkout.calculate_price("EEB") == 80

    # Tests for breaking inputs
    def test_none_input(self, checkout):
        assert checkout.calculate_price(None) == -1

    def test_numeric_input(self, checkout):
        assert checkout.calculate_price(123) == -1

    def test_list_input(self, checkout):
        assert checkout.calculate_price(["A", "B"]) == -1

    def test_invalid_sku_input(self, checkout):
        assert checkout.calculate_price("EFG") == -1

    def test_too_long_sku_input(self, checkout):
        assert checkout.calculate_price("A" * 101) == -1
