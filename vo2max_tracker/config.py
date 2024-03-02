# Copyright (C) 2022-2024 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

import logging

from vo2max_tracker.core.config import Config


class UserConfig(Config):
    """
    User's custom configuration (See Config class for more details about default values)
    """

    # Directory where activities are located. Default = "./activities"
    #ACTIVITY_DIR = "./activities"

    # Directory where cache for every parsed FIT is located. Default = "./cache"
    #CACHE_DIR = "./cache"

    # Log level (DEBUG, INFO, WARN, ERROR, FATAL, CRITICAL). Default = Logging.INFO
    #LOG_LEVEL = logging.DEBUG

    # File to log. Default = "./log/vo2max_tracker.log"
    #LOG_FILE = "./log/vo2max_tracker.log"

    # If you have a high DPI monitor and the resulting charts are too small
    # you can set this property to 200 (2x zoom) or greater
    # Default = 150 (as a compromise between normal monitors vs high dpi ones)
    #DPI = 200

    # Scatter chart instead of the default plot one?. Default = False
    #SCATTER = True

    # Show tooltip on mouse hover instead of clicking on each point?. Default = False
    #TOOLTIP_ON_HOVER = True

    # When grouping sports, use sub-sport category as part of the group?. Default = True
    # e.g. When setting it to True, outdoor cycling will be different than indoor cycling
    #GROUP_BY_SUBSPORT = False

    # Sports that match the specified regex won't be shown in the chart
    #IGNORE_SPORT_REGEX = "walking*"

    # Add header as a first row of data?. Default = True
    #CSV_EXPORT_ADD_HEADER = False

    # Append data to an already existent file?. Default = False
    # When set to False, the export will fail if the output file already exists
    #CSV_EXPORT_APPEND_OUTPUT = True
