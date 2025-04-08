# -*- coding: utf-8 -*-

"""
Qrypto Schema - Token Schemas

This module contains the schema for the Qrypto application.

It defines the data models and their relationships using SQLAlchemy and Pydantic.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

#   {
#     "id": "0chain",
#     "symbol": "zcn",
#     "name": "Zus",
#     "platforms": {
#       "ethereum": "0xb9ef770b6a5e12e45983c5d80545258aa38f3b78",
#       "polygon-pos": "0x8bb30e0e67b11b978a5040144c410e1ccddcba30"
#     }
#   },


class TokenBase(BaseModel):
    """Token model for Base"""

    id: Optional[str]
    symbol: str
    name: str
    platforms: dict


class TokenCreate(TokenBase):
    """Token model for Create"""

    symbol: str  # symbol is required to create
    name: str  # symbol name is required to create
    platforms: dict  # platforms is required to create


class TokenUpdate(BaseModel):
    """Token model for Update"""

    id: str
    name: Optional[str] = None
    platforms: Optional[dict] = None


class TokenOut(TokenBase):
    """Token model for Full Output"""

    id: Optional[str]
    last_updated: Optional[datetime]

    # Pydantic Config class
    class Config:
        """Pydantic Config class for TokenOut"""

        # Allow ORM mode for SQLAlchemy models, so we can use them directly
        # in the response models
        # * 'orm_mode' has been renamed to 'from_attributes' in v2
        from_attributes = True
