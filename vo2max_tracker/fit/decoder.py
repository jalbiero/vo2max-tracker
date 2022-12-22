import logging
from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, List, Optional

from garmin_fit_sdk import Decoder, Stream

from vo2max_tracker.fit.errors import FitDecoderError

# Useful types
_FitValueDict = Dict[Any, Any]
_FitValueList = List[_FitValueDict]
_FitMessageDict = Dict[str, _FitValueList]

# Fit access constants
# TODO This is requires a redesign (maybe a field provider) because constants are not the 
#      same across devices, especially the ancient ones (I only have FR-920 and FR-920 for testing)

_SPORT_MESSAGE_ID: str = "sport_mesgs"
_SPORT_FIELD_ID: str = "sport"
_SPORT_SUB_SPORT_FIELD_ID: str = "sub_sport"

_SESSION_MESSAGE_ID: str = "session_mesgs"
_SESSION_START_TIME_FIELD_ID: str = "start_time"
_SESSION_END_TIME_FIELD_ID: str = "timestamp"
_SESSION_TOTAL_CALORIES_FIELD_ID: str = "total_calories"
_SESSION_AVG_HR_FIELD_ID: str = "avg_heart_rate"
_SESSION_MAX_HR_FIELD_ID: str = "max_heart_rate"
_SESSION_AVG_TEMP_FIELD_ID: str = "avg_temperature"
_SESSION_MAX_TEMP_FIELD_ID: str = "max_temperature"
_SESSION_AEROBIC_TE_FIELD_ID: str = "total_training_effect"
_SESSION_ANAEROBIC_TE_FIELD_ID: str = "total_anaerobic_training_effect"
_SESSION_DISTANCE_FIELD_ID: str = "total_distance"
_SESSION_CYCLING_AVG_POWER_FIELD_ID: str = "avg_power"
_SESSION_CYCLING_MAX_POWER_FIELD_ID: str = "max_power"
_SESSION_CYCLING_NOR_POWER_FIELD_ID: str = "normalized_power"
_SESSION_DEV_FIELDS_FIELD_ID: str = "developer_fields"
_SESSION_DEV_FIELDS_RUNNING_AVG_POWER_FIELD_ID: int = 2

# More about VO2Max constants (they are not in SDK!) here:
# https://forums.garmin.com/sports-fitness/running-multisport/f/forerunner-945/226862/extracting-precise-vo2max-from-fit-file
_VO2MAX_MESSAGE_ID: str = "140"
_VO2MAX_FIELD_ID: int = 7
_V02MAX_VALUE_FACTOR: float = 3.5 / 65536.0


@dataclass
class FitData:
    start_time: Optional[date] = None
    end_time: Optional[date] = None
    duration: Optional[str] = None
    sport: Optional[str] = None
    sub_sport: Optional[str] = None
    vo2max: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None
    avg_heart_rate: Optional[float] = None
    max_heart_rate: Optional[float] = None
    avg_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    aerobic_te: Optional[float] = None
    anaerobic_te: Optional[float] = None
    avg_power: Optional[float] = None
    max_power: Optional[float] = None
    nor_power: Optional[float] = None
    firmware: Optional[str] = None


class FitDecoder:
    """
    High level wrapper for Garmin SDK
    """

    def decode_from_file(self, path_file: str) -> FitData:
        logging.info("Decoding FIT file = %s", path_file)
        return self.decode_from_content(Stream.from_file(path_file), path_file)

    def decode_from_content(self, stream: Stream, source_file_hint: str = None) -> FitData:
        source: str = "N/A" if source_file_hint is None else source_file_hint
        logging.info("Decoding FIT content. Source file = %s", source)

        decoder: Decoder = Decoder(stream)

        if not decoder.is_fit():
            raise FitDecoderError(f"Content is not from a FIT file. Source = {source}")

        if not decoder.check_integrity():
            raise FitDecoderError(f"Content is corrupted. Source = {source}")

        messages: _FitMessageDict
        errors: List[Any]
        messages, errors = decoder.read()

        if len(errors) > 0:
            raise FitDecoderError(errors)

        return self.__process_messages(messages)

    def __process_messages(self, messages: _FitMessageDict) -> FitData:
        result: FitData = FitData()

        if _SPORT_MESSAGE_ID in messages:
            sport_value: _FitValueDict = messages[_SPORT_MESSAGE_ID][0]
            result.sport = sport_value[_SPORT_FIELD_ID]
            result.sub_sport = sport_value[_SPORT_SUB_SPORT_FIELD_ID]

        if _VO2MAX_MESSAGE_ID in messages:
            vo2max_value: _FitValueDict = messages[_VO2MAX_MESSAGE_ID][0]
            result.vo2max = vo2max_value[_VO2MAX_FIELD_ID] * _V02MAX_VALUE_FACTOR

        if _SESSION_MESSAGE_ID in messages:
            session: _FitValueDict = messages[_SESSION_MESSAGE_ID][0]

            # TODO Time is in UTC, it would be nice to convert them to Local Zone
            result.start_time = session.get(_SESSION_START_TIME_FIELD_ID)
            result.end_time = session.get(_SESSION_END_TIME_FIELD_ID)

            if result.start_time and result.end_time:
                # duration is alwayas used as str (instead of timedelta)
                result.duration = str(result.end_time - result.start_time)

            # TODO Distance is in units set in the watch. It would be nice to
            #      extract them in order to perform some conversions (for the sake of GUI)
            result.distance = session.get(_SESSION_DISTANCE_FIELD_ID)

            result.calories = session.get(_SESSION_TOTAL_CALORIES_FIELD_ID)
            result.avg_heart_rate = session.get(_SESSION_AVG_HR_FIELD_ID)
            result.max_heart_rate = session.get(_SESSION_MAX_HR_FIELD_ID)
            result.avg_temperature = session.get(_SESSION_AVG_TEMP_FIELD_ID)
            result.max_temperature = session.get(_SESSION_MAX_TEMP_FIELD_ID)
            result.aerobic_te = session.get(_SESSION_AEROBIC_TE_FIELD_ID)
            result.anaerobic_te = session.get(_SESSION_ANAEROBIC_TE_FIELD_ID)

            # TODO Upgrade to "match/case" when migrate to Python 3.10
            if result.sport == "running":
                # TODO This was tested with .fit(s) generated by FR-945 + foot pod + RD pod, maybe
                #      for FR-955 and later, power is stored in a proper field instead of a developer one
                if _SESSION_DEV_FIELDS_FIELD_ID in session:
                    value: Optional[_FitValueDict] = session.get(_SESSION_DEV_FIELDS_FIELD_ID)

                    if value is not None:
                        result.avg_power = value.get(_SESSION_DEV_FIELDS_RUNNING_AVG_POWER_FIELD_ID)

            elif result.sport == "cycling":
                result.avg_power = session.get(_SESSION_CYCLING_AVG_POWER_FIELD_ID)
                result.max_power = session.get(_SESSION_CYCLING_MAX_POWER_FIELD_ID)
                result.nor_power = session.get(_SESSION_CYCLING_NOR_POWER_FIELD_ID)

            # TODO Extract firmware version
            # result.firmware =

        return result
