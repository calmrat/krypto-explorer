# -*- coding: utf-8 -*-

"""
Qrypto - CoinGecko Service - Core: Logging
"""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("qrypt")
