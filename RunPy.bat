@echo off
:: 将控制台代码页更改为 UTF-8
chcp 65001 > nul
:: 运行程序
if "%~1"=="" (
    echo %1 是空的
	start "Quicker" %USERPROFILE%\miniconda3\envs\Quicker\python.exe %CD%\main.py
) else (
    echo %1 不是空的
	cd /d %1
	start "Quicker" %USERPROFILE%\miniconda3\envs\Quicker\python.exe %1\main.py
)
:: 等待用户按任意键继续
:: pause
exit