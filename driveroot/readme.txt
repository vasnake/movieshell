# -*- coding: utf-8 -*-

MovieShell is a Python program for view movies from large USB HDD.
MovieShell make it easy by generate and show list of all movies from HDD in one
paged list of buttons. One button - one movie. Press the button, view the movie.

Copyright (C) 2013, Valik Snake
Originally by Valik <vasnake@gmail.com>, 2010

Licensed under GNU GENERAL PUBLIC LICENSE (http://www.gnu.org/licenses/gpl.txt)

usage example:
look into autorun.inf, ar.cmd, bin\startup.cmd, bin\fromdvd.cmd

Writed and tested for Windows XP SP3, Python 2.7
also tested for Windows 7

Russian text

Мувишелл был задуман и впоследствии исполнен как программа, упрощающая жизнь пожилых людей,
желающих смотреть кино на компе, но не желающих разбираться в буковках, кнопочках, списках файлов и прочей белиберде,
типа последовательности действий вызова плеера и выбора файла с диска.
А также для тех, кто хочет помочь этим людям смотреть кино без лишних напрягов.
Воткнул, нажал, смотри.
Основной сценарий такой: воткнули USB диск в комп, сработал авторан (или сами щелкнули специконку на рабочем столе),
развернулось окно со списком фильмов для просмотра. Щелкаем мышкой по названию фильма и смотрим.
Аналогично работаем с DVD, хотя изначально программа заточена именно на использование внешних USB дисков.

Чтобы работать с USB диском, на нем, кроме фильмов, надо разместить содержимое пакета, в корне диска, в составе
    bin\
    ar.cmd
    autorun.ico
    Autorun.inf
после чего выполнить первоначальный сбор информации: start ar.cmd scan

При простом щелчке ЛКМ по названию фильмы запускается плеер Media Player Classic.
Если щелкнуть ЛКМ при зажатой кнопке Ctrl, то запускается плеер VLC.

Некоторые замечания к комплектации, подготовке и установке.
Как это сделано у меня.

Поскольку в Вин7 отменили авторан, пришлось добавить свой пускач
bin/startup.cmd
Его задача - найти на подключенном внешнем диске ту программу, которую
должен был запускать механизм авторана, и запустить ее.
Предполагается, что пускач, в составе пакета Мувишелл, расположен на компе пользователя
а не только на внешнем диске, и выглядит как красивая иконка с названием типа "Смотреть кино!".
Рекомендую использовать.

Еще добавлена опция запуска шелла для DVD, содержащих как, собственно, DVD-кино, так и коллекции видеофайлов
bin\fromdvd.cmd
При запуске скрипт ищет в корне всех подключенных к системе дисков (в подкаталоги не заглядывает!)
видеоматериалы и составляет временный файл - список кино. После чего запускает Мувишелл для этого списка.
Для такого варианта использования, как и для пускача, Мувишелл надо записать на комп пользователя а не только на внешний диск.

На компе пользователя необходимо установить (версии программ не стесняйтесь брать из Интернет свежие,
этот текст был написан сто лет назад)
python-2.7.1.msi (http://www.python.org/getit/releases/2.7.3/)
Обычно это дает папку C:\Python27
Содержимое этой папки надо скопировать на внешний диск с программой, в подкаталог
/bin/Python27

Очень желательно установить на комп пользователя допы к Питону
pywin32-216.win32-py2.7.exe (http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win32-py2.7.exe/download)
без них не будет работать разворачивание окна на весь экран.

В папку
/bin/vlc
внешнего диска надо развернуть прекрасный плеер
vlc-1.1.11-win32.zip (http://sourceforge.net/projects/vlc/files/2.0.5/win32/vlc-2.0.5-win32.zip/download)
так, чтобы программа могла найти файл bin\vlc\vlc.exe

Рекомендую обеспечить наличие файла
C:\Program Files\K-Lite Codec Pack\Media Player Classic\mpc-hc.exe
путем установки прекрасного пакета
K-Lite_Codec_Pack_790_Mega.exe (http://codecguide.com/download_k-lite_codec_pack_mega.htm)
Тогда можно будет смотреть тяжелые фильмы, используя видеоакселератор.

Пути к плеерам прописаны в
bin\const.py
можете править при необходимости.
