rem ��������� ����� ������ � ������� / ������� �����
@echo off
cls

rem ##################################
rem ���� � pyinstaller
set pyinstPath=c:\python26\pyinstaller
rem ����� � .spec ������� � .exe � \dist
set buildPath=%pyinstPath%\bin
rem ##################################

set moveBin=0
set fileParam=0

rem �������� ���������� ���������� bat-�����
:ParamChk
rem ���� ��� ��������� ���������� ��� �� ���, ��������� � ����������
if "%1%"=="" goto binBuild
rem � ������ ������� ����������
goto p%1

:p-F
:p/F
:p/file
:p--file
rem � ������ ���� ��� ����� �������
if not "%2"=="" (
	set pyFile=%2
	rem ����������� ������� ��� ���������� ���������, ��������� ������
	if not %fileParam%==1 set fileParam=1
)
rem ������� shift �������� ���������, �������� bat ����� �� 1
rem �.�. ��� �������� %3, ���� %2 � �.�.
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
rem ����� ��������� � ����������
echo.
echo Use: %~n0 [/F [path]filename] [/O dir] [/M]
echo.
echo /F, -F, /file, --file - Path to .py file 
echo /O, -O, /out, --out - Output directory. Default directory - %buildPath%
echo /M, -M, /move, --move - Move created binary to .py file directory
goto :EOF

:binBuild
rem ���� �� ��� ������ .py ����
if %fileParam%==0 echo No file to work with. Use /h for help & goto :EOF
rem ##################################
rem ����������� � ����������� �� ����
rem ������ ���������, � ������������ � �������� ����� ����������� spec ����
set specParams=-F -X -o %buildPath%
rem ##################################

rem ��������� ������ spec �����
"%pyinstPath%\MakeSpec.py" %specParams% "%pyFile%"
rem �������� ��� ����� ��� ������. ������� ������
for %%i in (%pyFile%) do (set fileName=%%~ni)
rem ��������� ������ ���������
%pyinstPath%\Build.py "%buildPath%\%fileName%.spec"

rem ��� ������������� ����������� exe
if %moveBin%==1 (
	rem �������� �����, � ������� ����� ����������. ������� ��������!
	for %%i in (%pyFile%) do (set outDir=%%~pi)
	rem ������� ����������� � ������� ��� ������������� ���������� .exe
	rem ���� � ����� �� ������, ��� � � .py �����
	move /y "%buildPath%\dist\%fileName%.exe" %outDir%
)