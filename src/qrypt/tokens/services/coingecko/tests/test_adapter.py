# -*- coding: utf-8 -*-

"""
Crypto Explorer CLI - Token Services - Tests

This module contains the tests for the CoinGecko service for the Krypto Explorer application.

"""

import pytest

from qrypt.tokens.services.coingecko.adapter import CoinGeckoAdapter


@pytest.mark.live_api
async def test_coingecko_adapter__simple_supported_vs_currencies():
    """
    Test the CoinGeckoAdapter class.
    """
    # Create an instance of the CoinGeckoAdapter
    # with the default endpoint strategy

    client = CoinGeckoAdapter()

    # Fetch supported vs currencies
    supported_vs_currencies = await client.api.simple_supported_vs_currencies.fetch()

    # Check if the response is a list
    assert isinstance(supported_vs_currencies, list)
    assert len(supported_vs_currencies) > 0
    assert all(isinstance(item, str) for item in supported_vs_currencies)

    # Check if the response contains expected currencies (e.g., "btc", "eth", "bnb")
    assert set(["btc", "eth", "bnb"]).intersection(set(supported_vs_currencies))


@pytest.mark.live_api
async def test_coingecko_adapter__coins_markets():
    """
    Test the CoinGeckoAdapter class.
    """
    # Create an instance of the CoinGeckoAdapter
    # with the default endpoint strategy

    client = CoinGeckoAdapter()

    # Fetch market data for a specific coin
    params = {"vs_currency": "usd", "ids": "bitcoin"}
    market_data = await client.api.coins_markets_data.fetch(params=params)

    # Check if the response is a list
    assert isinstance(market_data, list)
    assert len(market_data) > 0

    # Check if the first item in the list is a dictionary
    assert isinstance(market_data[0], dict)

    # Check if the response contains expected keys
    assert "id" in market_data[0]
    assert "symbol" in market_data[0]

    print(market_data[0])


@pytest.mark.live_api
async def test_coingecko_adapter__coins_list():
    """
    Test the CoinGeckoAdapter class.
    """
    # Create an instance of the CoinGeckoAdapter
    # with the default endpoint strategy

    client = CoinGeckoAdapter()

    # Fetch market data for a specific coin
    response = await client.api.coins_list.fetch()

    # Check if the response is a list
    assert isinstance(response, list)
    assert len(response) > 0

    # Check if the first item in the list is a dictionary
    assert isinstance(response[0], dict)

    # Check if the response contains expected keys
    assert "id" in response[0]
    assert "symbol" in response[0]

    print(response[0])
