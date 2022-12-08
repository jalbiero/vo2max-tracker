#import logging
from vo2max_tracker.core.config import BaseConfig


class Config(BaseConfig):
    """
    See BaseConfig class for more details about default values
    """

    # Directory where activities are located
    #
    ACTIVITY_DIR = "./activities"
    #ACTIVITY_DIR = "./tests/activities"

    # Log level (DEBUG, INFO, WARN, ERROR, FATAL, CRITICAL), uncoment the 1st line
    # in this file if you plan to set a different log level
    #
    #LOG_LEVEL = logging.DEBUG

    # File to log
    #
    #LOG_FILE = "./log/vo2max_tracker.log"

    # Clone log file to console? (set to False if you plan to use the CSV/JSON feature)
    #
    #LOG_TO_CONSOLE = True

    # If you have a high DPI monitor and the resulting charts are too small
    # you can set this property to 200 (2x zoom) or greater
    #
    DPI = 250

    # Scatter chart instead of default plot one?
    #
    #SCATTER = True

    # Recreate cache files? If for some reason you feel like the chart is not
    # OK, you can try to recreate the cache. Be aware that this will force to
    # re-parse all activities (which in turn, it ends up in slower start-up)
    #
    RECREATE_CACHE = True
