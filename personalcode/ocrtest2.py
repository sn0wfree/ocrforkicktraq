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

import pytesseract,os,gc
from PIL import Image, ImageStat
import StringIO, cStringIO
import tweepy
import requests
import requests_cache
#import cv2
import numpy as np
'''
9:4:5:[1.0, 3.0, 3.0, 3.0]:[2.0, 2.0, 3.0, 1.0, 2.0]
8:4:5:[2.0, 3.0, 3.0, 2.0]:[2.0, 2.0, 2.0, 2.0, 2.0]
2:4:5:[3.0, 3.0, 3.0, 2.0]:[3.0, 1.0, 2.0, 1.0, 4.0]
3:4:5:[2.0, 3.0, 3.0, 2.0]:[3.0, 1.0, 2.0, 1.0, 3.0]
4:4:5:[3.0, 1.0, 1.0, 5.0]:[2.0, 2.0, 4.0, 1.0, 1.0]
5:4:5:[4.0, 3.0, 3.0, 2.0]:[4.0, 1.0, 3.0, 1.0, 3.0]
6:4:5:[3.0, 3.0, 3.0, 1.0]:[2.0, 1.0, 3.0, 2.0, 2.0]
7:4:5:[1.0, 3.0, 2.0, 2.0]:[4.0, 1.0, 1.0, 1.0, 1.0]
0:4:5:[3.0, 2.0, 2.0, 3.0]:[2.0, 2.0, 2.0, 2.0, 2.0]
K:4:5:[5.0, 1.0, 2.0, 2.0]:[2.0, 2.0, 2.0, 2.0, 2.0]
R:4:5:[5.0, 2.0, 2.0, 3.0]:[3.0, 2.0, 3.0, 2.0, 2.0]
eurodollarsymbol:4:5:[3.0, 3.0, 3.0, 2.0]:[3.0, 1.0, 3.0, 1.0, 3.0]
poundsymbol:4:5:[2.0, 4.0, 3.0, 3.0]:[2.0, 1.0, 4.0, 1.0, 4.0]
1:2:5:[1.0, 5.0]:[2.0, 1.0, 1.0, 1.0, 1.0]
minus:3:1:[1.0, 1.0, 1.0]:[3.0]
dollarsymbol:5:7:[2.0, 3.0, 7.0, 3.0, 2.0]:[1.0, 4.0, 2.0, 3.0, 2.0, 4.0, 1.0]
comma:2:2:[1.0, 1.0]:[1.0, 1.0]

'''




def dailypledges_lable_confirm(image):
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

def chart_confirm(chartimage,type,linewidth='default'):
    if linewidth =='default':
        #target_pixel=(0,114,104,99,100,105,109,113,112,111,108,103,106)
        d=range(98,115)
        d.append(0)
        target_pixel=tuple(d)
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
    #else:
        #print 'entering to calculating linewidth model'
    return chartimage

def dailypledges_chart_bottom_confirm(image):
    mainchart_coordinate_axis_box=(78,221,920,222)
    mainchart_without_day_box=(78,40,920,218)
    mainchart_coordinate_axis = image.crop(mainchart_coordinate_axis_box)
    #mainchart_coordinate_axis.show()
    mainchart_without_day=image.crop(mainchart_without_day_box)
    #mainchart_without_day.show()
    #mianchart_day_b=chart_confirm(mianchart_day,'day')
    mainchart_coordinate_axis_b=chart_confirm(mainchart_coordinate_axis,'mainchart')
    mainchart_without_day_b=chart_confirm(mainchart_without_day,'mainchart')
    return mainchart_without_day_b,mainchart_coordinate_axis_b

def rollazero(image,box):
    (x1,y1,x2,y2)=box
    rebox=((x1+x2)/2-(y2-y1)/2,y2-(x2-x1),(x1+x2)/2-(y2-y1)/2+(y2-y1),y2)
    #print box,rebox
    region = image.crop(box)
    blank = image.crop(rebox)
    pix=blank.load()
    for y in xrange(blank.size[1]):
        for x in xrange(blank.size[0]):
            pix[x,y]=(255,255,255,255)
    #blank.show()
    region = region.transpose(Image.ROTATE_90)
    blank=blank.transpose(Image.ROTATE_90)
    #print blank.size[1],blank.size[0]#croped
    #print region.size[1],region.size[0]#changed
    if blank.size[1]==region.size[0]:
        #print 1
        image.paste(blank,box)
        image.paste(region,rebox)
    else:
        pass
        #print 0
    return image

def rollallzero(image,dictforimage):
    pixel=image.load()
    pixelfordict=dictforimage.load()
    counts=0
    uncounts=0
    #print dictforimage.size[0]
    #print range(dictforimage.size[1])
    scale=ImageStat.Stat(dictforimage).count[2]
    #print scale
    aa=(0,171,842,178)
    #a=image.crop(aa).show()
    for x in xrange(image.size[0]):
        if pixel[x,171]==pixelfordict[2,0] and x+10<image.size[0]:
            uncounts=0
            counts=0
            for i in xrange(dictforimage.size[1]):
                for j in xrange(dictforimage.size[0]):
                    if pixel[x-2+j,171+i] == pixelfordict[j,i]:
                        counts+=1
                    else:
                        uncounts+=1
                        break
        if counts >=scale :
            #print x
            #print 'have one'
            box=(x-2,171,x+8,178)
            image=rollazero(image,box)
            counts=0
    #image = image.transpose(Image.ROTATE_270)
    return image

def scanrown(image):
    dicts={}
    pixels=image.load()
    for i in xrange(image.size[1]):
        sumpix=0
        for j in xrange(image.size[0]):
            if pixels[j,i][0]==0:
                sumpix+=1
            else:
                pass
        if sumpix >1:
            dicts[i]=sumpix
    return dicts

def scanaxis(image):
    dicts={}
    pixels=image.load()
    for i in xrange(image.size[1]):
        sumpix=0
        for j in xrange(image.size[0]):
            if pixels[j,i][0]==0:
                sumpix+=1
            else:
                pass
        if sumpix >=1:
            dicts[i]=sumpix
    return dicts

def forsilceandsearchrowsandcolums(image,image_axis):
    dicts=scanrown(image)
    dicts_axis=scanaxis(image_axis)
    #print dicts_axis

    dailyimage=cropdailybar(dicts,dicts_axis,image)
    #dailyimage[0].show()
    pledged_dailyimage={}
    listdailyimage=list(dailyimage)
    lenlistdailyimage=len(listdailyimage)

    return dailyimage

def splitcolumtocharacter(dailydata5):
    #sellect line which have characters
    character={}
    pixels=dailydata5.load()
    for j in xrange(dailydata5.size[0]):
        sumpix=0
        for i in xrange(dailydata5.size[1]):
            if pixels[j,i][0]==0:
                sumpix+=1
            else:
                pass
        if sumpix >=1:
            character[j]=sumpix
    #extract each whole char line
    a=sorted(list(character))
    lena=len(a)
    counts=0
    line={}
    count=0
    for i in xrange(0,lena):
        if i <(lena-1):
            if  (a[i+1]-a[i])<2:
                count+=1
            else:
                line[counts]=(a[i]-count,a[i])
                count=0
                counts+=1
        else:
            line[counts]=(a[i]-count,a[i])
                #return a dict
    characters={}
    #print line
    listline=list(line)
    for i in listline:
        #i is the number of day
        (x1,x2)=line[i]
        box=(x1,0,x2+1,dailydata5.size[1])
        locals()['day%s'%i]=dailydata5.crop(box)
        characters[i]=locals()['day%s'%i]
    return characters




def charactersearchprocessforchart(image,characters_dict, opt=True,types='pledge'):
    dd='cannot recognize'
    #opt dict
    if opt == True :
        if types =='pledge':
            keys={}
            del characters_dict['pledgelabledollarsymbol0']
            del characters_dict['pledgechartdollarsymbol0']
            characters_dict_keys=characters_dict.keys()
            for key in characters_dict_keys:
                key_drop=key.split('chart')[1]
                if key_drop =='dollarsymbol':
                    keys['$']=characters_dict[key]
                elif key_drop =='0':
                    keys['0']=characters_dict[key]
                elif key_drop =='1':
                    keys['1']=characters_dict[key]
                elif key_drop =='2':
                    keys['2']=characters_dict[key]
                elif key_drop =='3':
                    keys['3']=characters_dict[key]
                elif key_drop =='4':
                    keys['4']=characters_dict[key]
                elif key_drop =='5':
                    keys['5']=characters_dict[key]
                elif key_drop =='6':
                    keys['6']=characters_dict[key]
                elif key_drop =='7':
                    keys['7']=characters_dict[key]
                elif key_drop =='8':
                    keys['8']=characters_dict[key]
                elif key_drop =='9':
                    keys['9']=characters_dict[key]
                elif key_drop ==',':
                    keys[',']=characters_dict[key]
        characters_dict=keys

    characters_dict_value=characters_dict.values()
    characters_dict_value[5].show()
    #print image
    #print characters_dict['pledgechartdollarsymbol']
    for value in characters_dict_value:
        value.save("temp.tif")
        temp=Image.open("temp.tif").convert("RGBA")
        os.remove("temp.tif")
        if image == temp:
            #print value
            dd=characters_dict.keys()[characters_dict.values().index(value)]
            break
    return dd

def read_whole_line_test(days):
    for i in xrange(sorted(list(days))):
        readline=''
        if charactersearchprocessforchart(days[i],characters_dict)!='cannot recognize':
            locals()['%sth_letter'%i]=charactersearchprocessforchart(days[i],characters_dict)
            readline+=locals()['%sth_letter'%i]
        else:
            readline+='meet Error'
    return realine


def read_characteristic_lib_csv(characteristiclibs_file_csv):
    characteristiclibs_csv=readacsv(characteristiclibs_file_csv)
    pd.options.mode.chained_assignment = None
    for i in xrange(len(characteristiclibs_csv['the_number_of_pixel_in_each_column'])):
        temp_a=characteristiclibs_csv['the_number_of_pixel_in_each_column'][i]
        a=[float(st) for st in temp_a.split('-')]
        characteristiclibs_csv['the_number_of_pixel_in_each_column'][i]=tuple(a)
    for j in xrange(len(characteristiclibs_csv['the_number_of_pixel_in_each_row'])):
        temp_b=characteristiclibs_csv['the_number_of_pixel_in_each_row'][j]
        b=[float(st) for st in temp_b.split('-')]
        characteristiclibs_csv['the_number_of_pixel_in_each_row'][j]=tuple(b)
    #characteristiclibs_csv=characteristiclibs_csv.set_index('name')
    return characteristiclibs_csv


def read_characteristic_lib(file):

    characteristiclibs={}

    with open(file,'r') as f:
        libs=f.readlines()
        #print libs
        #libs=f_lib[0].split(';')
        for lib in libs:
            characteristicvalue={}
            the_number_of_pixel_in_each_column=[]
            the_number_of_pixel_in_each_row=[]
            if lib !='':
                items=lib.split(':')
                name=items[0]
                the_number_of_columns=items[1]
                the_number_of_rows=items[2]

                each_column=items[3].split(',')
                each_row=items[4].split(',')
                for columns in each_column:
                    if '[' in columns:
                        columns=columns.split('[')[1]
                    elif ']' in columns:
                        colums=columns.split(']')[0]
                    the_number_of_pixel_in_each_column.append(columns)
                for rows in each_row:
                    if '[' in rows:
                        rows=rows.split('[')[1]
                    elif ']' in rows:
                        rows=rows.split(']')[0]
                    the_number_of_pixel_in_each_row.append(rows)
            characteristicvalue['name']=name
            characteristicvalue['the_number_of_columns']=the_number_of_columns
            characteristicvalue['the_number_of_rows']=the_number_of_rows
            characteristicvalue['the_number_of_pixel_in_each_row']=the_number_of_pixel_in_each_row
            characteristicvalue['the_number_of_pixel_in_each_column']=the_number_of_pixel_in_each_column
            characteristiclibs[name]=characteristicvalue
    return characteristiclibs

def read_characteristic_libs(file):
    if os.path.splitext(file)[1]=='.txt':
        characteristiclibs=read_characteristic_lib(file)
    elif os.path.splitext(file)[1]=='.csv':
        characteristiclibs=read_characteristic_lib_csv(file)
    else:
        print 'please type correct file'
        raise Exception('please type correct file')
    return characteristiclibs

def pandalizationfortest(character_image):
    pix=character_image.load()

    data = np.zeros((character_image.size[1],character_image.size[0]))
    #data[0][1]=1
    for i in xrange(character_image.size[0]):
        for j in xrange(character_image.size[1]):

            data[j,i]=pix[i,j][0]-255
    dataset=pd.DataFrame(data)
    #print datas
    for i in dataset:
        for j in dataset.index:
            if dataset[i][j]<0 :
                dataset[i][j]=1
            else:
                dataset[i][j]=0
    return dataset

def sumacharacteristicforsingleroworcolumn(sum_row):
    listsum_row=list(sum_row)
    sumrow=[]
    lenlistsqsum_row=len(listsum_row)
    for i in xrange(lenlistsqsum_row):
        if listsum_row[i] !=0:
            sumrow.append(listsum_row[i])
        else:
            pass
    return sumrow

def characteristicfunction(character_image,setup=False,name='null',path='null'):
    characteristicvalue={}
    dataset=pandalizationfortest(character_image)

    #the number of column,
    the_number_of_columns=dataset.shape[1]
    the_number_of_rows=dataset.shape[0]
    #thenumber_of_row=dataset.shape[1]
    sum_row = dataset.sum(axis=1) #the characteristic for each row
    sum_column = dataset.sum(axis=0) #the characteristic for each column
    the_number_of_pixel_in_each_row=sumacharacteristicforsingleroworcolumn(sum_row)
    the_number_of_pixel_in_each_column=sumacharacteristicforsingleroworcolumn(sum_column)
    characteristicvalue['the_number_of_columns']=the_number_of_columns
    characteristicvalue['the_number_of_rows']=the_number_of_rows
    characteristicvalue['the_number_of_pixel_in_each_row']=tuple(the_number_of_pixel_in_each_row)
    characteristicvalue['the_number_of_pixel_in_each_column']=tuple(the_number_of_pixel_in_each_column)
    #characteristicvalue['dataset']=dataset
    if setup==True:
        if name=='null' and path=='null':
            name=input('please enter the name of characters:')
            path=input('please enter the fullpath of file which may store the characteristic value:')
        else:
            pass

        with open(path+'/characteristic.txt','a+') as f:
            the_number_of_rows=len(characteristicvalue['the_number_of_pixel_in_each_row'])
            #f.write('%s'%characteristicvalue)
            f.write(str(name) + ':')
            f.write(str(characteristicvalue['the_number_of_columns'])+':')
            f.write(str(the_number_of_rows)+':')
            f.write(str(characteristicvalue['the_number_of_pixel_in_each_column'])+':')
            f.write(str(characteristicvalue['the_number_of_pixel_in_each_row'])+'\n')
    return characteristicvalue



def cropfordailydata(roll,line):
    dailyimage={}
    for i in xrange(len(line)):
        (y1,y2)=line[i]
        box=(0,y1-1,roll.size[0],y2+2)
        locals()['data%s'%i]=roll.crop(box)

        dailyimage[i]=locals()['data%s'%i]
    #dailyimage[0].show()
    return dailyimage


def readacsv(file):
    with open(file,'r+') as f:
        w=pd.read_csv(file,skip_footer=1,engine='python')
    return w

def returnthercharacteristicsymbol(dailyimage11):
    lencolumn=len(dailyimage11['the_number_of_pixel_in_each_column'])
    lenrow=len(dailyimage11['the_number_of_pixel_in_each_row'])
    global characteristiclibs
    c2c= characteristiclibs[characteristiclibs.the_number_of_columns==lencolumn]
    c2c=c2c[c2c.the_number_of_rows==lenrow]
    c2c=c2c[c2c.the_number_of_pixel_in_each_column==dailyimage11['the_number_of_pixel_in_each_column']]
    c2c=c2c[c2c.the_number_of_pixel_in_each_row==dailyimage11['the_number_of_pixel_in_each_row']]
    #print c2c
    a=c2c.name.tolist()
    #print a
    if a ==[]:
        a=''
    else:
        a=a[0]
        #print a
    return a


def splitdailydataprocess(roll):
    dicts=scanrown(roll)
    a=sorted(list(dicts))
    line=[]
    loca=(a[0],0)
    lena=len(a)
    params=2
    for i in xrange(0,lena):
        if i <(lena-1):
            if  (a[i+1]-a[i])<=params:
                if loca[1]<=a[i+1]:
                    loca=(loca[0],a[i+1])
                elif loca[1]>a[i+1]:
                    raise Exception('image daily split process err')
            elif (a[i+1]-a[i])>params:
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
    return line

if __name__ == '__main__':
    gc.enable()
    ppppp='/Users/sn0wfree/Documents/python_projects/ocrforkicktraq/dict'
    localtxt=ppppp+'/characteristic.txt'
    localcsv=ppppp+'/characteristic.csv'
    global characteristiclibs
    characteristiclibs=read_characteristic_libs(localcsv)

    path_a='/Users/sn0wfree/Documents/python_projects/ocrforkicktraq'
    image_file=path_a+'/'+'dailypledges-6.png'
    image=Image.open(image_file).convert("RGBA")
    path=path_a+'/dict'
    image,axis=dailypledges_chart_bottom_confirm(image)

    roll = image.transpose(Image.ROTATE_270)

    line=splitdailydataprocess(roll)

    dailyimage=cropfordailydata(roll,line)
    #dailyimage[2].show()
    #dailyimage[3].show()
    def wholerecogniseprocess(dailyimage):
        dailyimage_word={}
        lenlist=list(dailyimage)
        for i in lenlist:
            word=''
            subdailyimage=splitcolumtocharacter(dailyimage[i])
            first_symbol=characteristicfunction(subdailyimage[0])

            first_symbol_v=returnthercharacteristicsymbol(first_symbol)
            #print first_symbol_v
            if first_symbol_v == '':
                dailyimage_rotate_temp=dailyimage[i].transpose(Image.ROTATE_90)
                subdailyimage_rotate_temp=splitcolumtocharacter(dailyimage_rotate_temp)
                subdailyimage=subdailyimage_rotate_temp
            else:
                pass
            #subdailyimage[0].show()

            lensublist=list(subdailyimage)

            for j in lensublist:
                symbol=''
                subdailyimage1=characteristicfunction(subdailyimage[j])
                symbol=returnthercharacteristicsymbol(subdailyimage1)
                #print symbol
                #print type(symbol),type(word)
                word+=symbol
            dailyimage_word[i]=word
        return dailyimage_word
    #dailyimage[1].show()
    dailyimage_word=wholerecogniseprocess(dailyimage)
    print dailyimage_word

    #dailyimage[2].show()

    #.values()







    #print characteristiclibs['1']
    #headers=['name','the_number_of_columns','the_number_of_rows','the_number_of_pixel_in_each_column','the_number_of_pixel_in_each_row']
    #each_column=characteristiclibs[headers[3]].tolist()
    #print each_column,characteristiclibs_csv


    #characteristiclibs_csv=transferfromcsvbalabalatoform(characteristiclibs_csv)

    #print dailyimage11






    #print characteristiclibs[characteristiclibs.the_number_of_column==dailyimage11['the_number_of_pixel_in_each_row']]
