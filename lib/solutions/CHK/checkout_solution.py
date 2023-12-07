class Checkout:
    def __init__(self):
        self.prices = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40}
        self.offers = {
            "A": {"quantity": 3, "price": 130},
            "B": {"quantity": 2, "price": 45},
            "E": {"quantity": 2, "free_item": "B"},
        }
        self.max_sku_length = 100

    def validate_skus(self, skus):
        if not isinstance(skus, str) or len(skus) > self.max_sku_length:
            return False
        if any(sku not in self.prices for sku in skus):
            return False
        if (
            not skus.isupper() and skus != ""
        ):  # Ensure all characters are uppercase or it's an empty string
            return False
        return True

    def calculate_price(self, skus):
        if not self.validate_skus(skus):
            return -1
        if skus == "":
            return 0

        # Split SKUs and count
        counts = {sku: skus.count(sku) for sku in set(skus)}

        # Calculate total considering all possible offer combinations
        total = self.calculate_best_price(counts)

        return total

    def calculate_best_price(self, counts):
        # Recursive function to calculate the best price considering all offers
        if not counts:
            return 0

        min_total = float("inf")

        for sku, count in counts.items():
            new_counts = counts.copy()
            new_counts[sku] -= 1
            if new_counts[sku] == 0:
                del new_counts[sku]

            # Price without applying the offer
            total_price = self.prices[sku] + self.calculate_best_price(new_counts)
            min_total = min(min_total, total_price)

            # Price with applying the offer (if available)
            if sku in self.offers:
                offer = self.offers[sku]
                if "quantity" in offer and count >= offer["quantity"]:
                    new_counts_offer = new_counts.copy()
                    new_counts_offer[sku] -= offer["quantity"] - 1
                    if new_counts_offer[sku] <= 0:
                        del new_counts_offer[sku]

                    total_price_offer = offer["price"] + self.calculate_best_price(
                        new_counts_offer
                    )
                    min_total = min(min_total, total_price_offer)

        return min_total

    @staticmethod
    def run_tests():
        checkout = Checkout()
        test_cases = [
            # Round 1 specific tests
            ("A", 50),
            ("AA", 100),
            ("AAA", 130),  # 3A for 130
            ("AAAA", 180),  # 3A for 130 + 1A
            # Round 2 specific tests
            ("AAAAA", 200),  # 5A for 200
            ("AAAAAA", 250),  # 5A for 200 + 1A
            ("EE", 80),  # 2E get one B free, but only E's price is counted
            ("EEB", 80),  # 2E get one B free, B is not charged
            # Tests combining offers across different items
            ("AB", 80),  # No offers
            ("ABB", 95),  # 2B for 45
            ("ABEE", 120),  # 2E get one B free, only one B charged
            # Tests for illegal input
            ("a", -1),
            ("1", -1),
            ("A" * 101, -1),  # Exceeding max SKU length
            # Tests confirming customer-favoring policy
            ("AAAB", 160),  # 3A for 130 + 1A + 1B
        ]

        passed = 0
        for skus, expected in test_cases:
            result = checkout.calculate_price(skus)
            if result == expected:
                passed += 1
            else:
                print(
                    f"Test failed for input '{skus}': Expected {expected}, got {result}"
                )

        return f"{passed}/{len(test_cases)} tests passed."


# Run the tests using the static method
test_results = Checkout.run_tests()
print(test_results)


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


