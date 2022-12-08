from datetime import datetime, timezone

from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.reader import ZipFitReader


def test_zip_fit_reader():
    reader: ZipFitReader = ZipFitReader()

    data: FitData = reader.read("./tests/activities/walking.zip")

    assert data.start_time == datetime(2022, 10, 24, 16, 52, 27, tzinfo=timezone.utc)
    assert data.sport == "walking"
    assert data.vo2max >= 51.33 and data.vo2max <= 51.40


def test_zip_fit_reader_file_not_found():
    try:
        reader: ZipFitReader = ZipFitReader()
        reader.read("./tests/activities/non-existent-file.zip")
        assert False

    except FileNotFoundError:
        assert True

    except:
        assert False
