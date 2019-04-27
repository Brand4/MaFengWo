import requests
from lxml import etree
import os
import re

class Trip(object):
    def __init__(self,username,password):
        self.loginUrl = 'https://passport.mafengwo.cn/login/'
        word = input('输入你想查询的城市：')
        self.cityUrl = 'http://www.mafengwo.cn/search/s.php?t=info&q=' + word
        self.username = username
        self.password = password
        self.isTrue = True
        #self.login()


    def login(self):
        datas = {
            'passport':self.username,
            'password':self.password
        }
        headers = {
        'referer':'https://passport.mafengwo.cn/',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2888.400'
        }
        s = requests.session()
        r = s.post(self.loginUrl, data= datas, headers = headers)

    def makedir(self,title):
        title = re.sub('\|','',title)
        title = re.sub('\:','',title)
        title = re.sub(r'>','',title)
        title = re.sub(r'<','',title)
        title = re.sub('\*','',title)

        self.path = 'D:\\蚂蜂窝\\' + title +'\\'
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
        else:
            print('该文件夹已存在')

    def get_travel_notes(self):
        headers = {
        'referer':'http://www.mafengwo.cn/mdd/',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2888.400'
        }
        r = requests.get(self.cityUrl,headers = headers)
        html = etree.HTML(r.text)
        # self.title = html.xpath('//div[@class="ct-text "]/h3/a[@class = "_j_search_link"]/text()')
        # print(self.title)
        self.ID = html.xpath('//div[@class="ct-text "]/h3/a[@class = "_j_search_link"]/@href')

        info = html.xpath('//div[@class="ct-text "]/h3/a[@class = "_j_search_link"]')
        print(info)
        self.title = []
        a = 0
        for i in range(len(info)):
            self.title.append(info[a].xpath('string(.)'))
            print(self.title[a])
            a += 1

        count = 0
        number = 1
        self.ss = 0
        for i in range(len(self.title)):
            self.makedir(str(self.title[count]))
            count += 1
            self.get_picture()

    def get_picture(self):
        for i in range(len(self.ID)):
            self.newPageUrl = str(self.ID[self.ss])
            head = {
                'Referer': self.newPageUrl,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            self.ss += 1
            r = requests.get(str(self.newPageUrl),headers = head)
            #print(r.text)
            html = etree.HTML(r.text)
            self.pictureUrl = html.xpath('//img/@data-src')
            print(self.pictureUrl)
            c = 0
            for i in range(len(self.pictureUrl)):
                print(self.pictureUrl[c])
                self.pictures = requests.get(self.pictureUrl[c])
                c += 1
                fq = open(self.path + str(c) +'.jpg','wb')     #下载图片，并保存和命名
                fq.write(self.pictures.content)
                fq.close()
            break
            

l = Trip('18623451466','www169749')
l.get_travel_notes()