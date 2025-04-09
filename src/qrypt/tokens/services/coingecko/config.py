# -*- coding: utf-8 -*-

"""
Qrypto - CoinGecko Service - Configuration
"""

import os

from qrypt.core.config import ConfigBase
from qrypt.tokens.services.coingecko.constants import (
    BASE_URL_V3,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_VS_CURRENCY,
    HEADER_ACCEPT_JSON,
)


class CoinGeckoConfig(ConfigBase):
    """
    Configuration class for the CoinGecko service.
    """

    base_url: str
    timeout: int
    headers: dict
    demo_user: bool
    vs_currency: str

    def __init__(self, validate: bool = True) -> None:
        self.base_url = os.environ.get("COINGECKO_BASE_URL", BASE_URL_V3)
        self.timeout = int(
            os.environ.get("KE_COINGECKO_API_TIMEOUT", DEFAULT_TIMEOUT_SECONDS)
        )  # seconds
        self.headers = HEADER_ACCEPT_JSON
        self.demo_user = (
            os.environ.get("KE_COINGECKO_API_DEMO_USER", "false").lower() == "true"
        )
        self.api_key = os.environ.get("KE_COINGECKO_API_KEY", "")

        # If demo user is enabled, add the demo API key to the headers
        if self.api_key and self.demo_user:
            self.headers.update({"x-cg-demo-api-key": self.api_key})

        self.vs_currency = os.environ.get(
            "KE_COINGECKO_API_VS_CURRENCY", DEFAULT_VS_CURRENCY
        )

        super().__init__(validate=validate)

    def validate(self):
        """
        Validate the configuration.
        """
        if not self.base_url:
            raise ValueError("Base URL is not set")
        if not self.base_url.startswith("http"):
            raise ValueError("Base URL must start with http or https")
        if not self.timeout:
            raise ValueError("Timeout is not set")
        if not isinstance(self.timeout, int):
            raise ValueError("Timeout must be an integer")
        if self.timeout <= 0:
            raise ValueError("Timeout must be greater than 0")
        if self.demo_user and not self.api_key:
            raise ValueError("API key is required for demo user")
        if self.api_key and not self.demo_user:
            raise NotImplementedError(
                "API key is only supported for DEMO account users"
            )
