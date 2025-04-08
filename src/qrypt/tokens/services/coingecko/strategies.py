# -*- coding: utf-8 -*-

"""
Qrypto - CoinGecko Service - Endpoints

This module contains the Coingecko service endpoints for the Qrypto application.
It provides functions to interact with the CoinGecko API.


Simple (Free) Endpoints:
* simple/supported_vs_currencies
* coins/markets

"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import aiohttp

from qrypt.core.log import logger as log
from qrypt.tokens.services.coingecko.constants import (
    DEFAULT_TIMEOUT_SECONDS,
    HEADER_ACCEPT_JSON,
    TTL_30_SECONDS,
)

type EndpointResponse = Optional[list[dict]]


def cached_token(key: str, jsonfile: Path, ttl: int = TTL_30_SECONDS):
    """
    Decorator to cache the token in a JSON file.
    :param jsonfile: The JSON file to cache the token in
    :return: The decorator
    """

    def load(key):
        with open(jsonfile, mode="r", encoding="utf8") as f:
            cache = json.load(f)
            _data = cache.get(key, [])
            data, ctime = _data.get("data"), _data.get("ctime")
            if not data:
                raise ValueError(f"Cache for {key} not found in {jsonfile}")
            if not ctime:
                raise ValueError(f"Cache for {key} has no ctime in {jsonfile}")
            return (data, ctime)

    def save(data):
        ctime = datetime.now(timezone.utc).timestamp()
        with open(jsonfile, mode="w", encoding="utf8") as f:
            json.dump({key: {"data": data, "ctime": ctime}}, f)
        return data

    def decorator(fn):
        async def wrapped(*args, **kwargs):
            if jsonfile.exists():
                try:
                    data, ctime = load(key)
                except ValueError as e:
                    log.debug("Cache not found: %s", e)
                else:
                    lifespan = datetime.now(timezone.utc).timestamp() - ctime
                    is_valid = lifespan < ttl
                    log.debug("Cache lifespan: %s", lifespan)
                    log.debug("Cache TTL: %s", ttl)
                    log.debug("Cache ctime: %s", ctime)
                    log.debug("Cache is_valid: %s", is_valid)

                    # Check if the data exists, and is still valid
                    if data and is_valid:
                        log.debug("🎯 | HIT - Loading from CACHE")
                        return data

            log.debug("⚡️ | MISS - Loading from LIVE API")
            res = await fn(*args, **kwargs)
            return save(res)

        return wrapped

    return decorator


@dataclass
class EndpointStrategyBase(ABC):
    """
    Endpoint call to get the supported vs currencies from CoinGecko
    """

    base_url: str
    endpoint: str
    method: str
    headers: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)
    timeout: int = DEFAULT_TIMEOUT_SECONDS

    @property
    def url(self) -> str:
        """Generate the full URL for the endpoint"""
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

    async def __call__(self) -> EndpointResponse:
        """
        Call the fetch method
        :return: The supported vs currencies
        """
        return await self.fetch(
            params=self.params, data=self.data, timeout=self.timeout
        )

    async def _get(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        headers: dict = dict(),
    ) -> EndpointResponse:
        """
        Asynchronous GET request to the endpoint

        :param params: The parameters to send with the request
        :param timeout: The timeout for the request
        :return: The response from the endpoint
        """
        log.debug("Calling GET on endpoint")

        headers = headers if headers else HEADER_ACCEPT_JSON

        log.debug("URL: %s", self.url)
        log.debug("Headers: %s", headers)
        log.debug("Params: %s", params)
        log.debug("Data: %s", data)
        log.debug("Timeout: %s", timeout)

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
                    log.debug("Error: %s - %s", response.status, response.reason)
                    response.raise_for_status()
        return None

    @abstractmethod
    async def fetch(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        headers: dict = dict(),
    ) -> EndpointResponse:
        """
        Fetch the endpoint data. This method should be implemented by subclasses.
        :param params: The parameters to send with the request (optional)
        :param data: The data to send with the request (optional)
        :param timeout: The timeout for the request (optional)

        :return: endpoint response
        """
        raise NotImplementedError("Subclasses must implement this method")


@dataclass
class EndpointSimpleSupportedVsCurrenciesStrategy(EndpointStrategyBase):
    """
    Endpoint call to get the supported vs currencies from CoinGecko
    """

    # FIXME: Pull from Config
    @cached_token(
        "simple_supported_vs_currencies", Path("localcache/service_coingecko.json")
    )
    async def fetch(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        headers: dict = dict(),
    ) -> EndpointResponse:
        """
        Fetch the supported vs currencies from CoinGecko
        :return: The supported vs currencies
        """
        log.debug("Fetching supported vs currencies from CoinGecko")
        return await self._get(
            params=params, data=data, timeout=timeout, headers=headers
        )


@dataclass
class EndpointCoinsMarketDataStrategy(EndpointStrategyBase):
    """
    Endpoint to get the market data for a specific coin from CoinGecko

    :param params: The parameters to send with the request (required: vs_currency)
    """

    @cached_token("coins_marketa_data", Path("localcache/service_coingecko.json"))
    async def fetch(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        headers: dict = dict(),
    ) -> EndpointResponse:
        """
        Fetch the supported vs currencies from CoinGecko
        :return: The supported vs currencies
        """
        log.debug("Fetching Coin Market Data from CoinGecko")
        return await self._get(
            params=params, data=data, timeout=timeout, headers=headers
        )


@dataclass
class EndpointCoinsListStrategy(EndpointStrategyBase):
    """
    Endpoint to get the list of coins from CoinGecko
    """

    @cached_token("coins_list", Path("localcache/service_coingecko.json"))
    async def fetch(
        self,
        params: dict = dict(),
        data: dict = dict(),
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        headers: dict = dict(),
    ) -> EndpointResponse:
        """
        Fetch the list of coins from CoinGecko
        :return: The list of coins (with meta data)
        """
        log.debug("Fetching Coin List from CoinGecko")
        return await self._get(
            params=params, data=data, timeout=timeout, headers=headers
        )


ENDPOINT_STRATEGY_TYPES = (
    EndpointSimpleSupportedVsCurrenciesStrategy
    | EndpointCoinsMarketDataStrategy
    | EndpointCoinsListStrategy
)
