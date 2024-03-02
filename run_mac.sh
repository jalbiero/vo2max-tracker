#!/usr/bin/env zsh

# Copyright (C) 2022-2024 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

scriptDir=${0:a:h}
pushd $scriptDir

# Check if there is an associated virtual environment (dependencies downloaded)
cmdOutput=$(poetry env list)

if [[ "$cmdOutput" == "" ]]; then
    poetry install --only main
fi

poetry run app "$@"

popd
