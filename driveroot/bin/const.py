# -*- coding: utf-8 -*-

'''
Created on Dec 23, 2010

@author: Valik <vasnake@gmail.com>

 Copyright (C) 2010, Valik Snake
 Originally by Valik <vasnake@gmail.com>, 2010

    This file is part of MovieShell.

    MovieShell is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MovieShell is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MovieShell.  If not, see <http://www.gnu.org/licenses/>.

Constants for MovieShell

'''

CP = 'utf8'

PLAYER_VLC = r'bin\vlc\vlc.exe'
OPTS_VLC = ['--fullscreen', '--video-on-top', '--sub-track=99']
PLAYER_MPC = r'c:\Program Files (x86)\K-Lite Codec Pack\Media Player Classic\mpc-hc.exe'
OPTS_MPC = ['/play', '/close', '/fullscreen']

MDB_FILENAME = u'.movieslist'
NUM_BUTTONS_ON_PAGE = 20

SORT_FILE_DATE = 'filedate'
SORT_MOVIE_NAME = 'moviename'

CMD_ENTER = 'enter'
CMD_LEAVE = 'leave'
CMD_SORT = 'sort'
CMD_PAGE = 'showpart'
CMD_CTRL_DOWN = 'ctrldown'
CMD_CTRL_UP = 'ctrlup'

WIDTH_CTRL_BTN = 25
WIDTH_MOVIE_BTN = 80
WIDTH_PAGE_BTN = 15

COLOR_CURR_BTN = (230, 255, 230)
COLOR_HOVER_BTN = (255, 250, 220)
COLOR_RIGHT = (90, 90, 99)
COLOR_TOP = (70, 70, 99)
COLOR_LIST = (77, 77, 77)

BAG_KEY_MOVIE = 'movie'

#Bitmasks: BIT_SHIFT = 0x001 BIT_CAPSLOCK = 0x002 BIT_CONTROL = 0x004 BIT_LEFT_ALT = 0x008 BIT_NUMLOCK = 0x010 BIT_RIGHT_ALT = 0x080 BIT_MB_1 = 0x100 BIT_MB_2 = 0x200 BIT_MB_3 = 0x400
BIT_CONTROL = 0x004

if __name__ == '__main__':
    import sys
    print 'sys.argv[0] = [%s], sys.path[0] = [%s]' % (sys.argv[0], sys.path[0])
