#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Supported desktop environments
# - gnome (Unity, Gnome 3)
# - fluxbox (Fluxbox, Openbox, JWM, AfterStep)

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.request import urlopen

try:
    # Python 2
    from urllib import quote_plus
except ImportError:
    # Python 3
    from urllib.parse import quote_plus

import os
import sys
import getopt
import json
import random
import getopt
import subprocess

# Default settings, create settings.ini file instead of editing this file
wallpaperGetUrls =
["http://www.mylittlewallpaper.com/c/all/api/v2/random.json?size=2&limit=1"]
desktopEnvironment = "gnome"
wallpaperSaveFolder = "wallpapers"
favouritesUsername = ""
favouritesToken = ""

# Change to current directory
dir_name = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_name)

if os.path.exists("settings.ini"):
    try:
        import ConfigParser as cParser
    except ImportError:
        import configparser as cParser

    config = cParser.ConfigParser()
    config.read("settings.ini")
    if config.has_option("MyLittleWallpaperChanger", "wallpaperGetUrls"):
        urlsString = config.get("MyLittleWallpaperChanger", "wallpaperGetUrls")
        wallpaperGetUrls = urlsString.split(" ")
    desktopEnvironment = config.get("MyLittleWallpaperChanger",
                                    "desktopEnvironment")
    wallpaperSaveFolder = config.get("MyLittleWallpaperChanger",
                                     "wallpaperSaveFolder")
    if config.has_option("MyLittleWallpaperChanger", "favouritesUsername"):
        favouritesUsername = config.get("MyLittleWallpaperChanger",
                                        "favouritesUsername")
    if config.has_option("MyLittleWallpaperChanger", "favouritesToken"):
        favouritesToken = config.get("MyLittleWallpaperChanger",
                                     "favouritesToken")

if favouritesUsername and favouritesToken:
    import hashlib
    import uuid
    requestId = uuid.uuid4().hex
    urlHash = hashlib.sha256(str(favouritesUsername + favouritesToken +
                             requestId).encode('utf-8')).hexdigest()
    wallpaperGetUrls = ["http://www.mylittlewallpaper.com/c/all/api/v2/" +
                        "favourites.json?limit=1&sort=random&requestId=" +
                        requestId + "&userName=" +
                        quote_plus(favouritesUsername) + "&hash=" + urlHash]


def get_wallpaper():
    if not os.path.exists(wallpaperSaveFolder):
        os.makedirs(wallpaperSaveFolder)

    random.shuffle(wallpaperGetUrls)
    wallpaperGetUrl = wallpaperGetUrls[0]

    # Fetch json from server
    try:
        jsonData = json.loads(urlopen(wallpaperGetUrl, timeout=60).read().
                              decode('utf-8'))
    except Exception as e:
        print(e)
        return ""

    # Check if json contains a wallpaper
    for wallpaper in jsonData["result"]:
        fullImageUrl = wallpaper["fullImageURL"]
        imageName = os.path.basename(fullImageUrl)
        if not os.path.exists(os.path.join(wallpaperSaveFolder, imageName)):
            try:
                imageData = urlopen(fullImageUrl, timeout=60).read()
                if len(imageData) > 0:
                    fileHandler = open(os.path.join(wallpaperSaveFolder,
                                                    imageName), "wb")
                    fileHandler.write(imageData)
                    fileHandler.close()
                else:
                    raise Exception("Empty file, exiting")
            except Exception as e:
                print(e)
                return ""

        return imageName
    return ""


def change_wallpaper(wallpaper_uri):
    # Todo: Add support for other desktop environments
    try:
        if desktopEnvironment == "gnome":
            os.system("gsettings set org.gnome.desktop.background " +
                      "picture-uri '%s'" % (wallpaper_uri))
        elif desktopEnvironment == "fluxbox":
            try:
                subprocess.Popen(["fbsetbg", wallpaper_uri])
            except:
                sys.stderr.write("Failed to set desktop wallpaper. Please " +
                                 "install fbsetbg.")
        else:
            sys.stderr.write("Failed to set desktop wallpaper. Unsupported " +
                             "desktop environment.")
            return False
        return True
    except Exception as e:
        print(e)
        return False

wallpaperFilename = get_wallpaper()
if wallpaperFilename:
    file_path = os.path.abspath(os.path.join(wallpaperSaveFolder,
                                             wallpaperFilename))
    change_wallpaper("file://" + file_path)
