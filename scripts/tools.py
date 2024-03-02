# Copyright (C) 2022-2024 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

from subprocess import CompletedProcess, run
from sys import argv
from typing import List


def exec(cmds: List[str]) -> None:
    cp: CompletedProcess[str] = run(cmds)
    cp.check_returncode()


def all() -> None:
    exec(["isort", "."])
    exec(["autopep8",  "."])
    exec(["mypy", "./vo2max_tracker", "./tests"])
    #exec(["pylint", "vo2max_tracker"])
    #exec(["pylint", "tests"])


def pytest() -> None:
    all()
    exec(["pytest", *argv[1:]])  # extra arguments passed to pytest. e.g. poetry run tests -v -s


if __name__ == "__main__":
    all()
