#!/bin/bash

git pull
mkdir -p "~/.pyhole/"
cp "configs/custom.conf" "~/.pyhole/pyhole.conf"
tools/run_pyhole.sh
