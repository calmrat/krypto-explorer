# -*- coding: utf-8 -*-

"""
Qrypto - User Models

This module defines the User model and its properties for the Qrypto application.

It includes the SQLAlchemy model for the database and the Pydantic schema for data validation.

"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from qrypt.core.db import Base  # ← You need this to register the model


class User(Base):
    """User model for SQLAlchemy"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, unique=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_used = Column(
        DateTime,
        default=None,
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )
