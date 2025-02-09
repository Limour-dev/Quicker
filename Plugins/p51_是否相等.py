import pyperclip
import keyboard
import asyncio

hotkey = 'ctrl+alt+e'
timeout = 2

async def callback(after):
    old_clip = pyperclip.paste()
    keyboard.send('ctrl+c')
    await asyncio.sleep(0.2)
    new_clip = pyperclip.paste()
    if old_clip.strip() == new_clip.strip():
        print(f'\n\n===通过检查===\n{old_clip} == {new_clip}\n===通过检查===\n')
        # after.msg('通过检查！')
    else:
        print(f'\n\n===未通过检查===\n{old_clip} != {new_clip}\n===未通过检查===\n')
        pyperclip.copy(old_clip)
        # after.msg('未通过检查！')