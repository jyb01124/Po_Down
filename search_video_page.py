#https://www.pornhub.com/video/search?search=fuck2

# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import re

class search_video_page:
    def __init__(self):
        pass
    
    def search(self, word, page):
        url = "https://www.pornhub.com/video/search?search=" + word + "&page=" + str(page)
        
        html = requests.get(url)
        html = html.content
        soup = BeautifulSoup(html,'html.parser')

        tmp_0 = soup.find_all("a", {"href":re.compile("view_video.php"), "data-related-url":False, "target":False, "class":""})

        url = "https://www.pornhub.com"

        vkey = {}

        for i in range(0,len(tmp_0)):
            tmp_1 = str(tmp_0[i]).split('"')
            vkey[str(tmp_1[3])] = tmp_1[5]

        print(vkey)
        

    def j(self):    
        for i in range(0,len(b)-1):
            for j in range(i+1,len(b)):
                if b[i] == b[j]:
                    print(i)
                    print(j)
                    print(b[i])


        

if __name__ == "__main__":
    s = search_video_page()
    s.search("fuck",1)
    s.search("fuck",2)