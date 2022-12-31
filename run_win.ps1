# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

poetry show *> $null

if ($LastExitCode -ne 0) {
    poetry install --only main
}  

poetry run app @args