# coding = 'utf-8'
import requests
from bs4 import BeautifulSoup
import urllib
import os
import re
from lxml import etree
import lxml

n = 0
length = len(range(67))

# 1. 请求网站获取相应信息
def get_infos(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("已获取服务器相应...")
    print("正在解析图片地址...")
    response.encoding = 'gb2312'
    html = etree.HTML(response.text)
    objects = html.xpath("//div[@class='graphic_list page_width']/ul/a")

    img_infos = []
    for object in objects:
        img_group = object.xpath("@href")[0]
        dirname = object.xpath("li/p/text()")[0]
        img = object.xpath("li/dl/img/@data-original")[0]
        # 组图链接
        img_group = "http://www.xingmeng365.com/" + img_group
        img = "http://www.xingmeng365.com/" + img
        dir_list_name = "E:/星梦365/" + dirname
        info = {
            'img_group': img_group,
            'img': img,
            'dir_list_name': dir_list_name
        }
        img_infos.append(info)
    return img_infos


# 2.获取组图所有图片
def get_img(img_infos):
    print("正在查找图片组图...")
    for info in img_infos:
        img_html = requests.get(info['img_group'], headers=headers)
        img_html.raise_for_status()
        img_html.encoding = "gb2312"
        html = etree.HTML(img_html.text)
        # print(img_url)
        # 获取图片页数
        page = html.xpath("//div[@class='n_page']/text()")
        # 转换为字符串类型
        page = str(page[1])
        # 去除多余字符
        page = page.strip("\n\t\r").split(" ")
        page = re.sub("\D", "", page[0])
        page = page.replace(page[0], '')
        page = int(page)
        count = 0  # 计数
        print("准备下载", info['dir_list_name'])
        for i in range(page):
            name = info['dir_list_name'] + "/" + str(count + 1) + ".jpg"
            if os.path.exists(name):
                print("此文件已下载过...")
                continue
            # 拼接图片链接
            i = i + 1
            i = str(i)
            img_url = info['img_group'] + "&mm=" + i
            img = requests.get(img_url, headers=headers)
            img.raise_for_status()
            img.encoding = "gb2312"
            img_text = etree.HTML(img.text)

            # 图片链接
            img_g_url = img_text.xpath("//div[@class='text']/a/img/@src")[0]
            img_g_url = "http://www.xingmeng365.com" + img_g_url

            if not os.path.exists(info['dir_list_name']):
                os.makedirs(info['dir_list_name'])

            print("正在调用下载程序...")
            download(img_g_url, name)
            count = count + 1
            print("正在下载第：", count,'个...')


def download(url, name):
    if url == None:  # 地址若为None则跳过
        pass
    print("请求下载中...")
    urllib.request.urlretrieve(url, name)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5383.400 QQBrowser/10.0.1313.400'
}

for i in range(67):
    i = i + 1
    url = "http://www.xingmeng365.com/?ToPage=" + str(i)
    get_img(get_infos(url))
    n = n+1
    if n == length:
        print("下载任务已完成")
