@REM -*- coding: utf-8 -*-
@REM movieshell autorun main script
@REM You can use it in three forms:
@REM start ar.cmd
@REM 	if you have movieslist file on your storage;
@REM start ar.cmd scan
@REM 	if you need scan storage for movies and create/update movieslist;
@REM start ar.cmd --listfile pathtomovieslistfile
@REM 	if you have movieslist file somwere not expected by movieshell.

@echo on
chcp 1251 > nul
set wd=%~dp0
set dl=%wd:~0,2%
pushd "%wd%"
set PYTHONPATH=
:: @cls

set path=%dl%\bin\Python27;%dl%\bin;%dl%\bin\vlc;%path%

REM ~ python.exe -u %dl%\bin\shell.py "%1"
REM ~ start /min python.exe -u %dl%\bin\shell.py "%1" "%2"

start pythonw.exe bin\shell.py "%1" "%2"
REM ~ python.exe -u bin\shell.py "%1" "%2"

popd
exit
