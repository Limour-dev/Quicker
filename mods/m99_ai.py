import os
import json
import urllib.request
import urllib.error


def post_json(url: str, data: dict, headers: dict, decoding='utf-8'):
    json_data = json.dumps(data)
    bytes_data = json_data.encode('utf-8')
    headers.update({'Content-Type': 'application/json'})
    request = urllib.request.Request(url, data=bytes_data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(request) as response:
            response_content = response.read()
            return response_content.decode(decoding)
    except urllib.error.HTTPError as e:
        # 输出HTTP状态码和原因
        print(f"HTTP error occurred: {e.code} - {e.reason}")
        # 输出响应的错误内容（如果有的话）
        if e.fp:
            error_message = e.fp.read().decode('utf-8')
            print("Error message:", error_message)
            return error_message
    except urllib.error.URLError as e:
        # 输出与URL相关的错误
        print(f"URL error occurred: {e.reason}")
        return e.reason
    except Exception as e:
        # 输出其他所有错误
        raise e


def AI(system: str, user: str):
    response_content: str = post_json(url=QUICKER_AI_URL,
                                      data={
                                          'model': QUICKER_AI_MODEL,
                                          'messages': [
                                              {'role': 'system', 'content': system},
                                              {'role': 'user', 'content': user}
                                          ]
                                      },
                                      headers={'Authorization': QUICKER_AI_KEY})
    assistant = json.loads(response_content)
    print(assistant)
    return assistant['choices'][0]['message']['content']


# 获取配置
QUICKER_AI_URL = os.getenv('QUICKER_AI_URL', 'https://api.openai.com/v1/chat/completions')
QUICKER_AI_KEY = os.getenv('QUICKER_AI_KEY', 'sk-free')
QUICKER_AI_MODEL = os.getenv('QUICKER_AI_MODEL', 'gpt-4o-mini')

if __name__ == '__main__':
    print(QUICKER_AI_URL)
    print(QUICKER_AI_KEY)
    print(QUICKER_AI_MODEL)
    print(AI('response_language: zh-CN', 'hello!'))