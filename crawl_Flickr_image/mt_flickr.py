'''
Created on July 25, 2012
Flickr Image Search without using the Flickr Image Search API. Instead,
the requests module is used.

@author: sky
'''

import os
import logging
import time
import threading
logging.basicConfig(filename=__file__+'.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ITEMS = file('queries.txt').read().split('\n')
print ITEMS

def crawl_one(q):
    time.sleep(1)
    n = 10
    cmd = 'python flickr.py %s %d' % (q,n)
    os.system(cmd)


class myThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)

    def run(self):
        threadLock.acquire()
        item = ''
        if len(ITEMS) > 0:
            item = ITEMS.pop()
            item = item.strip('\r')
            print "%d items remaining" % (len(ITEMS))
        threadLock.release()
        if item and not item.startswith('#'):
            crawl_one(item)


threadLock = threading.Lock()
threads = []
nThreads = 1
for i in range(nThreads):
    threads.append(myThread(i))
for t in threads:
    t.start()

while len(ITEMS) > 0:
    for i in range(len(threads)):
        if not threads[i].isAlive():
            threads[i] = myThread(i)
            threads[i].start()
print "Exiting Main Tread"
