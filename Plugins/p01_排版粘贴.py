import pyperclip, keyboard, re

# https://github.com/mhammond/pywin32

hotkey = 'ctrl+alt+v'
timeout = 2


def isalpha(s: str):
    return 'a' <= s <= 'z' or 'A' <= s <= 'Z'


# 引用文献
reg_1 = re.compile(r'\[\d+?[-–,]?\d*?](?=[.。\?？,，])')


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
        if lastC == '-' and isalpha(line[0]):  # 连字符
            if len(res[-1]) >= 2 and isalpha(res[-1][-2]):
                res[-1] = res[-1][:-1]
                res.append(line)
                continue
        if (isalpha(lastC) or lastC == ',') and isalpha(line[0]):  # 断开的两行单词
            res.append(' ' + line)
            continue
        if lastC in {'.', '。', '!', '！', '?', '？'}:
            res.append('\n' + line)
            continue
        res.append(line)
    return reg_1.sub('', ''.join(res))


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
