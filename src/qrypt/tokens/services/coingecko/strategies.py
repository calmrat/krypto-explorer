# -*- coding: utf-8 -*-

"""
Qrypto - CoinGecko Service - Endpoints

This module contains the Coingecko service endpoints for the Qrypto application.
It provides functions to interact with the CoinGecko API.


Simple (Free) Endpoints:
* simple/supported_vs_currencies
* coins/markets

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import aiohttp

API_URL_BASE_v3 = "https://api.coingecko.com/api/v3"


@dataclass
class EndpointStrategyBase(ABC):
    """
    Endpoint call to get the supported vs currencies from CoinGecko
    """

    base_url: str
    endpoint: str
    method: str
    headers: dict
    params: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)
    timeout: int = 10

    @abstractmethod
    async def fetch(self) -> Optional[dict]:
        """
        Fetch the supported vs currencies from CoinGecko
        :return: The supported vs currencies
        """
        raise NotImplementedError("Subclasses must implement this method")

    async def __call__(self) -> Optional[dict]:
        """
        Call the fetch method
        :return: The supported vs currencies
        """
        return await self.fetch()


@dataclass
class EndpointSimpleSupportedVsCurrenciesStrategy(EndpointStrategyBase):
    """
    Endpoint call to get the supported vs currencies from CoinGecko
    """

    async def fetch(self) -> Optional[dict]:
        """
        Fetch the supported vs currencies from CoinGecko
        :return: The supported vs currencies
        """
        print("Fetching supported vs currencies from CoinGecko")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{self.endpoint}",
                headers=self.headers,
                params=self.params,
                timeout=aiohttp.ClientTimeout(self.timeout),
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error: {response.status} - {response.reason}")
                    # Handle error response
                    response.raise_for_status()
        return None


@dataclass
class EndpointCoinsMarketDataStrategy(EndpointStrategyBase):
    """
    Endpoint to get the market data for a specific coin from CoinGecko
    """

    async def fetch(self) -> Optional[dict]:
        """
        Fetch the market data for a specific coin from CoinGecko
        :return: The market data for the specific coin
        """
        print("Fetching market data for a specific coin from CoinGecko")
        return None


ENDPOINT_STRATEGY_TYPES = (
    EndpointSimpleSupportedVsCurrenciesStrategy | EndpointCoinsMarketDataStrategy
)
