# -*- coding: utf-8 -*-

"""
Qrypto - Token Models

This module defines the Token model and its properties for the Qrypto application.

It includes the SQLAlchemy model for the database and the Pydantic schema for data validation.

"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from qrypt.core.db import Base  # ← You need this to register the model


def get_current_time() -> datetime:
    """Get the current UTC time"""
    return datetime.now(timezone.utc)


class BlockchainPlatform(Base):
    """BlockchainPlatforms model for SQLAlchemy"""

    __tablename__ = "blockchain_platforms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    platform_name = Column(String, nullable=False)
    platform_address = Column(String, nullable=False)
    token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    token = relationship("Token", back_populates="platforms")

    # Back reference to Token
    token = relationship("Token", back_populates="platforms")

    last_updated = Column(
        DateTime,
        default=get_current_time,
        onupdate=get_current_time,
    )


class Token(Base):
    """Token model for SQLAlchemy"""

    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol = Column(String, index=True, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    logo_url = Column(String, nullable=True)
    last_updated = Column(
        DateTime,
        default=get_current_time,
        onupdate=get_current_time,
    )
    # Establish relationship with BlockchainPlatforms
    platforms = relationship(
        "BlockchainPlatforms", back_populates="token", lazy="dynamic"
    )
