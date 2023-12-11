from pprint import pprint

pricing_table_string = """
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
| F    | 10    | 2F get one F free      |
| G    | 20    |                        |
| H    | 10    | 5H for 45, 10H for 80  |
| I    | 35    |                        |
| J    | 60    |                        |
| K    | 80    | 2K for 150             |
| L    | 90    |                        |
| M    | 15    |                        |
| N    | 40    | 3N get one M free      |
| O    | 10    |                        |
| P    | 50    | 5P for 200             |
| Q    | 30    | 3Q for 80              |
| R    | 50    | 3R get one Q free      |
| S    | 30    |                        |
| T    | 20    |                        |
| U    | 40    | 3U get one U free      |
| V    | 50    | 2V for 90, 3V for 130  |
| W    | 20    |                        |
| X    | 90    |                        |
| Y    | 10    |                        |
| Z    | 50    |                        |
+------+-------+------------------------+"""


def parse_pricing_table(pricing_table):
    # Split the string into lines
    lines = pricing_table.strip().split("\n")

    # Dictionary to store the parsed data
    parsed_data = {}

    for line in lines:
        # Check if the line contains data (and is not a border)
        if "+" not in line and "Item" not in line:
            # Split the line into parts and strip whitespace
            parts = [part.strip() for part in line.split("|") if part]

            # Add the parsed data to the dictionary
            if len(parts) == 3:
                item, price, special_offers = parts
                parsed_data[item] = {"Price": price, "Special offers": special_offers}

    return parsed_data


# Use the function
pricing_table_dict = parse_pricing_table(pricing_table_string)
print("\n\n basic parsing")
pprint(pricing_table_dict)


# reformat pricing data to have special offers stored manageably


def reformat_pricing_data(pricing_data):
    # List to store the reformatted data
    reformatted_data = []

    # Iterate over the items in the dictionary
    for item in pricing_data:
        # Skip the header row
        if item == "Item":
            continue

        # Get the price of the item
        price = pricing_data[item]["Price"]

        # Check if there's a special offer for the item
        if pricing_data[item]["Special offers"]:
            # Split multiple offers into separate entries
            offers = pricing_data[item]["Special offers"].split(", ")
            for offer in offers:
                reformatted_data.append(
                    {item: {"Price": price, "Special offers": offer}}
                )
        else:
            # If there are no special offers, add the item with an empty offer field
            reformatted_data.append({item: {"Price": price, "Special offers": ""}})

    return reformatted_data


# Reformat the pricing table dictionary
reformatted_pricing_data = reformat_pricing_data(pricing_table_dict)
print("\n\nreformatted pricing data to split out prices!")
pprint(reformatted_pricing_data)

# Reformat the pricing table dictionary
reformatted_pricing_data = reformat_pricing_data(pricing_table_dict)


def parse_special_offers(data):
    parsed_offers = {}

    for item_data in data:
        for item, details in item_data.items():
            offer = details["Special offers"]
            price = int(details["Price"])

            # Handle complex offers
            if offer:
                if "for" in offer:
                    # Simple offers like "3A for 130"
                    parts = offer.split(" ")
                    count = int(
                        parts[0][0]
                    )  # Assuming the count is the first character
                    total_price = int(parts[2])
                    parsed_offers[offer] = {
                        "input": {
                            item: {
                                "count": count,
                                "t_price": float(price * count),
                                "price_calc": f"{count}*{price}",
                            }
                        },
                        "output": {
                            item: {
                                "count": count,
                                "t_price": float(total_price),
                                "price_calc": str(total_price),
                            }
                        },
                    }

                elif "get one" in offer:
                    # Offers like "2E get one B free"
                    (
                        primary_item_count,
                        free_item,
                        free_item_price,
                    ) = parse_get_one_free_offer(item, price, offer, data)

                    parsed_offers[offer] = {
                        "input": {
                            item: {
                                "count": primary_item_count,
                                "t_price": float(price * primary_item_count),
                                "price_calc": f"{primary_item_count}*{price}",
                            },
                            free_item: {
                                "count": 1,
                                "t_price": float(free_item_price),
                                "price_calc": f"1*{free_item_price}",
                            },
                        },
                        "output": {
                            item: {
                                "count": primary_item_count,
                                "t_price": float(price * primary_item_count),
                                "price_calc": f"{primary_item_count}*{price}",
                            },
                            free_item: {
                                "count": 1,
                                "t_price": 0.0,
                                "price_calc": "0*1",
                            },
                        },
                    }
            else:
                # Default offer (no special offer)
                parsed_offers[""] = {
                    "input": {
                        item: {"count": 1, "t_price": float(price), "price_calc": ""}
                    },
                    "output": {
                        item: {"count": 1, "t_price": float(price), "price_calc": ""}
                    },
                }

    return parsed_offers


# Helper function to parse "get one free" offers
def parse_get_one_free_offer(item, price, offer, data):
    parts = offer.split(" ")
    primary_item_count = int(parts[0][0])  # Assuming the count is the first character
    free_item = parts[4]  # Assuming the free item is the last word in the offer
    free_item_price = 0
    for offer_data in data:
        if free_item in offer_data:
            free_item_price = int(offer_data[free_item]["Price"])
            break
    return primary_item_count, free_item, free_item_price


# Parse the special offers from the reformatted pricing data using the final format
parsed_special_offers = parse_special_offers(reformatted_pricing_data)
print("\n\n parse special offers into input / output format ready for processing")
pprint(parsed_special_offers)


# class Checkout:
#     def __init__(self):
#         self.prices = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40, "F": 10}
#         self.offers = {
#             "A": {"quantity": 3, "price": 130},
#             "B": {"quantity": 2, "price": 45},
#             "E": {"quantity": 2, "free_item": "B"},
#             # Adding logic for F as per the new requirements
#             "F": {"quantity": 3, "price": 20},  # 3 for the price of 2
#         }
#         self.max_sku_length = 100

#     def validate_skus(self, skus):
#         if not isinstance(skus, str) or len(skus) > self.max_sku_length:
#             return False
#         if any(sku not in self.prices for sku in skus):
#             return False
#         if (
#             not skus.isupper() and skus != ""
#         ):  # Ensure all characters are uppercase or it's an empty string
#             return False
#         return True

#     def calculate_price(self, skus):
#         if not self.validate_skus(skus):
#             return -1
#         if skus == "":
#             return 0

#         total = 0
#         counts = {sku: skus.count(sku) for sku in set(skus)}

#         # Handle special offer for E before iterating
#         if "E" in counts:
#             free_bs = counts["E"] // 2
#             counts["B"] = max(0, counts.get("B", 0) - free_bs)

#         for sku, count in counts.items():
#             if sku == "A":
#                 total += (
#                     (count // 5) * 200
#                     + ((count % 5) // 3) * 130
#                     + ((count % 5) % 3) * self.prices[sku]
#                 )
#             elif sku in self.offers and "quantity" in self.offers[sku]:
#                 offer = self.offers[sku]
#                 if "price" in offer:  # Regular multi-buy offers
#                     total += (count // offer["quantity"]) * offer["price"] + (
#                         count % offer["quantity"]
#                     ) * self.prices[sku]
#                 elif "free_item" in offer:  # Offers that give a free item
#                     total += count * self.prices[sku]
#             else:
#                 total += count * self.prices[sku]

#         return total


# @staticmethod
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
        ("F", 10),
        ("FF", 20),
        ("FFF", 20),
        ("FFFF", 30),
        ("FFFFFF", 40),
        ("FFFFFFF", 50),
        ("FXF", -1),
        ("FAB", 90),
        ("FFAB", 100),
        ("FFFAAA", 150),
        ("FFFFFFAB", 120),
        ("FFFFD", 45),
        ("FFFFFFFFFF", 70),
    ]
    # run and print tests
    passed = sum(
        1 for skus, expected in test_cases if checkout.calculate_price(skus) == expected
    )
    for skus, expected in test_cases:
        result = checkout.calculate_price(skus)
        if result != expected:
            print(f"Test failed for input '{skus}': Expected {expected}, got {result}")
    return f"{passed}/{len(test_cases)} tests passed."


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
    # checkout_system = Checkout()
    # return checkout_system.calculate_price(skus)
    pass


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




