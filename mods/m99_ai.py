import os
from typing import Literal

try:
    from m50_httpx import post_json, auto_async
except ModuleNotFoundError:
    from .m50_httpx import post_json, auto_async


@auto_async
def AI(system: str, user: str, model_level: Literal[0, 1, 2] = 2, sync=True):
    def warp(assistant):
        print(assistant)
        return assistant['choices'][0]['message']['content']

    return post_json(url=QUICKER_AI_URL,
                     data={
                         'model': QUICKER_AI_MODEL[model_level],
                         'messages': [
                             {'role': 'system', 'content': system},
                             {'role': 'user', 'content': user}
                         ]
                     },
                     headers={'Authorization': QUICKER_AI_KEY}, warp=warp, sync=sync)


# 获取配置
QUICKER_AI_URL = os.getenv('QUICKER_AI_URL', 'https://api.openai.com/v1/chat/completions')
QUICKER_AI_KEY = os.getenv('QUICKER_AI_KEY', 'sk-free')
QUICKER_AI_MODEL = os.getenv('QUICKER_AI_MODEL', 'gpt-4o-mini')
QUICKER_AI_MODEL = QUICKER_AI_MODEL.split('|')
if len(QUICKER_AI_MODEL) == 1:
    QUICKER_AI_MODEL = QUICKER_AI_MODEL * 3
print(f'AI 0: {QUICKER_AI_MODEL[0]}', f'AI 1: {QUICKER_AI_MODEL[1]}', f'AI 2: {QUICKER_AI_MODEL[2]}')

if __name__ == '__main__':
    print(QUICKER_AI_URL)
    print(QUICKER_AI_KEY)
    print(AI('response_language: zh-CN', 'hello!', 1))
