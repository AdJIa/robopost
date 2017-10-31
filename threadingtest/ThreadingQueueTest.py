import threading
import time
import queue

exitFlag = 0

class myThread (threading.Thread):

  def __init__(self, threadID, name, q):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.q = q

  def run(self):
    print("线程开始：" + self.name)
    process_data(self.name, self.q)
    print("退出线程：" + self.name)


def process_data(name, q):
  while not exitFlag:
    queueLock.acquire()
    if not q.empty():
      data = q.get()
      queueLock.release()
      print("%s process %s " % (name, data))
    else:
      queueLock.release()
    time.sleep(1)
  pass

threadList = ["thread-1", "thread-2", "thread-3", "thread-4"]
nameList = ["one", "two", "three", "four", "five"]

queueLock = threading.Lock()
workQueue = queue.Queue(10)

threads = []

for index, item in enumerate(threadList):
  thread = myThread(index, item, workQueue)
  thread.start()
  threads.append(thread)

#填充队列
queueLock.acquire()
for word in nameList:
  workQueue.put(word)
queueLock.release()

#等待队列清空
while not workQueue.empty():
  pass

#通知结束循环
exitFlag = 1

#等待所有线程完成
for t in threads:
  t.join()
print("退出主线程")