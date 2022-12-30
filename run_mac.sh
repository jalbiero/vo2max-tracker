#!/bin/zsh

# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

poetry show > /dev/null 2>&1

if [[ $? != 0 ]]; then
    poetry install --only main
fi

poetry run app $@