# -*- coding: utf-8 -*-

"""
Qrypto Schema - Token Schemas

This module contains the schema for the Qrypto application.

It defines the data models and their relationships using SQLAlchemy and Pydantic.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TokenBase(BaseModel):
    """Token model for Base"""

    id: int
    symbol: str
    name: str
    platforms: dict
    last_updated: Optional[datetime]
    logo_url: Optional[str] = None


class TokenOut(TokenBase):
    """Token model for Full Output"""

    # Pydantic Config class
    class Config:
        """Pydantic Config class for TokenOut"""

        # Allow ORM mode for SQLAlchemy models, so we can use them directly
        # in the response models
        # * 'orm_mode' has been renamed to 'from_attributes' in v2
        from_attributes = True
