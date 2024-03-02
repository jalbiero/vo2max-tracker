# Copyright (C) 2022-2024 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

from math import isclose
from typing import Union


def is_close(val_a: Union[float, None], val_b: float, tol: float) -> bool:
    assert val_a is not None
    return isclose(val_a, val_b, abs_tol=tol)
