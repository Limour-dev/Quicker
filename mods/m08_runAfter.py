import asyncio
import inspect
import time
from threading import Thread, Lock

from sortedcontainers import SortedList


class runAfter:

    def event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        self.loop.close()

    def __init__(self, intervals=0.001):
        self.q = asyncio.Queue()
        self.loop = asyncio.new_event_loop()
        self.ep = Thread(target=self.event_loop, daemon=True)
        self.ep.start()
        self.run(self.clock_loop())
        self.L = Lock()
        self.t = SortedList(key=lambda x: x[0])
        self.run(self.manager_loop(intervals))

    def __call__(self, intervals, callback, *args):
        if intervals <= 0:
            task = self.q.put((intervals, callback, args))
            self.run(task)
            return
        task = (time.time() + intervals, callback, args)
        with self.L:  # 锁里不要 await
            self.t.add(task)

    def run(self, task):
        asyncio.run_coroutine_threadsafe(task, self.loop)

    async def manager_loop(self, intervals):
        while True:
            if self.t:
                with self.L:  # 锁里不要 await
                    idx = self.t.bisect_right((time.time(),))
                    if idx > 0:
                        # print(self.t)
                        for task in self.t[:idx]:
                            self.run(self.q.put(task))
                        del self.t[:idx]
                        # print(self.t)
            await asyncio.sleep(intervals)

    async def clock_loop(self):
        while True:
            try:
                task = await self.q.get()
                task = task[1](*task[2])
                if inspect.iscoroutine(task):
                    self.run(task)
            except Exception as e:
                print(e)


if __name__ == '__main__':
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
