# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

import json
import logging
from dataclasses import asdict
from datetime import datetime
from functools import reduce
from typing import Any, List

from vo2max_tracker.core.config import Config
from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.provider import fit_data_provider


def _get_sorted_data(config: Config) -> List[FitData]:
    # TODO This function needs to load all FIT in memory in order to sort
    #      them by date. It could be problematic if the user has a lot of activities
    # TODO A future version could use a sorted container instead of sorting the list at the end

    data: List[FitData] = []

    fit_data: FitData
    for fit_data in fit_data_provider(config):
        if fit_data.vo2max is not None and fit_data.vo2max > 0:
            data.append(fit_data)

    data.sort(key=lambda d: datetime(2000, 1, 1) if d.start_time is None else d.start_time)

    return data


def _str(value: Any) -> str:
    """
    Converts any value to string. None values will be converted to "" instead of "None"
    """

    return "" if value is None else str(value)


def to_csv(output_file: str, config: Config):
    """
    Exports all activities in 'config.ACTIVITY_DIR' to 'output_file' in CSV format 
    """

    # Append or overwrite?
    open_mode: str = "w+" if config.CSV_EXPORT_APPEND_OUTPUT else "w"

    with open(output_file, open_mode) as csv:
        # TODO Check this https://docs.python.org/3/library/os.html#os.linesep (\n for now)

        if config.CSV_EXPORT_ADD_HEADER:
            header: str = reduce(lambda a, b: a + ", " + b, asdict(FitData()).keys())
            csv.write(f"{header}\n")

        sorted_data: List[FitData] = _get_sorted_data(config)
        logging.info(f"Exporting {len(sorted_data)} activities in CSV format to {output_file}")

        fit_data: FitData
        for fit_data in sorted_data:
            if fit_data.vo2max is not None and fit_data.vo2max > 0:
                fit_dic: dict[str, Any] = asdict(fit_data)
                row: str = reduce(lambda a, b: _str(a) + ", " + _str(b), fit_dic.values())
                csv.write(f"{row}\n")


def to_json(output_file: str, config: Config):
    """
    Exports all activities in config.ACTIVITY_DIR to 'output_file' in JSON format 
    """

    with open(output_file, "x") as outf:
        sorted_data: List[FitData] = _get_sorted_data(config)
        logging.info(f"Exporting {len(sorted_data)} activities in JSON format to {output_file}")

        json.dump([asdict(fit_data) for fit_data in sorted_data], outf, default=str)
