import pytest

from lib.solutions.HLO.hello_solution import hello


class TestHello:
    def test_hello(self):
        # Test with a sample name
        assert hello("John") == "Hello, John!", "The greeting was not correct"

        # You can add more tests with different names here
        assert hello("Alex") == "Hello, Alex!", "The greeting was not correct"
        assert hello("Sarah") == "Hello, Sarah!", "The greeting was not correct"


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "friend_name, expected",
    [
        pytest.param("Alice", "Hello, Alice!", id="happy_path_alice"),
        pytest.param("Bob", "Hello, Bob!", id="happy_path_bob"),
        pytest.param("Charlie", "Hello, Charlie!", id="happy_path_charlie"),
    ],
)
def test_hello_happy_path(friend_name, expected):
    # Act
    result = hello(friend_name)

    # Assert
    assert result == expected


# Edge cases
@pytest.mark.parametrize(
    "friend_name, expected",
    [
        pytest.param("", "Hello, !", id="edge_case_empty_string"),
        pytest.param(" ", "Hello,  !", id="edge_case_space"),
        pytest.param("123", "Hello, 123!", id="edge_case_numeric"),
        pytest.param("A" * 1000, f"Hello, {'A' * 1000}!", id="edge_case_long_name"),
    ],
)
def test_hello_edge_cases(friend_name, expected):
    # Act
    result = hello(friend_name)

    # Assert
    assert result == expected


# # Error cases
# @pytest.mark.parametrize(
#     "friend_name",
#     [
#         pytest.param(None, id="error_case_none"),
#         pytest.param(123, id="error_case_numeric"),
#         pytest.param(True, id="error_case_boolean"),
#     ],
# )
# def test_hello_error_cases(friend_name):
#     # Act and Assert
#     with pytest.raises(TypeError):
#         hello(friend_name)
