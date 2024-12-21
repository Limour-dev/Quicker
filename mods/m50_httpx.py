import asyncio
import inspect
from typing import Callable, Any
import json, httpx
from functools import wraps


def check_async():
    # 检查当前函数是否在协程中调用
    try:
        # 获取当前事件循环
        loop = asyncio.get_running_loop()
        if not loop:
            return False
        # 如果能获取到事件循环且当前帧在协程中，返回 True
        caller_frame = inspect.currentframe().f_back.f_back
        caller_code = caller_frame.f_code
        caller_name = caller_code.co_name
        caller = caller_frame.f_globals.get(caller_name)
        if inspect.iscoroutinefunction(caller):
            return True
    except RuntimeError:
        # 如果不在协程中运行，获取事件循环会抛出RuntimeError
        pass
    # 不在协程中，返回 False
    return False


def auto_async(func: Callable) -> Callable:
    """装饰器：使函数在同步和异步环境中都能正常工作"""

    @wraps(func)
    def wrapper(*args, sync=None, **kwargs) -> Any:
        if sync is None:
            sync = not check_async()
        return func(*args, sync=sync, **kwargs)

    return wrapper


# def _post_sync(url: str, data: bytes, headers: dict, warp: Callable = None):
#     request = urllib.request.Request(url, data=data, headers=headers, method='POST')
#     with urllib.request.urlopen(request) as response:
#         response_content = response.read()
#     return warp(response_content) if warp else response_content

def _post_sync(url: str, data: bytes, headers: dict, warp: Callable = None):
    with httpx.Client() as client:
        response = client.post(url, content=data, headers=headers)
    return warp(response.content) if warp else response.content


async def _post_async(url: str, data: bytes, headers: dict, warp: Callable = None):
    # 建立连接
    async with httpx.AsyncClient() as client:
        response = await client.post(url, content=data, headers=headers)
    return warp(response.content) if warp else response.content


def post(url: str, data: bytes, headers: dict, warp: Callable = None, sync=True):
    if not sync:
        print('_post_async', url)
        return _post_async(url, data, headers, warp)
    else:
        print('_post_sync', url)
        return _post_sync(url, data, headers, warp)


def post_json(url: str, data: dict, headers: dict, warp: Callable = None, sync=True):
    json_data = json.dumps(data)
    bytes_data = json_data.encode('utf-8')
    headers.update({'Content-Type': 'application/json'})

    def _warp(response_content):
        res = json.loads(response_content.decode('utf-8'))
        return warp(res) if warp else res

    return post(url, bytes_data, headers, _warp, sync)
