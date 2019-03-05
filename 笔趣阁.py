import requests
from lxml import etree
import lxml
import sys
import os
import re
import ssl

# 获取小说名和链接，并创建相对的目录
def get_bookname(url):
    html = requests.get(url,headers=headers)
    objects = etree.HTML(html.text)
    objs = objects.xpath("//ul[@class='list-group list-top']/li")

    # 用来存储小说信息
    url_book = []
    for obj in objs:
        #获取小说名和小说链接
        book_name = obj.xpath("div[@class='row']/div[@class='col-md-5 col-sm-4 col-xs-9 text-overflow']/a/text()")[0]
        book_url =  obj.xpath("div[@class='row']/div[@class='col-md-5 col-sm-4 col-xs-9 text-overflow']/a/@href")[0]


        # 去除不符合windows文件夹/文件命名规范的字符
        book_name = validateTitle(book_name)
        # 指定目录名
        dirname = "D:/笔趣阁小说/" + book_name

        info = {
            'title' :book_name,
            'dirname' :dirname,
            'book_url' :book_url
        }
        url_book.append(info)
        # print(url_book)
        # 如果没目录不存在就创建
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    return url_book

# 获取小说章节名和文章链接
def get_bookurl(url):
    for item in url:
        book_list = requests.get(item['book_url'])
        book_lists = etree.HTML(book_list.text)
        book_list = book_lists.xpath("//ul[@class='_chapter']/li")

        # 获取章节名字组成文件名，获取对应的内容链接
        list_info = []
        for list in book_list:
            list_name = list.xpath('a/text()')[0]
            list_url  = list.xpath('a/@href')[0]

            # 网站上a标签内链接有个回车，所以去除回车
            list_url = list_url.replace('\n', "")

            #  去除不符合windows命名规范的字符
            list_name = validateTitle(list_name)
            # 拼接文件名
            filename = item['dirname']+"/"+list_name+".txt"
            info = {
                'list_name' :list_name,
                'filename' : filename,
                'list_url' : list_url
            }
            list_info.append(info)
        for list_content in list_info:
            # 如果程序重新运行，检查是否存在文件，如果存在就是上次运行下载过，跳过这个章节
            if os.path.exists(list_content['filename']):
                print("此章节已下载，开始下载下一章")
                continue
            contents = ""
            #小说可能存在两页或三页
            for p in range(3):
                p=p+1
                url = list_content['list_url'].rstrip('.html')
                url = url+"_%s.html"%(p)
                # print(url)
                response = requests.get(url)
                # 解决� \ufffd 乱码问题，
                #response.encoding = 'gbk'
                content = etree.HTML(response.text)
                content = content.xpath("//div[@id='content']/text()")
                # print(type(content))
                content = "\n".join(content)
                content = "\n".join(content.split())
                # 把乱码转换为“？”
                content = re.sub("�","?",content)
                # 拼接所有页数的小说内容
                contents += content
            # print(contents)
            with open(list_content["filename"], 'w') as f:
                f.write(contents)
                print(list_content['filename']+"已下载完成")





# 处理不能被当做文件名的特殊字符
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5383.400 QQBrowser/10.0.1313.400'}


if __name__ == '__main__':
    for page in range(298):
        url = "https://www.biquge5.com/shuku/1/allvisit-0-{page}.html".format(page=page+1)
        book_urls = get_bookname(url)
        get_bookurl(book_urls)