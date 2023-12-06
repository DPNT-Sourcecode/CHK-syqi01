from hello_solution import hello

words = hello("anything")
print(words)

# test_hello_world.py

# Function to be tested
# def hello(_):
# return "Hello, world!"


# Test for the function
# test class
class TestHelloWorld:
    # test method
    def test_hello(self):
        assert hello("any string") == "Hello, world!"


# This allows pytest to run the test when this file is executed
if __name__ == "__main__":
    import pytest

    pytest.main()
