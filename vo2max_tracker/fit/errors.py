# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

class FitError(RuntimeError):
    ...


class FitDecoderError(FitError):
    ...


class FitReaderError(FitError):
    ...
