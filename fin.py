# -*- coding: utf8 -*-
import string, requests, sys, os, threading
from bs4 import BeautifulSoup
import asyncio

def make_video_url(url):
    html = requests.get(url)
    html = html.content
    soup = BeautifulSoup(html,'html.parser')

    tmp_0 =[]
    tmp_1 = []
    tmp_2 = []
    set_ = []

    best = "1080"
    very_good = "720"
    good = "480"
    bad = "240"

    mp4 = ".mp4"

    broken_for = 0
    im_URL = 0
    title = 0

    title = soup.find_all("title")
    title = str(title)
    title = title.replace('[<title>','')
    title = title.replace('</title>]','')
    title = title + mp4

    tmp_0 = soup.find_all("script",type="text/javascript")
    tmp_1 = str.split(str(tmp_0[5]),'"')

    for count in range(0,len(tmp_1)):
        if tmp_1[count].find(mp4) > 0:
            tmp_1[count] = tmp_1[count].replace('\\','')
            tmp_2.insert(0,tmp_1[count])
           
    for switch in range(0,5):
        for count in range(0,len(tmp_2)):
            dic = {
                0 : best,
                1 : very_good,
                2 : good,
                3 : bad
                }[switch]
                    
            if tmp_2[count].find(dic) > 0:
                im_URL = tmp_2[count]
                broken_for = 1
                break
        
        if broken_for == 1:
            break

    set_.append(im_URL)
    set_.append(title)

    return set_

while(1):
    print ("1. 영상 이름 검색\n")
    print ("2. 배우 이름 검색\n")
    sel = input("검색 방법을 선택해 주세요. : ")

    tmp_0 =[]
    tmp_1 = []
    vi_down_URL = []
    
    num = 1

    if sel == '1':
        url_i = "https://www.pornhub.com/video/search?search="
    elif sel == '2':
        url_i = "https://www.pornhub.com/pornstar/"
    else:
        print ("1번과 2번중 하나를 골라주세요.\n")
        continue

    url_v = "https://www.pornhub.com/view_video.php?"
    
    while(1):
        if sel == '1':
            search = input("검색하실 단어를 적어주세요 : ")
        elif sel == '2':
            search = input("검색하실 배우 이름을 정확히 적어주세요 : ")
		
        search = search.replace(' ','+')

        if sel == '1':
            bun = "&"
        elif sel == '2':
            bun = "?"

        url = url_i + search + bun + "page=" + str(num)

        html_v = requests.get(url)
        html_v = html_v.content

        soup = BeautifulSoup(html_v,'html.parser')
		
        if sel == '1':
            bad_search = b'<div id="noResultBigText">No Search Results.</div>'
        elif sel == '2':
            bad_search = b'<h1><span>Error Page Not Found</span></h1>'	
		
        if html_v.find(bad_search) < 0:
            break
			
        if sel_1 == '1':
            print ("검색 결과가 존재 하지 않습니다.\n 다른 단어로 검색해 주세요.\n")
        elif sel_2 == '2':
            print ("배우의 이름이 정확하지 않습니다.\n 다시 한번 적어주세요\n")
        
    while(num<=1):
        os.system("cls")
        print ("검색된 %d번째 페이지의 동영상 리스트를 작성하고 있습니다." %(num))
                
        if html_v.find(bad_search) > 0:
            print ("페이지가 더 이상 존재하지 않습니다.\n프로그램을 종료합니다.\n")
            break
        else:
            pass

        tmp_0 = soup.find_all("li",_vkey=True)

        for count in range(0,len(tmp_0)):
            tmp_0[count].clear()
            tmp_1 = str.split(str(tmp_0[count]),' ')
            tmp_1[1] = tmp_1[1].replace('_vkey','viewkey')
            tmp_1[1] = tmp_1[1].replace('"','')
            tmp_1[1] = url_v + tmp_1[1]
            vi_down_URL.append(tmp_1[1])

        print ("검색된 "+str(num)+"번째 페이지 까지의 동영상의 수 %d개" %(len(vi_down_URL)))
        

        num+=1
        del tmp_0[:]
        del tmp_1[:]

    work = [[],[],[],[],[],[],[],[]]
    working = [0,0,0,0,0,0,0,0] #완료된 스위치 내 작업의 개수
    max_working = [0,0,0,0,0,0,0,0] #최대 작업 량

    address = []
    name = []
    size_max = []
    down_size = [0,0,0,0,0,0,0,0]

    flag = [0,0,0,0,0,0,0,0]

    for count in range(0,len(vi_down_URL)): # URL 을 스위치 별별로 나누기 0~7반까지
        switch = count%8 
        work[switch].append(vi_down_URL[count])

    for cnt in range(0,8): # 스위치별 최대 작업량 계산.
        max_working[cnt] = len(work[cnt])

    print ('다운로드 프로세스를 초기화 하고 있습니다.')

    tmp_list = []
    tmp_name = []

    for switch in range(0,8): # tmp_list 라는 리스트공간에 make_viedo_url 의 리턴값을 저장하여, 주소와 이름 분리해서 저장.
        tmp_list = make_video_url(work[switch][working[switch]])
        tmp_name.append(tmp_list[1])
        address.append(requests.get(tmp_list[0],stream=True))
        name.append(open(tmp_list[1], 'wb'))

    print ('다운로드를 시도할 파일의 길이를 읽어 오고 있습니다. ')

    for switch in range(0,8): 
        size_max.append((int)(address[switch].headers["Content-Length"]))

    switch = 0

    print ('다운로드를 시작합니다.')

    while(1):        
        if flag[switch]==1:
            continue
        if flag[0]==1 and flag[1]==1 and flag[2]==1 and flag[3]==1 and flag[4]==1 and flag[5]==1 and flag[6]==1 and flag[7]==1:
            break

        address[switch].headers = {'Connection' : 'keep-alive'}
        tmp = address[switch].raw.read(1024, decode_content=True)
        down_size[switch] += len(tmp)

        name[switch].write(tmp)

        os.system("cls")
        print (tmp_name[switch]+" :  "+"("+(str)(down_size[switch])+"/"+(str)(size_max[switch])+")")

        if down_size[switch] >= size_max[switch]:
            working[switch] += 1
            if working[switch] >= max_working[switch]:
                flag[switch]=1
                continue
            tmp_list = make_video_url(work[switch][working[switch]])
            tmp_name[switch] = tmp_list[1]            
            address[switch] = requests.get(tmp_list[0],stream=True)
            name[switch] = open(tmp_list[1], 'wb')
            size_max[switch] = (int)(address[switch].headers["Content-Length"])
            address[switch].headers = {'Connection' : 'keep-alive'}
            down_size[switch] = 0

        if switch == 7:
            switch = 0
            continue

        switch += 1
        
        
        

#    while(1):
       #filesize_dl += len()

    

        
            




    


     
        
# ------------------------------------------------------------------------------------------------ 여기까지가 video_url 뽑는 코드
'''
r = requests.get()
c = open('a.mp4', 'wb')
while True:
    print ('1')
    d = r.raw.read(512, decode_content=True)
    c.write(d)
    if not d:
        break
'''











            
