def dotenv():
    import os
    with open('.env', 'r', encoding='utf-8') as env:
        for line in env:
            tmp = line.strip().split('=', maxsplit=1)
            if len(tmp) <= 1:
                continue
            k, v = tmp[0].strip(), tmp[1].strip()
            if (not k) or (not v):
                continue
            os.environ[k] = v

dotenv()

import keyboard, time, asyncio

import mods.m03_windows as wnd
from mods.m08_runAfter import runAfter
from mods.m99_ai import AI
from mods.m10_message import callback as message
import mods.m11_uiauto as uiauto

import importlib

hwnd = wnd.GetForegroundWindow()
after = runAfter(0.1)
after.AI = AI
after.uiauto = uiauto
after.msg = message(after, wnd)


def showAndHideWindow():
    while True:
        wnd.ShowWindow(hwnd, 0)
        yield 'showAndHideWindow: 隐藏窗口'
        wnd.ShowWindow(hwnd, 1)
        yield 'showAndHideWindow: 显示窗口'


showAndHideWindow = showAndHideWindow()


def hotkey_showAndHideWindow():
    PrintForegroundWindow()
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


async def wait4release(_hotkey: str):
    _keys = _hotkey.split('+')
    while True:
        if not any(keyboard.is_pressed(key) for key in _keys):
            break
        await asyncio.sleep(0.01)
        # print(list((key, keyboard.is_pressed(key)) for key in _keys))


def PrintForegroundWindow(t_path=None, hotkey=''):
    p_hwnd = wnd.GetForegroundWindow()
    p_title = wnd.GetWindowText(p_hwnd)
    p_path = uiauto.GetProcessFileName(p_hwnd)
    print('当前活动窗口', p_hwnd, p_title, p_path, hotkey)
    return t_path(p_hwnd, p_title, p_path, hotkey) if t_path else True


def hotkey_plugin_create(_path):
    plugin = importlib.import_module(_path, 'Plugins')

    try:
        tt_path = plugin.t_path
    except AttributeError:
        tt_path = ''
    if type(tt_path) is str:
        def t_path(p_hwnd, p_title, p_path, hotkey):
            return p_path.endswith(tt_path)
    else:
        t_path = tt_path

    async def hotkey_callback(hotkey):
        if not PrintForegroundWindow(t_path, hotkey):
            print(_path, '目标程序不符合，忽略快捷键')
            return
        await wait4release(hotkey)
        after(0, plugin.callback, after)

    def hotkey_plugin(hotkey):
        print(time.ctime(), hotkey, _path)
        after(0, hotkey_callback, hotkey)

    print(time.ctime(), 'plugin_create', plugin.hotkey, tt_path, _path)
    if type(plugin.hotkey) is str:
        hotkeys = [plugin.hotkey]
    else:
        hotkeys = plugin.hotkey
    return hotkeys, plugin.timeout, hotkey_plugin


# HACK: keyboard caught windows+l pressed event when user is locking screen,
# but missing the released event. by https://gitee.com/pmh905001/shouyu
def clear_pressed_events(hotkey):
    print(time.ctime(), hotkey, 'clear_pressed_events')
    with keyboard._pressed_events_lock:
        print(time.ctime(), 'clear_pressed_events', keyboard._pressed_events)
        keyboard._pressed_events.clear()
        print(time.ctime(), 'clear_pressed_events', keyboard._pressed_events)


def _is_key_overtime(pressed_events):
    for event in pressed_events.values():
        if time.time() - event.time > 2:
            return True


def health_check():
    # print(time.ctime(), 'health_check')
    with keyboard._pressed_events_lock:
        if _is_key_overtime(keyboard._pressed_events):
            print(time.ctime(), 'health_check', keyboard._pressed_events)
            keyboard._pressed_events.clear()
        after(2, health_check)


def main():
    keyboard.add_hotkey('windows+l', clear_pressed_events, args=('windows+l',))
    keyboard.add_hotkey(-133, clear_pressed_events, args=('微信按下了F22',))  # 万恶的微信
    after(2, health_check)
    keyboard.add_hotkey('alt+l', hotkey_showAndHideWindow)
    Plugins = get_all_files_in_directory('Plugins', '.py')
    for path in Plugins:
        hotkeys, timeout, callback = hotkey_plugin_create(path)
        for hotkey in hotkeys:
            keyboard.add_hotkey(hotkey, callback, args=(hotkey,), timeout=timeout)


if __name__ == '__main__':
    main()
    if wnd.GetWindowText(hwnd) == 'Quicker':
        hotkey_showAndHideWindow()  # 隐藏窗口
        keyboard.wait()
