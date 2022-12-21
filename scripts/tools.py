from subprocess import CompletedProcess, run
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
    exec(["pytest"])


if __name__ == "__main__":
    all()
