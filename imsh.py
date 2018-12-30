import requests
from bs4 import BeautifulSoup
while True:
    url = input("URL : ")

    html = requests.get(url)
    html = html.content
    soup = BeautifulSoup(html,'html.parser')

    quality = [[],[],[],[]]

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
            quality[i] = dict({qul[0]:qul[1], add[0]:add[1]})
        except:
            pass

    for i in range(0,v_num):
        try:
            print(str(quality[i]["quality"]) + " : " + str(quality[i]["videoUrl"]))
        except:
            pass

