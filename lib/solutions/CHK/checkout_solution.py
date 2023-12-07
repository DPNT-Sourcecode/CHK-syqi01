# Stage 4 - Define likely breaking inputs

# Breaking inputs to consider:
# 1. None or empty input.
# 2. Incorrect object types (e.g., numbers, lists instead of strings).
# 3. Strings containing invalid characters (not A, B, C, D).
# 4. Very long strings (performance testing).

# Let's proceed to Stage 4.2 - Writing the first pass of the code with basic tests.
# Note: As requested, we're using Python built-in libraries only.


class Checkout:
    def __init__(self):
        # Prices and offers could also be loaded from a DataFrame for more complex scenarios
        self.prices = {"A": 50, "B": 30, "C": 20, "D": 15}
        self.offers = {
            "A": {"quantity": 3, "price": 130},
            "B": {"quantity": 2, "price": 45},
        }

    @staticmethod
    def is_valid_sku(sku):
        return sku in "ABCD"

    def calculate_price(self, skus):
        if not isinstance(skus, str):
            return -1
        total = 0
        counts = {sku: skus.count(sku) for sku in set(skus) if self.is_valid_sku(sku)}
        for sku, count in counts.items():
            if sku in self.offers:
                offer = self.offers[sku]
                total += (count // offer["quantity"]) * offer["price"] + (
                    count % offer["quantity"]
                ) * self.prices[sku]
            else:
                total += count * self.prices.get(sku, 0)
        return total

    def run_tests(self):
        # Testing with valid inputs
        print("\nTesting valid inputs")
        tests = [("ABCD", 115), ("AAAA", 180), ("", 0), ("AAAB", 160), ("AB", 80)]
        for test in tests:
            result = self.calculate_price(test[0])
            print(
                f"Testing function: {test[0]}: {result} ... {'PASSED' if result == test[1] else 'FAILED'}"
            )

        # Testing with breaking inputs
        print("\nTesting breaking inputs")
        breaking_tests = [None, 123, ["A", "B"], "EFG", "A" * 1000]
        for test in breaking_tests:
            result = self.calculate_price(test)
            print(
                f"Testing function with {test}: {result} ... {'PASSED' if result == -1 else 'FAILED'}"
            )


# Instantiate Checkout class and run tests
checkout_system = Checkout()
checkout_system.run_tests()

# TODO 1. Breaking inputs not handled robustly: consider more thorough input validation.
# TODO 2. Refactor: this code could be shorter and more modular using list comprehensions.
# TODO 3. Consider using a database or external file for SKU data for scalability.
# TODO 4. Testing is currently not very robust and doesn't handle all edge cases.
# TODO 5. Optimize for higher scale, e.g., by using more efficient data structures.
# TODO 6. Refactoring into a more object-oriented design would be beneficial.
# TODO 7. Add/check type annotations for better code clarity and error checking.
# TODO 8. Implement stricter validation, possibly using libraries like Pydantic.
# TODO 9. Consider error logging for production readiness.
# TODO 10. Explore possibilities of integrating with a front-end for a full application.


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    raise NotImplementedError()


# CHK_R1
# ROUND 1 - Our supermarket
# The purpose of this challenge is to implement a supermarket checkout that calculates the total price of a number of items.

# In a normal supermarket, things are identified using Stock Keeping Units, or SKUs.
# In our store, we'll use individual letters of the alphabet (A, B, C, and so on).
# Our goods are priced individually. In addition, some items are multi-priced: buy n of them, and they'll cost you y pounds.
# For example, item A might cost 50 pounds individually, but this week we have a special offer:
#  buy three As and they'll cost you 130.

# Our price table and offers:
# +------+-------+----------------+
# | Item | Price | Special offers |
# +------+-------+----------------+
# | A    | 50    | 3A for 130     |
# | B    | 30    | 2B for 45      |
# | C    | 20    |                |
# | D    | 15    |                |
# +------+-------+----------------+


# Notes:
#  - For any illegal input return -1

# In order to complete the round you need to implement the following method:
#      checkout(String) -> Integer

# Where:
#  - param[0] = a String containing the SKUs of all the products in the basket
#  - @return = an Integer representing the total checkout value of the items

