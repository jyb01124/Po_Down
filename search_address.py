import requests
from bs4 import BeautifulSoup

class search_address:

    viewkey = ""

    def __init__(self):
        pass

    def set_viewkey(self, viewkey):
        self.viewkey = viewkey
        
    def viewkey_download_address(self):

        url = "https://www.pornhub.com/view_video.php?viewkey=" + self.viewkey

        html = requests.get(url)
        html = html.content
        soup = BeautifulSoup(html,'html.parser')

        quality = {}

        tmp_0 = soup.find_all("script",type="text/javascript")
        tmp_1 = str(tmp_0[2]).split('[{')
        tmp_2 = tmp_1[1].split('}]')
        video = tmp_2[0].split('},{')

        v_num = len(video)

        for i in range(0,v_num):
            STR = video[i].replace('"','')
            STR = STR.split(",")
            qul = STR[2].split(":")
            add = STR[3].split(":")
            try:
                add[1] = add[1] + ":" + add[2]
                add[1] = add[1].replace("\\","")
                quality[qul[1]] = add[1]
            except:
                pass
        
        return quality
