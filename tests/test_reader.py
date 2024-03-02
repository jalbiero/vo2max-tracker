# Copyright (C) 2022-2024 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

from datetime import datetime, timezone

from tests.util import is_close
from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.errors import FitReaderError
from vo2max_tracker.fit.reader import ZipFitReader


def test_zip_fit_reader() -> None:
    reader: ZipFitReader = ZipFitReader()

    data: FitData = reader.read("./tests/activities/walking_fr945.zip")

    assert data.start_time == datetime(2022, 10, 24, 16, 52, 27, tzinfo=timezone.utc)
    assert data.end_time == datetime(2022, 10, 24, 18, 2, 4, tzinfo=timezone.utc)
    assert data.duration == "1:09:37"

    assert data.sport == "walking"
    assert data.sub_sport == "generic"

    assert is_close(data.vo2max, 51.33, 0.01)
    assert is_close(data.distance, 6816.86, 0.01)
    assert is_close(data.calories, 547.0, 0.1)

    assert is_close(data.avg_heart_rate, 117.0, 0.1)
    assert is_close(data.max_heart_rate, 168.0, 0.1)

    assert is_close(data.avg_temperature, 28.0, 0.1)
    assert is_close(data.max_temperature, 31.0, 0.1)

    assert is_close(data.aerobic_te, 2.4, 0.1)
    assert is_close(data.anaerobic_te, 0.7, 0.1)

    assert data.avg_power is None
    assert data.max_power is None
    assert data.nor_power is None


def test_zip_fit_reader_file_not_found() -> None:
    try:
        reader: ZipFitReader = ZipFitReader()
        reader.read("./tests/activities/non-existent-file.zip")
        assert False

    except FileNotFoundError as ex:
        print("Error:", ex)  # run with "pytest -s" to see this message
        assert True

    except:
        assert False


def test_zip_fit_reader_no_fit_inside() -> None:
    try:
        reader: ZipFitReader = ZipFitReader()
        reader.read("./tests/activities/no_fit_inside.zip")
        assert False

    except FitReaderError as ex:
        print("Error:", ex)  # run with "pytest -s" to see this message
        assert True

    except:
        assert False
