import logging
from typing import Optional


class Config:
    """
    Base class that defines available configuration options as well
    as its default values 
    """

    ACTIVITY_DIR: str = "./activities_920"
    CACHE_DIR: str = "./cache_920"

    LOG_LEVEL: int = logging.ERROR
    LOG_FILE: str = "./log/vo2max_reader.log"
    LOG_TO_CONSOLE: bool = False

    DPI: Optional[int] = None
    SCATTER: bool = False
    TOOLTIP_ON_HOVER: bool = True
    GROUP_BY_SUBSPORT: bool = True

    # Recreate cache files?
    RECREATE_CACHE: bool = False
