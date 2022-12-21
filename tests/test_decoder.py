from datetime import datetime, timezone

from vo2max_tracker.fit.decoder import FitData, FitDecoder
from vo2max_tracker.fit.errors import FitError
from vo2max_tracker.fit.provider import fit_data_provider


def test_decode_from_file() -> None:
    decoder: FitDecoder = FitDecoder()

    data: FitData = decoder.decode_from_file("./tests/activities/running.fit")

    assert data.start_time == datetime(2022, 10, 23, 17, 36, 12, tzinfo=timezone.utc)
    assert data.sport == "running"
    assert data.vo2max is not None
    assert data.vo2max >= 51.39 and data.vo2max <= 51.40


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
