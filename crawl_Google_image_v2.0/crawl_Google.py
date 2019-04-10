import re
import os
import sys
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BaseSaveDir = 'downloads'

browser = webdriver.Chrome('./chromedriver_google')

img_pattern = re.compile(r'imgurl=(?P<img_url>[^"]+)&amp;imgrefurl=', re.VERBOSE)
txt_pattern = re.compile(r'"pt":"(?P<pt>[^"]*)","s":"(?P<s>[^"]*)"', re.VERBOSE)

image_downloader = urllib.URLopener()

queries = file('queries.txt').read().split('\n')
img_num = 500

for query in queries:
    if not query:
        continue
    
    start = 0
    icount = 0
    for ipage in range(img_num):
        url = 'https://www.google.com.sg/search?q='+query+'&safe=active&hl=en&source=lnt&tbs=itp%3Aphoto%2Cic%3Acolor%2Ccdr%3A1%2Ccd_min%3A1%2F1%2F'+str(2000+ipage)+'%2Ccd_max%3A1%2F1%2F'+str(2001+ipage)+'&tbm=isch'
        browser.get(url)
        WebDriverWait(browser, 6000).until(EC.presence_of_element_located((By.XPATH,"//div[@id='searchform']")))     

        html_source = browser.page_source
        img_matches = img_pattern.findall(html_source)
        txt_matches = txt_pattern.findall(html_source)

        start += len(img_matches)

        try:
            assert(len(img_matches)==len(txt_matches))
            
            for ii in range(len(img_matches)):
                try:
                    if not os.path.exists(os.path.join(BaseSaveDir, query)):
                        os.makedirs(os.path.join(BaseSaveDir, query))
                    img_url = img_matches[ii]
                    ext = img_url.split('.')[-1]
                    if ext=='gif':
                        continue
                    save_img_file = os.path.join(BaseSaveDir, query, str(icount)+'.'+ext)
                    print save_img_file                    
                    print img_url

                    if img_url=='http://love.catchsmile.com/wp-content/uploads/Kiss-Me-1.jpg':
                        continue

                    if img_url=='http://www.motherearthnews.com/~/media/Images/MEN/Editorial/Articles/Magazine%252520Articles/1985/11-01/Build%252520a%252520Homemade%252520Gym/096-090-01-sit-up-bench.jpg':
                        continue
                    
                    txt_match = txt_matches[ii]
                    desc = txt_match[0]+' '+txt_match[1]
                    save_txt_file = os.path.join(BaseSaveDir, query, str(icount)+'.txt')
                    fp = open(save_txt_file, 'w')
                    fp.write(desc.encode('utf-8'))
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
os.system('taskkill /f /im chromedriver_google.exe')


        



        
