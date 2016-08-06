from urllib2 import Request, urlopen, URLError
import time
import urllib2
import requests
from lxml import etree
import os,gc,sys
import pandas as pd
import unicodecsv
import csv,unicodecsv
import multiprocessing as mp
import datetime
import time
import threading
import Queue
#import celery
from PIL import Image

#from downloadimage import *


def Onlynum(s,oth=''):
    statuscodefornum=0

    #s2 = s.lower();
    fomart = '0123456789.'
    for c in s:
        if not c in fomart:
            statuscodefornum = 1
            break
        else:
            pass
    return statuscodefornum

def scanfolderprocess(rdir):
    fo=os.walk(rdir)
    f=[]
    for root,subfolder,files in fo:
        #print root
        num=root.lstrip(rdir)
        #print num,type(num)
        statuscodefornum=Onlynum(num)
        if statuscodefornum == 0 and num !='':
            #print num
            number=float(num)
            f.append(number)
        else:
            print num
            pass
    return f


def multi_scanfolderprocess(a):
    pool=mp.Pool()
    f_a=pool.map(scanfolderprocess,(a,))
    #print f_a
    if len(f_a)==1:
        f=f_a[0]
    elif len(f_a)!=1:
        f=f_a
    pool.close()
    return f


def writeacsvprocess(file,headers,item):
    with open(file,'r') as project_data:
        project_data_read_csv = unicodecsv.reader(project_data,headers)
        if not headers in project_data_read_csv:
            status=0
        else:
            status=1
        #print status
    with open(file,'a') as project_data:
        project_data_csv = unicodecsv.DictWriter(project_data,headers)
        if status ==0:
            project_data_csv.writeheader()
        project_data_csv.writerows(item)
        #project_data.write('\n')
def readacsv(file):
    with open(file,'rw') as f:
        w=pd.read_csv(file,skip_footer=1,engine='python')
    return w


def ss(i):
    y=i*i
    b=os.getpid()
    return y,b


if __name__=='__main__':
    #a=[{0: 'dot', 1: 'dot', 2: 'dot', 3: 'dot', 4: 'dot', 5: 'dot', 6: 'dot', 7: 'dot', 8: 'dot', 9: 'dot', 10: 'dot', 11: 'dot', 12: 'dot', 13: 'dot', 14: 'dot', 15: 'dot', 16: 'dot', 17: 'dot', 18: 'dot', 19: 'dot', 20: 'dot', 21: 'dot', 22: 'dot', 23: 'dot', 'Project_ID': 1011352051.0}, {0: 'dot', 1: 'dot', 2: 'dot', 3: 'dot', 4: 'dot', 5: 'dot', 6: 'dot', 7: 'dot', 8: 'dot', 9: 'dot', 10: 'dot', 11: 'dot', 12: 'dot', 13: 'dot', 14: 'dot', 15: 'dot', 16: 'dot', 17: 'dot', 18: 'dot', 19: 'dot', 20: 'dot', 21: 'dot', 22: 'dot', 23: 'dot', 24: 'dot', 25: 'dot', 26: 'dot', 'Project_ID': 1012665249.0, 28: 'dot', 27: 'dot'}, {0: '1', 1: '0', 2: '0', 3: '1', 4: '0', 5: '1', 6: '0', 7: '0', 8: '0', 9: '0', 10: '0', 11: '0', 12: '0', 13: '0', 14: '0', 15: '0', 16: '0', 17: '0', 18: '0', 19: '0', 20: '0', 'Project_ID': 1012924504.0}, {0: '29', 1: '28', 2: '11', 3: '9', 4: '23', 5: '10', 6: '11', 7: '6', 8: '11', 9: '8', 10: '7', 11: '12', 12: '7', 13: '12', 14: '15', 15: '10', 16: '5', 17: '8', 18: '15', 19: '7', 20: '3', 21: '3', 22: '16', 23: '14', 24: '12', 25: '2', 26: '2', 'Project_ID': 1015375165.0, 28: '17', 29: '9', 30: '14', 31: '14', 27: '1'}, {0: '3', 1: '2', 2: '0', 3: '0', 4: '0', 5: '1', 6: '0', 7: '0', 8: '0', 9: '0', 10: '0', 11: '0', 12: '0', 13: '0', 14: '1', 15: '0', 16: '0', 17: '0', 18: '0', 19: '0', 20: '0', 21: '0', 22: '0', 23: '0', 24: '0', 25: '0', 26: '0', 'Project_ID': 1016595269.0, 28: '0', 29: '0', 30: '0', 31: '0', 32: '0', 33: '0', 34: '0', 27: '0', 36: '0', 37: '0', 38: '0', 39: '0', 40: '0', 41: '0', 35: '0'}, {0: '6', 1: '4', 2: '0', 3: '5', 4: '3', 5: '3', 6: '1', 7: '1', 8: '0', 9: '2', 10: '4', 11: '0', 12: '0', 13: '1', 14: '1', 15: '1', 16: '1', 17: '1', 18: '1', 19: '0', 20: '0', 21: '0', 22: '1', 23: '0', 24: '2', 25: '1', 26: '2', 'Project_ID': 1017118969.0, 28: '2', 29: '0', 30: '0', 27: '1'}, {0: '3', 1: '3', 2: '0', 3: '0', 4: '3', 5: '0', 6: '2', 7: '1', 8: '0', 9: '0', 10: '1', 11: '1', 12: '3', 13: '6', 14: '2', 15: '0', 16: '0', 17: '3', 18: '1', 19: '1', 20: '1', 21: '1', 22: '3', 23: '0', 24: '0', 25: '0', 26: '0', 'Project_ID': 101799307.0, 28: '4', 29: '2', 30: '0', 31: '0', 32: '0', 33: '1', 34: '0', 27: '1', 36: '1', 37: '1', 38: '2', 39: '0', 35: '2'}, {0: '1', 1: '1', 2: '0', 3: '0', 4: '0', 5: '0', 6: '0', 7: '0', 8: '0', 9: '0', 10: '0', 11: '0', 12: '0', 'Project_ID': 1019217557.0}, {0: 'dot', 1: 'dot', 2: 'dot', 3: 'dot', 4: 'dot', 5: 'dot', 6: 'dot', 7: 'dot', 8: 'dot', 9: 'dot', 10: 'dot', 11: 'dot', 12: 'dot', 13: 'dot', 14: 'dot', 15: 'dot', 16: 'dot', 17: 'dot', 18: 'dot', 19: 'dot', 20: 'dot', 21: 'dot', 22: 'dot', 23: 'dot', 24: 'dot', 25: 'dot', 26: 'dot', 'Project_ID': 1019741337.0, 28: 'dot', 29: 'dot', 30: 'dot', 27: 'dot'}, {0: '0', 1: '1', 2: '1', 3: '0', 4: '0', 5: '0', 6: '2', 7: '0', 8: '1', 9: '1', 10: '0', 11: '0', 12: '0', 13: '0', 14: '7', 15: '2', 16: '0', 17: '0', 18: '0', 19: '0', 20: '0', 21: '1', 22: '0', 23: '0', 24: '0', 25: '0', 26: '0', 'Project_ID': 1022100836.0, 28: '0', 29: '0', 30: '0', 31: '0', 32: '0', 33: '0', 34: '0', 27: '0', 36: '0', 37: '0', 38: '1', 39: '2', 40: '0', 41: '0', 42: '2', 43: '0', 44: '0', 45: '2', 46: '1', 47: '0', 48: '0', 49: '0', 50: '0', 51: '0', 52: '0', 53: '2', 54: '0', 55: '0', 56: '0', 57: '1', 58: '1', 59: '0', 60: '0', 35: '0'}]
    #test=input('test')
    pool = mp.Pool()
    results = pool.map(ss,xrange(10))
    for result in results:
        (y,b)=result
        print '%s result : %s'%(b,y)



'''
    b=[]

    a='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image/error.csv'
    #print a
    f=readacsv(a)
    headers=['Project_ID','status']
    f_project_id=f['Project_ID'].tolist()
    f_status=f['status'].tolist()

    for i in xrange(len(f_project_id)):
        dic={}
        dic['Project_ID']=f_project_id[i]
        dic['status']=f_status[i]
        b.append(dic)

    print b

    writeacsvprocess(a,headers,b)



    headers=['Project_ID','status']
'''


    #for i in xrange(lenlistsqsum_row):
    #    if listsum_row[i] !=0:
    #        sumrow1.append(listsum_row[i])
    #print sumrow1
    #sumrow2.append[listsum_row_s for listsum_row_s in listsum_row [if listsum_row_s !=0]]
    #print sumrow2


'''
    def run(x,y):
        ff1=time.time()
        if x ==1:

            for i in xrange(0,y):
                pool=mp.Pool()
                f_a=pool.map(scanfolderprocess,(a,))

                if len(f_a)==1:
                    f=f_a[0]
                elif len(f_a)!=1:
                    f=f_a
                pool.close()
                #pool.join()
        else:
            for i in xrange(0,y):
                f=scanfolderprocess(a)
        #print f[0]

        return (time.time()-ff1)/y
    for x in xrange(2):
        if x==1:
            print 'multiprocessing_time: %s'%run(x,y)
        else:
            print 'normal_time: %s'%run(x,y)
'''
