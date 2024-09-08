from threading import Thread, Lock
from queue import Queue
import time
from sortedcontainers import SortedList


def clock_loop(q: Queue):
    while True:
        try:
            task = q.get()
            task[1](*task[2])
        except Exception as e:
            print(e)


class runAfter:
    q: Queue
    p: list
    l: Lock
    t: SortedList
    m: Thread

    def __init__(self, intervals=0.001, t_num=1):
        self.q = Queue()
        self.p = [Thread(target=clock_loop, args=(self.q,), daemon=True) for _ in range(t_num)]
        for td in self.p:
            td.start()
        self.l = Lock()
        self.t = SortedList(key=lambda x: x[0])
        self.m = Thread(target=manager_loop, args=(self, intervals), daemon=True)
        self.m.start()

    def __call__(self, intervals, callback, *args):
        task = (time.time() + intervals, callback, args)
        with self.l:
            self.t.add(task)


def manager_loop(self: runAfter, intervals):
    while True:
        if self.t:
            with self.l:
                idx = self.t.bisect_right((time.time(),))
                if idx > 0:
                    # print(self.t)
                    for task in self.t[:idx]:
                        self.q.put(task)
                    del self.t[:idx]
                    # print(self.t)
        time.sleep(intervals)


if __name__ == '__main__':
    after = runAfter()
    after(0, print, 'aa', 'bb')
    time.sleep(0.1)
    after(3, print, 3)
    after(2, print, 2)
    time.sleep(0.1)
    after(1, print, 1)
    after(0, print, 'cc', 'dd')
    after(0, print, 'ee', 'ff')
    time.sleep(5)
