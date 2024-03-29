"""Unit tests for src/random_name_generator.py ."""

import os
from typing import List, Optional

import pytest
from marko_namo.marko_namo import MarkoNamo


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
    test_word: str, n_grams: Optional[List[int]], expected: dict
) -> None:
    """Passes in sample words & ensures the generated frequency table matches the expected output.

    Args:
        test_word (str): Word to test with
        n_grams (List[str]): n-grams to test with, eg [1] or [2,4,5], etc
        expected (dict): Expected frequency table that should be outputted
    """
    rng = MarkoNamo(
        name_length=1,
        number_of_names=1,
        domain_extensions=[],
        training_words=[],
        n_grams=n_grams,
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
    """Generate a random word & ensure they match the expected generation criteria.

    Args:
        word_list (List[str]): Words to learn from
        max_word_length (int): Maximum word length to generate
    """
    rng = MarkoNamo(
        name_length=1,
        number_of_names=50,
        domain_extensions=[],
        training_words=[],
        n_grams=[1, 2],
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
                "godaddy_key": os.getenv("GODADDY_PROD_KEY"),
                "godaddy_secret": os.getenv("GODADDY_PROD_SECRET"),
                "godaddy_env": os.getenv("GODADDY_PROD_ENV"),
            }
        ),
        (
            {
                "name_length": 5,
                "number_of_names": 0,
                "domain_extensions": [".ai", ".info"],
                "training_words": ["toasted", "sandwhich"],
                "n_grams": [2, 3],
                "godaddy_key": os.getenv("GODADDY_OTE_KEY"),
                "godaddy_secret": os.getenv("GODADDY_OTE_SECRET"),
                "godaddy_env": os.getenv("GODADDY_OTE_ENV"),
            }
        ),
        (
            {
                "name_length": 5,
                "number_of_names": 10,
                "domain_extensions": [".ai", ".info"],
                "training_words": ["toasted", "sandwhich"],
                "n_grams": [2, 3],
                "godaddy_key": os.getenv("GODADDY_OTE_KEY"),
                "godaddy_secret": os.getenv("GODADDY_OTE_SECRET"),
                "godaddy_env": os.getenv("GODADDY_OTE_ENV"),
            }
        ),
        (
            {
                "name_length": 5,
                "number_of_names": 10,
                "domain_extensions": [".ai", ".info"],
                "training_words": ["toasted", "sandwhich"],
                "n_grams": [2, 3],
                "godaddy_key": None,
                "godaddy_secret": None,
                "godaddy_env": None,
            }
        ),
    ],
)
def test_create_random_names(inputs: dict) -> None:
    """Generate a suite of random words & ensure they match the expected generation criteria.

    Args:
        inputs (dict): Testing parameter suite that should match:
            - The config.yml &
            - RandomNameGenerator init parameters
    """
    rng = MarkoNamo(
        name_length=inputs["name_length"],
        number_of_names=inputs["number_of_names"],
        domain_extensions=inputs["domain_extensions"],
        training_words=inputs["training_words"],
        n_grams=inputs["n_grams"],
        godaddy_key=inputs["godaddy_key"],
        godaddy_secret=inputs["godaddy_secret"],
        godaddy_env=inputs["godaddy_env"],
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


def test_config_usage() -> None:
    """Tests reading & using the config file."""
    rng = MarkoNamo(config_file="tests/test_config.yml")

    names, availability_info = rng.create_random_names()

    # Assess created names
    assert isinstance(names, list)
    assert all(isinstance(x, str) for x in names)
    assert len(names) <= 5

    # Assess GoDaddy Response
    assert isinstance(availability_info, list) or availability_info is None
    if isinstance(availability_info, list) and len(availability_info) > 0:
        assert all(isinstance(x, dict) for x in availability_info)
