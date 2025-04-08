# -*- coding: utf-8 -*-

"""
Qrypto - Constants

This module contains the constants used throughout the Qrypto application.
"""

# FIXME?
# SQLite settings
# sqlite_check_same_thread: bool = False

import os
from abc import ABC, abstractmethod
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_DATABASE_URL = "sqlite:///./qrypt.db"


class ConfigBase(ABC):
    """Configuration base class"""

    def __init__(self, validate: bool = True) -> None:
        # Load .env variables
        load_dotenv()

        if validate:
            self.validate()

    @abstractmethod
    def validate(self):
        """Validate the configuration"""
        raise NotImplementedError("Subclasses must implement this method")


class DBConfigBase(ABC):
    """Database configuration base class"""

    database_url: str = ""

    def __init__(self, validate: bool = True) -> None:
        # Load .env variables
        load_dotenv()

        self.database_url = os.environ.get("KE_DATABASE_URL", DEFAULT_DATABASE_URL)

        # Validate the config setup
        if validate:
            self.validate()

    @abstractmethod
    def validate(self):
        """Validate the configuration"""
        raise NotImplementedError("Subclasses must implement this method")

    @property
    @abstractmethod
    def url(self) -> str:
        """Construct the database URL"""
        raise NotImplementedError("Subclasses must implement this method")


class DBConfigSQLite(DBConfigBase):
    """SQLite database configuration class"""

    def validate(self):
        if not self.database_url:
            raise ValueError("Database URL is required")
        if not self.database_url.startswith("sqlite:///"):
            raise ValueError("Database URL must start with 'sqlite:///'")

    @property
    def url(self) -> str:
        """Construct the SQLite database URL"""
        return self.database_url


class DBConfigPostgreSQL(DBConfigBase):
    """SQLite database configuration class"""

    database_pw: str = ""
    database_user: str = ""
    database_host: str = ""
    database_port: str = ""
    database_name: str = ""

    def __init__(self, validate: bool = True) -> None:
        self.database_pw = os.environ.get("KE_DATABASE_PW", "")
        self.database_user = os.environ.get("KE_DATABASE_USER", "")
        self.database_host = os.environ.get("KE_DATABASE_HOST", "")
        self.database_port = os.environ.get("KE_DATABASE_PORT", "")
        self.database_name = os.environ.get("KE_DATABASE_NAME", "")
        super().__init__(validate=validate)

    def validate(self) -> None:
        if not self.database_url:
            raise ValueError("Database URL is required")
        if not self.database_user:
            raise ValueError("Database user is required")
        if not self.database_pw:
            raise ValueError("Database password is required")
        if not self.database_host:
            raise ValueError("Database host is required")
        if not self.database_port:
            raise ValueError("Database port is required")
        if not self.database_name:
            raise ValueError("Database name is required")

    @property
    def url(self) -> str:
        """Construct the PostgreSQL database URL"""
        return (
            f"postgresql://{self.database_user}:{self.database_pw}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )


class APIConfigBase(ABC):
    """API configuration base class"""

    static_dir: Path

    def __init__(self, validate: bool = True) -> None:
        self.static_dir = (
            Path(os.environ.get("KE_API_STATIC_DIR", "")).expanduser().absolute()
        )

        if validate:
            self.validate()

    @abstractmethod
    def validate(self) -> None:
        """Validate the configuration"""
        raise NotImplementedError("Subclasses must implement this method")


class FastAPIConfig(APIConfigBase):
    """FastAPI configuration class"""

    def validate(self) -> None:
        if not self.static_dir:
            raise ValueError("Static directory is required")
        if not os.path.isdir(self.static_dir):
            raise ValueError(f"Static directory does not exist: {self.static_dir}")


class AppConfig:
    """Database configuration class"""

    db: DBConfigSQLite | DBConfigPostgreSQL
    api: FastAPIConfig

    def __init__(self) -> None:
        """Initialize the application configuration"""
        if os.environ.get("KE_DATABASE_URL", "").startswith("postgresql"):
            self.db = DBConfigPostgreSQL()
        else:
            self.db = DBConfigSQLite()

        self.api = FastAPIConfig()
