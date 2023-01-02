#!/usr/bin/env bash

# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

# Check if there is an associated virtual environment (dependencies downloaded)
cmdOutput=$(poetry env list)

if [[ "$cmdOutput" == "" ]]; then
    poetry install --only main
fi

poetry run app "$@"
