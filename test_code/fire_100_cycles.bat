@echo off
echo TDC-GP22 持续交替发波 100 周期
echo ========================================
echo.

set JTOOL=.claude\skills\jtool\scripts\lib\jtool.exe
set /a count=0

:loop
set /a count+=1
echo 周期 %count%/100

REM 发送 FIRE_UP (命令 0x01, 数据 00)
%JTOOL% spiwcmd -i 0 -c 01 00 2>nul

REM 短暂延时
timeout /t 0 /nobreak >nul

REM 发送 FIRE_DOWN (命令 0x01, 数据 00)
%JTOOL% spiwcmd -i 0 -c 01 00 2>nul

REM 间隔 100ms
timeout /t 1 /nobreak >nul

if %count% lss 100 goto loop

echo.
echo ========================================
echo 发波完成！
echo 请用示波器观察 FIRE_UP 和 FIRE_DOWN 引脚
echo ========================================
pause
