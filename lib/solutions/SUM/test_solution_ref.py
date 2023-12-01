# test_data_analyzer.py

import django
from django.conf import settings
from django.test import TestCase

# Configure Django settings
settings.configure(
    INSTALLED_APPS=[
        # List any apps that your tests need to be aware of
    ],
    SECRET_KEY="a-very-secret-key",
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    # ... other settings as needed ...
)

# Initialize Django
django.setup()

# Your DataAnalyzer class (or import it if it's defined elsewhere)
from lib.solutions.SUM.solution_ref import DataAnalyzer  # noqa: E402


class TestDataAnalyzer(TestCase):
    # Tests for calculate_mean with valid data
    def test_calculate_mean_with_list_of_integers(self):
        data = [1, 2, 3, 4, 5]
        expected = 3.0
        result = DataAnalyzer.calculate_mean(data)
        self.assertEqual(result, expected)

    def test_calculate_mean_with_list_of_floats(self):
        data = [1.5, 2.5, 3.5, 4.5, 5.5]
        expected = 3.5
        result = DataAnalyzer.calculate_mean(data)
        self.assertEqual(result, expected)

    # TODO Tests for calculate_mean with invalid data
    # def test_calculate_mean_with_empty_list(self):
    #     data = []
    #     result = DataAnalyzer.calculate_mean(data)
    #     self.assertIsNone(result)

    # TODO def test_calculate_mean_with_non_list_input(self):
    #     data = "not a list"
    #     result = DataAnalyzer.calculate_mean(data)
    #     self.assertIsNone(result)

    # Tests for calculate_median with valid data
    def test_calculate_median_with_ordered_list(self):
        data = [1, 2, 3, 4, 5]
        expected = 3
        result = DataAnalyzer.calculate_median(data)
        self.assertEqual(result, expected)

    def test_calculate_median_with_unordered_list(self):
        data = [5, 4, 3, 2, 1]
        expected = 3
        result = DataAnalyzer.calculate_median(data)
        self.assertEqual(result, expected)

    # Tests for calculate_median with invalid data
    # TODO def test_calculate_median_with_empty_list(self):
    #     data = []
    #     result = DataAnalyzer.calculate_median(data)
    #     self.assertIsNone(result)

    # TODO def test_calculate_median_with_non_list_input(self):
    #     data = "not a list"
    #     result = DataAnalyzer.calculate_median(data)
    #     self.assertIsNone(result)

    # Tests for calculate_mode with valid data
    def test_calculate_mode_with_single_mode(self):
        data = [1, 2, 3, 3, 4]
        expected = [3]
        result = DataAnalyzer.calculate_mode(data)
        self.assertEqual(result, expected)

    def test_calculate_mode_with_multiple_modes(self):
        data = [1, 1, 2, 2, 3, 3, 4]
        expected = [1, 2, 3]
        result = DataAnalyzer.calculate_mode(data)
        self.assertEqual(result, expected)

    # Tests for calculate_mode with invalid data
    # TODO def test_calculate_mode_with_empty_list(self):
    #     data = []
    #     expected = []
    #     result = DataAnalyzer.calculate_mode(data)
    #     self.assertEqual(result, expected)

    # TODO def test_calculate_mode_with_non_list_input(self):
    #     data = "not a list"
    #     result = DataAnalyzer.calculate_mode(data)
    #     self.assertIsNone(result)

    # Hypothetical test for standard deviation
    def test_calculate_standard_deviation_with_valid_data(self):
        data = [1, 2, 3, 4, 5]
        expected = 1.58  # Example standard deviation value
        result = DataAnalyzer.calculate_standard_deviation(data)
        self.assertAlmostEqual(result, expected, places=2)

    # TODO def test_calculate_standard_deviation_with_empty_list(self):
    #     data = []
    #     result = DataAnalyzer.calculate_standard_deviation(data)
    #     self.assertIsNone(result)

    # Hypothetical test for linear regression
    def test_calculate_linear_regression_with_valid_data(self):
        data = [(1, 1), (2, 2), (3, 3)]  # Example data points
        expected_slope = 1
        expected_intercept = 0
        slope, intercept = DataAnalyzer.calculate_linear_regression(data)
        self.assertAlmostEqual(slope, expected_slope, places=2)
        self.assertAlmostEqual(intercept, expected_intercept, places=2)

    # TODO def test_calculate_linear_regression_with_empty_list(self):
    #     data = []
    #     slope, intercept = DataAnalyzer.calculate_linear_regression(data)
    #     self.assertIsNone(slope)
    #     self.assertIsNone(intercept)


# Run the tests
if __name__ == "__main__":
    django.test.utils.setup_test_environment()  # type: ignore
    django.test.runner.DiscoverRunner().run_tests(["test_data_analyzer"])  # type: ignore
