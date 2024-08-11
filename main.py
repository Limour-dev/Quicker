import keyboard, time


def showAndHideWindow():
    from mods.m03_windows import GetForegroundWindow, ShowWindow
    hwnd = GetForegroundWindow()
    while True:
        ShowWindow(hwnd, 0)
        yield 'showAndHideWindow: 隐藏窗口'
        ShowWindow(hwnd, 1)
        yield 'showAndHideWindow: 显示窗口'


showAndHideWindow = showAndHideWindow()


def hotkey_showAndHideWindow():
    print(time.ctime(), next(showAndHideWindow))


if __name__ == '__main__':
    keyboard.add_hotkey('alt+l', hotkey_showAndHideWindow)
    keyboard.wait()
