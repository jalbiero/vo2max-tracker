# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

import argparse
import logging
import sys
import traceback

from vo2max_tracker.config import UserConfig
from vo2max_tracker.core.chart import plot
from vo2max_tracker.core.config import Config
from vo2max_tracker.core.export import to_csv, to_json
from vo2max_tracker.version import __version__


def build_arg_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    general_group = parser.add_argument_group(title='General options')
    export_group = parser.add_argument_group(title='Export options')

    general_group.add_argument(
        "-v",
        "--version",
        help="show VO2MaxReader version",
        default=False,
        action="store_true")

    general_group.add_argument(
        "-r",
        "--rcache",
        help="Recreate FIT cache. The application start-up will be very slow, be patience.",
        default=False,
        action="store_true")

    export_group.add_argument(
        "-c",
        "--csv",
        help="Export all activities in CSV format",
        default=False,
        action="store_true")

    export_group.add_argument(
        "-j",
        "--json",
        help="Export all activities in JSON format",
        default=False,
        action="store_true")

    export_group.add_argument(
        "-o",
        "--output",
        help="Output file (when not specified, './export_output.txt' will be used",
        default="export_output.txt")

    return parser


def setup_log(config: Config) -> None:
    logging.basicConfig(filename=config.LOG_FILE,
                        level=config.LOG_LEVEL,
                        format="%(asctime)s %(levelname)8s [%(module)s] %(message)s")

    if config.LOG_TO_CONSOLE:
        # All INFO/WARN/ERROR messages are cloned to screen
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)


def main() -> None:
    config: UserConfig = UserConfig()

    setup_log(config)

    try:
        logging.debug(f"Starting VO2Max Tracker, version = {__version__}")

        parser: argparse.ArgumentParser = build_arg_parser()
        args: argparse.Namespace = parser.parse_args()

        if args.version:
            print(__version__)

        elif args.csv:
            to_csv(args.output, config)

        elif args.json:
            to_json(args.output, config)

        else:
            config.RECREATE_CACHE = args.rcache
            plot(config)

    except Exception as ex:  # pylint: disable=broad-except
        logging.error(f"Error: {ex}. {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
