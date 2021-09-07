import os
import logging
from time import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sys
from datetime import datetime
import requests
import json
from pathlib import Path

#init item
user_agent = UserAgent()
currenttime = datetime.now().strftime('%Y-%m-%d-%H')
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

def fop(filename):
    with open(filename,'r') as f:
        return json.load(f)

def writeJson(newData, fileName='recorder.json'):
    with open(fileName,'r+') as f:
        fileData = json.load(f)
        fileData.update({newData : currenttime})
        f.seek(0)
        json.dump(fileData,f,indent=4)

def imageDown(url,topic,folder):
    try:
        os.mkdir(os.path.join(os.getcwd(),folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(),folder))
    Dcard_Api = {
        'popular': 'false',#熱門
        'limit': '30'#顯示文章篇數，最多100篇
    }
    #init
    Dcard = requests.get(url,headers={'user-agent':user_agent.random})
    Dcard_to_Json = json.loads(Dcard.text)
    #print(Dcard_to_Json)
    idList = []
    risuList = []
    pptList = []
    lurlList = []
    imageResipotary = []
    for item in Dcard_to_Json:
        idList.append(item['id'])
    with open('../mainId.json','r',encoding = 'utf-8') as f:
        mainLib = json.load(f)
    idLib = {}
    for x in idList:
        if str(x) in mainLib.keys():
            print('page collision on',str(x))
            continue
        idLib[str(x)]=folder
    with open('../partId.json','w',encoding = 'utf-8') as f:
        f.write(json.dumps(idLib,indent=4,ensure_ascii=False))
    print(idList)

    print(idList)
    for ids in idList:
        api = 'https://www.dcard.tw/f/'
        url = api + topic + '/p/' + str(ids) 
        resp = requests.get(url,headers={'user-agent':user_agent.random})
        soup = BeautifulSoup(resp.text,"html.parser")
        posurl = soup.select('a[href]')
        for link in posurl:
            if link['href'].find('https://risu.io') != -1:
                risuList.append(link['href'])
            if link['href'].find('https://ppt.cc') != -1:
                pptList.append(link['href'])
            if link['href'].find('https://lurl.cc') != -1:
                lurlList.append(link['href'])  
        images = soup.find_all('img')
        for image in images:
            if image['src'].find('https://imgur.dcard.tw/') != -1:
                imageResipotary.append(image['src'])
                print(image['src'])
                with open(image['src'][24:],'wb') as f:
                    im = requests.get(image['src'],headers={'user-agent':user_agent.random})
                    f.write(im.content)

if __name__ == '__main__':
    if os.path.isdir('Dcard' + currenttime):
        print('噁男，太急了')
        exit(-1)
    
    api = 'https://www.dcard.tw/service/api/v2/forums/'
    topic = 'pet'#the topic
    posurl = '/posts?popular=true&limit='
    page = str(3)#change pages
    url = api + topic + posurl + page

    print("today is =", currenttime)
    print('start crawling')
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    start_time = time()

    imageDown(url,topic,'Dcard' + currenttime)
    path = os.getcwd()
    os.chdir(os.path.abspath(os.path.join(path,os.pardir)))

    mainId = fop('mainId.json')
    partId = fop('partId.json')
    mainId.update(partId)

    with open('mainId.json','w',encoding = 'utf-8')as f:
        f.write(json.dumps(mainId,indent=4,ensure_ascii=False))
    print('end crawling')
    print(f'Total time used: {(time() - start_time):.2f} sec', file=sys.stderr)