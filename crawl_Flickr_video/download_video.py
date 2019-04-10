
import requests
import os
import sys
import re
import time

BaseSaveDir = 'downloads'

if __name__ == "__main__":

    query = sys.argv[1]
    urls = file(os.path.join(BaseSaveDir,query,'converted_urls.txt')).read().split('\n')
    for url in urls:
        url = url.strip('\r')
        if not url:
            continue
        cut_idx = url.find('photos/')
        part_url = url[cut_idx+7:]
        #print part_url
        alias = part_url.split('/')[0]
        video_id = part_url.split('/')[1]       
        video_file_name = os.path.join(BaseSaveDir,query,alias+'_'+video_id+'.mp4')
        command = 'curl -L "%s" -o "%s"' %(url,video_file_name)
        print command
        os.system(command)
        
