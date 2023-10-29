from multiprocessing import Process, Queue
import time


class TestProcess:
    def __init__(self, q:Queue) -> None:
        self.q  = q

    def start(self):
        while True:
            i = self.q.get(True, 10)
            if i==0:
                print("leave")
                self.q.put_nowait(i)
                break


def test_process():
    q = Queue()
    def put_int():
        for i in [10,3,0]:
            q.put(i)
            time.sleep(5)
    p_ = Process(target=put_int, args=[])
    t = TestProcess(q)
    p = Process(target=t.start, args=[])
    p_.start()
    p.start()
    p_.join()
    p.join()

if __name__ == '__main__':
    test_process()
