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

    # Parameterized tests for valid and breaking inputs
    @pytest.mark.parametrize(
        "input_string, expected_output",
        [
            # Valid inputs
            ("", 0),
            ("A", 50),
            ("B", 30),
            ("C", 20),
            ("D", 15),
            ("E", 40),
            ("ABCD", 115),
            ("AAAA", 180),
            ("AAAB", 160),
            ("AB", 80),
            ("EE", 80),
            ("EEB", 80),
            ("ABCDE", 155),
            ("AAAAA", 230),
            ("AAAAAA", 260),
            ("AAAAAAA", 310),
            ("AAAAAAAA", 360),
            ("AAAAAAAAA", 390),
            ("AAAAAAAAAA", 440),
            ("EE", 80),
            ("EEB", 80),
            ("EEEB", 120),
            ("EEEEBB", 160),
            ("BEBEEE", 160),
            ("AA", 100),
            ("AAA", 130),
            ("AAAA", 180),
            ("AAAAA", 230),
            ("AAAAAA", 260),
            ("B", 30),
            ("BB", 45),
            ("BBB", 75),
            ("BBBB", 90),
            ("ABCDEABCDE", 280),
            ("CCADDEEBBA", 280),
            ("AAAAAEEBAAABB", 485),
            ("ABCDECBAABCABBAAAEEAA", 675),
            # Breaking inputs
            (None, -1),
            (123, -1),
            (["A", "B"], -1),
            ("EFG", -1),
            ("A" * 101, -1),
            ("a", -1),
            ("-", -1),
            ("ABCa", -1),
            ("AxA", -1),
        ],
    )
    def test_checkout(self, checkout, input_string, expected_output):
        assert checkout.calculate_price(input_string) == expected_output
