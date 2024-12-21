import pyperclip, keyboard
import re

hotkey = ('alt+3', 'ctrl+alt+3')
timeout = 2


def t_path(p_hwnd, p_title, p_path, hotkey_):
    if p_path.endswith('zotero.exe'):
        return hotkey_ == hotkey[1]
    else:
        return hotkey_ == hotkey[0]


system_prompt = r'''response_language: zh-CN
+ 将输入的摘要以中文列表的形式输出
+ 简明概要，重点突出
'''

r_1 = re.compile(r'\s*\n[\n\r\s]*\n')


def processing(_text: str, after):
    res = r_1.sub('\n', _text)
    res = res.strip()
    return after.AI(system_prompt, res, 1)


def ctrlV():
    keyboard.send('ctrl+v')


def callback(after):
    pyperclip.copy(processing(pyperclip.paste(), after))
    after(0.1, ctrlV)


if __name__ == '__main__':
    from mods.m08_runAfter import runAfter

    after = runAfter(0.1)
    keyboard.add_hotkey(hotkey, callback, args=(after,), timeout=timeout)
    keyboard.wait()
