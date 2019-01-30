import time
import requests
from lxml import etree
import re
import os

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2888.400'}

#创建文件夹
def makedir(title):
    title = re.sub('\|','',title)
    title = re.sub(':|<|>|"|/|:','',title)
    title = re.sub('\?|\*','',title)
    title = re.sub('\\\\','',title)

    path = 'D:\\蚂蜂窝\\' + title +'\\'
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        return path,True
    else:
        print('该游记已存在')
        return path,False

#获得html文本
def getHtml(url):
    res = requests.get(url,headers = headers)
    html = etree.HTML(res.text)
    return html

#下载
def download(html):
    pictureUrl = html.xpath('//img/@data-rt-src')
    title = html.xpath('//div[@class="vi_con"]/h1/text()')
    pathnew,isExist = makedir(str(title))
    n = 1
    length = len(pictureUrl)

    while isExist==True:
        for i in pictureUrl:
            r = requests.get(i, headers = headers)
            fq = open(pathnew + str(n) +'.jpg','wb')     #下载图片，并保存和命名
            fq.write(r.content)
            fq.close()
            print('下载进度:  ' + str(int((n/length)*100)) + '%' ,end = "\r")
            n += 1
        isExist = False
        print('下载进度:  ' + '100%')
        print('下载完成')

def start():
    url = input('请输入游记网址:  ')
    html = getHtml(url)
    download(html)

if __name__ == '__main__':
    start()