# import pytest

# from lib.solutions.HLO.hello_solution import hello


# # Happy path tests with various realistic test values
# @pytest.mark.parametrize(
#     "param, expected",
#     [
#         pytest.param("world!", "Hello, World!", id="happy-world"),
#         pytest.param("John", "Hello, World!", id="happy-john"),
#         pytest.param("Jane", "Hello, World!", id="happy-jane"),
#         pytest.param("123", "Hello, World!", id="happy-numeric"),
#         pytest.param("user@example.com", "Hello, World!", id="happy-email"),
#     ],
# )
# def test_hello_happy_path(param, expected, capsys):
#     # Act
#     result = hello(param)

#     # Assert
#     captured = capsys.readouterr()
#     assert captured.out == f"Hello {param}\n"
#     assert result == expected


# # Edge cases
# @pytest.mark.parametrize(
#     "param, expected",
#     [
#         pytest.param("", "Hello, World!", id="edge-empty-string"),
#         pytest.param(" ", "Hello, World!", id="edge-space"),
#         pytest.param("\t", "Hello, World!", id="edge-tab"),
#         pytest.param("\n", "Hello, World!", id="edge-newline"),
#     ],
# )
# def test_hello_edge_cases(param, expected, capsys):
#     # Act
#     result = hello(param)

#     # Assert
#     captured = capsys.readouterr()
#     assert captured.out == f"Hello {param}\n"
#     assert result == expected


# # Error cases
# # @pytest.mark.parametrize(
# #     "param",
# #     [
# #         pytest.param(None, id="error-none"),
# #         pytest.param(123, id="error-numeric"),
# #         pytest.param([], id="error-list"),
# #         pytest.param({}, id="error-dict"),
# #     ],
# # )
# # def test_hello_error_cases(param, capsys):
# #     # Act and Assert
# #     with pytest.raises(TypeError):
# #         hello(param)

