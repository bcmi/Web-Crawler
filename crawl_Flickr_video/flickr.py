
import requests
import os
import sys
import re
import time

patterns = {
    'image_url':  r'"url":"(?P<image_url>[^"]+)","key":"t"',
    'pathalias':  r'"pathAlias":"(?P<pathalias>[^"]+)"'}

re_patterns = {
    'pathalias': re.compile(patterns['pathalias'], re.VERBOSE),
    'image_url': re.compile(patterns['image_url'], re.VERBOSE)}


SERVER = 'https://www.flickr.com'
BaseSaveDir = 'downloads'


class Flickr(object):

    """Search image in Flickr image search engines and extract the result"""

    def __init__(self):
        self.server = SERVER
        print 'Using sever: ' + self.server

    def search(self, keyword, n):
        """ return at least n images of query keyword """

        # handle combined keywords
        keyword = '+'.join(keyword.split('-'))
        print 'Processing keyword(s): ', keyword

        web_url_list = list()
        img_num = 0
        rset = list()
        for i in range(n):
            time.sleep(0.5)
            req = (self.server +
                   '/search/?q=%s&ct=0&mt=videos&adv=1' %
                   (keyword) +
                   '&page=%s' %
                   str(i + 1))
            print 'Trying ', req

            try:
                r = requests.get(req)
            except:
                continue

            aliases = re_patterns['pathalias'].findall(r.content)
            image_urls = re_patterns['image_url'].findall(r.content)
            if len(aliases)==0:
                break
        

            try:
                assert(len(aliases)==len(image_urls))
                for k in range(len(aliases)):
                    alias = aliases[k]
                    raw_image_url = image_urls[k]
                    image_name = raw_image_url.split('/')[-1]
                    image_id = image_name.split('_')[0]
                    web_url = SERVER+'/photos/'+alias+'/'+image_id
                    html_file_name = os.path.join(BaseSaveDir, query, alias+'_'+image_id+'.html')
                    command = 'curl --silent "%s" -o "%s"' %(web_url, html_file_name)
                    print command
                    os.system(command)
                    web_url_list.append(web_url)
                    img_num += 1
                    if img_num>=n:
                        break

            except:
                continue

            if img_num>=n:
                break
        return web_url_list

SAVE_DIR = 'downloads'

if __name__ == "__main__":

    query = sys.argv[1]
    num_image = int(sys.argv[2])

    if not os.path.exists(os.path.join(BaseSaveDir,query)):
        os.makedirs(os.path.join(BaseSaveDir,query))

    s = Flickr()
    rset = s.search(query, num_image)

    fd = open(os.path.join(BaseSaveDir,query,'urls.txt'),'w')
    for r in rset:
        print>>fd, r
            

    fd.close()
