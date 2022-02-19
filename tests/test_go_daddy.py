"""Unit tests for src/go_daddy.py."""

from typing import List
import os

from src.go_daddy import GoDaddy

import pytest


@pytest.fixture(params=["OTE", "PROD"])
def setup_go_daddy(request) -> None:
    """Create an instance of GoDaddy to test against.

    Returns:
        GoDaddy: Instantiated GoDaddy client
    """
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
    "domains, extensions, num_expected",
    [
        ([], [], 0),
        (["google", "apple", "daskgljhas"], [".com"], 3),
        (["google", "apple", "daskgljhas"], [".com", ".com.au"], 6),
    ],
)
def test_check_domain_availability(
    setup_go_daddy: object, domains: List[str], extensions: List[str], num_expected: int
) -> None:

    response = setup_go_daddy.check_domain_availability(domains, extensions)
    assert isinstance(response, dict)
    assert len(response.get("domains")) == num_expected
