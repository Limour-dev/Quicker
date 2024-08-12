import pyperclip, keyboard, time

try:
    import mods.m03_windows as wnd
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, sys.path[0] + "/../")
    import mods.m03_windows as wnd

# https://github.com/mhammond/pywin32


hotkey = 'alt+1'
timeout = 2


def typesetting(_text: str):
    res = []
    for line in _text.split('\n'):
        line = line.strip()
        line = line.replace('\r', '')
        if not line:  # 跳过空行
            continue
        if not res:  # 第一行不处理
            res.append(line)
            continue
        lastC = res[-1][-1]
        if (lastC.isalpha() or lastC == ',') and line[0].isalpha():  # 断开的两行单词
            res.append(' ' + line)
            continue
        if lastC in {'.', '。', '!', '！', '?', '？'}:
            res.append('\n' + line)
            continue
        res.append(line)
    return ''.join(res)


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
