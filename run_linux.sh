#!/usr/bin/env bash

poetry show > /dev/null 2>&1

if [[ $? != 0 ]]; then
    poetry install --only main
fi

poetry run app $@
