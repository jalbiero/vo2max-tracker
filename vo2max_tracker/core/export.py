# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

from vo2max_tracker.core.config import Config
from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.provider import fit_data_provider


def to_csv(config: Config, add_header: bool = False):
    if add_header:
        print("date, sport, sub sport, vo2max")

    fit: FitData
    for fit in fit_data_provider(config):
        if fit.vo2max is not None and fit.vo2max > 0:
            print(f"{fit.start_time}, {fit.sport}, {fit.sub_sport}, {fit.vo2max}")


def to_json():
    pass
