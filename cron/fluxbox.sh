#!/usr/bin/env bash

export DISPLAY=:0.0
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

$DIR/wallpaper_change.py
