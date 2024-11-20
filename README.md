# Quicker
```conda
conda run -n git git clone --depth=1 https://github.com/Limour-dev/Quicker.git
conda run -n git git pull
conda install conda-forge::mamba
mamba create -n Quicker conda-forge::pyperclip conda-forge::keyboard conda-forge::sortedcontainers conda-forge::uiautomation
# conda install conda-forge::pyperclip conda-forge::keyboard conda-forge::sortedcontainers conda-forge::uiautomation
```
+ `win+r` 将 `RunPy.bat` 的快捷方式放入 `shell:startup` 文件夹
+ 测试时手动运行 `RunAsAdmin.bat`
