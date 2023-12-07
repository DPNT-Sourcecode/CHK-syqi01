# noinspection PyUnusedLocal
# friend_name = unicode string
# def hello(param):
#     """
#     param is a string, for now, we ignore it
#     prepare the message you wish to return
#     """
#     print(f"Hello {param}")
#     return "Hello, World!"


# hello("world!")


# noinspection PyUnusedLocal
def hello(friend_name):
    """
    friend_name is a string containing the name of a friend.
    Returns a greeting string saying hello to the friend.
    """
    return f"Hello, {friend_name}!"


# Testing the function
print(hello("John"))  # Should print "Hello, John!"


# HLO_R2
# ROUND 2 - Hello friend

# This is the last round of the warmup.
# Once you complete it, you should be able to start the official challenge.

# You are given the name of a friend. Say hello to them!
# Example: if name of friend is "John" than return "Hello, John!".

# Notes:
#  - Use the provided parameter.

# In order to complete the round you need to implement the following method:
#      hello(String) -> String

# Where:
#  - param[0] = a String containing a name
#  - @return = a String containing a message
