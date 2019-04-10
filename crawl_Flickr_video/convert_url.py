import re
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BaseSaveDir = 'downloads'
re_pattern = re.compile(r'class="download_links"><a\s*href="(?P<video_url>[^"]+)"', re.VERBOSE)

browser = webdriver.Chrome('./chromedriver')

queries = file('queries.txt').read().split('\n')
for query in queries:
    if not query:
        continue

    raw_urls = file(os.path.join(BaseSaveDir,query,'urls.txt')).read().split('\n');

    fp = open(os.path.join(BaseSaveDir,query,'converted_urls.txt'),'w')
    for raw_url in raw_urls:
        if not raw_url:
            break
        print raw_url
        browser.get('http://savevideo.me')
        
        # Find the search box
        elem = browser.find_element_by_id('url')
        # Enter the raw url in the search box
        elem.send_keys(raw_url + Keys.RETURN)    

        # Wait until the new page is loaded
        WebDriverWait(browser, 6000).until(EC.presence_of_element_located((By.XPATH,"//div[@class='download_links']")))     

        # Get the page source of new page
        html_source = browser.page_source

        # Find the converted url
        matches = re_pattern.findall(html_source)
        url = matches[0]
        video_id = url.split('/')[-2]
        converted_url = raw_url+'/play/site/'+video_id
        print converted_url
        print>>fp, converted_url

    fp.close()
    
browser.close()
os.system('taskkill /f /im chromedriver.exe')


    



    
