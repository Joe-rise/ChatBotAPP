#-*- coding:utf-8 _*-  
""" 
@author:bluesli 
@file: threaded_generator.py 
@time: 2018/10/27 
"""
from threading import Thread
from queue import Queue

class ThreadGenerator(object):

    def __init__(self,iterator,#迭代器
                 sentinel=object(), #哨兵,进行监视
                 queue_maxsize=0,
                 deamon=False,# 后台模式
                 ):
        self._iterator = iterator
        self._sentinel = sentinel
        self._queue = Queue(maxsize=queue_maxsize)
        self._thread = Thread(
            name=repr(iterator),#一特定的格式进行复制操作；
            target = self._run
        )
        self._thread.deamon=deamon
        self._started =False
    # def __repr__(self):
    #     return "threadedGenerator({!r})".format(self._iterator)
    #
    def _run(self):
        try:
            # 便利迭代器，判断是否启动线程生成器没有就直接返回；有就将迭代器的值加入队列；
            # 最后再将哨兵加入队列中
            for value in self._iterator:
                if not self._started:
                    return
                self._queue.put(value)
        finally:
            # 最后将哨兵加入队列，队列的末尾为哨兵，也就是说如果队列中的值为哨兵了，那么队列中就没有值了；就停止迭代
            self._queue.put(self._sentinel)
    #
    # def _close(self):
    #     self.started = False
    #     try:
    #         while True:
    #             self._queue.get(timeout=30)
    #     except KeyboardInterrupt as e:
    #         raise e
    #     except:
    #         pass
    #
    # def __iter__(self):
    #     self._started = True
    #     self._thread.start()
    #     for value in iter(self._queue.get,self._sentinel):
    #         yield value # 能够记录位置；从上一次开始，运行yeild后面的代码
    #     self._thread.join()
    #     self._started =False

    def __next__(self):
        if not self._started:
            self._started=True
            self._thread.start()
        # 获取队列中的值
        value = self._queue.get(timeout=30)
        # 判断一下value值是否和哨兵的值相同，如果相同，则停止迭代
        if value == self._sentinel:
            raise StopIteration
        return value
    # 内存溢出，线程卡死；

# 定义测试类
def test():
    def gene():
        i = 0
        while True:
            yield i
            i +=1
    t = gene()
    test = ThreadGenerator(t)
    for i in range(20):
        print(next(test))






if __name__ == '__main__':
    test()
    #     # 内存溢出，线程卡死；
    # 多线程的方式取处理数据；效率高，防止系统卡顿；所有的数据在新的线程中做，可以防止主线程的卡顿现象；

