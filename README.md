# My Little Wallpaper - Python wallpaper switcher for Linux

Random wallpaper switcher for My Little Wallpaper.

Currently supported desktop environments / window managers:

- `gnome` - Unity, Gnome and Cinnamon
- `fluxbox` - Fluxbox, Openbox, JWM, AfterStep (requires **fbsetbg**, experimental)

Looking for Windows equivalent? Check the [software page](http://www.mylittlewallpaper.com/c/all/software) at mylittlewallpaper.com.

## Usage

Just run the script from command line with `./wallpaper_change.py`

If you want to change settings, copy settings.example.ini to settings.ini and modify the file.

### Favourites

To be able to switch between favourite wallpapers randomly, API token is needed. This can be found in [account settings](http://www.mylittlewallpaper.com/c/all/account).

An example for settings can be found in settings.example.fav.ini

## Cron

Copy equivalent shell script from cron folder to repository root and configure it to crontab. For example:

```
0 * * * * /home/folder/Documents/MLWPWallpaperChanger/gnome.sh >/dev/null 2>&1
```
