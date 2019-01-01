# -*- coding: utf8 -*-

import requests, os, re
from bs4 import BeautifulSoup



class search_video_page:
    restrict = [
        ["\\",""],
        ["/",""],
        [":",""],
        ["?",""],
        ['"',''],
        ["<","["],
        [">","]"],
        ["|","&"]
    ]

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

        for i in range(4,len(tmp_0)):
            tmp = str(tmp_0[i])
            tmp_1 = str(tmp).split('"')

            for j in range(0,len(self.restrict)):
                tmp_1[5]=str(tmp_1[5]).replace(self.restrict[j][0],self.restrict[j][1])
            
            vkey[str(tmp_1[3])] = tmp_1[5]

        return vkey