# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

import logging
from os import listdir, path
from typing import Generator, List

from vo2max_tracker.core.config import Config
from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.errors import FitError
from vo2max_tracker.fit.reader import FitCacheReader, FitReader, ReaderManager


def _file_provider(dir: str, ext: List[str]) -> Generator[str, None, None]:
    """
    Returns a lazy sequence of file names (with the specified extensions) in 
    the provided directory
    """

    file: str
    for file in listdir(dir):
        fullname: str = path.join(dir, file)
        if path.isfile(fullname):
            file_ext: str = path.splitext(file)[1]
            if file_ext in ext:
                yield fullname


def fit_data_provider(config: Config) -> Generator[FitData, None, None]:
    """
    Returns a lazy sequence of FitData based on the FIT files found in the
    config.ACTIVITY_DIR. There is no guaranteed order in the sequence, it's all 
    depends on the order of the files in the file system.
    """

    reader_mgr: ReaderManager = ReaderManager()

    if config.RECREATE_CACHE:
        logging.info("Wait while recreating FIT cache...")

    else:
        num_of_act: int = sum(1 for _ in _file_provider(config.ACTIVITY_DIR, reader_mgr.get_registered_extensions()))
        num_of_cached_act: int = sum(1 for _ in _file_provider(config.CACHE_DIR, [FitCacheReader.file_cache_ext()]))

        new_activities: int = num_of_act - num_of_cached_act

        if new_activities > 0:
            logging.info(f"Detected {new_activities} new activit(y/ies). Wait while it is/they are processed")

    logging.debug("Looking for FIT files in %s", config.ACTIVITY_DIR)

    file: str
    for file in _file_provider(config.ACTIVITY_DIR, reader_mgr.get_registered_extensions()):
        try:
            logging.debug("Found %s file", file)
            file_ext: str = path.splitext(file)[1]

            reader: FitReader = FitCacheReader(reader_mgr.get_reader(file_ext), config)
            fit_data = reader.read(file)

            yield fit_data

        except FitError as ex:
            logging.warn("Unexpected error (ignored) = %s", ex)
