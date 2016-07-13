from urllib2 import Request, urlopen, URLError
import time
import urllib2
import requests
from lxml import etree
import re,os,gc,os
import pandas as pd
import unicodecsv
import csv
import multiprocessing as mp
import datetime
import time
import threading
import Queue

#from PIL import Image
import pytesseract
from PIL import Image

def read_a_file(file):
    with open(file,'r') as f:
        f_collected=f.readlines()
    return f_collected
def write_a_file(file,item):
    with open(file,'w') as f:
        lenitem=len(item)
        for i in xrange(0,lenitem):
            f.write(item[i])

def webscraper_png(img_url):
    #root_url = 'https://www.kickstarter.com'
    try:
          img = urllib2.urlopen(img_url).read()
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason

        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code

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
            kicktraq_url = 'http://www.kicktraq.com'+kickstarterurl_drophttp
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
def optimalforcollected(collected_file,target_file):
    collected_dict={}
    target_dict={}
    search_dict={}
    collected = readacsv(collected_file)
    target=readacsv(target_file)
    target_ID=target['Project_ID']
    collected_ID=collected['Project_ID']
    #print type(target_ID)
    lentargetProject_ID=len(target_ID)
    lencollectedProject_ID=len(collected_ID)
    for i in xrange(0,lencollectedProject_ID):
        collected_dict[collected['Project_ID'][i]]=collected['url'][i]
    for i in xrange(0,lentargetProject_ID):
        target_dict[target['Project_ID'][i]]=target['url'][i]
    a=list(target_dict)
    b=list(collected_dict)
    print len(b),len(a),a[1]
    c=list(set(a)-set(b))
    print len(c),type(c),c[1]
    for key in c:
        search_dict[key]=target_dict[key]
    return search_dict

def writeacsvprocess(file,headers,item):
    with open(file,'r+') as project_data:
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

def savingallimageforeachproject(key):
    global collected_file
    global savingdatapath
    global pngfilekicktraqurl
    global pngfilekickstarterurl
    type_png=['dailypledges.png','dailybackers.png','dailycomments.png']
    headers=['Project_ID','url']
    global totalitem_kicktraqurl
    global counts

    if key !='':
        item_kicktraqurl={}
        for i in type_png:
            locals()['kickstraq%s'%i]=generateimageurl(pngfilekicktraqurl[key],i)
            if locals()['kickstraq%s'%i] !='Error':
                img_daily=webscraper_png(locals()['kickstraq%s'%i])
                savingimage(img_daily,savingdatapath,key,i)
        item_kicktraqurl['Project_ID']=key
        item_kicktraqurl['url']=pngfilekickstarterurl[key]
        totalitem_kicktraqurl.append(item_kicktraqurl)
        if len(totalitem_kicktraqurl)>50:
            writeacsvprocess(collected_file,headers,totalitem_kicktraqurl)
            totalitem_kicktraqurl=[]
            gc.collect()
        f2 = time.time()
        w=(len(file)-counts)*(f2-f1)
        sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects and remaining time: %.4f mins" % (counts,f2-f1,w))
        #sys.stdout.write("\rthis spider has already read %d projects" % (counts))
        sys.stdout.flush()


    writeacsvprocess(collected_file,headers,totalitem_kicktraqurl)

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




gc.enable()
totalitem_kicktraqurl=[]

target_file='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/target/target.csv'
collected_file='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/target/collected.csv'
savingdatapath='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/data'
pngfilekickstarterurl = optimalforcollected(collected_file,target_file)

queue = Queue.Queue()
class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            (target) = self.queue.get()
            savingallimageforeachproject(target)

            #time.sleep(1/10)
            self.queue.task_done()

def main(pngfilekicktraqurl,y):

    for j in xrange(y):
        t = ThreadClass(queue)
        t.setDaemon(True)
        t.start()
    lpngfilekicktraqurl=list(pngfilekicktraqurl)
    for key in lpngfilekicktraqurl:
        queue.put(key)
    queue.join()

#someurl='https://www.kickstarter.com/projects/822494155/the-marshall-project-reports-on-life-inside?ref=category_newest'
pngfilekicktraqurl={}
y=4
for key in pngfilekickstarterurl:
    #change from kcikstarter url to kicktraqurl
    kicktraq_url=obtain_kicktraqurl(pngfilekickstarterurl[key])
    #group kicktraqurl
    pngfilekicktraqurl[key]=kicktraq_url
#if want to save all picture , run following line code for saving
main(pngfilekicktraqurl,y)
#creat a intermediary folder
dailypledges_png = 'dailypledges.png'
dailybackers_png='dailybackers.png'
dailycomments_png='dailycomments.png'
type_png=['dailypledges.png','dailybackers.png','dailycomments.png']




#target=  publicpath +'/project_data.csv'
#now =  datetime.datetime.today()
#pathfile=publicpath+ '/%s.zip' % now
#print 'compress process completed'
#zipafilefordelivery(pathfile,target)

#print 'begin sending email'
#mail_username='linlu19920815@gmail.com'
#mail_password='19920815'
#to_addrs="snowfreedom0815@gmail.com"
#attachmentFilePaths=pathfile
#sendmailtodelivery(mail_username,mail_password,to_addrs,attachmentFilePaths)
#print 'email sent'

gc.collect()





#print type(img_dailypledges)

#print type(im)
#print im
