# -*- coding: utf-8 -*-

"""
Qrypto - Database Management Functions
"""

from typing import Optional

from sqlalchemy import inspect

from qrypt.core.db import Base, engine
from qrypt.core.log import logger as log
from qrypt.tokens.models import Token  # noqa pylint: disable=unused-import
from qrypt.users.models import User  # noqa pylint: disable=unused-import

TARGET_TABLES: set = {"tokens", "users"}


def check_tables(tables: set = TARGET_TABLES) -> Optional[set]:
    inspector = inspect(engine)
    db_tables = set(inspector.get_table_names())
    if not tables.issubset(db_tables):
        log.warning("Missing tables in the database: %s", tables - db_tables)
        raise RuntimeError(f"Missing tables in the database: {tables - db_tables}")
    return db_tables


def init_db() -> None:
    """Initialize the database"""
    # Import all models here to ensure they are registered with SQLAlchemy
    # from qrypt.tokens.models import Token  # noqa: F401
    # from qrypt.users.models import User  # noqa: F401

    # Create the database tables
    log.debug("Initializing Database...")
    Base.metadata.create_all(bind=engine)
    check_tables()
    log.debug("Database initialized successfully.")


def drop_db() -> None:
    """Drop the database tables"""
    log.debug("Dropping Database...")
    Base.metadata.drop_all(bind=engine)
    try:
        tables = check_tables()
    except RuntimeError:
        log.debug("Database dropped successfully.")
    else:
        log.warning("Failed to drop the following tables: %s", tables)
        raise RuntimeError(f"Failed to drop the following tables: {tables}")
