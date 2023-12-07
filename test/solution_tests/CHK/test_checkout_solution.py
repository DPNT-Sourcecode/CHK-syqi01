import pytest

from lib.solutions.CHK.checkout_solution import Checkout


class TestCheckout:
    @pytest.fixture
    def checkout_system(self):
        return Checkout()

    @pytest.mark.parametrize(
        "skus, expected",
        [
            (None, -1),
            (123, -1),
            (["A", "B"], -1),
            ("EFG", -1),
            ("A" * 1000, -1),  # if you decide to treat overly long strings as invalid
        ],
    )
    def test_calculate_price_with_breaking_inputs(
        self, checkout_system, skus, expected
    ):
        assert checkout_system.calculate_price(skus) == expected

    @pytest.mark.parametrize(
        "skus, expected",
        [
            (None, -1),
            (123, -1),
            (["A", "B"], -1),
            ("EFG", -1),
            ("A" * 1000, -1),
            ("", -1),  # Testing for empty string as well
        ],
    )
    def test_calculate_price_with_breaking_inputs(
        self, checkout_system, skus, expected
    ):
        assert checkout_system.calculate_price(skus) == expected




