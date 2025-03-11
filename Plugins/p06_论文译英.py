import pyperclip, keyboard
from .p01_排版粘贴 import ctrlV, typesetting

hotkey = 'ctrl+shift+t'
timeout = 2
system_prompt = r'''response_language: en-US
+ Paraphrase the user's input in an objective and formal written tone, ensuring the original meaning remains unchanged.
+ Employ professional terminology while maintaining concise language.
+ Adopt a style that blends the approaches of scientists and popular science writers, making the content professional yet accessible.
+ Avoid analysis, descriptions, or lists; ensure the text forms a natural paragraph that seamlessly integrates into the original content.
'''


def callback(after):
    text = typesetting(pyperclip.paste())
    text = after.AI(system_prompt, text, 0)
    pyperclip.copy(text)
    after(0.1, ctrlV)


if __name__ == '__main__':
    from ..mods.m08_runAfter import runAfter

    after = runAfter(0.1)
    keyboard.add_hotkey(hotkey, callback, args=(after,), timeout=timeout)
    keyboard.wait()
