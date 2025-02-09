import pyperclip, keyboard
import re

hotkey = 'alt+4'
t_path = 'zotero.exe'
timeout = 2
system_prompt = r'''response_language: zh-CN
+ 提取输入摘要的关键词，以每行一个的形式输出
+ 全面但与主题相关、简明、使用术语
'''

r_1 = re.compile(r'\s*\n[\n\r\s]*\n')
r_2 = re.compile(r'^- ', re.MULTILINE)


async def processing(_text: str, after):
    res = r_1.sub('\n', _text)
    res = res.strip()
    res = await after.AI(system_prompt, res, 2)
    res = r_2.sub('', res)
    return res


async def callback(after):
    res = await processing(pyperclip.paste(), after)
    pyperclip.copy(res)
    # after.msg('抽取完成！')
