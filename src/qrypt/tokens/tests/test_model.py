# -*- coding: utf-8 -*-

"""
Qrypto - Token Models - Tests
"""

import pytest

from qrypt.tokens.models import Token

# We don't really need to test these SQLalchemy models
# more than to 'pin' them in place and make sure they are
# not changed by accident.


@pytest.fixture
def sample_token():
    return Token(
        id=1,
        ext_id="_",
        symbol="BTC",
        name="Bitcoin",
        logo_url="http://example.com/logo.png",
    )


def test_token_creation(sample_token):
    assert sample_token.id == 1
    assert sample_token.ext_id == "_"
    assert sample_token.symbol == "BTC"
    assert sample_token.name == "Bitcoin"
    assert sample_token.logo_url == "http://example.com/logo.png"
