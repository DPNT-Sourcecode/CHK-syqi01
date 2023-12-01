# Where:
#  - param[0] = a positive integer between 0-100
#  - param[1] = a positive integer between 0-100
#  - @return = an Integer representing the sum of the two numbers
import sys

sys.path.append("/Users/alexfoster/Documents/Code/accelerate_runner")

print(sys.path)


def sum(x: int, y: int) -> int:
    if not (0 <= x <= 100) or not (0 <= y <= 100):
        raise ValueError("Arguments must be integers between 1 and 100 (inclusive)")
    return x + y


print(sum(7, 99))
