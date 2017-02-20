###这篇文章干嘛的？
本屌在上网时偶然看到一个图片网站，网站的尺度是这样的： 



![图片站首页](https://raw.githubusercontent.com/panacena/mmPictures/master/1240.png)

里面的美女**露骨而不露点**，简直是宅男福利。一时兴起，决定将网站上的图片down下来研究研究。正好最近在研究python，所以决定用这个抓取图片存到本地，将图片url存到 mongodb以防止以后用。

源码项目github地址 ： https://github.com/panacena/mmPictures/
本人博客地址 ：  http://www.jianshu.com/u/61f41588151d
***
####爬虫初识
网络爬虫（又被称为网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者），是一种按照一定的规则，自动的抓取万维网信息的程序或者脚本。
要学习Python爬虫，我们要学习的共有以下几点：
* Python基础知识
* Python中urllib和urllib2库的用法
* Python正则表达式
* Python爬虫框架Scrapy
* Python爬虫更高级的功能
当然，我们今天暂时不需要使用框架进行爬取，只用urllib2等库进行操作。其它的一些关于爬虫的一些基本信息，可以在这位大神的博客中学习到。[学习爬虫点我](http://cuiqingcai.com/1052.html)。
***
####开始爬取
#####确定URL开始抓取
1. 我们以 http://www.zngirls.com/rank/sum/ 为起始页面进行爬取，打开网页后右键查看源代码。
打开这个url后，如图1。我们需要关心的是红色链接的内容。
![图1](https://raw.githubusercontent.com/panacena/mmPictures/master/2.png)

2. 这个如何查找呢?如果你用的是360浏览器，在MM图片那右击，选择“审查元素”。之后就可以查看到点击MM头像后跳转的url地址和MM头像的url地址  。图2：
![图2](https://raw.githubusercontent.com/panacena/mmPictures/master/3.png)

3 . 现在还是没有看到写真的图片，我们点击MM的头像，进入到了下图的页面  http://www.zngirls.com/girl/21751/ 可以看到如图3这个页面也没有写真的具体图片，只是写真的封面集合。不急，我们继续点击封面。
![图3](https://raw.githubusercontent.com/panacena/mmPictures/master/4.png)
4 .  点击封面后，http://www.zngirls.com/g/19671/1.html  进入的页面就可以看到写真的具体图片了。这时我们就可以爬取图片地址了。当然，这个也是分页的，所以也需要获取一共多少页以及每一页的url。

![Paste_Image.png](https://raw.githubusercontent.com/panacena/mmPictures/master/5.png)

#####开始码代码吧
从上面的步骤我们整理一下思路，大概分为以下三部：
* 第一步 从 http://www.zngirls.com/rank/sum/ 开始抓取MM点击头像的链接(注意是分页的)
* 第二部 从 http://www.zngirls.com/girl/21751/ 抓取每一个写真集合的链接(注意是分页的)
* 第三部 从 http://www.zngirls.com/g/19671/1.html 在写真图片的具体页面抓取图片(注意是分页的)


**1. 从起始页面 http://www.zngirls.com/rank/sum/ 开始首选先获取分页的页数以及每一页的url，方便下一步获取点击MM获取专辑url地址。接着解析每一页的html，获取每一页中点击MM头像后跳转的专辑集合页面。**

```
"""
从起始页面 http://www.zngirls.com/rank/sum/ 开始获取排名的页数和每一页的url

"""
def  mmRankSum():
    req = urllib2.Request("http://www.zngirls.com/rank/sum/", headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    #首先获取页码数,然后用循环的方式挨个解析每一个页面
    pages = htmlpath.xpath('//div[@class="pagesYY"]/div/a/@href')


    for i in range( len(pages) -2 ):

        pagesitem="http://www.zngirls.com/rank/sum/"+ pages[i]
        mmRankitem(pagesitem)

"""
参数 url : 分页中每一页的具体url地址
通过穿过来的参数，使用  lxml和xpath 解析 html，获取每一个MM写真专辑页面的url

"""
def mmRankitem(url):
    req = urllib2.Request(url, headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    pages = htmlpath.xpath('//div[@class="rankli_imgdiv"]/a/@href')
    for i in range(len(pages)):

        print "http://www.zngirls.com/" + pages[i]
```
***
**2. 从mmRankitem方法中获取到的url中解析每一个MM写真专辑图片的具体地址，也就是写真图片列表的页面。**

```
"""
参数 albumsurl: 每一个MM专辑的页面地址
通过穿过来的参数，获取每一个MM写真专辑图片集合的地址

"""
def getAlbums(girlUrl):
    req = urllib2.Request(girlUrl, headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    pages = htmlpath.xpath('//div[@class="igalleryli_div"]/a/@href')
    for i in range(len(pages)):
         print  "http://www.zngirls.com/" + pages[i]+"album/"
         getAlbums("http://www.zngirls.com/" + pages[i]+"/album/")
```

**3.  从每一页中获取图片的url，已经每一张图片的名称，方便下一步进行下载。**


```
"""
参数 url : 每一个MM写真专辑图片集合的地址
通过穿过来的参数，首先先获取图片集合的页数，然后每一页解析写真图片的真实地址

"""
def getPagePicturess(albumsurl):
    req = urllib2.Request(albumsurl, headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)
    pages = htmlpath.xpath('//div[@id="pages"]/a/@href')
    for i in range(len(pages)-2):
        savePictures("http://www.zngirls.com" + pages[i])

"""
参数 url : 每一个MM写真专辑图片集合的地址(进过分页检测)
通过穿过来的参数，直接解析页面，获取写真图片的地址，然后下载保存到本地。

"""
def savePictures(itemPagesurl):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        , "Connection": "keep-alive"
        , "Referer": "image / webp, image / *, * / *;q = 0.8"
        ,"Accept":"image/webp,image/*,*/*;q=0.8"
    }
    req = urllib2.Request(itemPagesurl, headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)
    print itemPagesurl
    pages = htmlpath.xpath('//div[@class="gallery_wrapper"]/ul/img/@src')
    for i in range(len(pages) ):
        print pages[i]
        pciturelist.append(pages[i])
```


**4  .获取每张图片的url，可每张照片的名称，然后下载到本地。**

```
"""
参数 url : 每一个MM写真专辑图片集合的地址(进过分页检测)
通过穿过来的参数，直接解析页面，获取写真图片的地址，然后下载保存到本地。

"""
def savePictures(itemPagesurl):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        , "Connection": "keep-alive"
        , "Referer": "image / webp, image / *, * / *;q = 0.8"
        ,"Accept":"image/webp,image/*,*/*;q=0.8"
    }
    req = urllib2.Request(itemPagesurl, headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)
    print itemPagesurl
    pages = htmlpath.xpath('//div[@class="gallery_wrapper"]/ul/img/@src')

    names = htmlpath.xpath('//div[@class="gallery_wrapper"]/ul/img/@alt')
    for i in range(len(pages) ):
        print pages[i]
        pciturelist.append(pages[i])

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            , "Connection": "keep-alive"
            , "Referer": pages[i]
        }
        req = urllib2.Request(pages[i], headers=headers)

        urlhtml = urllib2.urlopen(req)

        respHtml = urlhtml.read()

        binfile = open('%s.jpg' % ( names[i] ) , "wb")
        binfile.write(respHtml);
        binfile.close();

```

***
**5. 执行完毕后(时间可能会比较长)，就可以在文件夹里面看到一张一张的图片都下载完毕。再这里注意的是防止出现反爬虫，可以用设置header或者代理等方式。**
![图片下载到了文件夹中](https://raw.githubusercontent.com/panacena/mmPictures/master/6.png)

没有设置一些header等参数时，有时会出现如下这种情况，这种情况应该是网站有反爬虫的机制。

![反爬虫](https://raw.githubusercontent.com/panacena/mmPictures/master/7.png)


***
源码项目github地址 ： https://github.com/panacena/mmPictures/
这是本人学习python后写的一个小例子。代码写的很烂。以后会学习Scrapy等框架然后在重新重构一下代码。希望可以给个star~~~
