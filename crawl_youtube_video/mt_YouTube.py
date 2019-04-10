import fnmatch;
import os;
import sys;
import shutil;
import re;
import time;
import threading;
import tempfile

video_dir="downloads";
nThreads = 1;


def get_ITEMS(video_dir):
    
    event_file = os.path.join('queries.txt');
    fp = open(event_file, 'r');
    queries = list();
    for line in fp:
        clean_line = line.strip('\n').strip('\r');
        if clean_line=='':
            continue;
        queries.append(clean_line);
    fp.close();
    #event_name_list = file(event_file).read().split('\n')[0:-1];
    
    dirs = map( lambda x: x.replace('"','').replace(' ', '+').replace('+','_'), queries);
    h = {};
    for d in dirs:
        url_file = os.path.join(video_dir, d, 'urls.lst');
        for f in file(url_file).read().split('\n')[0:200]:
            if not f.strip():
                continue
            if h.has_key(f)==False:
                h[f] = os.path.join(video_dir, d);
    return h;


def download_one(url, save_dir): 
    check_format = ['.flv', '.mp4'];
    format_code = {'.flv':34, '.mp4':18};
    for fm in check_format:
        save_file_name = os.path.join(save_dir, url[len('https://www.youtube.com/watch?v='):len(url)] + fm);
    	if os.path.exists(save_file_name):
       	    #print save_file_name, ' [EXIST]';
            return;


    for fm in check_format:
        cmdline = './youtube-dl "%s" -w -f %d --write-description --write-info-json --output %s/' % (url, format_code[fm], save_dir) + '%\(id\)s' + fm;
        print cmdline;
        time_start_ = time.time();
        try:
            os.system(cmdline);
        except:
            pass;
        time_end_ = time.time();
        print '%g sec.' % (time_end_-time_start_,);

        save_file_name = os.path.join(save_dir, url[len('https://www.youtube.com/watch?v='):len(url)] + fm);
        if os.path.exists(save_file_name):
            print save_file_name, ' [EXIST]';
            return;
        print '[TRY next format]';




class myThread (threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID;
        threading.Thread.__init__(self);
    
    def run(self):
        threadLock.acquire();
        item="";
        if len(ITEMS)>0:
            item = ITEMS.popitem();
            #print "%d files remaining" % (len(ITEMS));
        threadLock.release();
        if len(item)>0:
            download_one(item[0], item[1]);

threadLock = threading.Lock();

ITEMS = get_ITEMS(video_dir); 

start_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime());
print start_time;

threads = [];
for i in range(nThreads):
    threads.append(myThread(i));

for t in threads:
    t.start();


while len(ITEMS)>0:
    for i in range(len(threads)):
        if not threads[i].isAlive():
            threads[i]=myThread(i);
            threads[i].start();
print "Exiting Main Tread";
end_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime());
print 'START TIME: %s' % start_time;
print 'END   TIME: %s' % end_time;
