import re
import os
import sys
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BaseSaveDir = 'downloads'

browser = webdriver.Chrome('./chromedriver_bing')

img_pattern1 = re.compile(r'imgurl:&amp;quot;(?P<img_url>[^"]+)&amp;quot;,ow:', re.VERBOSE)
img_pattern2 = re.compile(r'imgurl:&quot;(?P<img_url>[^"]+)&quot;,ow:', re.VERBOSE)
web_pattern = re.compile(r'href="(?P<web_url>[^"]+)"\s*ihk=', re.VERBOSE)
txt_pattern = re.compile(r'<span\s*class="cap_items">\s*<span>\s*(?P<txt_url>[^$]+)\s*</span>\s*<a\s*href="#"\s*class="cap_exp"', re.VERBOSE)

image_downloader = urllib.URLopener()

queries = file('queries.txt').read().split('\n')
img_num = 500

for query in queries:
    if not query:
        continue
    
    start = 0
    icount = 0
    for ipage in range(img_num):
        url = 'https://www.bing.com/images/search?q='+query+'&qft=+filterui:color2-color+filterui:photo-photo&offset='+str(start)+'&count=30'
        print url
        browser.get(url)
        WebDriverWait(browser, 6000).until(EC.presence_of_element_located((By.XPATH,"//div[@id='mm_header']")))     

        html_source = browser.page_source
        web_matches = web_pattern.findall(html_source)
        img_matches = img_pattern1.findall(html_source)
        if len(img_matches)==0:
            img_matches = img_pattern2.findall(html_source)

        print len(img_matches)
        print len(web_matches)
        start += len(img_matches)

        try:
            assert(len(img_matches)==len(web_matches))
            
            for ii in range(len(img_matches)):
                try:
                    if not os.path.exists(os.path.join(BaseSaveDir, query)):
                        os.makedirs(os.path.join(BaseSaveDir, query))
                    img_url = img_matches[ii]
                    ext = img_url.split('.')[-1]
                    if len(ext)>4:
                        save_img_file = os.path.join(BaseSaveDir, query, str(icount)+'.jpg')
                    else:  
                        save_img_file = os.path.join(BaseSaveDir, query, str(icount)+'.'+ext)

                    print 'page'+str(ipage)+'_'+str(ii)
                    print save_img_file
                    
                    web_match = web_matches[ii]
                    web_url = 'https://www.bing.com'+web_match.replace('&amp;amp;','&').replace('&amp;','&')

                    r = requests.get(web_url)        
                    txt_matches = txt_pattern.findall(r.content)
                    desc = txt_matches[0]
                    save_txt_file = os.path.join(BaseSaveDir, query, str(icount)+'.txt')
                    fp = open(save_txt_file, 'w')
                    fp.write(desc)
                    fp.close()
                    image_downloader.retrieve(img_url, save_img_file)
                    icount += 1
                    if icount>=img_num:
                        break
                except Exception,e:
                    print e
                    continue
            if icount>=img_num:
                break
        except Exception,e:
            print e
            pass
            

browser.close()
os.system('taskkill /f /im chromedriver_bing.exe')


        



        
