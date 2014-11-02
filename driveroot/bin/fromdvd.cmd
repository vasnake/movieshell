@REM -*- coding: utf-8 -*-
@REM Movieshell DVD starter script, use it instead of Windows autorun feature.
@REM Copy movieshell pack to computer apps dir, like C:\opt\movieshell
@REM make shortcut on Desktop contained command
@REM start C:\opt\movieshell\bin\fromdvd.cmd

@echo on
chcp 1251 > nul
set wd=%~dp0
set dl=%wd:~0,2%
pushd "%wd%"
set PYTHONPATH=
:: @cls

set path=c:\Python27;%path%

REM ~ start /min python.exe -u %dl%\bin\shell.py "%1"
REM ~ pythonw.exe %dl%\bin\shell.py "%1"
REM ~ start /min python.exe -u .\fromdvd.py

start pythonw.exe .\fromdvd.py
REM ~ python.exe -u .\fromdvd.py

popd
exit
