from pprint import pprint
import re

pricing_table_string = """
+------+-------+---------------------------------+
| Item | Price | Special offers                  |
+------+-------+---------------------------------+
| A    | 50    | 3A for 130, 5A for 200          |
| B    | 30    | 2B for 45                       |
| C    | 20    |                                 |
| D    | 15    |                                 |
| E    | 40    | 2E get one B free               |
| F    | 10    | 2F get one F free               |
| G    | 20    |                                 |
| H    | 10    | 5H for 45, 10H for 80           |
| I    | 35    |                                 |
| J    | 60    |                                 |
| K    | 70    | 2K for 120                      |
| L    | 90    |                                 |
| M    | 15    |                                 |
| N    | 40    | 3N get one M free               |
| O    | 10    |                                 |
| P    | 50    | 5P for 200                      |
| Q    | 30    | 3Q for 80                       |
| R    | 50    | 3R get one Q free               |
| S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| U    | 40    | 3U get one U free               |
| V    | 50    | 2V for 90, 3V for 130           |
| W    | 20    |                                 |
| X    | 17    | buy any 3 of (S,T,X,Y,Z) fr 45 |
| Y    | 20    | buy any 3 of (S,T,X,Y,Z) fr 45 |
| Z    | 21    | buy any 3 of (S,T,X,Y,Z) fr 45 |
+------+-------+---------------------------------+"""
#
# """
# +------+-------+------------------------+
# | Item | Price | Special offers         |
# +------+-------+------------------------+
# | A    | 50    | 3A for 130, 5A for 200 |
# | B    | 30    | 2B for 45              |
# | C    | 20    |                        |
# | D    | 15    |                        |
# | E    | 40    | 2E get one B free      |
# | F    | 10    | 2F get one F free      |
# | G    | 20    |                        |
# | H    | 10    | 5H for 45, 10H for 80  |
# | I    | 35    |                        |
# | J    | 60    |                        |
# | K    | 80    | 2K for 150             |
# | L    | 90    |                        |
# | M    | 15    |                        |
# | N    | 40    | 3N get one M free      |
# | O    | 10    |                        |
# | P    | 50    | 5P for 200             |
# | Q    | 30    | 3Q for 80              |
# | R    | 50    | 3R get one Q free      |
# | S    | 30    |                        |
# | T    | 20    |                        |
# | U    | 40    | 3U get one U free      |
# | V    | 50    | 2V for 90, 3V for 130  |
# | W    | 20    |                        |
# | X    | 90    |                        |
# | Y    | 10    |                        |
# | Z    | 50    |                        |
# +------+-------+------------------------+"""


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
                if "buy any" in offer:
                    # Example offer: "buy any 3 of STXYZ for 45"
                    parts = offer.split(" ")
                    count = extract_number(parts[2])  # The required count
                    group_items = parts[
                        4
                    ]  # The group of items involved (e.g., "STXYZ")
                    special_price = int(parts[-1])  # The special price

                    parsed_offers[offer] = {
                        "type": "cross-product",
                        "input": [
                            {
                                "items": list(group_items),
                                "count": count,
                                "price_calc": "variable",
                            }
                        ],
                        "output": [
                            {
                                "items": list(group_items),
                                "count": count,
                                "t_price": float(special_price),
                            }
                        ],
                    }

                if "for" in offer:
                    # Simple offers like "3A for 130"
                    parts = offer.split(" ")
                    count = extract_number(parts[0])
                    total_price = int(parts[2])
                    parsed_offers[offer] = {
                        "input": [
                            {
                                item: item,
                                "count": count,
                                "t_price": float(price * count),
                                "price_calc": f"{count}*{price}",
                            }
                        ],
                        "output": [
                            {
                                item: item,
                                "count": count,
                                "t_price": float(total_price),
                                "price_calc": str(total_price),
                            }
                        ],
                    }

                elif "get one" in offer:
                    # Offers like "2E get one B free"
                    (
                        primary_item_count,
                        free_item,
                        free_item_price,
                    ) = parse_get_one_free_offer(item, price, offer, data)

                    parsed_offers[offer] = {
                        "input": [
                            {
                                "item": item,
                                "count": primary_item_count,
                                "t_price": float(price * primary_item_count),
                                "price_calc": f"{primary_item_count}*{price}",
                            },
                            {
                                "item": free_item,
                                "count": 1,
                                "t_price": float(free_item_price),
                                "price_calc": f"1*{free_item_price}",
                            },
                        ],
                        "output": [
                            {
                                "item": item,
                                "count": primary_item_count,
                                "t_price": float(price * primary_item_count),
                                "price_calc": f"{primary_item_count}*{price}",
                            },
                            {
                                "item": free_item,
                                "count": 1,
                                "t_price": 0.0,
                                "price_calc": "0*1",
                            },
                        ],
                    }
            else:
                # Default offer (no special offer)
                parsed_offers[""] = {
                    "input": [
                        {
                            item: item,
                            "count": 1,
                            "t_price": float(price),
                            "price_calc": "",
                        }
                    ],
                    "output": [
                        {
                            item: item,
                            "count": 1,
                            "t_price": float(price),
                            "price_calc": "",
                        }
                    ],
                }

    return parsed_offers


def extract_number(s):
    match = re.search(r"\d+", s)
    return int(match.group()) if match else None


# Helper function to parse "get one free" offers
def parse_get_one_free_offer(item, price, offer, data):
    parts = offer.split(" ")
    primary_item_count = int(parts[0][0])  # Assuming the count is the first character
    free_item = parts[3]  # Assuming the free item is the last word in the offer
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

# snapshot for regression testing at speed
snapshot_1 = {
    "": {
        "input": [{"Z": "Z", "count": 1, "price_calc": "", "t_price": 50.0}],
        "output": [{"Z": "Z", "count": 1, "price_calc": "", "t_price": 50.0}],
    },
    "10H for 80": {
        "input": [{"H": "H", "count": 10, "price_calc": "10*10", "t_price": 100.0}],
        "output": [{"H": "H", "count": 10, "price_calc": "80", "t_price": 80.0}],
    },
    "2B for 45": {
        "input": [{"B": "B", "count": 2, "price_calc": "2*30", "t_price": 60.0}],
        "output": [{"B": "B", "count": 2, "price_calc": "45", "t_price": 45.0}],
    },
    "2E get one B free": {
        "input": [
            {"count": 2, "item": "E", "price_calc": "2*40", "t_price": 80.0},
            {"count": 1, "item": "B", "price_calc": "1*30", "t_price": 30.0},
        ],
        "output": [
            {"count": 2, "item": "E", "price_calc": "2*40", "t_price": 80.0},
            {"count": 1, "item": "B", "price_calc": "0*1", "t_price": 0.0},
        ],
    },
    "2F get one F free": {
        "input": [
            {"count": 2, "item": "F", "price_calc": "2*10", "t_price": 20.0},
            {"count": 1, "item": "F", "price_calc": "1*10", "t_price": 10.0},
        ],
        "output": [
            {"count": 2, "item": "F", "price_calc": "2*10", "t_price": 20.0},
            {"count": 1, "item": "F", "price_calc": "0*1", "t_price": 0.0},
        ],
    },
    "2K for 150": {
        "input": [{"K": "K", "count": 2, "price_calc": "2*80", "t_price": 160.0}],
        "output": [{"K": "K", "count": 2, "price_calc": "150", "t_price": 150.0}],
    },
    "2V for 90": {
        "input": [{"V": "V", "count": 2, "price_calc": "2*50", "t_price": 100.0}],
        "output": [{"V": "V", "count": 2, "price_calc": "90", "t_price": 90.0}],
    },
    "3A for 130": {
        "input": [{"A": "A", "count": 3, "price_calc": "3*50", "t_price": 150.0}],
        "output": [{"A": "A", "count": 3, "price_calc": "130", "t_price": 130.0}],
    },
    "3N get one M free": {
        "input": [
            {"count": 3, "item": "N", "price_calc": "3*40", "t_price": 120.0},
            {"count": 1, "item": "M", "price_calc": "1*15", "t_price": 15.0},
        ],
        "output": [
            {"count": 3, "item": "N", "price_calc": "3*40", "t_price": 120.0},
            {"count": 1, "item": "M", "price_calc": "0*1", "t_price": 0.0},
        ],
    },
    "3Q for 80": {
        "input": [{"Q": "Q", "count": 3, "price_calc": "3*30", "t_price": 90.0}],
        "output": [{"Q": "Q", "count": 3, "price_calc": "80", "t_price": 80.0}],
    },
    "3R get one Q free": {
        "input": [
            {"count": 3, "item": "R", "price_calc": "3*50", "t_price": 150.0},
            {"count": 1, "item": "Q", "price_calc": "1*30", "t_price": 30.0},
        ],
        "output": [
            {"count": 3, "item": "R", "price_calc": "3*50", "t_price": 150.0},
            {"count": 1, "item": "Q", "price_calc": "0*1", "t_price": 0.0},
        ],
    },
    "3U get one U free": {
        "input": [
            {"count": 3, "item": "U", "price_calc": "3*40", "t_price": 120.0},
            {"count": 1, "item": "U", "price_calc": "1*40", "t_price": 40.0},
        ],
        "output": [
            {"count": 3, "item": "U", "price_calc": "3*40", "t_price": 120.0},
            {"count": 1, "item": "U", "price_calc": "0*1", "t_price": 0.0},
        ],
    },
    "3V for 130": {
        "input": [{"V": "V", "count": 3, "price_calc": "3*50", "t_price": 150.0}],
        "output": [{"V": "V", "count": 3, "price_calc": "130", "t_price": 130.0}],
    },
    "5A for 200": {
        "input": [{"A": "A", "count": 5, "price_calc": "5*50", "t_price": 250.0}],
        "output": [{"A": "A", "count": 5, "price_calc": "200", "t_price": 200.0}],
    },
    "5H for 45": {
        "input": [{"H": "H", "count": 5, "price_calc": "5*10", "t_price": 50.0}],
        "output": [{"H": "H", "count": 5, "price_calc": "45", "t_price": 45.0}],
    },
    "5P for 200": {
        "input": [{"P": "P", "count": 5, "price_calc": "5*50", "t_price": 250.0}],
        "output": [{"P": "P", "count": 5, "price_calc": "200", "t_price": 200.0}],
    },
}


# snapshot function
for offer in parsed_special_offers.keys():
    if (
        snapshot_1[offer]["input"] == parsed_special_offers[offer]["input"]
        and snapshot_1[offer]["output"] == parsed_special_offers[offer]["output"]
    ):
        pass
    else:
        print(f"offer: {offer}")
        print(f"input: {parsed_special_offers[offer]['input']}")
        print(f"output: {parsed_special_offers[offer]['output']}")
        print(f"snapshot: {snapshot_1[offer]}")
        print(f"snapshot test 1 {snapshot_1[offer]==parsed_special_offers[offer]}")
        print(
            f"snapshot test 2 {snapshot_1[offer]['input']==parsed_special_offers[offer]['input']}"
        )
        print(
            f"snapshot test 3 {snapshot_1[offer]['output']==parsed_special_offers[offer]['output']}"
        )

print(f"snapshot test 1 {snapshot_1 == parsed_special_offers}")


# Function to calculate savings for each offer and add to the dict
def calculate_savings(offers):
    for offer, details in offers.items():
        input_total = sum(item["t_price"] for item in details["input"])
        output_total = sum(item["t_price"] for item in details["output"])
        saving = input_total - output_total
        offers[offer]["saving"] = saving
    return offers


special_offers_w_savings = calculate_savings(parsed_special_offers)
pprint("\n\n special offers with savings")
pprint(special_offers_w_savings)

# now have savings for each offer, can sort by savings and apply offers in order of savings

# Sample shopping cart as a string
shopping_cart_str = "AAABAEEFF"

# Sort the offers based on savings
sorted_offers = sorted(
    special_offers_w_savings.items(),
    key=lambda x: x[1]["saving"],
    reverse=True,
)


def sort_cart(cart):
    # Convert the shopping cart string into a sorted list
    sorted_cart = sorted(list(shopping_cart_str))
    return sorted_cart


sorted_cart = sort_cart(shopping_cart_str)


# main function to calculate price
def apply_offers_to_cart_v2(cart, offers):
    # validate the cart using simple regex
    if cart == []:
        return 0
    regex_pattern = r"^[A-Z]+$"
    if not re.match(regex_pattern, "".join(cart)):
        return -1

    working_cart = cart.copy()
    total_price = 0

    for offer_name, offer_details in offers:
        if offer_name:  # Skip the empty offer
            # Initialize an empty dictionary for offer requirements
            offer_requirements = {}

            # Iterate through each item detail in the offer's input
            for item_details in offer_details["input"]:
                # Determine the item key (name)
                if "item" in item_details:
                    item_key = item_details["item"]
                else:
                    # If 'item' key is not present, use the first key (assuming it's the item name)
                    item_key = next(iter(item_details))

                # Accumulate the count for each item
                if item_key in offer_requirements:
                    offer_requirements[item_key] += item_details["count"]
                else:
                    offer_requirements[item_key] = item_details["count"]

            # Check if the offer can be applied
            can_apply_offer = all(
                working_cart.count(item) >= count
                for item, count in offer_requirements.items()
            )
            while can_apply_offer:
                # Apply the offer
                for output_item in offer_details["output"]:
                    total_price += output_item["t_price"]
                # Remove the used items from the working cart
                for item, count in offer_requirements.items():
                    for _ in range(count):
                        working_cart.remove(item)

                # Re-check if the offer can still be applied
                can_apply_offer = all(
                    working_cart.count(item) >= count
                    for item, count in offer_requirements.items()
                )

    # Calculate the price for items without offers
    for item in working_cart:
        item_price = float(pricing_table_dict[item]["Price"])
        total_price += item_price

    return total_price


total_cart_price_v2 = apply_offers_to_cart_v2(sorted_cart, sorted_offers)
print(f"\n\n total cart price : {total_cart_price_v2}")


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    sorted_cart = sorted(list(skus))
    best_price = apply_offers_to_cart_v2(sorted_cart, sorted_offers)
    return best_price


# total_cart_price_v2 = apply_offers_to_cart_v2(sorted_cart, sorted_offers)

# temp = checkout("AAAAA")
# pprint("FINAL CHECK")
# pprint(temp)


test_cases = [
    ("", 0),  # it was zero. changed back
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
    # ("FXF", -1), # this must be wrong. -1? Commenting out for now.
    ("FAB", 90),
    ("FFAB", 100),
    ("FFFAAA", 150),
    ("FFFFFFAB", 120),
    ("FFFFD", 45),
    ("FFFFFFFFFF", 70),
]


def quick_test(cart_function, test_cases):
    results = []
    for test_case in test_cases:
        try:
            input_str, expected = test_case
            sorted_cart = sorted(list(input_str))
            got = cart_function(sorted_cart, sorted_offers)
            result = f"I: {input_str} | E: {expected} | G: {got} | {'✅' if got == expected else '❌'}"
        except Exception as e:
            result = f"I: {input_str} | E: {expected} | Error: {str(e)} | ❌"
        results.append(result)
    return results


pprint(quick_test(apply_offers_to_cart_v2, test_cases))
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



