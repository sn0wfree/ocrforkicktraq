#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by Lin Lu 2016
#-----------------------------------------------------------------------------------------------
'''
this code is for my dissertation.
'''
#-----------------------------------------------------------------------------------------------

from urllib2 import Request, urlopen, URLError
import time
import urllib2
import requests
from lxml import etree
import os,gc,sys,random
import pandas as pd
import unicodecsv
import csv
import multiprocessing as mp
import datetime
import time
import threading
import Queue
import fcntl
#import celery
from PIL import Image

queue = Queue.Queue()

def conn_try_again(max_retries=5,default_retry_delay=1):
    def _conn_try_again(function):
        RETRIES = 0
        #重试的次数
        count = {"num": RETRIES}
        def wrapped(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception, err:
                if count['num'] < max_retries:
                    time.sleep(default_retry_delay)
                    count['num'] += 1
                    return wrapped(*args, **kwargs)
                else:
                    raise Exception(err)
        return wrapped
    return _conn_try_again



def read_a_file(file):
    with open(file,'r') as f:
        f_collected=f.readlines()
    return f_collected
def write_a_file(file,item):
    with open(file,'w') as f:
        lenitem=len(item)
        for i in xrange(0,lenitem):
            f.write(item[i])

def get_proxy(proxy_url):
    import re,urllib2
    proxies=[]
    headers={'headers':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    #proxy_url='https://www.xicidaili.com/'

    #global proxies
    try:
        req = urllib2.Request(proxy_url,None,headers)
    except:
        print('connot access proxy information!')
        return
    response = urllib2.urlopen(req)
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
    # random choose a proxy
    proxy = random.choice(proxies)
    # if available
    if proxy == None:
        proxy_support = urllib2.ProxyHandler({})
    else:
        proxy_support = urllib2.ProxyHandler({'http':proxy})
    opener = urllib2.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',headers['User-Agent'])]
    urllib2.install_opener(opener)
    print('auto switching proxy：%s' % ('local' if proxy==None else proxy))

def reset_or_initial_ip_address(reset=False):
    import os
    import socket
    import socks
    if reset:
        os.system("""(echo authenticate '"mypassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
    else:
        pass
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket






class Lock:

    LOCK_EX = fcntl.LOCK_EX

    def __init__(self, filename='processlock.txt'):
        self.filename = filename
        # 如果文件不存在则创建
        self.handle = open(filename, 'w')
    def acquire(self):
        # 给文件上锁
        fcntl.flock(self.handle, LOCK_EX)

    def release(self):
        # 文件解锁
        fcntl.flock(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        try:
            self.handle.close()
            os.remove(self.filename)
            print 'remove file....'
        except:
            pass



def webscraper_png(img_url,ty):
    lasturl=img_url.split(ty)[0]
    header={'headers':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    tor_headers={"Host":"www.kicktraq.com",
                 "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0",

                 "Accept":"image/png,image/*;q=0.8,*/*;q=0.5",
                 "Accept-Language":"en-US,en;q=0.5",
                 "Accept-Encoding":"gzip, deflate",
                 "Referer":lasturl,
                 "Connection":"keep-alive"

                  }


    #root_url = 'https://www.kickstarter.com'
    try:
        req = urllib2.Request(img_url,None,tor_headers)
        #if 'Response [403]' not in str(req):
        img = urllib2.urlopen(req).read()
        '''
        else:
            reset_or_initial_ip_address(reset=True)
            time.sleep(1)

            req = urllib2.Request(img_url,None,tor_headers)
            img = urllib2.urlopen(req).read()

            img='Error'
        '''
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            img=''
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            img=''
    return img

def savingimage(img,path,project_ID,typefile):
    if os.path.isdir(path +'/%s'%project_ID):
        pass
    else:
        os.makedirs(path +'/%s'%project_ID)
    with open(path+ '/%s/'%project_ID +typefile,'wb') as png:
        png.write(img)

def obtain_kicktraqurl(kickstarterurl):
    if kickstarterurl !='':
        if 'https://www.kickstarter.com' in kickstarterurl:
            kickstarterurl_drophttp=kickstarterurl.split('https://www.kickstarter.com')[1]
            kicktraq_url = 'https://www.kicktraq.com'+kickstarterurl_drophttp
        else:
            kicktraq_url='Error'
    else:
        kicktraq_url='Error'
    return kicktraq_url

#image_file = 'dailypledges.png'
#im = Image.open(image_file)
def generateimageurl(kickstraqurl,pngfile):
    if kickstraqurl !='Error' and kickstraqurl != '':
        if '?ref=category_newest' in kickstraqurl:
            kicktraqurl_droplast=kickstraqurl.split('?ref=category_newest')[0]
            kicktraq_imageurl=kicktraqurl_droplast+'/'+pngfile
        else:
            kicktraq_imageurl='Error'
    else:
        kicktraq_imageurl='Error'

    return kicktraq_imageurl

def readacsv(file):
    with open(file,'r+') as f:
        w=pd.read_csv(file,skip_footer=1,engine='python')
    return w

def scanfolderprocess(rdir):
    fo=os.walk(rdir)

    f=[]
    for root,subfolder,files in fo:
        #print root
        num=root.lstrip(rdir)
        #print num,type(num)
        if num !='':
            number=float(num)

            f.append(number)
        else:
            pass

    return f

def getDirList( p ):
        p = str( p )
        if p=="":
              return [ ]
        #p = p.replace( "/","/")
        if p[-1] != "/":
             p = p+"/"
        a = os.listdir( p )
        #b = [ x   for x in a if os.path.isdir( p + x ) ]

        b = [ float(x)   for x in a if os.path.isdir( p + x ) ]
        return b



def optimalforcollected(savingdatapath_dict,target_file):

    collected_dict={}
    target_dict={}
    search_dict={}
    #print savingdatapath_dict

    #collected_ID=pool.map(scanfolderprocess,(savingdatapath_dict,))
    collected_ID=getDirList(savingdatapath_dict)
    #collected = readacsv(collected_file)
    target=readacsv(target_file)
    target_ID=target['Project_ID']

    #collected_ID=collected['Project_ID']
    #print type(target_ID)
    lentargetProject_ID=len(target_ID)
    #lencollectedProject_ID=list(collected_ID)
    #for i in xrange(0,lencollectedProject_ID):
    #    collected_dict[collected['Project_ID'][i]]=collected['url'][i]
    for i in xrange(0,lentargetProject_ID):
        target_dict[target['Project_ID'][i]]=target['url'][i]
    #a=listtargetProject_ID)
    #b=list(collected_dict)
    #print len(b),len(a),a[1]
    c=list(set(target_ID)-set(collected_ID))
    #print len(c),type(c),c[1]
    for key in c:
        search_dict[key]=target_dict[key]
    pool.close()
    pool.join()
    return search_dict

def writeacsvprocess(file,headers,item):
    with open(file,'r') as project_data:
        project_data_read_csv = unicodecsv.reader(project_data,headers)
        if not headers in project_data_read_csv:
            status=0
        else:
            status=1
    with open(file,'a') as project_data:
        project_data_csv = unicodecsv.DictWriter(project_data,headers)
        if status ==0:
            project_data_csv.writeheader()
        project_data_csv.writerows(item)

def progress_test(counts,lenfile,speed,w):
    bar_length=20
    eta=time.time()+w
    precent =counts/float(lenfile)
    ETA=datetime.datetime.fromtimestamp(eta)
    hashes = '#' * int(precent * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|read %d projects|Speed: %.4f | ETA: %s """ % (precent*100,hashes + spaces,counts,speed,ETA))

    sys.stdout.flush()

def savingallimageforeachproject(key):
    global collected_file
    global y

    global savingdatapath_dict
    global pngfilekicktraqurl
    global pngfilekickstarterurl
    type_png=['dailypledges.png','dailybackers.png','dailycomments.png']
    headers=['Project_ID','url']
    global totalitem_kicktraqurl
    global counts,collected_key
    f1=time.time()
    if key !='':
        w_key=[]
        item_kicktraqurl={}
        item_kicktraqurl['Project_ID']=key
        item_kicktraqurl['url']=pngfilekickstarterurl[key]
        totalitem_kicktraqurl.append(item_kicktraqurl)
        collected_key.append(key)
        w_key.append(key)
        counts+=1
        imagetodownloadprocess(w_key)
    if counts % 10 !=0:
        time.sleep(random.uniform(0.1,0.2))
    else:
        time.sleep(3)
    time.sleep(random.random()*y)

    f2 = time.time()
    #totalitem_kicktraqurl=[]
    #collected_key=[]
    w=(len(file1)-counts)*(f2-f1)/y
    progress_test(counts,len(file1),f2-f1,w)


        #print counts,aaa
        #writeacsvprocess(collected_file,headers,totalitem_kicktraqurl)#totalitem_kicktraqurl is just a name ,but it  just hold all ids and kick_urls

    gc.collect()
    #time.sleep(random.uniform(0.1,1))


    #writeacsvprocess(collected_file,headers,totalitem_kicktraqurl)



def imagetodownloadprocess(collected_key):

    type_png=['dailypledges.png','dailybackers.png','dailycomments.png']
    for key in collected_key:
        for i in type_png:
            locals()['kickstraq%s'%i]=generateimageurl(pngfilekicktraqurl[key],i)
            locals()['img_daily%s'%i]=webscraper_png(locals()['kickstraq%s'%i],i)
            if locals()['img_daily%s'%i]!='Error':
                savingimage(locals()['img_daily%s'%i],savingdatapath_dict,key,i)


    time.sleep(random.random())





def zipafilefordelivery(file,target):
    with zipfile.ZipFile(file, 'w',zipfile.ZIP_DEFLATED) as z:
        z.write(target)
        z.close

def getAttachment(attachmentFilePath):
    contentType, encoding = mimetypes.guess_type(attachmentFilePath)

    if contentType is None or encoding is not None:
        contentType = 'application/octet-stream'

    (mainType, subType) = contentType.split('/', 1)
    with open(attachmentFilePath, 'r') as file:
        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(),_subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(),_subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(file.read())

    encode_base64(attachment)

    attachment.add_header('Content-Disposition', 'attachment',filename=os.path.basename(attachmentFilePath))
    return attachment

def sendmailtodelivery(mail_username,mail_password,to_addrs,*attachmentFilePaths):
    from_addr = mail_username
    # HOST & PORT
    HOST = 'smtp.gmail.com'
    PORT = 25
    # Create SMTP Object
    smtp = smtplib.SMTP()
    #print 'connecting ...'
    # show the debug log
    smtp.set_debuglevel(1)

    # connet
    try:
        print smtp.connect(HOST,PORT)
    except:
        print 'CONNECT ERROR ****'
    # gmail uses ssl
    smtp.starttls()
    # login with username & password
    try:
        #print 'loginning ...'
        smtp.login(mail_username,mail_password)
    except:
        print 'LOGIN ERROR ****'
    # fill content with MIMEText's object
    msg = MIMEMultipart()
    for attachmentFilePath in attachmentFilePaths:
        msg.attach(getAttachment(attachmentFilePath))
    msg.attach(email.mime.text.MIMEText('data collecting process has completed at %s and here is the data file'% now,'plain', 'utf-8'))
    msg['From'] = from_addr
    msg['To'] = ';'.join(to_addrs)
    msg['Subject']='data collecion completed'
    #print msg.as_string()
    smtp.sendmail(from_addr,to_addrs,msg.as_string())
    smtp.quit()

class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            (target) = self.queue.get()
            savingallimageforeachproject(target)

            time.sleep(1/10)
            self.queue.task_done()


def main(pngfilekicktraqurl,y):

    lpngfilekicktraqurl=list(pngfilekicktraqurl)
    for key in lpngfilekicktraqurl:
        queue.put(key)
    queue.join()

def statuscode():
    statuscode=input('please enter stastus code(0-99):')
    if statuscode == 1000 :
        #macbook
        savingdatapath='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image'
    elif statuscode ==1001 :
        #raspberry pi
        savingdatapath='/home/pi/datasharing/image'
    elif statuscode == '2nd':
        savingdatapath='/home/pi/datasharing/image/errorfor2ndcollectedurl'
    else:
        savingdatapath=input('please input the saving data path:')
    return savingdatapath



def chunks(item,n):
    lenitem=len(item)
    dic={}
    #split item by n
    for i in xrange(0,lenitem,n):
        if i+n < lenitem:
            dic[i]=item[i:i+n]
        else:
            dic[i]=item[i:]
    return dic



if __name__=='__main__':
    gc.enable()
    totalitem_kicktraqurl=[]
    global counts,collected_key
    global y
    counts=0
    collected_key=[]
    pool = mp.Pool()




    savingdatapath=statuscode()

    y=input('please enter the No. of workers(recommadation:4):')
    mail = input('mail it?(1 or 0):')

    if mail ==1:
        mail_password=input('please enter mail password:')
    else:
        pass

    savingdatapath_dict=savingdatapath+'/file'
    target_file= savingdatapath+'/'+'target.csv'
    #target_file=input('please input the target_file path:')
    #collected_file=savingdatapath+'/'+'collected.csv'
    pngfilekickstarterurl = optimalforcollected(savingdatapath_dict,target_file)
    #pngfilekickstarterurl = optimalforcollected(collected_file,target_file)
    pngfilekicktraqurl={}
    for key in pngfilekickstarterurl:
        #change from kcikstarter url to kicktraqurl
        kicktraq_url=obtain_kicktraqurl(pngfilekickstarterurl[key])
        #group kicktraqurl
        pngfilekicktraqurl[key]=kicktraq_url
    #if want to save all picture , run following line code for saving
    global file1
    file1=list(pngfilekicktraqurl)

    #分割 

    headers=['Project_ID','url']
    partss=y*10
    #splitfile1=chunks(file1,partss)
    reset_or_initial_ip_address(reset=False)

    print ' image download process begin'
    '''
    because the time of collection for each 50 images  will speed less 0.005s
    and the store process will spend a lot of time if i follow the previous design,
    the store action and collection action will conflict each other.
    furthermore i have tried to use threadlock for handling this conflict,
    but i find each access the global variable will interrupt every thread,
    that will ruin and spend more CPU resouce on switching start and stop status
    thus i choose to split into several small part to handle and save, with loop function to continues
    '''
    for j in xrange(y):
        t = ThreadClass(queue)
        t.setDaemon(True)
        t.start()

    #for splita in splitfile1.values():
    #    f1 = time.time()
    #    partpngfilekicktraqurl={}
    #    for ids in splita:
    #        partpngfilekicktraqurl[ids]=pngfilekicktraqurl[ids]

    lpngfilekicktraqurl=list(pngfilekicktraqurl)
    lpngfilekicktraqurl_split = chunks(lpngfilekicktraqurl,y*20)
    for packet in lpngfilekicktraqurl_split:
        reset_or_initial_ip_address(reset=True)
        time.sleep(1)
        temp_a={}
        for key in packet:
            a[key]=pngfilekicktraqurl[key]
        #results=pool.map(savingallimageforeachproject,packet)
        main(a,y)



        #if counts % 10 !=0:
    #time.sleep(random.uniform(1,3))
        #else:
         #   time.sleep(5)


    #creat a intermediary folder
    print 'download pic process completed'



    #dailypledges_png = 'dailypledges.png'
    #dailybackers_png='dailybackers.png'
    #dailycomments_png='dailycomments.png'
    #type_png=['dailypledges.png','dailybackers.png','dailycomments.png']



    if mail ==1:
        target=savingdatapath_dict
        now =  datetime.datetime.today()
        pathfile=savingdatapath+ '/%s.zip' % now
        print 'compress process completed'
        zipafilefordelivery(pathfile,target)

        print 'begin sending email'
        mail_username='linlu19920815@gmail.com'

        to_addrs="snowfreedom0815@gmail.com"
        attachmentFilePaths=pathfile
        sendmailtodelivery(mail_username,mail_password,to_addrs,attachmentFilePaths)
        print 'email sent'
    else:
        pass

    print "woolaa,woolaa, my job is done. my bed! I'm coming zZZ "
