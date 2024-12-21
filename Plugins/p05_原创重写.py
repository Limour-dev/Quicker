import pyperclip, keyboard
from .p01_排版粘贴 import ctrlV, typesetting

hotkey = 'ctrl+shift+r'
timeout = 2
system_prompt = r'''response_language: zh-CN
+ 以客观书面语转述用户输入，保持用户原意不变
+ 使用专业词汇，保持语言精练
+ 结合人类科学家和科普作家的风格，专业并且易于阅读
+ 不分析，不描述，不列表，保持文字为一个自然段、能无缝融入原文
'''


def callback(after):
    text = typesetting(pyperclip.paste())
    text = after.AI(system_prompt, text, 0)
    text: str = text.replace(',', '，')
    text: str = text.replace('(', '（')
    text: str = text.replace(')', '）')
    pyperclip.copy(text)
    after(0.1, ctrlV)


if __name__ == '__main__':
    from ..mods.m08_runAfter import runAfter

    after = runAfter(0.1)
    keyboard.add_hotkey(hotkey, callback, args=(after,), timeout=timeout)
    keyboard.wait()
