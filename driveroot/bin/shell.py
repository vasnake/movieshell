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

Оболочка,
запуск кина из файлов, имена файлов записаны в списке, хранимом в виде файла;
для каждого файла типа "кино" создается кнопка,
нажатие на которую приводит к запуску кина.
Файл и именами фильмов создается (и обновляется) запуском оболочки с параметром scan
После создания файла, параметры фильмов можно править (русское название, английское название,...)

Обязательная структура каталогов и раскладка файлов проекта:
от корня диска
\bin\
    jsonpickle\
    Python27\	-	рантаймовый Питон. Иногда в виде "портабл" не работает, тогда надо ставить Питон в систему
    vlc\		-	видеоплеер
    shell.py
    vlib.py
    const.py
\.movieslist	-	база фильмов, создается/обновляется запуском шелла с параметром scan
\ar.cmd		-	скрипт для авторана, должен запускать шелл
\autorun.ico
\Autorun.inf

Tkinter начал изучать отсюда
http://www.ferg.org/thinking_in_tkinter/all_programs.html

todo
 * поиск/фильтр по подстроке
 * сортировка по дате выхода фильмы
done
 * выводить только те кнопки, которые ссылаются на реальный файл
 * отсортировать кнопки по дате файла
 * сделать буквы побольше и пожирней на кнопках
 * рисовать эффект прохождения курсора над кнопкой
 * разворачивать окно на полный экран
 * сделать вывод кнопок группами по 20 штук (200-300 файлов это норма)
 * кнопка текущей группы имеет нажатый вид (размер, чтоб текст весь влезал)
 * фильмы можно сортировать и по именам и по датам
 * цвет фона затемнить
 * немного рефакторинга для уменьшения длины функций и приведения кода в норму
 * возможность смотреть в других плеерах (при зажатом CTRL?)
 * игнорировать регистр буков при сортировке по названиям
 * подсветку активных кнопок более явной (тон сменить с серого на желтоватый?)
 * подстройка под Win7
 * добавлен пускач startup.cmd заменяющий авторан
 * добавлен пускач fromdvd.cmd открывающий список фильмов с DVD
'''

usage = 'tcl/tk "Movies List" program. Compile to exe and use with autorun option for CD'

import os, time, re, subprocess
from Tkinter import *

from vlib import *
import const


class VAppListMovies:
    ''' считать из файла список кинов и вывести
    интерфейс для удобного выбора и просмотра кина
    '''
    numButtons = const.NUM_BUTTONS_ON_PAGE
    mainFrame = '' # frame - container
    topFrame = '' # top frame for control buttons
    rightFrame = '' # right frame for page buttons
    frame = '' # movie buttons container
    currPage = 1
    sortMethod = const.SORT_FILE_DATE # 'filedate' # moviename
    ctrlPressed = False

    def __init__(self, tk, rootdir):
        print 'listMovies.init'
        sc = VScanner(rootdir)
        self.dictMovies = sc.dictMovies
        self.rootDir = rootdir
        tk.title('Список фильмов')
        self.tk = tk
        # make it cover the entire screen
        w, h = tk.winfo_screenwidth(), tk.winfo_screenheight()
        print 'VAppListMovies.init, w %s x h %s px' % (w, h)
        #tk.overrideredirect(1)
        # windows 7 taskpane on right side:
        tk.geometry("%dx%d+0+0" % (w-100, h-77))

        tk.focus_set()
        tk.bind('<Escape>', self.quitFunc)
        tk.bind('<Control_L>', lambda event: self(evt=event, cmd=const.CMD_CTRL_DOWN))
        tk.bind('<Control_R>', lambda event: self(evt=event, cmd=const.CMD_CTRL_DOWN))
        tk.bind('<KeyRelease-Control_L>', lambda event: self(evt=event, cmd=const.CMD_CTRL_UP))
        tk.bind('<KeyRelease-Control_R>', lambda event: self(evt=event, cmd=const.CMD_CTRL_UP))
        self.bgColor = tk.cget('bg')


    def configure(self, movieslistfilename=''):
        print 'listMovies.configure'
        if movieslistfilename:
            sc = VScanner(rootdir=self.rootDir, fullname=movieslistfilename)
            self.dictMovies = sc.dictMovies

        self.currPage = 1
        self.showButtons()
    # def configure(self)


    def doWork(self):
        print 'listMovies.doWork'
        self.tk.iconify()
        self.tk.update()
        self.tk.deiconify()
        #self.tk.wm_attributes("-topmost", 1)
        self.tk.after(500, self.maximizeWindow)
        #self.tk.valmID = 'root'
        #self.tk.bind('<Map>', maximizeWindow)
        self.tk.mainloop()


    def maximizeWindow(self):
        ''' use winapi
        SendMessage(hwnd, WM_SYSCOMMAND, SC_MAXIMIZE, 0);
        PostMessage - is async wersion of SendMessage
        '''
        print 'listMovies.maximizeWindow'
        try:
            import string, win32con, win32gui
            w = self.tk
            sh = w.wm_frame() # var type [<type 'str'>], var value ['0x180116']
            h = string.atoi(sh, 0)
            win32gui.PostMessage(h, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
            #~ win32gui.SendMessage(h, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
        except Exception, e:
            if type(e).__name__ == 'COMError': print 'COM Error, msg [%s]' % e
            else:
                print "can't maximize window"
                import traceback
                traceback.print_exc(file=sys.stderr)
    # def maximizeWindow(self):


    def quitFunc(self, event):
        print 'VAppListMovies.quitFunc'
        self.tk.destroy()


    def bindHover(self, b):
        b.bind(
            '<Any-Enter>',
            lambda event, btn=b, cmd=const.CMD_ENTER: self(evt=event, btn=btn, cmd=cmd)
        )
        b.bind(
            '<Any-Leave>',
            lambda event, btn=b, cmd=const.CMD_LEAVE: self(evt=event, btn=btn, cmd=cmd)
        )
        #~ b.bind('<FocusIn>', lambda event, btn=b, cmd='enter': self(evt=event, btn=btn, cmd=cmd) )
        #~ b.bind('<FocusOut>', lambda event, btn=b, cmd='leave': self(evt=event, btn=btn, cmd=cmd) )


    def createFrame(self):
        print 'listMovies.createFrame'
        tk = self.tk
        frame = self.mainFrame
        if frame: frame.destroy()

        # container, main frame
        frame = Frame(tk)
        frame.pack(expand=YES, fill=BOTH)
        self.mainFrame = frame

        # right frame, page controls
        frame = Frame(self.mainFrame, width=100, borderwidth=5, bg="#%02x%02x%02x" % const.COLOR_RIGHT)
        frame.pack(side=RIGHT, expand=NO, fill=Y)
        self.rightFrame = frame

        # top frame, sort, filter
        frame = Frame(self.mainFrame, height=50, borderwidth=5, bg="#%02x%02x%02x" % const.COLOR_TOP)
        frame.pack(side=TOP, expand=NO, fill=X)
        self.topFrame = frame

        # movies buttons frame
        frame = Frame(self.mainFrame, bg="#%02x%02x%02x" % const.COLOR_LIST)
        frame.pack(side=LEFT, expand=YES, fill=BOTH)
        self.frame = frame

        # right frame sys.buttons
        b = Button(self.rightFrame, text="Exit (выход)", width=20, command=tk.destroy)
        self.bindHover(b)
        b.grid(row=1, column=0)
        b.focus_force()
    # def createFrame(self)


    def addCtrlButton(self, t, s, c):
        ''' t - title; s - sort; c - column in grid
        '''
        b = Button(self.topFrame, text=t, width=const.WIDTH_CTRL_BTN, font=('Verdana', 10, 'bold'))
        b.bag = {}
        b.bag[const.CMD_SORT] = s
        b.configure(command = lambda btn=b, cmd=const.CMD_SORT: \
                    self(btn=btn, cmd=cmd) )
        if self.sortMethod == s:
            b.configure(bg="#%02x%02x%02x" % const.COLOR_CURR_BTN)
        b.grid(row=0, column=c)

    def addMovieButton(self, m, x):
        partNo = self.currPage - 1
        b = Button(self.frame, text=m.getTitle(), width=const.WIDTH_MOVIE_BTN, font=('Verdana', 12, 'bold'))
        b.bag = {}
        b.bag[const.BAG_KEY_MOVIE] = m
        b.configure(command = lambda btn=b: self(btn=btn))
        self.bindHover(b)
        b.grid(row=x-partNo, column=0)

    def addPageButton(self, t, x):
        partNo = self.currPage - 1
        numb = self.numButtons
        b = Button(self.rightFrame, text=t, width=const.WIDTH_PAGE_BTN, font=('Verdana', 10, 'bold'))
        b.bag = {}
        b.bag[const.CMD_PAGE] = x # 0,20,40
        b.configure(command = lambda btn=b, cmd=const.CMD_PAGE: self(btn=btn, cmd=cmd))
        if x == partNo:
            print "it's a curr.page button"
            b.configure(bg="#%02x%02x%02x" % const.COLOR_CURR_BTN) # b.configure(state=DISABLED)
        b.grid(row=(x/numb)+2, column=0)


    def showButtons(self):
        ''' recreate GUI
        '''
        print 'listMovies.showButtons'
        partNo = self.currPage - 1
        numb = self.numButtons
        self.createFrame()

        # control buttons
        self.addCtrlButton('Сортировка по дате записи', const.SORT_FILE_DATE, 0)
        self.addCtrlButton('Сортировка по названию кина', const.SORT_MOVIE_NAME, 1)

        mlist = sorted(self.dictMovies.values(), key=lambda m: m.storeDate, reverse=True)
        if self.sortMethod == const.SORT_MOVIE_NAME:
            mlist = sorted(self.dictMovies.values(), key=lambda m: m.getTitle().upper() )

        # нарисовать кнопки, открывающие фильмы
        x = 0
        for m in mlist:
            if x % numb == 0:
                self.addPageButton('фильмы %s - %s' % (x+1, x+numb), x)
            x += 1
            if x <= (partNo + numb) and x > partNo:
                pass
            else:
                continue

            self.addMovieButton(m, x)
        # for m in sorted(self.dictMovies ...
        self.maximizeWindow()
    # def showButtons(self, partNo)


    def __call__(self, evt='', btn='', cmd=''):
        ''' действие по нажатию кнопки, запуск фильмы
        Called when the instance is ``called'' as a function;
        if this method is defined, x(arg1, arg2, ...) is a shorthand for
        x.__call__(arg1, arg2, ...)
        '''
        if evt:
            if evt.state & const.BIT_CONTROL:
                if not self.ctrlPressed:
                    print 'switch ctrl to 1'
                self.ctrlPressed = True
            else:
                if self.ctrlPressed:
                    print 'switch ctrl to 0'
                self.ctrlPressed = False

        if cmd:
            if cmd == const.CMD_CTRL_DOWN:
                self.ctrlPressed = True
                print 'ctrl-btn-evt press'
            elif cmd == const.CMD_CTRL_UP:
                self.ctrlPressed = False
                print 'ctrl-btn-evt release'
            elif cmd == const.CMD_ENTER:
                btn.configure(bg="#%02x%02x%02x" % const.COLOR_HOVER_BTN)
            elif cmd == const.CMD_LEAVE:
                btn.configure(bg=self.bgColor) # self.tk.cget('bg')
            elif cmd == const.CMD_SORT:
                sort = btn.bag[const.CMD_SORT]
                if self.sortMethod != sort:
                    self.sortMethod = sort
                    self.currPage = 1
                    self.showButtons()
            elif cmd == const.CMD_PAGE:
                x = int(btn.bag[const.CMD_PAGE])
                print 'show buttons %s - %s' % (x+1, x+self.numButtons)
                self.currPage = x+1
                self.showButtons()
            return
        # if cmd

        # no cmd, show movie
        print 'listMovies.call'
        m = btn.bag[const.BAG_KEY_MOVIE]
        rd = self.rootDir
        fn = u'%s' % (rd+m.fileName)
        if not os.path.exists(fn.encode('cp1251')):
            fn = u'%s' % m.fileName

        cmdl = [const.PLAYER_MPC, fn.encode('cp1251')] + const.OPTS_MPC
        if self.ctrlPressed or not os.path.exists(const.PLAYER_MPC):
            cmdl = [rd+const.PLAYER_VLC] + const.OPTS_VLC + [fn.encode('cp1251')]
        print (u'cmd [%s]' % cmdl).encode('utf8')
        self.tk.iconify()
        print 'retcode [%s]' % subprocess.call(cmdl)
        self.tk.update()
        self.tk.deiconify()
        self.tk.focus_set()
    # def __call__(self, btn='', cmd='')

#class VAppListMovies


def getRootDir():
    wd = sys.path[0] # workdir, dirname where is shell.py
    rd = wd[:-3] # rootdir = workdir - bin dir
    return rd


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    print 'sys.argv[0] = [%s], sys.path[0] = [%s]' % (sys.argv[0], sys.path[0])

    fname = ''
    if argc > 1 and argv[1] == 'scan':
        t = VScanner(getRootDir())
        t.scan()
        sys.exit('scanned')
    elif argc > 2 and argv[1] == '--listfile':
        fname = argv[2]

    gui = Tk()
    appMovlist = VAppListMovies(gui, getRootDir())
    appMovlist.configure(fname)
    appMovlist.doWork()
    sys.exit(usage)


def trash(tk):
    """ Предыдущие попытки разворачивания окна на весь экран. Жалко выбрасывать
    """
    try:
        hwnd = tk.winfo_id() # noop, need PyHANDLE for win32api
#			hwnd = Toplevel().winfo_id()
        win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
#			win32api.SendMessage(hwnd, win32con.SC_MAXIMIZE, 0)
#			win32api.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#			win32ui.GetMainFrame().SendMessage(win32con.SC_MAXIMIZE, 0)
#			win32ui.GetMainFrame().ShowWindow(win32con.SW_MAXIMIZE)
#			win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    # get PyCWnd from hwnd
#			frame = win32ui.CreateWindowFromHandle(string.atoi(w.wm_frame(), 0))
        frame = win32ui.CreateWindowFromHandle(w.winfo_id())
        frame.SendMessage(win32con.SC_MAXIMIZE)
#		tk = self.tk
#		hwnd = tk.winfo_id() # need PyHANDLE for win32api
#			hwnd = Toplevel().winfo_id()
#		win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
#			win32api.SendMessage(hwnd, win32con.SC_MAXIMIZE, 0)
#			win32api.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#			win32ui.GetMainFrame().SendMessage(win32con.SC_MAXIMIZE, 0)
#			win32ui.GetMainFrame().ShowWindow(win32con.SW_MAXIMIZE)
#			win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    except Exception, e:
        if type(e).__name__ == 'COMError': print 'COM Error, msg [%s]' % e
        else:
            print "can't maximize window"
            import traceback
            traceback.print_exc(file=sys.stderr)
    def eMaximizeWindow(event):
        ''' use winapi
        http://python.net/crew/mhammond/win32/
        SendMessage(hwnd, WM_SYSCOMMAND, SC_MAXIMIZE, 0);
        PostMessage ?
        BOOL WINAPI ShowWindow(
          __in  HWND hWnd,
          __in  int nCmdShow
        ); // SW_MAXIMIZE - 3 Maximizes the specified window.
        http://stackoverflow.com/questions/3306189/using-tcl-extensions-to-set-native-window-style-in-tkinter
        '''

        print 'maximizeWindow'
        try:
            import string, win32con
            import win32ui
    #		import win32gui, win32api

            w = event.widget
            w.bind('<Map>', None)
            if w.valmID != 'root': return
            print 'maximizeWindow, root widget'
            # get PyCWnd from hwnd
            frame = win32ui.CreateWindowFromHandle(string.atoi(w.wm_frame(), 0))
            frame.SendMessage(win32con.SC_MAXIMIZE)
    #		tk = self.tk
    #		hwnd = tk.winfo_id() # need PyHANDLE for win32api
    #			hwnd = Toplevel().winfo_id()
    #		win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
    #			win32api.SendMessage(hwnd, win32con.SC_MAXIMIZE, 0)
    #			win32api.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    #			win32ui.GetMainFrame().SendMessage(win32con.SC_MAXIMIZE, 0)
    #			win32ui.GetMainFrame().ShowWindow(win32con.SW_MAXIMIZE)
    #			win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        except Exception, e:
            if type(e).__name__ == 'COMError': print 'COM Error, msg [%s]' % e
            else:
                print "can't maximize window"
                import traceback
                traceback.print_exc(file=sys.stderr)
#def maximizeWindow(self):
#			def trash():
