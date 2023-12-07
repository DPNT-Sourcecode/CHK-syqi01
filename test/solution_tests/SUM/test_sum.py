# from solutions.SUM import sum_solution
import pytest

from lib.solutions.SUM.sum_solution import compute


class TestSum:
    def test_sum(self):
        assert compute(1, 2) == 3


class TestCompute:
    # Happy path tests with various realistic test values
    @pytest.mark.parametrize(
        "x, y, expected",
        [
            pytest.param(1, 1, 2, id="positive_integers"),
            pytest.param(-1, -1, -2, id="negative_integers"),
            pytest.param(0, 0, 0, id="zeroes"),
            pytest.param(1.5, 2.5, 4.0, id="floating_point"),
            pytest.param(-1.5, 2.5, 1.0, id="mixed_sign_floats"),
        ],
        ids=str,
    )
    def test_compute_happy_path(self, x, y, expected):
        result = compute(x, y)
        assert result == expected, f"Expected {expected}, got {result}"

    # Edge cases
    @pytest.mark.parametrize(
        "x, y, expected",
        [
            pytest.param(0, 1, 1, id="zero_first_operand"),
            pytest.param(1, 0, 1, id="zero_second_operand"),
            pytest.param(1e100, 1e100, 2e100, id="large_values"),
            pytest.param(-1e100, -1e100, -2e100, id="large_negative_values"),
        ],
        ids=str,
    )
    def test_compute_edge_cases(self, x, y, expected):
        result = compute(x, y)
        assert result == expected, f"Expected {expected}, got {result}"

    # Error cases
    @pytest.mark.parametrize(
        "x, y, expected_exception",
        [
            pytest.param(1, "a", TypeError, id="string_second_operand"),
            pytest.param("a", 1, TypeError, id="string_first_operand"),
            pytest.param(None, 1, TypeError, id="none_first_operand"),
            pytest.param(1, None, TypeError, id="none_second_operand"),
        ],
        ids=str,
    )
    def test_compute_error_cases(self, x, y, expected_exception):
        with pytest.raises(expected_exception):
            compute(x, y)
