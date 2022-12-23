import argparse
import logging
import sys
import traceback

from vo2max_tracker.config import UserConfig
from vo2max_tracker.core.chart import plot
from vo2max_tracker.core.config import Config
from vo2max_tracker.core.export import to_csv
from vo2max_tracker.version import __version__


def build_arg_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        help="show VO2MaxReader version",
        default=False,
        action="store_true")

    parser.add_argument(
        "-c",
        "--csv",
        help="Console output of all activities in CSV format",
        default=False,
        action="store_true")

    parser.add_argument(
        "-r",
        "--rcache",
        help="Recreate FIT cache. The application start-up will be very slow, be patience.",
        default=False,
        action="store_true")

    return parser


def setup_log(config: Config) -> None:
    logging.basicConfig(filename=config.LOG_FILE,
                        level=config.LOG_LEVEL,
                        format="%(asctime)s %(levelname)8s [%(module)s] %(message)s")

    if config.LOG_TO_CONSOLE:
        # All WARN/ERROR messages are cloned to screen
        handler = logging.StreamHandler()
        handler.setLevel(logging.WARN)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)


def main() -> None:
    config: UserConfig = UserConfig()

    setup_log(config)

    try:
        logging.info(f"** Starting app, version = {__version__} **")

        parser: argparse.ArgumentParser = build_arg_parser()
        args: argparse.Namespace = parser.parse_args()

        if args.version:
            print(__version__)

        elif args.csv:
            to_csv(config, True)

        else:
            config.RECREATE_CACHE = args.rcache
            plot(config)

    except Exception as ex:  # pylint: disable=broad-except
        logging.error(f"Error: {ex}\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
