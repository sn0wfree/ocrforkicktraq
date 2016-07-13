#from PIL import Image
import pytesseract,os
from PIL import Image
import StringIO
import tweepy
import time
import datetime
import pandas as pd
from urllib2 import Request, urlopen, URLError
import urllib2
import requests
import requests_cache
from lxml import etree
#import cv2
import numpy as np
from matplotlib import pyplot as plt


def image_to_string(img, cleanup=True, plus=''):

    os.popen('tesseract ' + img + ' ' + img + ' ' + plus)
    with open(img + '.txt','r') as txt:
        text=txt.read()
    if cleanup:
        os.remove(img + '.txt')
    return text



#lable_middle.show()

#lable_middle_1.show()

#imgBuf = StringIO.StringIO(r.read())





def dailypledges_lable_cofirm(image):
    lable_bottom_box=(57,213,72,225)
    lable_bottom=image.crop(lable_bottom_box)
    pixel=lable_bottom.load()
    target_pixel=(128,138,156,136,133,155,180,165,160)
    for y in xrange(lable_bottom.size[1]):
        for x in xrange(lable_bottom.size[0]):
            if pixel[x,y][0] in target_pixel :
                if pixel[x,y][0] ==180 and pixel[x+1,y][0] ==165 and pixel[x,y+1][0] ==160:
                    pixel[x,y]=(255,255,255,255)
                else:
                    pixel[x,y]=(0,0,0,255)
            else:
                pixel[x,y]=(255,255,255,255)
    #lable_bottom_resized=lable_bottom.resize((1000,1000))
    return lable_bottom

def chart_confirm(chartimage,type):
    target_pixel=(0,114,104,99,105,109,113,112,108,103,106)
    aaaa=(0,128,160,165,166,161,134,138,180,152)
    pixel=chartimage.load()
    for y in xrange(chartimage.size[1]):
        for x in xrange(chartimage.size[0]):
            if type=='day':
                if pixel[x,y][2] in aaaa:
                    pixel[x,y]=(0,0,0,255)
                else:
                    pixel[x,y]=(255,255,255,255)
            elif type=='mainchart':
                if pixel[x,y][2] in target_pixel:
                    pixel[x,y]=(0,0,0,255)
                else:
                    pixel[x,y]=(255,255,255,255)
    return chartimage
def dailypledges_chart_bottom_confirm(image):
    mainchart_day_box=(78,223,920,236)
    mainchart_without_day_box=(78,40,920,218)

    mianchart_day = image.crop(mainchart_day_box)
    mainchart_without_day=image.crop(mainchart_without_day_box)

    #mianchart_day_b=chart_confirm(mianchart_day,'day')
    mainchart_without_day_b=chart_confirm(mainchart_without_day,'mainchart')
    return mainchart_without_day_b




if __name__ == '__main__':
    image_file = 'dailypledges 2.png'
    image = Image.open(image_file).convert("RGBA")
    #lable_box=(45,33,72,225)

    #lable_middle_box=(57,124,72,135)
    #lable_middle=im.crop(lable_middle_box)
    lable_bottom_png=dailypledges_lable_cofirm(image)
    #print type(lable_bottom_png)
    lable_bottom=lable_bottom_png
    #lable_bottom.show()
    #lable_bottom.save('/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict/$0.tif')

    lable_bottom.save("temp.tif")

    temp=Image.open("temp.tif").convert("RGBA")

    os.remove("temp.tif")
    dictforimage={}

    tif0=Image.open('/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict/lable$0.tif').convert("RGBA")
    #print type(tif0)
    if temp== tif0:
        print 'coordinate axis is at bottom'
        mainchart=dailypledges_chart_confirm(image)
        #oo=cropaimagefromimage(mainchart,(62,171,72,178))
        #oo.save('/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict/chart$0.tif')
        def compaereimageprocess(image,dictforimage):
            pixel=iamge.load()
            pixelfordict=dictforimage.load()
            count=0
            uncounts=0
            print len(dictforimage.size[1])

            scale=len(dictforimage.size[1])*len(dictforimage.size[0])
            for x in xrange(image.size[0]):
                if pixel[x,171]==pixelfordict[0,0] and uncounts == 0:
                    for i in xrange(dictforimage.size[1]):
                        for j in xrange(dictforimage.size[0]):
                            if pixel[x+j,171+i] == pixelfordict[j,i]:
                                counts+=1
                            else:
                                uncounts+=1
                                break
                    if counts==scale and uncounts==1:
                        print 'have one'






            #for y in xrange(iamge.size[1]):
            #
    else:
        print 'coordinate axis is at middle'








#print image_to_string("hz.font.exp0.tif")
