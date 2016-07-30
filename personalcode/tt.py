from urllib2 import Request, urlopen, URLError
import time
import urllib2
import requests
from lxml import etree
import os,gc,sys
import pandas as pd
import unicodecsv
import csv
import multiprocessing as mp
import datetime
import time
import threading
import Queue
#import celery
from PIL import Image

#from downloadimage import *


def scanfolderprocess(a):
    #(a,b)=c
    fo=os.walk(a)
    f=[]
    for root,subfolder,files in fo:
        #print subfolder
        num=root.lstrip(a)
        #print num,type(num)
        if num !='' and num!= '.vol':
            number=float(num)
            f.append(number)
        else:
            pass

    return f



def cropdailybar(dicts,dicts_axis,image):
    a=sorted(list(dicts))
    
    daylabel={}
    for i in xrange(len(dayslabel)):
        daylabel[dayslabel[i]]=i
    #print a


    counts=0
    line={}
    count=0
    for i in xrange(0,len(a)):
        if i <(lena-1):
            if  (a[i+1]-a[i])<=4:
                count+=1
            else:
                line[counts]=(a[i]-count,a[i])
                #gap.append(a[i+1]-a[i])
                count=0
                counts+=1
        else:
            if i==(lena-1):
                line[counts]=(a[i]-count,a[i])

    loca=(a[0],0)
    lena=len(a)
    for i in xrange(0,lena):
        if i <(lena-1):
            if  (a[i+1]-a[i])<2:
                if loca[1]<=a[i+1]:
                    loca=(loca[0],a[i+1])
                elif loca[1]>a[i+1]:
                    raise Exception('image daily split process err')
            elif (a[i+1]-a[i])>=2:
                if loca[1]==a[i]:
                    line.append(loca)
                    loca=(a[i+1],a[i+2])
                elif loca[1]<a[i]:
                    raise Exception('image daily split process err')
                elif loca[1]>a[i]:
                    raise Exception('image daily split process err')
        elif i ==(lena-1):
            loca=(loca[0],a[i])
            line.append(loca)
                #return a dict
    dailyimage={}
    #print line
    listline=list(line)
    #print line[0]
    #(a,w)=line[0]
    #boxa=(0,a-1,image.size[0],w+2)
    #ss=image.crop(boxa)
    #ss.show()

    for i in listline:
        (y1,y2)=line[i]
        average=(y1+y2)/2
        for row in list(daylabel):
            if row in xrange(average-2,average+2):
                loacted_day=daylabel[row]
                del daylabel[row]
                break
        box=(0,y1-1,image.size[0],y2+2)
        locals()['data%s'%i]=image.crop(box)

        dailyimage[loacted_day]=locals()['data%s'%i]
    #dailyimage[0].show()
    return dailyimage


if __name__=='__main__':
    test=input('test')
    ff1=time.time()


    b=0
    a='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image/file'
    #print a
    for i in xrange(0,250):
        c=(a,b)
        if test ==1:
            pool=mp.Pool()
            f_a=pool.map(scanfolderprocess,(a,))
            if len(f_a)==1:
                f=f_a[0]
            elif len(f_a)!=1:
                f=f_a
            pool.close()
            #pool.join()
        else:
            f=scanfolderprocess(a)
    #print f[0]

    print time.time()-ff1
