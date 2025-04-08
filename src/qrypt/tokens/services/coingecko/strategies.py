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

from qrypt.tokens.services.coingecko.constants import DEFAULT_TIMEOUT_SECONDS


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
    timeout: int = DEFAULT_TIMEOUT_SECONDS

    @property
    def url(self) -> str:
        if not self.base_url:
            raise ValueError("Base URL is not set")
        if not self.base_url.startswith("http"):
            raise ValueError("Base URL must start with http or https")

        # Ensure the base URL ends with a slash
        # and the endpoint does not start with a slash
        if not self.base_url.endswith("/"):
            self.base_url += "/"
        if not self.endpoint:
            raise ValueError("Endpoint is not set")
        if self.endpoint.startswith("/"):
            self.endpoint = self.endpoint[1:]
        return f"{self.base_url}{self.endpoint}"

    async def __call__(self) -> Optional[dict]:
        """
        Call the fetch method
        :return: The supported vs currencies
        """
        return await self.fetch()

    async def _get(
        self,
        headers: dict = dict(),
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> Optional[dict]:
        """
        Asynchronous GET request to the endpoint

        :param params: The parameters to send with the request
        :param timeout: The timeout for the request
        :return: The response from the endpoint
        """
        print("Calling GET on endpoint")
        print(f"URL: {self.url}")
        print(f"Headers: {headers}")
        print(f"Params: {params}")
        print(f"Data: {data}")
        print(f"Timeout: {timeout}")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                headers=headers,
                params=params,
                timeout=aiohttp.ClientTimeout(timeout),
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error: {response.status} - {response.reason}")
                    response.raise_for_status()
        return None

    @abstractmethod
    async def fetch(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> Optional[dict]:
        """
        Fetch the endpoint data. This method should be implemented by subclasses.
        :param params: The parameters to send with the request (optional)
        :param data: The data to send with the request (optional)
        :param timeout: The timeout for the request (optional)
        :raises ValueError: If the base URL is not set or does not start with http
        :raises ValueError: If the endpoint is not set or starts with a slash
        :raises ValueError: If the base URL does not end with a slash
        :raises ValueError: If the endpoint does not start with a slash
        :raises ValueError: If the endpoint is not set
        :raises ValueError: If the base URL is not set
        :raises ValueError: If the base URL does not start with http

        :return: endpoint response
        """
        raise NotImplementedError("Subclasses must implement this method")


@dataclass
class EndpointSimpleSupportedVsCurrenciesStrategy(EndpointStrategyBase):
    """
    Endpoint call to get the supported vs currencies from CoinGecko
    """

    async def fetch(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> Optional[dict]:
        """
        Fetch the supported vs currencies from CoinGecko
        :return: The supported vs currencies
        """
        print("Fetching supported vs currencies from CoinGecko")
        return await self._get(params=params, data=data, timeout=timeout)


@dataclass
class EndpointCoinsMarketDataStrategy(EndpointStrategyBase):
    """
    Endpoint to get the market data for a specific coin from CoinGecko
    """

    async def fetch(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> Optional[dict]:
        """
        Fetch the supported vs currencies from CoinGecko
        :return: The supported vs currencies
        """
        print("Fetching Coin Market Data from CoinGecko")
        return await self._get(params=params, data=data, timeout=timeout)


ENDPOINT_STRATEGY_TYPES = (
    EndpointSimpleSupportedVsCurrenciesStrategy | EndpointCoinsMarketDataStrategy
)
