@echo off
set PYTHONHOME=D:\Programs\Devel\Python27

rem REG ADD HKCR\Python.File\shell\open\command /ve /t REG_SZ /d ""D:\Programs\Devel\Python27\python.exe" "%1" %*"
rem ftype Python.File="D:\Programs\Devel\Python27\python.exe" "%1" %*
set PY_HOME=%PYTHONHOME%

set PYTHONPATH=%PYTHONHOME%;D:\Programs\Devel\Python27\Lib;D:\Programs\Devel\Python27\DLLs;D:\Programs\Devel\Python27\Lib\lib-tk
set PYTHONPATH=%PYTHONPATH%;D:\Programs\Devel\Python27\Scripts
set PATH=D:\Programs\Devel\Python27\;D:\Programs\Devel\Python27\Scripts\;%PATH%
cd D:\Programs\Devel\Python27_tests\uncompyle2\
cmd
