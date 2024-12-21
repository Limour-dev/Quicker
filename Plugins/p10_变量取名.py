import pyperclip
from .p01_排版粘贴 import ctrlV

hotkey = 'ctrl+alt+n'
timeout = 2
system_prompt = r'''response_language: en-US
+ Convert the input Chinese variable name to a Python style English variable name
+ Do not have any output other than the variable name
'''


async def processing(_text: str, after):
    res = _text.strip()
    res = await after.AI(system_prompt, res, 2)
    print(res)
    res = res.strip()
    return res


async def callback(after):
    res = await processing(pyperclip.paste(), after)
    pyperclip.copy(res)
    ctrlV()
