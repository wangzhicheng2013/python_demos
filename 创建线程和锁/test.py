import stomp
import time
import logging
import threading
import Queue
import thread

def test(i):
    global unfinished_thread
    print 'starting thread%d' %i
    time.sleep(i)
    lock.acquire()
    unfinished_thread -= 1
    print 'end thread%d' %i
    lock.release()

if __name__ == '__main__':
    unfinished_thread = 0
    lock = threading.Lock()
    start_time = time.time()
    for i in range(1, 4, 1):
        try:
            unfinished_thread += 1
            thread.start_new_thread(test, (i,))
        except:
            print "Error: unable to start thread:%d" %i
    while True:
        lock.acquire()
        if unfinished_thread != 0:
            lock.release()
            time.sleep(1)
            print 'there are remaining threads:%d' %unfinished_thread
        else:
            lock.release()
            break
    print 'elapase %d' %(time.time() - start_time)
