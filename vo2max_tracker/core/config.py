import logging
from typing import Union


class BaseConfig:
    """
    Base class that defines available configuration options as well
    as its default values 
    """

    # Directory where activities are located
    ACTIVITY_DIR: str = "./activities"

    # Directory where cache for every parsed FIT is located
    CACHE_DIR: str = "./cache"

    # Log level (DEBUG, INFO, WARN, ERROR, FATAL, CRITICAL).
    LOG_LEVEL: int = logging.INFO

    # File to log
    LOG_FILE: str = "./log/vo2max_reader.log"

    # Clone log file to console?
    LOG_TO_CONSOLE: bool = False

    # If you have a high DPI monitor and the resulting chart is too small
    # you can set this property to 200 (2x zoom) or greater
    DPI: Union[int, None] = None

    # Scatter chart instead of connected points?
    SCATTER: bool = False

    # Show tooltip on mouse hover instead of clicking on each point?
    TOOLTIP_ON_HOVER: bool = True

    # Recreate cache files?
    RECREATE_CACHE: bool = False

    # When grouping sport, use sub-sport category as part of the group?
    # e.g. When setting it to True, outdoor cycling will be different than indor cycling
    GROUP_BY_SUBSPORT: bool = True
