"""Unit tests for src/utils.py"""

from utils import merge_dictionaries, get_item_list
import pytest


@pytest.mark.parametrize(
    "test_dict1, test_dict2, expected",
    [
        ({"a": [1, 2, 3]}, {"a": [1, 2, 3]}, {"a": [1, 2, 3, 1, 2, 3]}),
        ({"a": [1, 2, 3]}, {"b": [1, 2, 3]}, {"a": [1, 2, 3], "b": [1, 2, 3]}),
        ({"a": [1, 2, 3]}, {}, {"a": [1, 2, 3]}),
        ({"a": [1, 2, 3]}, {"b": "a string"}, {"a": [1, 2, 3], "b": []}),
    ],
)
def test_merge_dictionaries(test_dict1: dict, test_dict2: dict, expected: dict) -> None:

    assert merge_dictionaries(test_dict1, test_dict2) == expected


@pytest.mark.parametrize(
    "test_dict, test_key, expected",
    [
        ({"a": [1, 2, 3]}, "a", [1, 2, 3]),
        ({"b": "pineapple"}, "b", []),
        ({"c": "pineapple"}, "not_c", []),
    ],
)
def test_get_item_list(test_dict: dict, test_key: str, expected) -> None:

    assert get_item_list(test_dict, test_key) == expected
