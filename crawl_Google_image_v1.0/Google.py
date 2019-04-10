import os
import sys
import requests
import re
import HTMLParser
import urllib

patterns = {'item_details': r'<a\s*href="/url\?q=(?P<web_url>[^"]+)">\s*<img\s*height="\d+"\s*src="(?P<img_url>[^"]+)"'}
re_patterns = re.compile(patterns['item_details'],re.VERBOSE)
html_parser = HTMLParser.HTMLParser()

BaseSaveDir = 'downloads'

class Search(object):
    ''' Search images by using the Google image search engine and extract the results '''

    def __init__(self):
        ''' Constructor '''
        self.server = 'https://www.google.com'
        print 'Using sever: ' + self.server

    def get(self, keyword, n):
        keyword = '+'.join(keyword.split(' '))
        print keyword
        rset = list()

        img_num = 0
        start = 0
        for ipage in range(n):
            req = (self.server + '/search?q=%s&hl=en&tbs=itp:photo,ic:color&tbm=isch' % (keyword)
                               + '&start=%d' % start)
            r = requests.get(req)
            
            matches = re_patterns.findall(r.content)
            start += len(matches)
            print len(matches)
            if matches:
                for ii in range(len(matches)):
                    match = matches[ii]
                    web_url = html_parser.unescape(match[0])
                    img_url = html_parser.unescape(match[1])
                    web_url = urllib.unquote(web_url)
                    img_url = urllib.unquote(img_url)
                    html_file_name = os.path.join(BaseSaveDir,query,str(img_num)+'.html')
                    img_file_name = os.path.join(BaseSaveDir,query,str(img_num)+'.jpg')
                    
                    cut_idx = web_url.find('&sa')
                    web_url = web_url[0:cut_idx]    
                    command = 'curl -L "%s" -o %s' %(web_url, html_file_name)
                    os.system(command)
                    command = 'curl --silent %s -o %s' %(img_url, img_file_name)
                    os.system(command)

                    img_num+=1
                    if img_num>=n:
                        break
            if img_num>=n:
                break
                     

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage:"
        print '\t%s query #images' % ('Google.py', )
        sys.exit(0)

    s = Search()
    query = sys.argv[1]
    num_image = int(sys.argv[2])

    if not os.path.isdir(os.path.join(BaseSaveDir, query)):
        os.makedirs(os.path.join(BaseSaveDir, query))
    rset = s.get(query, num_image)

    

