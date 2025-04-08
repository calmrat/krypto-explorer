# -*- coding: utf-8 -*-

"""
Qrypto - Token API

This module contains the API for the Qrypto application, specifically for managing tokens.

It defines the endpoints for creating, updating, deleting, and retrieving tokens.
It uses FastAPI for building the API and SQLAlchemy for database interactions.
It also includes the necessary authentication and authorization mechanisms.

"""

from fastapi import APIRouter, HTTPException

from qrypt.tokens.schema import TokenOut
from qrypt.tokens.services.coingecko.adapter import CoinGeckoAdapter

router = APIRouter(prefix="/api/v1/tokens", tags=["tokens"])

type EndPointResponseTokenList = list[TokenOut]
ResponseModel = TokenOut


@router.get("/", response_model=EndPointResponseTokenList)
async def list_tokens() -> EndPointResponseTokenList:
    """
    List all tokens.

    Returns a list of all tokens in the database.
    """

    client = CoinGeckoAdapter()
    coins = await client.api.coins_list()
    if not coins:
        return []

    last_updated = None

    return [
        TokenOut(
            id=coin.get("id"),
            symbol=coin.get("symbol", ""),
            name=coin.get("name", ""),
            platforms=coin.get("platforms", {}),
            last_updated=last_updated,
        )
        for coin in coins
    ]


@router.get("/{token_id}", response_model=TokenOut)
async def get_token(token_id: str) -> TokenOut:
    """
    Get a token by its ID.

    Args:
        token_id (str): The ID of the token to retrieve.

    Returns:
        TokenOut: The token with the specified ID.
    """

    client = CoinGeckoAdapter()
    coins = await client.api.coins_list()
    if not coins:
        raise HTTPException(status_code=404, detail=f"Token not found [{token_id}]")

    # Find the token with the specified ID
    coin = next((c for c in coins if c["id"] == token_id), None)
    if not coin:
        raise HTTPException(status_code=404, detail=f"Token not found [{token_id}]")

    last_updated = None

    return TokenOut(
        id=coin.get("id", ""),
        symbol=coin.get("symbol", ""),
        name=coin.get("name", ""),
        platforms=coin.get("platforms", {}),
        last_updated=last_updated,
    )
