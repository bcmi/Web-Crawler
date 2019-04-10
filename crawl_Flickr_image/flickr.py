""" Flickr image search without using the Flcikr Image Search API. """

import requests
import time
import sys
import os
import re

patterns = {
    'image_url':  r'"url":"(?P<image_url>[^"]+)","key":"m"',
    'pathalias':  r'"pathAlias":"(?P<pathalias>[^"]+)"'}

re_patterns = {
    'pathalias': re.compile(patterns['pathalias'], re.VERBOSE),
    'image_url': re.compile(patterns['image_url'], re.VERBOSE)}

# Constants
BaseServerUrl = 'https://www.flickr.com'
BaseSaveDir = 'downloads'


class Flickr(object):
    """Search image in Flickr image search engines and extract the result"""

    def __init__(self):
        self.server = BaseServerUrl
        print 'Base server URL: ' + self.server

    def search(self, keyword, n):
        """ return at least n images of query keyword """

        # handle combined keywords
        keyword = '+'.join(keyword.split('-'))
        print 'Processing keyword(s): ', keyword

        start = 0
        img_num = 0
        for i in range(n):
            time.sleep(0.5)
            req = (self.server + '/search/?q=%s&ct=0&mt=photos&adv=1' % (keyword)
                               + '&page=%s' % str(i+1))

            print 'Trying ', req

            try:
                r = requests.get(req, verify=True)
            except:
                continue
               
            aliases = re_patterns['pathalias'].findall(r.content)
            image_urls = re_patterns['image_url'].findall(r.content)
            print len(aliases)

            try:
                assert(len(aliases)==len(image_urls))
                for k in range(len(aliases)):
                    alias = aliases[k]
                    raw_image_url = image_urls[k]
                    image_url = ''.join(raw_image_url.split('\\'))
                    image_url = image_url[2:]
                    image_name = image_url.split('/')[-1]
                    ext = image_name.split('.')[-1]
                    image_id = image_name.split('_')[0]

                    if not os.path.exists(os.path.join(BaseSaveDir, query)):
                        try:
                            os.makedirs(os.path.join(BaseSaveDir,query))
                        except Exception,e:
                            print e
                             
                    image_file_name = os.path.join(BaseSaveDir, query, alias+'_'+image_id+'.'+ext);
                    command = 'curl --silent %s -o %s' %(image_url, image_file_name)
                    print command
                    os.system(command)
                    url_file_name = os.path.join(BaseSaveDir, query, alias+'_'+image_id+'.html');
                    web_url = BaseServerUrl+'/photos/'+alias+'/'+image_id
                    command = 'curl --silent %s -o %s' %(web_url, url_file_name)
                    print command
                    os.system(command)
                    img_num += 1
                    if img_num>=n:
                        break
            except:
                continue

            if img_num>=n:
                break

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(0)

    query = sys.argv[1]
    num_image = int(sys.argv[2])

    s = Flickr()
    s.search(query, num_image)

