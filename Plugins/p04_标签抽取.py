import pyperclip, keyboard, time
import re

try:
    import mods.m03_windows as wnd
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, sys.path[0] + "/../")
    import mods.m03_windows as wnd

# https://github.com/mhammond/pywin32


hotkey = 'alt+4'
timeout = 2
system_prompt = r'''response_language: zh-CN
+ 提取输入摘要的关键词，以每行一个的形式输出
+ 全面但与主题相关、简明、使用术语
'''

r_1 = re.compile(r'\s*\n[\n\r\s]*\n')
r_2 = re.compile(r'^- ', re.MULTILINE)


def processing(_text: str, after):
    res = r_1.sub('\n', _text)
    res = res.strip()
    res = after.AI(system_prompt, res, 2)
    res = r_2.sub('', res)
    return res


def ctrlV():
    keyboard.send('ctrl+v')


def callback(after):
    hwnd = wnd.GetForegroundWindow()
    print(hwnd, wnd.GetWindowText(hwnd))
    # 尝试了一万种方法，发送Ctrl+C失败。。。
    # 只能改成发送Ctrl+V了。。。
    pyperclip.copy(processing(pyperclip.paste(), after))
    after.msg('抽取完成！')


if __name__ == '__main__':
    from mods.m08_runAfter import runAfter

    after = runAfter(0.1)
    keyboard.add_hotkey(hotkey, callback, args=(after,), timeout=timeout)
    keyboard.wait()
