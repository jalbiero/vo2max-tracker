# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

import logging

from vo2max_tracker.core.config import Config


class UserConfig(Config):
    """
    User's custom configuration (See BaseConfig class for more details about default values)
    """

    # Directory where activities are located
    #ACTIVITY_DIR = "./activities"

    # Directory where cache for every parsed FIT is located
    #CACHE_DIR = "./cache"

    # Log level (DEBUG, INFO, WARN, ERROR, FATAL, CRITICAL).
    #LOG_LEVEL = logging.DEBUG

    # File to log
    #LOG_FILE = "./log/vo2max_tracker.log"

    # If you have a high DPI monitor and the resulting charts are too small
    # you can set this property to 200 (2x zoom) or greater
    DPI = 200

    # Scatter chart instead of the default plot one?
    #SCATTER = False

    # Show tooltip on mouse hover instead of clicking on each point?
    #TOOLTIP_ON_HOVER = False

    # When grouping sport, use sub-sport category as part of the group?
    # e.g. When setting it to True, outdoor cycling will be different than indoor cycling
    #GROUP_BY_SUBSPORT = False
