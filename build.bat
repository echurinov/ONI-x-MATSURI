::Runs this script as admin
::From https://stackoverflow.com/questions/1894967/how-to-request-administrator-access-inside-a-batch-file
@echo off

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

pip install -r requirements.txt
::pyinstaller --onefile --add-data "assets;assets" main.py --windowed
::downloads and installs NSIS (pynsist requirement)
powershell -Command "Invoke-WebRequest https://prdownloads.sourceforge.net/nsis/nsis-3.08-setup.exe -OutFile nsis-3.08-setup.exe"
START /WAIT nsis-3.08-setup.exe
::Runs pynsist to create installer
pynsist installer.cfg

