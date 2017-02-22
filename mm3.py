#!/usr/bin/env python
# -*-coding:utf-8-*-
import urllib.request
from lxml import etree
from os import system

"""
第一步: 从 http://www.zngirls.com/rank/sum/ 开始抓取MM点击头像的链接(注意是分页的)
#第二部  http://www.zngirls.com/girl/21751/ 抓取每一个写真集合的链接(注意是分页的)
#第三部 http://www.zngirls.com/g/19671/1.html 在写真图片的具体页面抓取图片(注意是分页的)
"""

picture_list = []

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
    , "Connection": "keep-alive"
}

"""
从起始页面 http://www.zngirls.com/rank/sum/ 开始获取排名的页数和每一页的url

"""


def mm_rank_sum():
    req = urllib.request.Request("http://www.zngirls.com/rank/sum/", headers=header)
    html = urllib.request.urlopen(req)
    html_data = html.read()
    html_path = etree.HTML(html_data)

    # 首先获取页码数,然后用循环的方式挨个解析每一个页面
    pages = html_path.xpath('//div[@class="pagesYY"]/div/a/@href')

    for i in range(len(pages) - 2):
        pages_item = "http://www.zngirls.com/rank/sum/" + pages[i]
        mm_rank_item(pages_item)


"""
参数 url : 分页中每一页的具体url地址
通过穿过来的参数，使用  lxml和xpath 解析 html，获取每一个MM写真专辑页面的url

"""


def mm_rank_item(url):
    req = urllib.request.Request(url, headers=header)
    html = urllib.request.urlopen(req)
    html_data = html.read()
    html_path = etree.HTML(html_data)

    pages = html_path.xpath('//div[@class="rankli_imgdiv"]/a/@href')
    for i in range(len(pages)):
        print("http://www.zngirls.com/" + pages[i] + "album/")
        get_albums("http://www.zngirls.com/" + pages[i] + "/album/")
        # print "http://www.zngirls.com/" + pages[i]


"""
参数 url : 每一个MM专辑的页面地址
通过穿过来的参数，获取每一个MM写真专辑图片集合的地址

"""


def get_albums(girl_url):
    req = urllib.request.Request(girl_url, headers=header)
    html = urllib.request.urlopen(req)
    html_data = html.read()
    html_path = etree.HTML(html_data)

    pages = html_path.xpath('//div[@class="igalleryli_div"]/a/@href')
    for i in range(len(pages)):
        get_page_pictures("http://www.zngirls.com/" + pages[i])


"""
参数 url : 每一个MM写真专辑图片集合的地址
通过穿过来的参数，首先先获取图片集合的页数，然后每一页解析写真图片的真实地址
"""


def get_page_pictures(albumsurl):
    req = urllib.request.Request(albumsurl, headers=header)
    html = urllib.request.urlopen(req)
    html_data = html.read()
    html_path = etree.HTML(html_data)
    pages = html_path.xpath('//div[@id="pages"]/a/@href')
    for i in range(len(pages) - 2):
        save_pictures("http://www.zngirls.com" + pages[i])


"""
参数 url : 每一个MM写真专辑图片集合的地址(进过分页检测)
通过穿过来的参数，直接解析页面，获取写真图片的地址，然后下载保存到本地。

"""


def save_pictures(item_pages_url):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
        , "Connection": "keep-alive"
        , "Referer" : "http://www.zngirls.com/img.html?img=" + "http://t2.onvshen.com:8080/gallery/22162/21936/0.jpg"
        # , "Referer": "image / webp, image / *, * / *;q = 0.8"
        , "Accept": "image/webp,image/*,*/*;q=0.8"
    }
    try:
        req = urllib.request.Request(item_pages_url, headers=header)
        html = urllib.request.urlopen(req)
        html_data = html.read()
        html_path = etree.HTML(html_data)
        print(item_pages_url)
        pages = html_path.xpath('//div[@class="gallery_wrapper"]/ul/img/@src')
        names = html_path.xpath('//div[@class="gallery_wrapper"]/ul/img/@alt')
    except Exception:
        pass
    for i in range(len(pages)):
        print(pages[i])
        picture_list.append(pages[i])

        try:

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
                , "Connection": "keep-alive"
                , "Referer": "http://www.zngirls.com/img.html?img=" + pages[i]
            }
            req = urllib.request.Request(pages[i], headers=headers)

            urlhtml = urllib.request.urlopen(req)

            respHtml = urlhtml.read()

            binfile = open('%s.jpg' % (names[i]), "wb")
            binfile.write(respHtml);
            binfile.close();
        except Exception:
            pass


mm_rank_sum()
"""
fl=open('list.txt', 'w')
for i in picture_list:
    fl.write(i)
    fl.write("\n")
fl.close()
print '关机ing'
"""
print('finish')
# system('shutdown -s')
