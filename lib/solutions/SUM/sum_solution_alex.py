from statistics import mean, stdev
from typing import List, Tuple, Union
import math


# sys.path.append("/Users/alexfoster/Documents/Code/accelerate_runner")

# print(sys.path)


def sum(x: int, y: int) -> int:
    if not (0 <= x <= 100) or not (0 <= y <= 100):
        raise ValueError("Arguments must be integers between 1 and 100 (inclusive)")
    return x + y


class DataAnalyzer:
    @staticmethod
    def calculate_standard_deviation(data: List[Union[int, float]]) -> float:
        # Handling for empty list or single element
        return 0 if len(data) < 2 else stdev(data)

    @staticmethod
    def calculate_linear_regression(points: List[Tuple[int, int]]) -> Tuple[float, float]:
        n = len(points)
        if n < 2:
            return (0, 0)  # Returning default values for insufficient points

        sum_x: int = sum(point[0] for point in points)  # Sum of x-coordinates
        sum_y: int = sum(point[1] for point in points)  # Sum of y-coordinates
        sum_x2: int = sum(point[0] ** 2 for point in points)  # Sum of squared x-coordinates
        sum_xy: int = sum(point[0] * point[1] for point in points)  # Sum of product of x and y coordinates

        denominator: int = n * sum_x2 - sum_x**2
        if denominator == 0:
            raise ValueError("LINREG: div 0 error")
            return (0, 0)  # Prevent division by zero

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n

        return slope, intercept

    @staticmethod
    def test():
        # Testing Standard Deviation
        print("Testing Standard Deviation:")
        tests = [([1, 2, 3, 4, 5], 1.581), ([10, 10, 10, 10, 10], 0), ([1.5, 2.5, 3.5, 4.5, 5.5], 1.581)]
        for test_input, expected in tests:
            result = round(DataAnalyzer.calculate_standard_deviation(test_input), 3)
            print(
                f"Test: {test_input}, Expected: {expected}, Result: {result} ... {'PASSED' if math.isclose(result, expected, abs_tol=0.01) else 'FAILED'}\n"
            )

        # Testing Linear Regression
        print("Testing Linear Regression:")
        tests = [
            ([(1, 1), (2, 2), (3, 3)], (1, 0)),
            ([(1, 2), (2, 4), (3, 6)], (2, 0)),
            ([(1, 3), (2, 3), (3, 3)], (0, 3)),
        ]
        for test_input, expected in tests:
            result = DataAnalyzer.calculate_linear_regression(test_input)
            result_rounded = (round(result[0], 2), round(result[1], 2))
            print(
                f"Test: {test_input}, Expected: {expected}, Result: {result_rounded} ... {'PASSED' if result_rounded == expected else 'FAILED'}\n"
            )


if __name__ == "__main__":
    # Instantiate class and call test method to test
    print(sum(7, 99))
    print("\n")
    DataAnalyzer.test()
