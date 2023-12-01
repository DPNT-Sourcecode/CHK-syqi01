import math
from statistics import mean, median, multimode, stdev
from typing import Any, List, Tuple, Union

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
    def calculate_mean(data: List[Union[int, float]]) -> float:
        return mean(data)

    @staticmethod
    def calculate_median(data: List[Union[int, float]]) -> float:
        return median(data)

    @staticmethod
    def calculate_mode(data: List[float]) -> List[int]:
        return multimode(data)  # type: ignore. mulitmode can handle floats #TODO - check

    @staticmethod
    def calculate_standard_deviation(data: List[Union[int, float]]) -> float:
        # Handling for empty list or single element
        return 0 if len(data) < 2 else stdev(data)

    @staticmethod
    def calculate_linear_regression(points: List[Tuple[int, int]]) -> Tuple[float, float]:
        n = len(points)
        if n < 2:
            return (0, 0)  # Returning default values for insufficient points

        sum_x, sum_y, sum_x2, sum_xy = (
            sum(p[0] for p in points),
            sum(p[1] for p in points),
            sum(p[0] ** 2 for p in points),
            sum(p[0] * p[1] for p in points),
        )

        denominator = n * sum_x2 - sum_x**2
        if denominator == 0:
            return (0, 0)  # Prevent division by zero

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n

        return slope, intercept

    # CPT code executor - self-testing

    # @staticmethod
    # def test():
    #     # Testing Standard Deviation
    #     print("Testing Standard Deviation:")
    #     tests = [([1, 2, 3, 4, 5], 1.581), ([10, 10, 10, 10, 10], 0), ([1.5, 2.5, 3.5, 4.5, 5.5], 1.581)]
    #     for test_input, expected in tests:
    #         result = round(DataAnalyzer.calculate_standard_deviation(test_input), 3)
    #         print(
    #             f"Test: {test_input}, Expected: {expected}, Result: {result} ... {'PASSED' if math.isclose(result, expected, abs_tol=0.01) else 'FAILED'}\n"
    #         )

    #     # Testing Linear Regression
    #     print("Testing Linear Regression:")
    #     tests = [
    #         ([(1, 1), (2, 2), (3, 3)], (1, 0)),
    #         ([(1, 2), (2, 4), (3, 6)], (2, 0)),
    #         ([(1, 3), (2, 3), (3, 3)], (0, 3)),
    #     ]
    #     for test_input, expected in tests:
    #         result = DataAnalyzer.calculate_linear_regression(test_input)
    #         result_rounded = (round(result[0], 2), round(result[1], 2))
    #         print(
    #             f"Test: {test_input}, Expected: {expected}, Result: {result_rounded} ... {'PASSED' if result_rounded == expected else 'FAILED'}\n"
    #         )


if __name__ == "__main__":
    # Instantiate class and call test method to test
    print(sum_lt_100(7, 99))
    print("\n")
    DataAnalyzer.test()

# TODOs at the end of the snippet
"""
TODO 1: Implement error handling for empty lists or invalid inputs.
TODO 2: Consider alternative algorithms for performance optimization.
TODO 3: Extend functionality to handle more complex data structures.
TODO 4: Add more comprehensive tests, especially for edge cases.
TODO 5: Explore the use of numpy for performance improvements on large datasets.
TODO 6: Implement logging for better traceability and debugging.
TODO 7: Review and refine type annotations for clarity and consistency.
TODO 8: Consider integration with data visualization tools for analysis insights.
TODO 9: Investigate parallel processing options for handling very large datasets.
TODO 10: Ensure compatibility with different Python versions and environments.
"""
