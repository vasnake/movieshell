# -*- mode: python; coding: utf-8 -*-
# (c) Valik mailto:vasnake@gmail.com

'''
Created on Jan 22, 2013

@author: Valik <vasnake@gmail.com>

 Copyright (C) 2013, Valik Snake
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

Russian text

Поскольку часть коллекции видео находится на DVD, нужна оболочка-меню для их просмотра.
Вставить DVD, закрыть повылезавшие окна, запустить ярлык к данной программе.
'''

usage = 'invoke this when DVD is inserted'

import os, sys, time, re, subprocess, tempfile
from vlib import findFiles, VScanner
from startup import getLogicalDrives


def saveMoviesList(nameslist):
    """ save list of movies file names to .movieslist file
    nameslist like ['E:\\wsdvdtest.iso', 'E:\\страшное кино.avi', 'D:\\VIDEO_TS']
    return file name for created file
    """
    tempdir = tempfile.gettempdir()
    #~ print tempdir
    moviesDir = VScanner(tempdir)
    moviesDir.destroyMoviesList(delfile=True)
    moviesDir.scan(nameslist=nameslist, storeFullName=True)
    return moviesDir.getMoviesListFN()
#def saveMoviesList():


def startMovieShell(fname):
    """ start UI inited from movies list file
    """
    pth = os.path.normpath(os.path.join(sys.path[0], '..', 'ar.cmd'))
    if os.path.exists(pth):
        cmd = [pth, '--listfile', fname]
        subprocess.call(cmd)
#def startMovieShell(fname):


def main():
    """ find all drives;
    on each drive find movies;
    make movies list;
    start MovieShell for this list.
    """

    drives = getLogicalDrives()
    print drives
    movies = []
    for d in drives:
        flist = findFiles(d+':/', recurse=0, pattern='*.flv;*.avi;*.mkv;*.iso;*.mp4;VIDEO_TS', return_folders=1)
        movies += flist
    print movies

    fname = saveMoviesList(movies)
    startMovieShell(fname)
#def main():


if __name__ == '__main__':
    print 'sys.argv[0] = [%s], sys.path[0] = [%s]' % (sys.argv[0], sys.path[0])
    main()
    sys.exit(usage)
