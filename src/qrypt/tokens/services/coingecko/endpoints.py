# -*- coding: utf-8 -*-

"""
Qrypto - CoinGecko Service - Endpoints

This module contains the Coingecko service endpoints for the Qrypto application.
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from qrypt.tokens.services.coingecko.strategies import ENDPOINT_STRATEGY_TYPES


@dataclass
class EndpointBase(ABC):
    base_url: str
    endpoint: str
    method: str
    headers: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.endpoint}"

    async def fetch(self, strategy: ENDPOINT_STRATEGY_TYPES) -> Optional[dict]:
        return await strategy.fetch()


# simple__supported_vs_currencies = EndpointSimpleSupportedVsCurrencies(
#     base_url="https://api.coingecko.com/api/v3",
#     endpoint="/simple/supported_vs_currencies",
#     method="GET",
#     headers={"accept": "application/json"},
# )

# coins__marketa_data = EndpointCoinsMarketData(
#     base_url="https://api.coingecko.com/api/v3",
#     endpoint="coins/markets",
#     method="GET",
#     headers={"accept": "application/json"},
# )

if __name__ == "__main__":
    pass
