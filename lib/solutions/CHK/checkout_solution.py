class Checkout:
    def __init__(self):
        self.prices = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40, "F": 10}
        self.offers = {
            "A": {"quantity": 3, "price": 130},
            "B": {"quantity": 2, "price": 45},
            "E": {"quantity": 2, "free_item": "B"},
            # Adding logic for F as per the new requirements
            "F": {"quantity": 3, "price": 20},  # 3 for the price of 2
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

        total = 0
        counts = {sku: skus.count(sku) for sku in set(skus)}

        # Handle special offer for E before iterating
        if "E" in counts:
            free_bs = counts["E"] // 2
            counts["B"] = max(0, counts.get("B", 0) - free_bs)

        for sku, count in counts.items():
            if sku == "A":
                total += (
                    (count // 5) * 200
                    + ((count % 5) // 3) * 130
                    + ((count % 5) % 3) * self.prices[sku]
                )
            elif sku in self.offers and "quantity" in self.offers[sku]:
                offer = self.offers[sku]
                if "price" in offer:  # Regular multi-buy offers
                    total += (count // offer["quantity"]) * offer["price"] + (
                        count % offer["quantity"]
                    ) * self.prices[sku]
                elif "free_item" in offer:  # Offers that give a free item
                    total += count * self.prices[sku]
            else:
                total += count * self.prices[sku]

        return total

    @staticmethod
    def run_tests():
        checkout = Checkout()
        test_cases = [
            ("", 0),
            ("A", 50),
            ("B", 30),
            ("C", 20),
            ("D", 15),
            ("E", 40),
            ("a", -1),
            ("-", -1),
            ("ABCa", -1),
            ("AxA", -1),
            ("ABCDE", 155),
            ("AA", 100),
            ("AAA", 130),
            ("AAAA", 180),
            ("AAAAA", 200),
            ("AAAAAA", 250),
            ("AAAAAAA", 300),
            ("AAAAAAAA", 330),
            ("AAAAAAAAA", 380),
            ("AAAAAAAAAA", 400),
            ("EE", 80),
            ("EEB", 80),
            ("EEEB", 120),
            ("EEEEBB", 160),
            ("BEBEEE", 160),
            ("BB", 45),
            ("BBB", 75),
            ("BBBB", 90),
            ("ABCDEABCDE", 280),
            ("CCADDEEBBA", 280),
            ("AAAAAEEBAAABB", 455),
            ("ABCDECBAABCABBAAAEEAA", 665),
            ("F", 10),  # Single F
            ("FF", 20),  # Two Fs
            ("FFF", 20),  # Three Fs (one should be free)
            ("FFFF", 30),  # Four Fs
            ("FFFFFF", 40),  # Six Fs (two free)
            ("FFFFFFF", 50),  # Seven Fs
            ("FXF", -1),  # Illegal input
            # Additional test cases involving item F
            ("FAB", 90),  # F (10) + A (50) + B (30) = 90
            ("FFAB", 100),  # 2F (20) + A (50) + B (30) = 100
            ("FFFAAA", 150),  # 3F (one free, 20) + 3A (130) = 180
            ("FFFFFFAB", 120),  # 6F (two free, 40) + A (50) + B (30) = 140
            ("FFFFD", 45),  # 4F (one free, 30) + D (15) = 50
            ("FFFFFFFFFF", 70),
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


checkout_test = Checkout()
test_results = checkout_test.run_tests()
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

# CHK_R3
# ROUND 3 - More items and offers
# A new item has arrived. Item F.
# Our marketing team wants to try rewording the offer to see if it affects consumption
# Instead of multi-pricing this item they want to say "buy 2Fs and get another F free"
# The offer requires you to have 3 Fs in the basket.

# Our price table and offers:
# +------+-------+------------------------+
# | Item | Price | Special offers         |
# +------+-------+------------------------+
# | A    | 50    | 3A for 130, 5A for 200 |
# | B    | 30    | 2B for 45              |
# | C    | 20    |                        |
# | D    | 15    |                        |
# | E    | 40    | 2E get one B free      |
# | F    | 10    | 2F get one F free      |
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


