import os

hotkey = 'w+p'
timeout = 2

IMAGEMAGICK = os.getenv('IMAGEMAGICK', 'magick.exe')

hwnd = 0


def t_path(p_hwnd, p_title, p_path, hotkey_):
    if not p_path.endswith('explorer.exe'):
        return False
    global hwnd
    hwnd = p_hwnd
    return True


def callback(after):
    path = after.uiauto.GetSelectFilePath(hwnd)
    if not path:
        print('未选中任何文件')
        return
    print('选中文件', path)
    for p in path:
        os.system(f'{IMAGEMAGICK} convert -resize "1000x1000>" -gravity center -quality 50 -define WebP:lossless=false "{p}" "{p}.webp"')


if __name__ == '__main__':
    print(IMAGEMAGICK)
