from threading import Thread
from queue import Queue
import time


def clock_loop(q: Queue, intervals):
    while True:
        try:
            task = q.get()
            if time.time() >= task[0]:
                task[1](*task[2])
            else:
                q.put(task)
        except Exception as e:
            print(e)
        time.sleep(intervals)


class runAfter:
    q: Queue
    t: Thread

    def __init__(self, intervals=0.001):
        self.q = Queue()
        self.t = Thread(target=clock_loop, args=(self.q, intervals), daemon=True)
        self.t.start()

    def __call__(self, intervals, callback, *args):
        task = (time.time()+intervals, callback, args)
        self.q.put(task)


if __name__ == '__main__':
    after = runAfter()
    after(0, print, 'aa', 'bb')
    after(3, print, 3)
    after(2, print, 2)
    after(1, print, 1)
    after(0, print, 'cc', 'dd')
    time.sleep(5)