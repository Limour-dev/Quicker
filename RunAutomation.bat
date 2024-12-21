@echo off
:: 将控制台代码页更改为 UTF-8
chcp 65001 > nul
:: 运行程序
start "Quicker" %USERPROFILE%\miniconda3\envs\Quicker\python.exe %USERPROFILE%\miniconda3\envs\Quicker\\Scripts\automation.py
:: 等待用户按任意键继续
pause
exit