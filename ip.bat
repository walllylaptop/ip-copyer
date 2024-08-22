@echo off
rem Verkrijg het IP-adres
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4 Address"') do set ip=%%i
set ip=%ip:~1%

rem Verzend het IP-adres naar de lokale database via een HTTP POST-verzoek
curl -X POST http://192.168.1.27:8000/api/store_ip -H "Content-Type: application/json" -d "{\"ip\": \"%ip%\"}"

echo IP-adres (%ip%) is verzonden naar de database.

rem Controleer of het batchbestand op een specifieke USB-stick staat
setlocal enabledelayedexpansion
set batchpath=%~dp0
set drive=%batchpath:~0,2%

rem Verkrijg het volume label van de schijf
for /f "delims=" %%a in ('powershell -command "Get-Volume -DriveLetter %drive:~0,1% | Select-Object -ExpandProperty FileSystemLabel"') do set volume=%%a

if /i "%volume%"=="HEMA_16GB" (
    echo Dit batchbestand staat op de USB-stick met de naam HEMA_16GB.
    pause
) else (
    echo Dit batchbestand staat niet op de USB-stick met de naam HEMA_16GB.
    goto :delete_self
)

:eof
endlocal
goto :eof

:delete_self
rem Verwijder het batchbestand
cd %~dp0
del "%~f0"
echo Batchbestand is verwijderd.
pause
