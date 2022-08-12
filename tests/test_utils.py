"""Unit tests for src/utils.py ."""

import pytest
from utils import get_item_list, merge_dictionaries


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
    """Compares the output of `merge_dictionaries` with pre-defined samples.

    Args:
        test_dict1 (dict): Dictionary 1 to merge with dict 2
        test_dict2 (dict): Dictionary 2 to merge with dict 1
        expected (dict): Expected dict after d1 & d2 are merged
    """
    assert merge_dictionaries(test_dict1, test_dict2) == expected


@pytest.mark.parametrize(
    "test_dict, test_key, expected",
    [
        ({"a": [1, 2, 3]}, "a", [1, 2, 3]),
        ({"b": "pineapple"}, "b", []),
        ({"c": "pineapple"}, "not_c", []),
    ],
)
def test_get_item_list(test_dict: dict, test_key: str, expected: list) -> None:
    """Tests extracting a list from a given dict regardless of whether the key exists.

    Args:
        test_dict (dict): Sample dictionary for testing
        test_key (str): Desired key to extract
        expected (_type_): Expected response value
    """
    assert get_item_list(test_dict, test_key) == expected
