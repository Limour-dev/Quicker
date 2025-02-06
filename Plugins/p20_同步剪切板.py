import httpx, os, pyperclip
import time

_timeout = httpx.Timeout(120.0, connect=10.0)

hotkey = ('ctrl+alt+8', 'ctrl+alt+9')
timeout = 2
cb_c_hash = 0

FASTAPI_URL=os.getenv('FASTAPI_URL', 'https://fastapi.limour.top/clipboard')
FASTAPI_KEY={
    'Limour': os.getenv('FASTAPI_KEY', '123456')
}

async def getHash():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{FASTAPI_URL}/hash', headers=FASTAPI_KEY)
    return response.json()['hash']

async def copy():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{FASTAPI_URL}/copy', headers=FASTAPI_KEY)
    return response.json()['input']

async def paste(text):
    headers = {
        'Content-Type': 'application/json'
    }
    headers.update(FASTAPI_KEY)
    data = {
        'input': text
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{FASTAPI_URL}/paste', headers=headers, json=data)
    return response.json()['hash']

async def callback(after):
    if after.hotkey == hotkey[0]:
        await update_clipboard()
    else:
        global cb_c_hash, monitor_clipboard_hash
        c_h = await getHash()
        if cb_c_hash != c_h or monitor_clipboard_hash != hash(pyperclip.paste()):
            pyperclip.copy(await copy())
            cb_c_hash = c_h
            print(time.ctime(), f'同步剪贴板<-服务器：{cb_c_hash}')
            monitor_clipboard_hash = hash(pyperclip.paste())

monitor_clipboard_hash = 0
async def update_clipboard():
    global cb_c_hash, monitor_clipboard_hash
    text = pyperclip.paste()
    if hash(text) != monitor_clipboard_hash:
        cb_c_hash = await paste(text)
        monitor_clipboard_hash = hash(text)
        print(time.ctime(), f'同步剪贴板->服务器：{monitor_clipboard_hash}')

async def monitor_clipboard(after):
    try:
        await update_clipboard()
    finally:
        after(3, monitor_clipboard, after)

def init(after):
    pass
    # after(0, monitor_clipboard, after)
