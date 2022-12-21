import json
import logging
from abc import ABC, abstractmethod
from asyncio.log import logger
from dataclasses import asdict
from datetime import datetime
from io import BytesIO
from os import path, sep
from typing import Any, Dict, List
from zipfile import ZipFile, ZipInfo

from garmin_fit_sdk import Stream

from vo2max_tracker.core.config import BaseConfig
from vo2max_tracker.fit.decoder import FitData, FitDecoder
from vo2max_tracker.fit.errors import FitReaderError
from vo2max_tracker.version import __version__


class FitReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> FitData:
        ...


class RawFitReader(FitReader):
    """
    Reads a FIT file from disk
    """

    def __init__(self):
        self.__decoder = FitDecoder()

    def read(self, file_path: str) -> FitData:
        logger.info("Reading FIT content from %s file", file_path)
        return self.__decoder.decode_from_file(file_path)


class ZipFitReader(FitReader):
    """
    Reads a FIT file from a ZIP file (this is useful when the activity is downloaded
    from Garmin Connect site instead of a simple copy from the watch)
    """

    def __init__(self):
        self.__decoder = FitDecoder()

    def read(self, file_path: str) -> FitData:
        logger.info("Looking for a FIT file in %s file", file_path)

        # If the .zip file contains more than 1 .fit file, only
        # the first one will be used
        with ZipFile(file_path, 'r') as zip:
            file: ZipInfo
            for file in zip.infolist():
                if file.filename.endswith(".fit"):
                    logging.info("Found %s in %s", file.filename, file_path)
                    content: Stream = Stream.from_bytes_io(BytesIO(zip.read(file)))
                    return self.__decoder.decode_from_content(content)

        raise FitReaderError(f"{file_path} does not contain a .fit file")


class FitCacheReader(FitReader):
    """
    Cache proxy reader (Fit SDK is really slow in Python so a cache is mandatory)
    """

    def __init__(self, reader: FitReader, config: BaseConfig) -> None:
        self.__external_reader = reader
        self.__config = config

    def read(self, file_path: str) -> FitData:
        cache_path: str = sep.join(
            [self.__config.CACHE_DIR, path.basename(file_path) + ".cache"])

        if not self.__config.RECREATE_CACHE and path.isfile(cache_path):
            logger.info("Cache hit for %s", file_path)
            return self._read_cache(cache_path)

        data: FitData = self.__external_reader.read(file_path)
        self._write_cache(cache_path, data)
        return data

    def _write_cache(self, cache_path: str, data: FitData) -> None:
        logger.info("Write json cache to %s", cache_path)
        with open(cache_path, "w") as cache:
            data_dict: Dict[str, Any] = asdict(data)

            # Add version (future usage)
            data_dict["_version"] = __version__

            # Dates will be serialized as strings (ISO format)
            cache.write(json.dumps(data_dict, default=str))

    def _read_cache(self, cache_path: str) -> FitData:
        logger.info("Read json cache from %s", cache_path)
        with open(cache_path, "r") as cache:
            data = FitData(**json.load(cache))

            # Date was read it as string, reconvert it to datetime
            data.start_time = datetime.fromisoformat(str(data.start_time))

            return data


class ReaderManager:
    """
    Manages the (file) reading strategies
    """

    def __init__(self):
        self.__strategy: Dict[str, FitReader] = {
            ".fit": RawFitReader(),
            ".zip": ZipFitReader(),
        }

    def add_reader(self, extension: str, reader: FitReader) -> None:
        self.__strategy[extension] = reader

    def get_reader(self, extension: str) -> FitReader:
        return self.__strategy[extension]

    def get_registered_extensions(self) -> List[str]:
        return [*self.__strategy.keys()]
