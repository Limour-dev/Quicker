import keyboard
import pyperclip

hotkey = 'ctrl+alt+n'
timeout = 2
system_prompt = r'''response_language: en-US
+ Convert the input Chinese variable name to a Python style English variable name
+ Do not have any output other than the variable name
'''


async def processing(_text: str, after):
    res = _text.strip()
    res = after.AI(system_prompt, res, 2)
    res = res.strip()
    return res


def ctrlV():
    keyboard.send('ctrl+v')


async def callback(after):
    res = await processing(pyperclip.paste(), after)
    pyperclip.copy(res)
    ctrlV()

