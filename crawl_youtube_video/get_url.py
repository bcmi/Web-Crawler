import os;
import YouTube;
import time;

s = YouTube.Search();
tgt_dir = 'downloads';

def crawl_one(query, num_image):
    save_dir = os.path.join(tgt_dir,query);
    save_dir = save_dir.replace('" ', '').replace(' "', '').replace('"', '').replace(' ', '+').replace('OR', '_').replace('+','_');
    if os.path.exists(save_dir)==False:
	os.makedirs(save_dir);

    rset = s.get(query, num_image);
    fd = open(os.path.join(save_dir, 'urls.lst'), "w");
    print>>fd, '\n'.join(map(lambda r: '%s' % (r['url']), rset));
    fd.close();


if __name__=="__main__":
    
    event_file = os.path.join('queries.txt');
    fp = open(event_file, 'r');
    queries = list();
    for line in fp:
        clean_line = line.strip('\n').strip('\r');
        queries.append(clean_line);
    fp.close();
    #queries = file(event_file).read().split('\n');

    start_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime());
    print start_time;
    for q in queries:
        if q=='':
	    continue
	crawl_one(q,10);
    end_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime());
    print '[Start time] ', start_time;
    print '[End time] ', end_time;
