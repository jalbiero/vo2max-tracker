# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

import logging
from typing import Optional


class Config:
    """
    Base class that defines available configuration options as well
    as its default values 
    """

    ACTIVITY_DIR: str = "./activities"
    CACHE_DIR: str = "./cache"

    LOG_LEVEL: int = logging.WARN
    LOG_FILE: str = "./log/vo2max_reader.log"

    DPI: Optional[int] = None
    SCATTER: bool = False
    TOOLTIP_ON_HOVER: bool = True
    GROUP_BY_SUBSPORT: bool = True

    # Properties not intended to be set by users
    LOG_TO_CONSOLE: bool = True
    RECREATE_CACHE: bool = False
