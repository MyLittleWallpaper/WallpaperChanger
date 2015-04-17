#!/usr/bin/env bash

# Settings


# Wallpaper change code
DISPLAY=:0
PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

$DIR/wallpaper_change.py
