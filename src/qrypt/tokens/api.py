# -*- coding: utf-8 -*-

"""
Qrypto - Token API

This module contains the API for the Qrypto application, specifically for managing tokens.

It defines the endpoints for creating, updating, deleting, and retrieving tokens.
It uses FastAPI for building the API and SQLAlchemy for database interactions.
It also includes the necessary authentication and authorization mechanisms.

"""

from datetime import datetime

from fastapi import APIRouter

from qrypt.tokens.schema import TokenOut
from qrypt.tokens.services.coingecko.adapter import CoinGeckoAdapter

router = APIRouter(prefix="/api/v1/tokens", tags=["tokens"])


@router.get("/", response_model=list[TokenOut])
async def list_tokens() -> list[TokenOut]:
    """
    List all tokens.

    Returns a list of all tokens in the database.
    """

    client = CoinGeckoAdapter()
    coins = await client.api.coins_list()

    # coins = [TokenOut(**coin) for coin in coins]
    coin = coins[0] if coins else dict()
    return [
        TokenOut(
            id="id",
            symbol="symbol",
            name="name",
            platforms={"ethereum": "asdfasdfasd"},
            last_updated=datetime.now(),
        )
    ]
