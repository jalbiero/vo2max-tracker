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

    LOG_LEVEL: int = logging.INFO
    LOG_FILE: str = "./log/vo2max_reader.log"

    DPI: Optional[int] = 150
    SCATTER: bool = False
    TOOLTIP_ON_HOVER: bool = False
    GROUP_BY_SUBSPORT: bool = True

    CSV_EXPORT_ADD_HEADER: bool = True
    CSV_EXPORT_APPEND_OUTPUT: bool = False

    # Properties not intended to be directly set by users
    LOG_TO_CONSOLE: bool = True
    RECREATE_CACHE: bool = False
