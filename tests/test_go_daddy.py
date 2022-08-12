"""Unit tests for src/go_daddy.py."""

import os
from typing import TYPE_CHECKING, List  # noqa

import pytest
from marko_namo.go_daddy import GoDaddy

if TYPE_CHECKING:
    from pytest import FixtureRequest as __FixtureRequest

    class FixtureRequest(__FixtureRequest):
        """Overload class for pytest fixtures to include typing."""

        param: str

else:
    from pytest import FixtureRequest


@pytest.fixture(params=["OTE", "PROD"])
def setup_go_daddy(request: FixtureRequest) -> GoDaddy:
    """Create an instance of GoDaddy to test against.

    Args:
        request (FixtureRequest): Pytest fixture request object

    Returns:
        GoDaddy: Instantiated GoDaddy client
    """
    if request.param == "PROD":

        gd_client = GoDaddy(
            key=os.environ["GODADDY_PROD_KEY"],
            secret=os.environ["GODADDY_PROD_SECRET"],
            env=request.param,
        )

    elif request.param == "OTE":
        gd_client = GoDaddy(
            key=os.environ["GODADDY_OTE_KEY"],
            secret=os.environ["GODADDY_OTE_SECRET"],
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
    """Provides example domains & checks the availability information is returned.

    Args:
        setup_go_daddy (object): Instantiated Object
        domains (List[str]): Sample domains to check
        extensions (List[str]): Desired extensions; .com, etc
        num_expected (int): Expected number of responses
    """
    response = setup_go_daddy.check_domain_availability(domains, extensions)  # type: ignore
    assert isinstance(response, dict)
    assert len(response["domains"]) == num_expected


def test_wrong_env() -> None:
    """Tests passing in an invalid environment."""
    with pytest.raises(Exception):
        GoDaddy(
            key=os.environ["GODADDY_PROD_KEY"],
            secret=os.environ["GODADDY_PROD_SECRET"],
            env="incorrect environment name",
        )
