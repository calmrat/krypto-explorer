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

import asyncio
from dataclasses import dataclass

from qrypt.tokens.services.coingecko.strategies import (
    EndpointCoinsMarketDataStrategy,
    EndpointSimpleSupportedVsCurrenciesStrategy,
)

# Declare constants
DEFAULT_TIMEOUT_SECONDS: int = 10

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

    api: CoinGeckoAPI
    base_url: str
    timeout: int

    def __init__(
        self, base_url: str = API_URL_BASE_v3, timeout: int = DEFAULT_TIMEOUT_SECONDS
    ):
        self.base_url = base_url
        self.timeout = timeout

        if self.base_url == API_URL_BASE_v3:
            self.api = CoinGeckoAPIv3(
                base_url=self.base_url,
                timeout=self.timeout,
                simple_supported_vs_currencies=EndpointSimpleSupportedVsCurrenciesStrategy(
                    base_url=self.base_url,
                    endpoint="simple/supported_vs_currencies",
                    method="GET",
                    headers={"accept": "application/json"},
                    params=dict(),
                    data=dict(),
                    timeout=self.timeout,
                ),
                coins_markets_data=EndpointCoinsMarketDataStrategy(
                    base_url=self.base_url,
                    endpoint="coins/markets",
                    method="GET",
                    headers={"accept": "application/json"},
                    params=dict(),
                    data=dict(),
                    timeout=self.timeout,
                ),
            )
        else:
            raise ValueError(f"Unsupported API URL: {self.base_url}")


if __name__ == "__main__":
    client = CoinGeckoAdapter()

    async def main():
        # Fetch supported vs currencies
        supported_vs_currencies = (
            await client.api.simple_supported_vs_currencies.fetch()
        )
        print(supported_vs_currencies)

    asyncio.run(main())

    import ipdb

    ipdb.set_trace()  # noqa: E402
