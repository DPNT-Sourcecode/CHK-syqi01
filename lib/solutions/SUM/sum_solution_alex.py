import math
from statistics import stdev
from typing import List, Tuple, Union


# def sum(data: List[float]) -> float:
#     return sum(data=data)


# sys.path.append("/Users/alexfoster/Documents/Code/accelerate_runner")

# print(sys.path)


def sum_lt_100(x: float, y: float) -> float:
    if not (0 <= x <= 100) or not (0 <= y <= 100):
        raise ValueError("Arguments must be integers between 1 and 100 (inclusive)")
    return x + y


class DataAnalyzer:
    @staticmethod
    def calculate_standard_deviation(data: List[Union[float, float]]) -> float:
        # Handling for empty list or single element
        return 0 if len(data) < 2 else stdev(data)

    @staticmethod
    def calculate_linear_regression(points: List[Tuple[float, float]]) -> Tuple[float, float]:
        n: int = len(points)
        if n < 2:
            return (0, 0)  # Returning default values for insufficient points

        sum_x: float = sum(point[0] for point in points)  # Sum of x-coord
        sum_y: float = sum(point[1] for point in points)  # Sum of y-coordinates
        sum_x2: float = sum(point[0] ** 2 for point in points)  # Sum of squared x-coordinates
        sum_xy: float = sum(point[0] * point[1] for point in points)  # Sum of product o f x and y coordinates

        denominator: float = n * sum_x2 - sum_x**2

        # Prevent division by zero
        try:
            if denominator == 0:
                raise ValueError("LINREG: div 0 error")
        except ValueError:
            return (0, 0)

        slope: float = (n * sum_xy - sum_x * sum_y) / denominator
        intercept: float = (sum_y - slope * sum_x) / n

        return slope, intercept

    @staticmethod
    def test() -> None:
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
    print(sum_lt_100()(7, 99))
    print("\n")
    DataAnalyzer.test()

