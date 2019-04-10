import os;
import sys;
import requests;
import re;
import subprocess;

patterns = {'item_details':   r'<li><div class="yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix yt-uix-tile"'+\
			      r'\s*data-context-item-id="(?P<id>[^"]+)"'
	    };

            
cpatterns = {'item_details' : re.compile(patterns['item_details'])};

class Search(object):
    '''
    Search image in google image search engines and extract the result
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.server = 'https://www.youtube.com';
        print 'Using sever: ' + self.server;
    
    
    def get(self, keyword, n):    
        keyword = '+'.join(keyword.split(' '));
	print keyword;
        start = 0;
        rset = list();
        for i in range(10000):
            req = (self.server + '/results?search_query=%s&filters=short' % (keyword) \
                               + '&page=%s' % str(i+1));
            print req;
            r = requests.get(req);       
	    #fd = open('debug.txt', "w");
            #print>>fd, r.content;
            #fd.close();
            cur_rset = self.parse(r, n);
            rset += cur_rset;
            if len(rset) < n and len(cur_rset)>0:
                start += len(cur_rset);
            else:
                break;
        for i in range(len(rset)):
            rset[i]['rank']=i;
        return rset;
    
    def parse(self, r, n):
        matches = cpatterns['item_details'].findall(r.content);
	i = 0;
        rset = list();
        if matches:      
            for m in matches:
                #rset.append(Result( m[0], m[1], m[2], m[3], m[4]));
		rset.append(Result(m));
		i = i + 1;
		if i >= n:
		    break;
        return rset;

class Result(dict):
    '''
    Class stores the infomation of returned images
    '''
    def __init__(self,id=''):
        self['id'] = id;
	self['url'] = 'https://www.youtube.com/watch?v=' + id;
         
