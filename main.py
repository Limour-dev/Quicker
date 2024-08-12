import keyboard, time

import mods.m03_windows as wnd
from mods.m08_runAfter import runAfter

import importlib

hwnd = wnd.GetForegroundWindow()
after = runAfter(0.1)


def showAndHideWindow():
    while True:
        wnd.ShowWindow(hwnd, 0)
        yield 'showAndHideWindow: 隐藏窗口'
        wnd.ShowWindow(hwnd, 1)
        yield 'showAndHideWindow: 显示窗口'


showAndHideWindow = showAndHideWindow()


def hotkey_showAndHideWindow():
    print(time.ctime(), 'alt+l', next(showAndHideWindow))


def get_all_files_in_directory(directory, ext=''):
    import re, os
    custom_sort_key_re = re.compile('([0-9]+)')

    def custom_sort_key(s):
        # 将字符串中的数字部分转换为整数，然后进行排序
        return [int(x) if x.isdigit() else x for x in custom_sort_key_re.split(s)]

    all_files = []
    for root, dirs, files in os.walk(directory):
        root: str = root[len(directory):]
        root.replace(os.path.sep, '.')
        for file in files:
            if file.endswith(ext):
                file_path = root + '.' + file[:-len(ext)]
                all_files.append(file_path)
    return sorted(all_files, key=custom_sort_key)


def wait4release(_hotkey: str):
    _keys = _hotkey.split('+')
    while True:
        if not any(keyboard.is_pressed(key) for key in _keys):
            break
        time.sleep(0.01)
    # print(list((key, keyboard.is_pressed(key)) for key in _keys))


def hotkey_plugin_create(_path):
    plugin = importlib.import_module(_path, 'Plugins')

    def hotkey_callback():
        wait4release(plugin.hotkey)
        plugin.callback(after)

    def hotkey_plugin():
        print(time.ctime(), plugin.hotkey, _path)
        after(0, hotkey_callback)

    print(time.ctime(), 'plugin_create', plugin.hotkey, _path)
    return plugin.hotkey, plugin.timeout, hotkey_plugin


def main():
    keyboard.add_hotkey('alt+l', hotkey_showAndHideWindow)
    Plugins = get_all_files_in_directory('Plugins', '.py')
    for path in Plugins:
        hotkey, timeout, callback = hotkey_plugin_create(path)
        keyboard.add_hotkey(hotkey, callback, timeout=timeout)


if __name__ == '__main__':
    main()
    if wnd.GetWindowText(hwnd) == 'Quicker':
        hotkey_showAndHideWindow()  # 隐藏窗口
        keyboard.wait()
