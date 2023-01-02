# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

from datetime import datetime, timezone

from tests.util import is_close
from vo2max_tracker.fit.decoder import FitData, FitDecoder
from vo2max_tracker.fit.errors import FitError
from vo2max_tracker.fit.provider import fit_data_provider


def test_decode_an_invalid_fit_file() -> None:
    try:
        decoder: FitDecoder = FitDecoder()
        decoder.decode_from_file("./tests/activities/invalid.fit")
        assert False

    except FitError as ex:
        print("Error:", ex)  # run with "pytest -s" to see this message
        assert True

    except:
        assert False


def test_decode_from_file() -> None:
    decoder: FitDecoder = FitDecoder()

    data: FitData = decoder.decode_from_file("./tests/activities/running_fr945.fit")

    assert data.start_time == datetime(2022, 10, 23, 17, 36, 12, tzinfo=timezone.utc)
    assert data.end_time == datetime(2022, 10, 23, 18, 21, 5, tzinfo=timezone.utc)
    assert data.duration == "0:44:53"

    assert data.sport == "running"
    assert data.sub_sport == "generic"

    assert is_close(data.vo2max, 51.39, 0.01)
    assert is_close(data.distance, 6219.21, 0.01)
    assert is_close(data.calories, 471.0, 0.1)

    assert is_close(data.avg_heart_rate, 142.0, 0.1)
    assert is_close(data.max_heart_rate, 181.0, 0.1)

    assert is_close(data.avg_temperature, 23.0, 0.1)
    assert is_close(data.max_temperature, 26.0, 0.1)

    assert is_close(data.aerobic_te, 3.1, 0.1)
    assert is_close(data.anaerobic_te, 3.2, 0.1)

    assert is_close(data.avg_power, 266, 1)
    assert data.max_power is None
    assert data.nor_power is None


# def test_decode_from_ancient_device() -> None:
#     decoder: FitDecoder = FitDecoder()

#     data: FitData = decoder.decode_from_file("./tests/activities/cycling_outdoor_fr920.FIT")

#     assert data.start_time == datetime(2022, 10, 23, 17, 36, 12, tzinfo=timezone.utc)
#     assert data.end_time == datetime(2022, 10, 23, 18, 21, 5, tzinfo=timezone.utc)
#     assert data.duration == "0:44:53"

#     assert data.sport == "running"
#     assert data.sub_sport == "generic"

#     assert is_close(data.vo2max, 51.39, 0.01)
#     assert is_close(data.distance, 6219.21, 0.01)
#     assert is_close(data.calories, 471.0, 0.1)

#     assert is_close(data.avg_heart_rate, 142.0, 0.1)
#     assert is_close(data.max_heart_rate, 181.0, 0.1)

#     assert is_close(data.avg_temperature, 23.0, 0.1)
#     assert is_close(data.max_temperature, 26.0, 0.1)

#     assert is_close(data.aerobic_te, 3.1, 0.1)
#     assert is_close(data.anaerobic_te, 3.2, 0.1)

#     assert is_close(data.avg_power, 266, 1)
#     assert data.max_power is None
#     assert data.nor_power is None
