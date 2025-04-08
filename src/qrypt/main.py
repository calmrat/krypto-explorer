# -*- coding: utf-8 -*-

"""
Qrypto - Main Entry Point

This module serves as the main entry point for the Qrypto application.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from qrypt.core.config import FastAPIConfig
from qrypt.core.log import logger as log
from qrypt.tokens.api import router

# Initialize the FastAPI app
app = FastAPI(title="Crypto Records Manager")

# Load FastAPI config options from .env file
config = FastAPIConfig()

# Add the router to the FastAPI app
app.include_router(router)

# Mount the static directory
log.debug("Serving static files from %s", config.static_dir)
app.mount("/static", StaticFiles(directory=config.static_dir), name="static")
