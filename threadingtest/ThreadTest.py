import _thread
import time

def print_time(theadName, delay):
  count = 0
  while count < 5:
    time.sleep(delay)
    count += 1
    print("%s:%s"%(theadName, time.ctime(time.time())))

try:
  _thread.start_new_thread(print_time, ("thead-1", 2,))
  _thread.start_new_thread(print_time, ("thead-2", 4,))
except:
  print("Error:无法启动线程")
while 1:
  pass
