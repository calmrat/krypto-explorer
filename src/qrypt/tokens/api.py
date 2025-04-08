# -*- coding: utf-8 -*-

"""
Qrypto - Token API

This module contains the API for the Qrypto application, specifically for managing tokens.

It defines the endpoints for creating, updating, deleting, and retrieving tokens.
It uses FastAPI for building the API and SQLAlchemy for database interactions.
It also includes the necessary authentication and authorization mechanisms.

"""

from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from qrypt.core.log import logger as log
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
    # coins = await client.api.coins_list()
    coins = DB
    if not coins:
        return []

    last_updated = None

    return [
        TokenOut(
            id=coin.id,
            symbol=coin.symbol,
            name=coin.name,
            platforms=coin.platforms,
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

    # client = CoinGeckoAdapter()
    # coins = await client.api.coins_list()
    # if not coins:
    #     raise HTTPException(status_code=404, detail=f"Token not found [{token_id}]")

    # For now, we will use the temporary DB
    global DB
    coins = DB

    # Find the token with the specified ID
    coin = next((c for c in coins if c.id == token_id), None)
    if not coin:
        raise HTTPException(status_code=404, detail=f"Token not found [{token_id}]")

    return TokenOut(
        id=coin.id,
        symbol=coin.symbol,
        name=coin.name,
        platforms=coin.platforms,
        last_updated=coin.last_updated,
    )


@router.post("/", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
async def create_token(data: dict) -> TokenOut:
    """
    Create a new token.

    Args:
        token (TokenOut): The token to create.

    Returns:
        TokenOut: The created token.
    """

    # Extract the token data from the request body
    name = data.get("name", "")
    symbol = data.get("symbol", "")
    platforms = data.get("platforms", dict())

    log.debug("Creating token: %s", name)
    log.debug("Token symbol: %s", symbol)
    log.debug("Token platforms: %s", platforms)

    last_updated = datetime.now()

    if not (symbol and name and platforms):
        log.error("Token symbol and name are required!")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token symbol and name are required",
        )

    token = TokenOut(
        id=get_id(),
        symbol=symbol,
        name=name,
        platforms=platforms,
        last_updated=last_updated,
    )

    global DB
    DB.append(token)

    log.debug("Token created: %s", token)
    log.debug("Tokens in DB: %s", len(DB))
    log.debug("Tokens in DB: %s", DB)
    return token


@router.put("/{token_id}", response_model=TokenOut)
async def update_token(token_id: str, data: dict) -> TokenOut:
    """
    Update an existing token.

    Args:
        token_id (str): The ID of the token to update.
        data (dict): The updated token data.

    Returns:
        TokenOut: The updated token.
    """

    log.debug("Updating token: %s", token_id)
    log.debug("Token data: %s", data)

    global DB

    idx = next((i for i, c in enumerate(DB) if c.id == token_id), None)

    if idx is not None:
        DB[idx].name = data.get("name", DB[idx].name)
        DB[idx].symbol = data.get("symbol", DB[idx].symbol)
        DB[idx].platforms = data.get("platforms", DB[idx].platforms)
        DB[idx].last_updated = datetime.now()

        log.debug("Token updated: %s", DB[idx])
        log.debug("Tokens remaining: %s", len(DB))
        return DB[idx]
    else:
        log.debug("Token not found: %s", token_id)
        raise HTTPException(status_code=404, detail=f"Token not found [ID: {token_id}]")


@router.delete("/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_token(token_id: str) -> None:
    """
    Delete a token by its ID.

    Args:
        token_id (str): The ID of the token to delete.

    Raises:
        HTTPException: If the token is not found.
    """
    global DB

    log.debug("Deleting token: %s", token_id)
    log.debug("Total tokens before deletion: %s", len(DB))

    idx = next((i for i, c in enumerate(DB) if c.id == token_id), None)

    if idx is not None:
        DB.pop(idx)
        log.debug("Token deleted: %s", token_id)
    else:
        log.debug("Token not found: %s", token_id)
        raise HTTPException(status_code=404, detail=f"Token not found [ID: {token_id}]")

    log.debug("Token deleted: %s", token_id)
    log.debug("Tokens remaining: %s", len(DB))


## TEMPORARY DB
DB = []
ID_AUTO = 0


def get_id() -> str:
    """
    Get a new ID for a token.

    Returns:
        str: A new ID for the token.
    """
    global ID_AUTO
    ID_AUTO += 1
    return str(ID_AUTO)
