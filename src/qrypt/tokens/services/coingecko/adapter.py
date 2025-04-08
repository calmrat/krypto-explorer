# -*- coding: utf-8 -*-

"""
Qrypto - CoinGecko Service - Adapter

This module contains the CoinGecko service for the Qrypto application.

It provides functions to interact with the CoinGecko API.

Features:

Adapter
- Fetch known token symbols from CoinGecko
- Fetch known token symbol meta data from CoinGecko
- Fetch last token price from CoinGecko

Cache
- Cache all token symbol & related data



"""

from abc import ABC
from dataclasses import dataclass

from qrypt.tokens.services.coingecko.config import CoinGeckoConfig
from qrypt.tokens.services.coingecko.constants import (
    BASE_URL_V3,
    DEFAULT_TIMEOUT_SECONDS,
    HEADER_ACCEPT_JSON,
)
from qrypt.tokens.services.coingecko.strategies import (
    EndpointCoinsListStrategy,
    EndpointCoinsMarketDataStrategy,
    EndpointSimpleSupportedVsCurrenciesStrategy,
)


@dataclass(kw_only=True)
class CoinGeckoAPI(ABC):
    """
    CoinGecko API
    """

    base_url: str
    timeout: int


@dataclass(kw_only=True)
class CoinGeckoAPIv3(CoinGeckoAPI):
    """
    Supported Endpoints for v3 of the CoinGecko API
    """

    simple_supported_vs_currencies: EndpointSimpleSupportedVsCurrenciesStrategy
    coins_markets_data: EndpointCoinsMarketDataStrategy
    coins_list: EndpointCoinsListStrategy


class CoinGeckoAdapter:
    """CoinGecko Adapter"""

    api: CoinGeckoAPIv3
    base_url: str
    timeout: int
    headers: dict

    def __init__(self, base_url: str, timeout: int, headers: dict):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers
        self.config = CoinGeckoConfig()

        if self.base_url == BASE_URL_V3:
            # Initialize the API with the v3 endpoints

            # Create the API object with the v3 endpoints
            self.api = CoinGeckoAPIv3(
                base_url=self.base_url,
                timeout=self.timeout,
                simple_supported_vs_currencies=EndpointSimpleSupportedVsCurrenciesStrategy(
                    base_url=self.base_url,
                    endpoint="simple/supported_vs_currencies",
                    method="GET",
                    headers=self.headers,
                    timeout=self.timeout,
                ),
                # Create the coins market data endpoint
                coins_markets_data=EndpointCoinsMarketDataStrategy(
                    base_url=self.base_url,
                    endpoint="coins/markets",
                    method="GET",
                    headers=self.headers,
                    timeout=self.timeout,
                    params={"vs_currency": self.config.vs_currency},
                ),
                # Create the coins list endpoint
                coins_list=EndpointCoinsListStrategy(
                    base_url=self.base_url,
                    endpoint="coins/list",
                    method="GET",
                    headers=self.headers,
                    timeout=self.timeout,
                    params={"include_platform": "true"},
                ),
            )
        else:
            raise ValueError(f"Unsupported API URL: {self.base_url}")
