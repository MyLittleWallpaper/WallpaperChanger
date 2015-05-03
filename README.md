# My Little Wallpaper - Python wallpaper switcher for Linux

Random wallpaper switcher for My Little Wallpaper.

Currently supported desktop environments / window managers:

- Unity, Gnome and Cinnamon
- Fluxbox, Openbox, JWM, AfterStep (experimental)

Looking for Windows equivalent? Check the [software page](http://www.mylittlewallpaper.com/c/all/software) at mylittlewallpaper.com.

## Usage

Just run the script from command line with `./wallpaper_change.py`

If you want to change settings, copy settings.example.ini to settings.ini and modify the file.

## Cron

Copy gnome.sh from cron folder to repository root and configure it to crontab. For example:

```
0 * * * * /home/folder/Documents/MLWPWallpaperChanger/gnome.sh >/dev/null 2>&1
```
