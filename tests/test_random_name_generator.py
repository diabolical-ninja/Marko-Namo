"""Unit tests for src/random_name_generator.py"""

import os
from typing import List
from unicodedata import name

from src.random_name_generator import RandomNameGenerator
from src.go_daddy import GoDaddy
import pytest


@pytest.fixture(params=["OTE", "PROD", "NO_DADDY"])
def setup_go_daddy(request) -> None:
    """Create an instance of GoDaddy to test against.

    Returns:
        GoDaddy: Instantiated GoDaddy client
    """
    gd_client = None
    if request.param == "PROD":

        gd_client = GoDaddy(
            key=os.getenv("GODADDY_PROD_KEY"),
            secret=os.getenv("GODADDY_PROD_SECRET"),
            env=request.param,
        )

    elif request.param == "OTE":
        gd_client = GoDaddy(
            key=os.getenv("GODADDY_OTE_KEY"),
            secret=os.getenv("GODADDY_OTE_SECRET"),
            env=request.param,
        )

    return gd_client


@pytest.mark.parametrize(
    "test_word, n_grams, expected",
    [
        (
            "abc",
            [],
            {},
        ),
        (
            "abc",
            [1],
            {
                "a": ["b"],
                "b": ["c"],
                "c": [None],
            },
        ),
        (
            "abc",
            [1, 2],
            {
                "a": ["b", "bc"],
                "b": ["c", None],
                "c": [None, None],
                "ab": ["c", None],
                "bc": [None, None],
            },
        ),
        (
            "abc",
            [2, 4],
            {
                "ab": [None, None],
                "bc": [None, None],
            },
        ),
        ("", [1, 2], {}),
    ],
)
def test_word_letter_frequency(
    test_word: str, n_grams: List[str], expected: dict
) -> None:

    rng = RandomNameGenerator(
        name_length=1,
        number_of_names=1,
        domain_extensions=[],
        training_words=[],
        n_grams=n_grams,
        godaddy=None,
    )

    letter_frequencies = rng.word_letter_frequency(test_word)

    assert letter_frequencies == expected


@pytest.mark.parametrize(
    "word_list, max_word_length",
    [
        (["hello", "world"], 1),
        (["python"], 5),
        (["hello", "world", "test"], 10),
    ],
)
def test_create_random_word(word_list: List[str], max_word_length: int) -> None:

    rng = RandomNameGenerator(
        name_length=1,
        number_of_names=50,
        domain_extensions=[],
        training_words=[],
        n_grams=[1, 2],
        godaddy=None,
    )

    word = rng.create_random_word(word_list, max_word_length)

    assert len(word) <= max_word_length + 2
    assert isinstance(word, str)


@pytest.mark.parametrize(
    "inputs",
    [
        (
            {
                "name_length": 10,
                "number_of_names": 1,
                "domain_extensions": [".com"],
                "training_words": ["hello", "world"],
                "n_grams": [1],
            }
        ),
        (
            {
                "name_length": 5,
                "number_of_names": 10,
                "domain_extensions": [".ai", ".info"],
                "training_words": ["toasted", "sandwhich"],
                "n_grams": [2, 3],
            }
        ),
    ],
)
def test_create_random_names(setup_go_daddy, inputs: dict) -> None:

    rng = RandomNameGenerator(
        name_length=inputs["name_length"],
        number_of_names=inputs["number_of_names"],
        domain_extensions=inputs["domain_extensions"],
        training_words=inputs["training_words"],
        n_grams=inputs["n_grams"],
        godaddy=setup_go_daddy,
    )

    names, availability_info = rng.create_random_names()

    # Assess created names
    assert isinstance(names, list)
    assert all(isinstance(x, str) for x in names)
    assert len(names) <= inputs["number_of_names"]

    # Assess GoDaddy Response
    assert isinstance(availability_info, list) or availability_info is None
    if isinstance(availability_info, list) and len(availability_info) > 0:
        assert all(isinstance(x, dict) for x in availability_info)
