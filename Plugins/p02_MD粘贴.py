import pyperclip, keyboard, time
import re

try:
    import mods.m03_windows as wnd
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, sys.path[0] + "/../")
    import mods.m03_windows as wnd

# https://github.com/mhammond/pywin32


hotkey = 'alt+2'
timeout = 2

r_1 = re.compile(r'\s*\n[\n\r\s]*\n')


def typesetting(_text: str):
    res = _text.replace('**', '')
    res = r_1.sub('\n', res)
    return res


def ctrlV():
    keyboard.send('ctrl+v')


def callback(after):
    hwnd = wnd.GetForegroundWindow()
    print(hwnd, wnd.GetWindowText(hwnd))
    # 尝试了一万种方法，发送Ctrl+C失败。。。
    # 只能改成发送Ctrl+V了。。。
    pyperclip.copy(typesetting(pyperclip.paste()))
    after(0.1, ctrlV)


if __name__ == '__main__':
    from mods.m08_runAfter import runAfter

    after = runAfter(0.1)
    keyboard.add_hotkey(hotkey, callback, args=(after,), timeout=timeout)
    keyboard.wait()
