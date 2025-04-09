# -*- coding: utf-8 -*-

"""
Qrypto - Token Models

This module defines the Token model and its properties for the Qrypto application.

It includes the SQLAlchemy model for the database.

"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from qrypt.core.db import Base, get_db
from qrypt.core.log import logger as log


def get_current_time() -> datetime:
    """Get the current UTC time"""
    return datetime.now(timezone.utc)


class Token(Base):
    """Token model for the Qrypto application."""

    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    ext_id: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=True
    )  # RENAME to gc_id (coingecko id)
    symbol: Mapped[str] = mapped_column(
        String, unique=False, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    logo_url: Mapped[str] = mapped_column(String, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, default=get_current_time, onupdate=get_current_time
    )

    platforms: Mapped[list["BlockchainPlatform"]] = relationship(
        back_populates="token", cascade="all, delete-orphan"
    )


class BlockchainPlatform(Base):
    """BlockchainPlatform model for the Qrypto application."""

    __tablename__ = "blockchain_platforms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    token_id: Mapped[int] = mapped_column(ForeignKey("tokens.id"), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, default=get_current_time, onupdate=get_current_time
    )

    # Relationship back to token
    token: Mapped["Token"] = relationship(back_populates="platforms")


# FIXME: add type for the input model type
def get_all(model) -> list[Token | BlockchainPlatform]:
    """Get all tokens from the database."""
    log.debug("Fetching all tokens from the database")
    db = next(get_db())
    try:
        tokens = db.query(model).all()
        return tokens
    finally:
        db.close()
