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

from dataclasses import dataclass

from qrypt.tokens.services.coingecko.constants import (
    DEFAULT_TIMEOUT_SECONDS,
    HEADER_ACCEPT_JSON,
)
from qrypt.tokens.services.coingecko.strategies import (
    EndpointCoinsMarketDataStrategy,
    EndpointSimpleSupportedVsCurrenciesStrategy,
)

# Base URL for CoinGecko API v3
API_URL_BASE_v3: str = "https://api.coingecko.com/api/v3"


@dataclass(kw_only=True)
class CoinGeckoAPI:
    """
    CoinGecko API
    """

    base_url: str = API_URL_BASE_v3
    timeout: int = DEFAULT_TIMEOUT_SECONDS


@dataclass(kw_only=True)
class CoinGeckoAPIv3(CoinGeckoAPI):
    """
    Supported Endpoints for v3 of the CoinGecko API
    """

    simple_supported_vs_currencies: EndpointSimpleSupportedVsCurrenciesStrategy
    coins_markets_data: EndpointCoinsMarketDataStrategy


class CoinGeckoAdapter:
    """CoinGecko Adapter"""

    api: CoinGeckoAPIv3
    base_url: str
    timeout: int

    def __init__(
        self, base_url: str = API_URL_BASE_v3, timeout: int = DEFAULT_TIMEOUT_SECONDS
    ):
        self.base_url = base_url
        self.timeout = timeout

        if self.base_url == API_URL_BASE_v3:
            # Initialize the API with the v3 endpoints

            # Create the API object with the v3 endpoints
            self.api = CoinGeckoAPIv3(
                base_url=self.base_url,
                timeout=self.timeout,
                simple_supported_vs_currencies=EndpointSimpleSupportedVsCurrenciesStrategy(
                    base_url=self.base_url,
                    endpoint="simple/supported_vs_currencies",
                    method="GET",
                    headers=HEADER_ACCEPT_JSON,
                    timeout=self.timeout,
                ),
                # Create the coins market data endpoint
                coins_markets_data=EndpointCoinsMarketDataStrategy(
                    base_url=self.base_url,
                    endpoint="coins/markets",
                    method="GET",
                    headers=HEADER_ACCEPT_JSON,
                    timeout=self.timeout,
                ),
            )
        else:
            raise ValueError(f"Unsupported API URL: {self.base_url}")
