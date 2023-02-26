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
    IGNORE_SPORT_REGEX: Optional[str] = None

    CSV_EXPORT_ADD_HEADER: bool = True
    CSV_EXPORT_APPEND_OUTPUT: bool = False

    # Properties not intended to be directly set by users
    LOG_TO_CONSOLE: bool = True
    RECREATE_CACHE: bool = False

    # TODO
    # Manual converter factors until units will be retrieved from FIT file
    # Note: These will apply to all FIT files so if one fit has distance in km
    # and another in miles, you will get wrong results. Use them at your own risk
    #
    # DISTANCE_FACTOR: Optional[float] = None
    # DISTANCE_UNIT: Optional[str] = None
    #
    # TEMPERATURE_FACTOR: Optional[float] = None
    # TEMPERATURE_UNIT: Optional[str] = None
