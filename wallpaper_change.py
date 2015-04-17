#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    # Try urllib (Python 2.x)
    from urllib.request import urlopen
except ImportError:
    # If not found, load urllib2 (Python 3.x)
    from urllib2 import urlopen

import os, sys, getopt, json, random, getopt

# Default settings, please create settings.ini file instead of editing this file
wallpaperGetUrls = ["http://www.mylittlewallpaper.com/c/all/api/v2/random.json?size=2&limit=1"]
desktopEnvironment = "gnome"
wallpaperSaveFolder = "wallpapers"

# Change to current directory
dir_name = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_name)

if os.path.exists("settings.ini"):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read("settings.ini")
    urlsString = config.get("MyLittleWallpaperChanger", "wallpaperGetUrls")
    wallpaperGetUrls = urlsString.split(" ");
    desktopEnvironment = config.get("MyLittleWallpaperChanger", "desktopEnvironment")
    wallpaperSaveFolder = config.get("MyLittleWallpaperChanger", "wallpaperSaveFolder")

def get_wallpaper():
    if not os.path.exists(wallpaperSaveFolder):
        os.makedirs(wallpaperSaveFolder)
    
    random.shuffle(wallpaperGetUrls)
    wallpaperGetUrl = wallpaperGetUrls[0]
    
    # Fetch json from server
    try:
        jsonData = json.loads(urlopen(wallpaperGetUrl, timeout = 60).read())
    except Exception, e:
        print e
        return ""
    
    # Check if json contains a wallpaper
    for wallpaper in jsonData["result"]:
        fullImageUrl = wallpaper["fullImageURL"]
        imageName = os.path.basename(fullImageUrl)
        if not os.path.exists(os.path.join(wallpaperSaveFolder, imageName)):
            try:
                imageData = urlopen(fullImageUrl, timeout = 60).read()
                if len(imageData) > 0:
                    fileHandler = open(os.path.join(wallpaperSaveFolder, imageName), "wb")
                    fileHandler.write(imageData)
                    fileHandler.close()
                else:
                    raise Exception("Empty file, exiting")
            except Exception, e:
                print e
                return ""
        
        return imageName
    return ""

def change_wallpaper(wallpaper_uri):
    # Todo: Add support for other desktop environments
    try:
        if desktopEnvironment == "gnome":
            os.system("gsettings set org.gnome.desktop.background picture-uri '%s'" % (wallpaper_uri))
        else:
            sys.stderr.write("Failed to set desktop wallpaper. Unsupported desktop environment.")
            return False
        return True
    except Exception, e:
        print e
        return False

wallpaperFilename = get_wallpaper()
if wallpaperFilename:
    file_path = os.path.abspath(os.path.join(wallpaperSaveFolder, wallpaperFilename))
    change_wallpaper("file://" + file_path)
