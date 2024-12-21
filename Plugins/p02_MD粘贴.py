import pyperclip, keyboard
import re

hotkey = ('alt+2', 'ctrl+alt+2')
timeout = 2


def t_path(p_hwnd, p_title, p_path, hotkey_):
    if p_path.endswith('zotero.exe'):
        return hotkey_ == hotkey[1]
    else:
        return hotkey_ == hotkey[0]


r_1 = re.compile(r'\s*\n[\n\r\s]*\n')
r_2 = re.compile(r'^(- )|(\d+?. )', re.MULTILINE)


def typesetting(_text: str):
    res = _text.replace('**', '')
    res = r_1.sub('\n', res)
    res = r_2.sub('', res)
    return res.strip()


def ctrlV():
    keyboard.send('ctrl+v')


def callback(after):
    pyperclip.copy(typesetting(pyperclip.paste()))
    after(0.1, ctrlV)


if __name__ == '__main__':
    from mods.m08_runAfter import runAfter

    after = runAfter(0.1)
    keyboard.add_hotkey(hotkey, callback, args=(after,), timeout=timeout)
    keyboard.wait()
