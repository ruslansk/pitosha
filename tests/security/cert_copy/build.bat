rem отключаем вывод команд в консоль / очищаем экран
@echo off
cls

rem ##################################
rem путь к pyinstaller
set pyinstPath=c:\python26\pyinstaller
rem папка с .spec файлами и .exe в \dist
set buildPath=%pyinstPath%\bin
rem ##################################

set moveBin=0
set fileParam=0

rem проверка параметров переданных bat-файлу
:ParamChk
rem если все параметры обработаны или их нет, переходим к выполнению
if "%1%"=="" goto binBuild
rem в случае наличия параметров
goto p%1

:p-F
:p/F
:p/file
:p--file
rem в случае если имя файла введено
if not "%2"=="" (
	set pyFile=%2
	rem минимальные условия для выполнения выполнены, разрешаем сборку
	if not %fileParam%==1 set fileParam=1
)
rem команда shift сдвигает параметры, заданные bat файлу на 1
rem т.е. был параметр %3, стал %2 и т.д.
shift & shift & goto ParamChk

:p-O
:p/O
:p/out
:p--out
if not "%2"=="" set buildPath=%2
shift & shift & goto ParamChk

:p-M
:p/M
:p/move
:p--move
set moveBin=1
shift & goto ParamChk

:p-H
:p/H
:p/help
:p--help
rem вывод подсказки о параметрах
echo.
echo Use: %~n0 [/F [path]filename] [/O dir] [/M]
echo.
echo /F, -F, /file, --file - Path to .py file 
echo /O, -O, /out, --out - Output directory. Default directory - %buildPath%
echo /M, -M, /move, --move - Move created binary to .py file directory
goto :EOF

:binBuild
rem если не был указан .py файл
if %fileParam%==0 echo No file to work with. Use /h for help & goto :EOF
rem ##################################
rem редактируем в зависимости от нужд
rem задаем параметры, в соответствии с которыми будет создаваться spec файл
set specParams=-F -X -o %buildPath%
rem ##################################

rem выполняем сборку spec файла
"%pyinstPath%\MakeSpec.py" %specParams% "%pyFile%"
rem получаем имя файла для сборки. Костыль жуткий
for %%i in (%pyFile%) do (set fileName=%%~ni)
rem выполняем сборку бинарника
%pyinstPath%\Build.py "%buildPath%\%fileName%.spec"

rem при неодходимости переместить exe
if %moveBin%==1 (
	rem получаем папку, в которую будем перемещать. Костыль вернулся!
	for %%i in (%pyFile%) do (set outDir=%%~pi)
	rem команда перемещения с заменой без подтверждения перемещает .exe
	rem файл с таким же именем, как и у .py файла
	move /y "%buildPath%\dist\%fileName%.exe" %outDir%
)