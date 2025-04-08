# -*- coding: utf-8 -*-

"""
Qrypto - Main Entry Point

This module serves as the main entry point for the Qrypto application.
"""

from fastapi import FastAPI

from qrypt.tokens.api import router

app = FastAPI(title="Crypto Records Manager")

app.include_router(router)
