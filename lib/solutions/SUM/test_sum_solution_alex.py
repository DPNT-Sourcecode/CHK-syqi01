# test_data_analyzer.py

import django
from django.conf import settings
from django.test import TestCase

# Configure Django settings
settings.configure(
    INSTALLED_APPS=[
        # List any apps that your tests need to be aware of
    ],
    # Any other settings required for your tests
)

# Initialize Django
django.setup()

# Your DataAnalyzer class (or import it if it's defined elsewhere)
from lib.solutions.SUM.sum_solution_alex import DataAnalyzer  # noqa: E402


# Test cases
class TestDataAnalyzer(TestCase):
    def test_calculate_standard_deviation(self):
        # Your test logic here
        self.assertAlmostEqual(DataAnalyzer.calculate_standard_deviation([1, 2, 3, 4, 5]), 1.58, places=2)

    def test_calculate_linear_regression(self):
        # Your test logic here
        self.assertEqual(DataAnalyzer.calculate_linear_regression([(1, 1), (2, 2), (3, 3)]), (1, 0))


# More tests as needed

# Run the tests
if __name__ == "__main__":
    django.test.utils.setup_test_environment()
    django.test.runner.DiscoverRunner().run_tests(["test_data_analyzer"])

