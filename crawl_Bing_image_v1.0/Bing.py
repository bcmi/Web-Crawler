
import time
import os
import sys
import requests
import re
import HTMLParser
import urllib
import urllib2

BaseSaveDir = 'downloads'
patterns = {
    'item': r't3="(?P<web_url>[^"]+)"\s*h="ID=images,\d+.\d+">\s*<img\s*class="img_hid"\s*src2="(?P<img_url>[^"]+)"'
    }
re_patterns = re.compile(patterns['item'], re.VERBOSE)
html_parser = HTMLParser.HTMLParser()


class Search(object):
    ''' Search image in Bing image search engines and extract the result '''
    def __init__(self):
        '''
        Constructor
        '''
        self.server = 'http://www.bing.com'
        print 'Using sever: ' + self.server

    def get(self, keyword, n):
        keyword = '+'.join(keyword.split())
        keyword = keyword.replace('"', '')
        start = 0
        img_num = 0
        rset = list()
        for ipage in range(n):
            req =(self.server + '/images/search?q=%s&qft=+filterui:color2-color+filterui:photo-photo' % (keyword)
                + '&offset=%d&count=30' % start);
            r = requests.get(req)
            fp = open('content.txt','w')
            fp.write(r.content)
            fp.close()
            matches = re_patterns.findall(r.content)
            start += len(matches)
            for ii in range(len(matches)):
                match = matches[ii]
                web_url = html_parser.unescape(match[0])
                img_url = html_parser.unescape(match[1])
                web_url = urllib.unquote(web_url)
                img_url = urllib.unquote(img_url)

                html_file_name = os.path.join(BaseSaveDir,query,str(img_num)+'.html')
                img_file_name = os.path.join(BaseSaveDir,query,str(img_num)+'.jpg')

                command = 'curl -L "%s" -o %s' %(web_url, html_file_name)
                print command
                os.system(command)
                        
                command = 'curl --silent "%s" -o %s' %(img_url, img_file_name)
                print command
                os.system(command)

                img_num += 1
                if img_num>=n:
                    break

            if img_num>=n:
                break            


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage:"
        print '\t%s query #images' % ('Bing.py',)
        sys.exit(0)

    s = Search()
    query = sys.argv[1]
    num_image = int(sys.argv[2])

    image_save_dir = os.path.join(BaseSaveDir, query)
    if not os.path.exists(image_save_dir):
        os.makedirs(image_save_dir)

    s.get(query, num_image)

