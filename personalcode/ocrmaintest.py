# coding:utf8

#from PIL import Image
import pytesseract,os,gc
from PIL import Image, ImageStat
import StringIO, cStringIO
#import tweepy
import time
import datetime
import pandas as pd
import requests
import requests_cache
from function import *
import numpy as np
#from matplotlib import pyplot as plt


if __name__ == '__main__':  
    gc.enable()
    image_file='dailypledges-5.png'
    image=Image.open(image_file).convert("RGBA")
    path='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict'
    #characters_dict=loading_characters_dictionary(path)
    #change the color
    image,axis=dailypledges_chart_bottom_confirm(image)
    #image.show()

    roll = image.transpose(Image.ROTATE_270)
    roll_axis = axis.transpose(Image.ROTATE_270)
    print roll_axis.size[0],roll_axis.size[1]
    dailydata=forsilceandsearchrowsandcolums(roll,roll_axis)
    characteristiclibs=read_characteristic_lib(path+'/characteristic.txt')
    #dailydata[0].show()
    liss={}
    for day in list(dailydata):
        day_char=splitcolumtocharacter(dailydata[day])
        pre_process=characteristicfunction(day_char[0])
        if pre_process['the_number_of_rows']>=10 and pre_process['the_number_of_columns'] >= 7:
            day_char[0]=day_char[0].transpose(Image.ROTATE_90)
        else:
            day_text=''
            for chars in day_char:
                char_d = characteristicfunction(chars)
                char=recogonize_char(char_d,characteristiclibs)
                day_text=day_text+char
        liss[day]=day_text
             # 2 4 5 6 7 0 euro pound KR
        #enter char recogonize
    ##recognize_process

    #print days
    #days[0].show()
    #print days[0].size[0],days[0].size[1]
