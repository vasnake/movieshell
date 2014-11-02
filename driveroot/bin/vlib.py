# -*- coding: utf-8 -*-

'''
Created on Nov 30, 2010

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

Russian text

Библиотека классов, используемых в оболочке,
запуск кина из файлов, имена файлов записаны в списке, хранимом в виде файла;
для каждого файла типа "кино" создается кнопка,
нажатие на которую приводит к запуску кина.

Через ключ командной строки можно запустить сканирование хранилища
с записью результатов в файл.

'''


import sys, os, time, re, subprocess

import jsonpickle
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

import const

moviesListFN = const.MDB_FILENAME
CP = const.CP

class VMovie:
    ''' параметры одного кина
    основной параметр - имя файла, записывается относительно
    корня хранилища; корнем считаю каталог в котором каталог bin\
    в котором этот скрипт
    '''
    fileName = '' # mandatory
    enTitle = ''
    ruTitle = ''
    storeDate = ''
    pubDate = ''
    director = ''

    def __init__(self):
        ''' конструктор должен быть минимален (без доп.параметров)
        ибо иначе не работает восстановление через jsonpickle.decode
        '''
        print 'VMovie.init'
        self.storeDate = u' '
        self.pubDate = u' '
        self.director = u' '
        self.fileName = u' '
        self.enTitle = u' '
        self.ruTitle = u' '

    def getTitle(self):
        t = ''
        if self.ruTitle.strip():
            t += self.ruTitle
        if self.ruTitle != self.enTitle:
            t += ' / %s' % self.enTitle
        if self.pubDate.strip():
            t += ' (%s)' % self.pubDate
        return t


    def configure(self, fn, rootdir=''):
        print 'VMovie.configure'
        self.fileName = fn
        self.enTitle = fn
        self.ruTitle = fn
        if rootdir == '':
            return
        else:
            print 'gather file info'
            fulln = rootdir + fn
            shortn = os.path.basename(fulln)

            sd = os.path.getctime(fulln) # file datetime (store date)
            sd = time.localtime(sd)
            sd = time.strftime('%Y-%m-%d %H-%M-%S', sd)
            self.storeDate = sd

            pd = '' # four digit from filename (pub. date)
            m = re.search('\d{4}', shortn)
            if m: # have published date
                pd = m.group()
                self.pubDate = pd

            # убрать из имени файла год, двойные точки, расширение
            # это будет титул
            t = re.sub('\d{4}', '', shortn)
            t = re.sub('\.{2}', '.', t)
            t = re.sub('\.(mkv|avi|flv|iso)', '', t)
            self.enTitle = self.ruTitle = t

            print (u'fileInfo: t [%s], sn [%s], fn [%s], sd [%s], pd [%s]' % (t, shortn, fulln, sd, pd)).encode('utf8')
    # def configure(self, fn, rootdir='')


    def encode(self):
        ''' encode to utf8 before serialize
        '''
        self.storeDate = self.storeDate.encode('utf8')
        self.pubDate = self.pubDate.encode('utf8')
        self.director = self.director.encode('utf8')
        self.fileName = self.fileName.encode('utf8')
        self.enTitle = self.enTitle.encode('utf8')
        self.ruTitle = self.ruTitle.encode('utf8')

# class VMovie


class VScanner:
    ''' поиск файлов кина и сохранение полученного списка;
    старые записи из файла сохраняются, если кино такое на диске есть.
    '''
    rootDir = ''
    dictMovies = ''

    def __init__(self, rootdir, fullname=''):
        print 'VScanner.init, root [%s]' % rootdir
        self.dictMovies = {}
        self.rootDir = rootdir
        self.fullname = fullname
        self.listFile = ''

        fl = ''
        try:
            fl = open(self.getMoviesListFN(), 'rU')
        except:
            print "file doesn't exists"
        if fl:
            ml = {}
            for x in fl:
                x = x.strip()
                if not x: continue
                print 'read line [%s]' % x
                m = jsonpickle.decode(x)
                print (u'rootdir + mov fn [%s]' % (rootdir + m.fileName)).encode('utf8')
                if os.path.exists(rootdir + m.fileName):
                    ml[m.fileName] = m
                elif os.path.exists(m.fileName):
                    ml[m.fileName] = m
                else:
                    print "file doesn't exist"
            fl.close()
            self.dictMovies = ml
    # def __init__(self, rootdir)


    def destroyMoviesList(self, delfile=False):
        self.dictMovies = {}
        if delfile:
            try:
                os.remove(self.getMoviesListFN())
            except:
                print "file doesn't exists"
    # def destroyMoviesList():


    def getMoviesListFN(self):
        if self.fullname:
            res = os.path.normpath(self.fullname)
        else:
            res = os.path.normpath(os.path.join(self.rootDir, moviesListFN))
        print (u"getMoviesListFN: '%s'" % res).encode(CP)
        return res
    # def getMoviesListFN()


    def scan(self, nameslist=None, storeFullName=False):
        print 'VScanner.scan'
        rd = self.rootDir
        rdl = len(rd)
        ml = self.dictMovies
        fl = open(self.getMoviesListFN(), 'w')
        self.listFile = fl

        if nameslist:
            res = nameslist
        else:
            res = findFiles(rd, recurse=1, pattern='*.flv;*.avi;*.mkv;*.iso', return_folders=0)

        for x in res:
            if storeFullName:
                x = x.decode('cp1251')
            else:
                x = x[rdl:].decode('cp1251') # get unicode from windows cp

            print (u'found movie [%s]' % x).encode('utf8')
            m = VMovie()
            if storeFullName:
                m.configure(x)
            else:
                m.configure(x, rd)

            try:
                m = ml[m.fileName]
                print 'entry exists already'
            except:
                print 'it is a new entry'

            m.encode()
            s = jsonpickle.encode(m)
            fl.write(s+'\n')
        # end for each file
        fl.close()

# class VScanner


def findFiles(root, recurse=0, pattern='*', return_folders=0):
    import fnmatch, os, string
    # initialize
    result = []
    # must have at least root folder
    try:
        names = os.listdir(root)
    except os.error:
        return result
    # expand pattern
    pattern = pattern or '*'
    pat_list = string.splitfields( pattern , ';' )

    # check each file
    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))
        # grab if it matches our pattern and entry type
        for pat in pat_list:
            if fnmatch.fnmatch(name, pat):
                if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
                    result.append(fullname)
                continue

        # recursively scan other folders, appending results
        if recurse:
            if os.path.isdir(fullname) and not os.path.islink(fullname):
                result = result + findFiles(fullname, recurse, pattern, return_folders)

    return result
# def findFiles(root, recurse=0, pattern='*', return_folders=0)


if __name__ == '__main__':
    print 'sys.argv[0] = [%s], sys.path[0] = [%s]' % (sys.argv[0], sys.path[0])
