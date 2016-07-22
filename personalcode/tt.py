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


def readacsv(file):
    with open(file,'r+') as f:
        w=pd.read_csv(file,skip_footer=1,engine='python')
    return w

def writeacsvprocess(file,headers,item):
    with open(file,'r') as project_data:
        project_data_read_csv = unicodecsv.reader(project_data,headers)
        if not headers in project_data_read_csv:
            status=0
        else:
            status=1
    with open(file,'a+') as project_data:
        project_data_csv = unicodecsv.DictWriter(project_data,headers)
        if status ==0:
            project_data_csv.writeheader()
        project_data_csv.writerows(item)


def csvr(file):
    aaaaa={}
    with open(file,'r') as project_data:
        project_data_read_csv = unicodecsv.DictReader(project_data)
        for row in project_data_read_csv:
            aaaaa[row['Project_ID']]=row['url']
    return aaaaa


aaa='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image/collected.csv'
headers=['Project_ID','url']
a_rac=readacsv(aaa)
a_csvr=csvr(aaa)
project_id=a_rac['Project_ID']

print a_rac['url'][1],a_rac['Project_ID'][1]
print a_csvr[project_id[0]]
