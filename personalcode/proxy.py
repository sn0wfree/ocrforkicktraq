import urllib.request
import re,random
from multiprocessing.dummy import Pool as ThreadPool
time_out = 3 # 全局变量 10 秒超时时间
count = 0
proxies = [None]
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
def get_proxy():
    proxies=[]
    proxy_url='http://www.xicidaili.com/'
    # 使用全局变量,修改之
    #global proxies
    try:
        req = urllib.request.Request(proxy_url,None,headers)
    except:
        print('无法获取代理信息!')
        return
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    p = re.compile(r'''<tr\sclass[^>]*>\s+
                                    <td>.+</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                </tr>''',re.VERBOSE)
    proxy_list = p.findall(html)
    for each_proxy in proxy_list[1:]:
        if each_proxy[4] == 'HTTP':
            proxies.append(each_proxy[0]+':'+each_proxy[1])
    return proxies


def change_proxy(proxies):
    # 随机从序列中取出一个元素
    proxy = random.choice(proxies)
    # 判断元素是否合理
    if proxy == None:
        proxy_support = urllib.request.ProxyHandler({})
    else:
        proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',headers['User-Agent'])]
    urllib.request.install_opener(opener)
    print('auto switching proxy：%s' % ('local' if proxy==None else proxy))
def get_req(url):
    # 先伪造一下头部吧,使用字典
    blog_eader = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
                'GET':url
                }
    req = urllib.request.Request(url,headers = blog_eader)
    return req
# 访问 博客
def look_blog(url):
    # 切换一下IP
    change_proxy()
    req = get_req(url)
    try:
        urllib.request.urlopen(req,timeout = time_out)
    except:
        return
    else:
        print('访问成功!')
# 迭代访问
def click_blog(url):
    for i in range(0,count):
        if(i == count):
            break
        print('当前访问 Blog %s 第 %d 次' % (url,i))
        look_blog(url)
# 获取博客的文章链表
def get_blog_list(url):
    req = get_req(url)
    try:
        response = urllib.request.urlopen(req,timeout = time_out)
    except:
        print('无法挽回的错误')
        return None
    # 由于 Csdn 是 utf-8 所以不需要转码
    html = response.read()
    # 存储一个正则表达式 规则
    regx = '<span class="link_title"><a href="(.+?)">'
    pat = re.compile(regx)
    # 其实这里 写作 list1 = re.findall('<span class="link_title"><a href="(.+?)">',str(html)) 也是一样的结果
    blog_list = re.findall(pat,str(html))
    return blog_list
if __name__ == '__main__':
    global count
    # 基本参数初始化
    # 获取代理
    get_proxy()
    print('有效代理个数为 : %d' % len(proxies))
    blogurl = input('输入blog链接:')
    # 这个地方原本是我的默认输入偷懒用的
    if len(blogurl) == 0:
        blogurl = 'http://blog.csdn.net/bkxiaoc/'
    print('博客地址是:%s' % blogurl)
    try:
        count = int(input('输入次数:'))
    except ValueError:
        print('参数错误')
        quit()
    if count == 0 or count > 999:
        print('次数过大或过小')
        quit()
    print('次数确认为 %d' % count)
    # 获取 博文 列表,由于测试时我的博文只有一页所以 只能获得一页的列表
    blog_list = get_blog_list(blogurl + '?viewmode=contents')
    if len(blog_list) == 0:
        print('未找到Blog列表')
        quit()
    print('启动!!!!!!!!!!!!!!!!!!!!')
    # 迭代一下 使用多线程
    index = 0
    for each_link in blog_list:
        # 补全头部
        each_link = 'http://blog.csdn.net' + each_link
        blog_list[index] = each_link
        index += 1
    # 有多少个帖子就开多少个线程的一半 let's go
    pool = ThreadPool(int(len(blog_list) / 2))
    results = pool.map(click_blog, blog_list)
    pool.close()
    pool.join()
    print('完成任务!!!!!!!!!!!!!!!!!!!!')
