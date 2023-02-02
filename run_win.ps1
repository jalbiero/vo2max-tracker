# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

Push-Location $PSScriptRoot

# Check if there is an associated virtual environment (dependencies downloaded)
$cmdOutput = poetry env list

if ([string]::IsNullOrEmpty($cmdOutput)) {
    poetry install --only main
}

poetry run app @args

Pop-Location
