# -*- coding: utf-8 -*-

"""
Qrypto - Database Module

This module contains the database setup and configuration for the Qrypto application.

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from qrypt.core.config import AppConfig, DBConfigSQLite
from qrypt.core.log import logger as log

config = AppConfig()

if not config.db.url:
    raise ValueError(
        "Database URL is not set. Please set the KE_DATABASE_URL environment variable."
    )

# Setup engine
if isinstance(config.db, DBConfigSQLite):
    log.debug("Using SQLite database.")
    engine = create_engine(config.db.url, connect_args={"check_same_thread": False})
else:
    log.debug("Using PostgreSQL database.")
    engine = create_engine(config.db.url)

log.debug("Setting up SQLAlchemy Session + Base.")
# Session + Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all models in the application."""


# Dependency
def get_db():
    """Get a database session"""
    log.debug("Getting database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
