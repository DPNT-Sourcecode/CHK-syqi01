# Stage 5 - Redo code with robust handling for breaking inputs


class Checkout:
    def __init__(self):
        self.prices = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40}
        self.offers = {
            "A": {"quantity": 3, "price": 130},
            "B": {"quantity": 2, "price": 45},
            "E": {"quantity": 2, "free_item": "B"},  # Special offer for E
        }
        self.max_sku_length = 100  # Set a maximum acceptable length for SKU strings

    def validate_skus(self, skus):
        # More robust validation of skus
        if not isinstance(skus, str) or len(skus) > self.max_sku_length:
            return False

        if any(sku not in self.prices for sku in skus):
            return False

        return True

    def calculate_price(self, skus):
        # Check for non-string, empty string, invalid characters, or too long string
        if not self.validate_skus(skus):
            return -1

        if skus == "":
            return 0

        total = 0
        counts = {sku: skus.count(sku) for sku in set(skus)}

        # Handle special offer for E
        if "E" in counts:
            free_bs = counts["E"] // 2
            counts["B"] = max(0, counts.get("B", 0) - free_bs)

        for sku, count in counts.items():
            if sku in self.offers:
                offer = self.offers[sku]
                if (
                    "quantity" in offer and "price" in offer
                ):  # Standard quantity-price offer
                    total += (count // offer["quantity"]) * offer["price"] + (
                        count % offer["quantity"]
                    ) * self.prices[sku]
                elif "free_item" in offer:  # Special free item offer (like for E)
                    total += count * self.prices[sku]
            else:
                total += count * self.prices.get(sku, 0)

        return total

    def run_tests(self):
        print("\nTesting valid inputs")
        tests = [
            ("ABCD", 115),
            ("AAAA", 180),
            ("", 0),
            ("AAAB", 160),
            ("AB", 80),
            ("EE", 80),  # Testing new offer for E
            ("EEB", 80),  # 2E get one B free
        ]
        for test in tests:
            result = self.calculate_price(test[0])
            print(
                f"Testing function: {test[0]}: {result} ... {'PASSED' if result == test[1] else 'FAILED'}"
            )

        print("\nTesting breaking inputs")
        breaking_tests = [None, 123, ["A", "B"], "EFG", "A" * 101]
        for test in breaking_tests:
            result = self.calculate_price(test)
            print(
                f"Testing function with {test}: {result} ... {'PASSED' if result == -1 else 'FAILED'}"
            )


# Instantiate Checkout class and run tests
# checkout_system = Checkout()
# checkout_system.run_tests()

# TODO 1: Implement more robust input validation using regular expressions to filter out any non-allowed characters.
# TODO 2: Refactor the calculate_price method to reduce its complexity and improve readability.
# TODO 3: Consider using a database or external file for SKU data to enhance scalability and ease of updates.
# TODO 4: Expand testing to include more edge cases, particularly for combined offers and large quantities.
# TODO 5: Optimize for higher scale, e.g., by using more efficient data structures or algorithms.
# TODO 6: Refactor into a more object-oriented design, perhaps by creating separate classes for Offers and SKUs.
# TODO 7: Add type annotations throughout the code for better clarity and to facilitate static analysis with tools like mypy.
# TODO 8: Explore using a library like Pydantic for stricter input validation and error handling.
# TODO 9: Implement error logging and handling mechanisms for better debugging and maintenance in a production environment.
# TODO 10: Consider the potential for a front-end integration, and how the backend logic might need to adapt for such a use case.


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    checkout_system = Checkout()
    return checkout_system.calculate_price(skus)


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


# CHK_R2
# ROUND 2 - More offers
# The checkout feature is great and our supermarket is doing fine. Is time to think about growth.
# Our marketing teams wants to experiment with new offer types and we should do our best to support them.

# We are going to sell a new item E.
# Normally E costs 40, but if you buy 2 of Es you will get B free. How cool is that ? Multi-priced items also seemed to work well so we should have more of these.

# Our price table and offers:
# +------+-------+------------------------+
# | Item | Price | Special offers         |
# +------+-------+------------------------+
# | A    | 50    | 3A for 130, 5A for 200 |
# | B    | 30    | 2B for 45              |
# | C    | 20    |                        |
# | D    | 15    |                        |
# | E    | 40    | 2E get one B free      |
# +------+-------+------------------------+


# Notes:
#  - The policy of the supermarket is to always favor the customer when applying special offers.
#  - All the offers are well balanced so that they can be safely combined.
#  - For any illegal input return -1

# In order to complete the round you need to implement the following method:
#      checkout(String) -> Integer

# Where:
#  - param[0] = a String containing the SKUs of all the products in the basket
#  - @return = an Integer representing the total checkout value of the items
