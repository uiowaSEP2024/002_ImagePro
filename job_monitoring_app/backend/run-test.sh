#!/bin/bash

script_dir=$(dirname "$0")
cd "$script_dir" || exit
APP_ENV='test' pytest --cov
