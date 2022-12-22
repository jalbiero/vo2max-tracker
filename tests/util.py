from math import isclose
from typing import Union


def is_close(val_a: Union[float, None], val_b: float, tol: float) -> bool:
    assert val_a is not None
    return isclose(val_a, val_b, abs_tol=tol)
