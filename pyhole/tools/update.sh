#!/bin/bash

git pull
cp "configs/custom.conf" "~/.pyhole/pyhole.conf"
tools/run_pyhole.sh
