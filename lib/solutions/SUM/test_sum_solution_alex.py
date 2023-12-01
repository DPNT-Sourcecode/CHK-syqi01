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
from lib.solutions.SUM.sum_solution_alex import DataAnalyzer  # noqa: E402


class TestDataAnalyzer(TestCase):
    def test_calculate_mean_with_valid_data(self):
        test_cases = [([1, 2, 3, 4, 5], 3.0), ([1.5, 2.5, 3.5, 4.5, 5.5], 3.5)]

        for data, expected in test_cases:
            with self.subTest(data=data):
                result = DataAnalyzer.calculate_mean(data)
                self.assertEqual(result, expected)

    def test_calculate_mean_with_invalid_data(self):
        test_cases = [([], None), ("not a list", None)]  # Handling empty list  # Handling invalid input

        for data, expected in test_cases:
            with self.subTest(data=data):
                result = DataAnalyzer.calculate_mean(data)
                self.assertIsNone(result)

    def test_calculate_median_with_valid_data(self):
        test_cases = [([1, 2, 3, 4, 5], 3), ([5, 4, 3, 2, 1], 3)]

        for data, expected in test_cases:
            with self.subTest(data=data):
                result = DataAnalyzer.calculate_median(data)
                self.assertEqual(result, expected)

    def test_calculate_median_with_invalid_data(self):
        test_cases = [([], None), ("not a list", None)]  # Handling empty list  # Handling invalid input

        for data, expected in test_cases:
            with self.subTest(data=data):
                result = DataAnalyzer.calculate_median(data)
                self.assertIsNone(result)

    def test_calculate_mode_with_valid_data(self):
        test_cases = [([1, 2, 3, 3, 4], [3]), ([1, 1, 2, 2, 3, 3, 4], [1, 2, 3])]

        for data, expected in test_cases:
            with self.subTest(data=data):
                result = DataAnalyzer.calculate_mode(data)
                self.assertEqual(result, expected)

    def test_calculate_mode_with_invalid_data(self):
        test_cases = [([], []), ("not a list", None)]  # Handling empty list  # Handling invalid input

        for data, expected in test_cases:
            with self.subTest(data=data):
                result = DataAnalyzer.calculate_mode(data)
                if isinstance(data, list):
                    self.assertEqual(result, expected)
                else:
                    self.assertIsNone(result)

    def test_calculate_standard_deviation(self):
        # Define test cases
        test_cases = [([1, 2, 3, 4, 5], 1.581), ([10, 10, 10, 10, 10], 0), ([1.5, 2.5, 3.5, 4.5, 5.5], 1.581)]

        # Run and assert tests
        for data, expected in test_cases:  # TODO shouldnt be loop.
            with self.subTest(data=data):
                result = DataAnalyzer.calculate_standard_deviation(data)
                self.assertAlmostEqual(result, expected, places=3)

    def test_calculate_linear_regression(self):
        # Define test cases
        test_cases = [
            ([(1, 1), (2, 2), (3, 3)], (1, 0)),
            ([(1, 2), (2, 4), (3, 6)], (2, 0)),
            ([(1, 3), (2, 3), (3, 3)], (0, 3)),
        ]

        # Run and assert tests
        for points, expected in test_cases:  # TODO - not loop
            with self.subTest(points=points):
                slope, intercept = DataAnalyzer.calculate_linear_regression(points)
                self.assertAlmostEqual(slope, expected[0], places=2)
                self.assertAlmostEqual(intercept, expected[1], places=2)


# Run the tests
if __name__ == "__main__":
    django.test.utils.setup_test_environment()  # type: ignore
    django.test.runner.DiscoverRunner().run_tests(["test_data_analyzer"])  # type: ignore


