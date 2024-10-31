import ctypes
import time
import locale

# 定义Windows API常量和结构体
HWND_TOPMOST = -1
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
WS_EX_LAYERED = 0x80000
LWA_ALPHA = 0x00000002

# 加载User32.dll和Gdi32.dll
user32 = ctypes.WinDLL('user32')
gdi32 = ctypes.WinDLL('gdi32')

# 获取屏幕尺寸
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# 设置窗口位置在屏幕底部中央
x = (screen_width - 300) // 2
y = screen_height - 100


def massage(_text: str, timeout: int = 1):
    # 创建一个透明的消息窗口
    hwnd = user32.CreateWindowExA(WS_EX_LAYERED, b"STATIC", _text.encode(locale.getpreferredencoding()), 0,
                                  x, y, 300, 50, 0, 0, 0, 0)

    # 设置窗口透明度
    user32.SetLayeredWindowAttributes(hwnd, 0, 200, LWA_ALPHA)

    user32.SetWindowPos(hwnd, HWND_TOPMOST, x, y, 300, 50, SWP_SHOWWINDOW | SWP_NOACTIVATE)

    # 显示窗口1秒
    user32.ShowWindow(hwnd, 1)
    time.sleep(timeout)

    # 销毁窗口
    user32.DestroyWindow(hwnd)


if __name__ == '__main__':
    massage('测试')
