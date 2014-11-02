movieshell
==========

UI for movies collection on ext. USB drive

If you have some ext. USB drive with movies, like avi/mp4/mkv or maybe iso (video DVD image)
and you need to simplify access to that library,
movieshell can help.

It's a Python program with UI based on Tkinter.
Writed and tested using MS Windows XP/Windows 7; Python 2.7

For playing movies, two options supported:

* [VLC media player](http://www.videolan.org/vlc/)
* [Media Player Classic](http://mpc-hc.org/downloads/)

For watch a movie, all you need to do is plug-in your ext. USB drive to computer,
start the movieshell (if autorun didn't do it) and
click on button with movie name on it.
If you click on button holding CTRL, movie will be started in alternate player.

Screenshots

![screenshot 1](movieshell01.png "screenshot 1")

![screenshot 2](movieshell02.png "screenshot 2")

## Install

Copy files and folders from folder `driveroot` into root folder of your USB ext. drive.

Install [Python 2.7](https://www.python.org/download/releases/2.7/) on computer.

Copy contents of C:\Python27 to /bin/Python27 on ext. USB drive.

Check contents of /bin/const.py file and make sure that movieshell can find video player executables.

## Run

Before using movieshell, you have to index movies library.
To do so, start scan process

    cmd.exe /k ar.cmd scan

After that you can start movieshell with command

    cmd.exe /k ar.cmd

In case if autorun didn't work.

## Links

* http://vasnake.blogspot.ru/2013/02/movieshell.html
* http://vasnake.blogspot.ru/2011/11/linux.html
* http://vasnake.blogspot.ru/2012/04/maximized-window.html
* http://vasnake.blogspot.ru/2011/10/getlogicaldrives.html
* http://vasnake.blogspot.ru/2010/12/magnate.html
