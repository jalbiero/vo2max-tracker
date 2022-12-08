from vo2max_tracker.core.config import BaseConfig
from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.provider import fit_data_provider


def to_csv(config: BaseConfig, add_header: bool = False):
    if add_header:
        print("date, sport, sub sport, vo2max")

    fit: FitData
    for fit in fit_data_provider(config.ACTIVITY_DIR):
        if fit.vo2max > 0:
            print(f"{fit.start_time}, {fit.sport}, {fit.sub_sport}, {fit.vo2max}")


def to_json():
    pass
