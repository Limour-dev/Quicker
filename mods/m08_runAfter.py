import asyncio
import inspect
from threading import Thread


class runAfter:

    def event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        self.loop.close()

    def __init__(self, intervals=0.001):
        self.loop = asyncio.new_event_loop()
        self.ep = Thread(target=self.event_loop, daemon=True)
        self.ep.start()

    def __call__(self, intervals, callback, *args):
        task = self.try_call(callback, args)
        if intervals <= 0:
            self.run(task)
            return
        self.loop.call_later(intervals, self.run, task)

    def run(self, task):
        asyncio.run_coroutine_threadsafe(task, self.loop)

    async def try_call(self, callback, args):
        try:
            task = callback(*args)
            if inspect.iscoroutine(task):
                self.run(task)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import time
    after = runAfter()


    async def aprint(*args):
        print(*args)


    after(0, print, 'aa', 'bb')
    time.sleep(0.1)
    after(3, aprint, 3)
    after(2, print, 2)
    time.sleep(0.1)
    after(1, aprint, 1)
    after(0, print, 'cc', 'dd')
    after(0, aprint, 'ee', 'ff')
    time.sleep(5)
