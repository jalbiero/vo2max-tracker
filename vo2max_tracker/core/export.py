# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

from ast import Dict
from dataclasses import asdict
from functools import reduce
from typing import Any
from vo2max_tracker.core.config import Config
from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.provider import fit_data_provider


def to_csv(config: Config, add_header: bool = True):
    if add_header:
        print(reduce(lambda a, b: a + ", " + b, asdict(FitData()).keys()))
        #print("date, sport, sub sport, vo2max")

    fit: FitData
    for fit in fit_data_provider(config):
        if fit.vo2max is not None and fit.vo2max > 0:
            fit_dic: Dict[str, Any] = asdict(fit)

            print(reduce(lambda a, b: str(a) + ", " + str(b), fit_dic.values()))

            #print(f"{fit.start_time}, {fit.sport}, {fit.sub_sport}, {fit.vo2max}")


def to_json():
    pass
