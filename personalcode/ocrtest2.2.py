#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by Lin Lu 2016
#-----------------------------------------------------------------------------------------------
'''
this code is for my dissertation.

'''
#version control


__author__='sn0wfree'
__version__='2.0.8.1'
__specialversion__='for GPU'


# when i begin to write this codes, i truely understand what i have done
# but now i'm not
#-----------------------------------------------------------------------------------------------
###

import os,gc,sys
import pandas as pd
import unicodecsv
import csv
import multiprocessing as mp
import datetime
import time,random
import threading
import Queue
from PIL import Image, ImageStat
import numpy as np
import shutil
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

queue = Queue.Queue()

global characteristiclibs
global counts,collected,collected_file
global error_ID,error_file,error_file_collected
global path_a
global dailypledges_dict_list,dailypledges_target_file
global dailycomments_dict_list,dailycomments_target_file
global dailybackers_dict_list,dailybackers_target_file
global y,error_counts
global lenfile


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

def dailypledges_chart_confirm(chartimage,type,linewidth='default'):
    if linewidth =='default':
        #target_pixel=(0,114,104,99,100,105,109,113,112,111,108,103,106)
        d=range(97,115)
        d.append(0)
        target_pixel=tuple(d)
        aaaa=(0,20,128,160,165,166,161,134,138,180,152)
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
    mainchart_coordinate_axis_box=(78,221,920,223)
    mainchart_without_day_box=(78,40,920,218)
    mainchart_coordinate_axis = image.crop(mainchart_coordinate_axis_box)
    #mainchart_coordinate_axis.show()
    mainchart_without_day=image.crop(mainchart_without_day_box)
    #mainchart_without_day.show()
    #mianchart_day_b=chart_confirm(mianchart_day,'day')
    mainchart_coordinate_axis_b=dailypledges_chart_confirm(mainchart_coordinate_axis,'mainchart')
    mainchart_without_day_b=dailypledges_chart_confirm(mainchart_without_day,'mainchart')
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
    pre_pixel=0
    pre4_pixel=0
    for i in xrange(image.size[1]):
        sumpix=0
        for j in xrange(image.size[0]):
            if pixels[j,i][0]==0:
                sumpix+=1
            else:
                pass
        if sumpix >=1:
            pre4_pixel=0
            dicts[i]=sumpix
            pre_pixel=sumpix
        else:
            pass





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
    #sumrow.append[listsum_row_s for listsum_row_s in listsum_row[if listsum_row_s !=0]]
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



def cropfordailydata(roll,line, seri= True ):
    dailyimage={}
    for i in xrange(len(line)):
        (y1,y2)=line[i]
        #print y2-y1
        box=(0,y1-1,roll.size[0],y2+2)
        locals()['data%s'%i]=roll.crop(box)
        if seri == False:
            dailyimage[i]=locals()['data%s'%i]
        elif seri == True:
            #print y1
            dailyimage[(y1,y2)]=locals()['data%s'%i]

        #dailyimage[i]=locals()['data%s'%i]
    #dailyimage[0].show()
    return dailyimage


def readacsv(file):
    with open(file,'r') as f:
        w=pd.read_csv(file,skip_footer=1,engine='python')
    return w

def returnthercharacteristicsymbol(dailyimage11):
    lencolumn=len(dailyimage11['the_number_of_pixel_in_each_column'])
    lenrow=len(dailyimage11['the_number_of_pixel_in_each_row'])
    global characteristiclibs
    c2c= characteristiclibs[(characteristiclibs.the_number_of_columns==lencolumn)& (characteristiclibs.the_number_of_rows==lenrow)]
    #c2c=c2c[c2c.the_number_of_rows==lenrow]
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







def addadaylableintoseries(dailyimage_word,axis):
    a= dailyimage_word[0]
    #print dailyimage_word

    axis_roll=axis.transpose(Image.ROTATE_270)
    #axis_roll.show()

    axis_p = pandalizationfortest(axis_roll).reset_index()
    axis_p_l=axis_p[axis_p[0]==1].reset_index(drop=True)
    ax=axis_p_l.rename(columns={'index':'day_pixel_location'})
    axis_list=ax['day_pixel_location'].tolist()
    if axis_list==[]:
        raise Exception('axis cannot be regnoised')
    else:
        pass

    day=[]
    j=0
    #print ax
    for i in xrange(len(axis_list)):
        #print a[j]
        if j < len(a):
            (y1,y2)=a[j]
            if axis_list[i]>=y1 and axis_list[i]<=y2:
                j+=1
                day.append(ax[ax['day_pixel_location']==axis_list[i]].index.tolist()[0])
            else:
                pass
        else:
            break

    #print day,len(day)
    dailyimage_word['day']=day
    return dailyimage_word

def wholerecogniseprocess(dailyimage,axis,isuseindex = False):
    dailyimage_word={}
    lenlist=list(dailyimage)
    #print dailyimage
    for i in lenlist:
        word=''
        subdailyimage=splitcolumtocharacter(dailyimage[i])
        first_symbol=characteristicfunction(subdailyimage[0])
        #subdailyimage[0].show()


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
    if isuseindex == True:
        dailyimage_word_df=pd.DataFrame(list(dailyimage_word.items())).set_index(0).sort_index()
    else:
        dailyimage_word_df=pd.DataFrame(list(dailyimage_word.items())).sort_values(by=0).reset_index(drop=True)


    dailyimage_word_withday=addadaylableintoseries(dailyimage_word_df,axis)

    return dailyimage_word_withday

def addlabelandcategoryprocess(dailyimage_word,datatype,NUMlabel=False):
    if NUMlabel==True :
        dailyimage_word=dailyimage_word.rename(columns={0:'pixel_location'})
    else:
        pass
    if datatype=='dailypledges':
        dailyimage_word_label=dailyimage_word.rename(columns={1:'dailypledges'})
    elif datatype=='dailycomments':
        dailyimage_word_label=dailyimage_word.rename(columns={1:'dailycomments'})
    elif datatype=='dailybackers':
        dailyimage_word_label=dailyimage_word.rename(columns={1:'dailybackers'})
    else:
        raise Exception('cannot recognise type of png')

    return dailyimage_word_label


def dailycomments_chart_confirm(chartimage,type,linewidth='default'):
    if linewidth =='default':
        #target_pixel=(0,114,104,99,100,105,109,113,112,111,108,103,106)
        d=range(0)
        d.append(0)
        target_pixel=tuple(d)
        aaaa=(0,20,128,160,165,166,161,134,138,180,152)
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

def dailycomments_chart_bottom_confirm(image):
    mainchart_coordinate_axis_box=(78,221,920,223)
    mainchart_without_day_box=(78,40,920,219)
    mainchart_coordinate_axis = image.crop(mainchart_coordinate_axis_box)
    #mainchart_coordinate_axis.show()
    mainchart_without_day=image.crop(mainchart_without_day_box)
    #mainchart_without_day.show()
    #mianchart_day_b=chart_confirm(mianchart_day,'day')
    mainchart_coordinate_axis_b=dailycomments_chart_confirm(mainchart_coordinate_axis,'mainchart')
    mainchart_without_day_b=dailycomments_chart_confirm(mainchart_without_day,'mainchart')
    return mainchart_without_day_b,mainchart_coordinate_axis_b
'''
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
                    raise Exception('image daily(row) split process errloca[1]>a[i+1]')
            elif (a[i+1]-a[i])>params:
                if loca[1]==a[i]:
                    line.append(loca)
                    loca=(a[i+1],a[i+2])
                elif loca[1]<a[i]:
                    raise Exception('image daily(row) split process errloca[1]<a[i]')
                elif loca[1]>a[i]:
                    raise Exception('image daily(row) split process errloca[1]>a[i]')
        elif i ==(lena-1):
            loca=(loca[0],a[i])
            line.append(loca)
    return line
'''
def splitdailydataprocess(roll):
    dicts=scanrown(roll)
    a=sorted(list(dicts))
    line=[]
    loca=(a[0],0)
    lena=len(a)
    params=2
    for i in xrange(0,lena):
        if i <(lena-2):
            if  (a[i+1]-a[i])<=params:
                if loca[1]<=a[i+1]:
                    loca=(loca[0],a[i+1])
                elif loca[1]>a[i+1]:
                    #pass
                    raise Exception('image daily split process err in commmentandbackers:loca[1]>a[i+1]')
            elif (a[i+1]-a[i])>params:
                if loca[1]==a[i]:
                    line.append(loca)
                    loca=(a[i+1],a[i+2])
                elif loca[1]<a[i]:
                    #print loca,a[i],a[i+1]
                    loca=(a[i+1],a[i+2])
                    #pass
                    #raise Exception('image daily split process err in commmentandbackers:loca[1]<a[i]')
                elif loca[1]>a[i]:
                    loca=(a[i+1],a[i+2])
                    #pass
                    #raise Exception('image daily split process err in commmentandbackers:loca[1]>a[i]')
        elif i ==(lena-2):
            if (a[i+1]-a[i])<=params:
                loca=(loca[0],a[i])
            elif (a[i+1]-a[i]) > params:
                pass
            line.append(loca)
    return line

def dailypledges_recognization_process(image_file):
    image=Image.open(image_file).convert("RGBA")
    image,axis=dailypledges_chart_bottom_confirm(image)
    roll = image.transpose(Image.ROTATE_270)
    line=splitdailydataprocess(roll)
    dailyimage=cropfordailydata(roll,line)
    dailyimage_word=wholerecogniseprocess(dailyimage,axis)
    dailyimage_word_labelled=addlabelandcategoryprocess(dailyimage_word,'dailypledges')
    gc.collect()
    return dailyimage_word_labelled

def dailybackers_recognization_process(dailybackers_image_file):
    image=Image.open(dailybackers_image_file).convert("RGBA")

    image,axis=dailybackers_chart_bottom_confirm(image)
    roll = image.transpose(Image.ROTATE_270)
    #roll.show()
    #axis.show()
    line=splitdailydataprocess(roll)
    #print line
    dailybackers=cropfordailydata(roll,line)

    #dailybackers[list(dailybackers)[0]].show()
    dailybackers_word=wholerecogniseprocess(dailybackers,axis)
    dailybackers_word_labelled=addlabelandcategoryprocess(dailybackers_word,'dailybackers')
    return dailybackers_word_labelled

def data_txt_write(dicts,file):
    with open(file,'a') as f:
        for item in dicts.values():
            f.write(str(item)+',')
        f.write(';')



def dailycomments_recognization_process(dailycomments_image_file):
    image=Image.open(dailycomments_image_file).convert("RGBA")

    image,axis=dailycomments_chart_bottom_confirm(image)
    roll = image.transpose(Image.ROTATE_270)
    #roll.show()
    #axis.show()

    line=splitdailydataprocess(roll)
    #print line
    dailycomments=cropfordailydata(roll,line)
    dailycomments_word=wholerecogniseprocess(dailycomments,axis)
    dailycomments_word_labelled=addlabelandcategoryprocess(dailycomments_word,'dailycomments')
    return dailycomments_word_labelled
def dailybackers_chart_confirm(chartimage,type,linewidth='default'):
    if linewidth =='default':
        #target_pixel=(0,114,104,99,100,105,109,113,112,111,108,103,106)
        d=range(0)
        d.append(0)
        target_pixel=tuple(d)
        aaaa=(0,20,128,160,165,166,161,134,138,180,152)
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

def dailybackers_chart_bottom_confirm(image):
    mainchart_coordinate_axis_box=(78,221,920,223)
    mainchart_without_day_box=(78,40,920,219)
    mainchart_coordinate_axis = image.crop(mainchart_coordinate_axis_box)
    #mainchart_coordinate_axis.show()
    mainchart_without_day=image.crop(mainchart_without_day_box)
    #mainchart_without_day.show()
    #mianchart_day_b=chart_confirm(mianchart_day,'day')
    mainchart_coordinate_axis_b=dailybackers_chart_confirm(mainchart_coordinate_axis,'mainchart')
    mainchart_without_day_b=dailybackers_chart_confirm(mainchart_without_day,'mainchart')
    return mainchart_without_day_b,mainchart_coordinate_axis_b


def total_generation_process(dailypledges_image_file,dailycomments_image_file,dailybackers_image_file):

    dailypledges_word=dailypledges_recognization_process(dailypledges_image_file)
        #print dailypledges_word
        #dailycomments
    dailycomments_word=dailycomments_recognization_process(dailycomments_image_file)
        #print dailycomments_word
        #dailybackers
    dailybackers_word=dailybackers_recognization_process(dailybackers_image_file)
        #print dailybackers_word

    return dailypledges_word,dailycomments_word,dailybackers_word

def OnlyStr(s,oth=''):
   #s2 = s.lower();
   fomart = '0123456789'
   for c in s:
       if not c in fomart:
           s = s.replace(c,'');
   return s;


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
            #print num
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


def writeacsvprocess_w(file,headers,item):
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

def dailypledges_dailycomments_dailybackers_collection(target_word,data_type,rdir):
    target_short_dict={}

    #target_word=target_word.loc[:,[data_type,'day']]
    #print target_word
    #print target_word

    #dailypledges_short.to_csv(dailypledges_file)
    #print target_word['day'].tolist()
    for day in target_word['day'].tolist():
        #day=int(day)
        #print day
        target_amount= target_word[target_word['day']==day][data_type].tolist()[0]
        #print target_amount

        #if data_type=='dailypledges':
        #    target_amount= target_word[target_word['day']==day]['dailypledges'].tolist()[0]
        #elif data_type=='dailycomments':
        #    target_amount= target_word[target_word['day']==day]['dailycomments'].tolist()[0]
        #elif data_type=='dailybackers':
        #    target_amount= target_word[target_word['day']==day]['dailybackers'].tolist()[0]

        target_short_dict['Project_ID']=rdir['Project_ID']
        target_short_dict[str(day)]=target_amount

    return  target_short_dict


def collected_list_overwrite(file,item):
    f = open (file,'a')
    lenitem=len(item)
    for i in xrange(0,lenitem):
        f.write(item[i]+'\n')
    f.close()



def savingcsvprocessfordailydata(path_a,dict_list):
    #data_types=['dailypledges','dailycomments','dailybackers']
    common_headers=['Project_ID','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',
                    '21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39',
                    '40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59',
                    '60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79',
                    '80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100']
    Project_ID_header=['Project_ID']
    error_Project_ID_header=['Project_ID','status']
    dailypledges_target_file= path_a+'/target/dailypledges.csv'
    dailycomments_target_file=path_a+'/target/dailycomments.csv'
    dailybackers_target_file=path_a+'/target/dailybackers.csv'
    (dailypledges_dict_list,dailycomments_dict_list,dailybackers_dict_list,error_ID)=dict_list
    writeacsvprocess(dailypledges_target_file,common_headers,dailypledges_dict_list)
    writeacsvprocess(dailycomments_target_file,common_headers,dailycomments_dict_list)
    writeacsvprocess(dailybackers_target_file,common_headers,dailybackers_dict_list)
    #writeacsvprocess(collected_file,Project_ID_header,collected)
    #print error_ID
    if error_ID == []:
        pass
    else:
        writeacsvprocess(error_file,error_Project_ID_header,error_ID)



def inputsetting(status):
    if status ==1000:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file'
    elif status ==1001:
        dict_path='/home/pi/datasharing/image/dict'
        path_a='/home/pi/datasharing/image'
        #path_a='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image'
    elif status==0:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image0'
    elif status==1:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image1'
    elif status==2:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image2'
    elif status==3:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image3'
    elif status==4:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image4'
    elif status==5:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image5'
    elif status==6:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image6'
    elif status==7:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image7'
    elif status==8:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image8'
    elif status==9:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image9'
    elif status==10:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image10'
    elif status==11:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image11'
    elif status==12:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image12'
    elif status==13:
        dict_path='/Users/sn0wfree/Documents/imagedatakick/image/dict'
        path_a='/Users/sn0wfree/Documents/imagedatakick/image/file/image13'
        #file_path='/Users/sn0wfree/Documents/imagedatakick/image/outcome/image13'
    else:
        dict_path=input('please type in the path of characteristic dict(without name):')
        path_a=input('please type in target file path:')
    return dict_path,path_a



def progress_test(counts,lenfile,speed,w):
    bar_length=20
    eta=time.time()+w
    precent =counts/float(lenfile)

    ETA=datetime.datetime.fromtimestamp(eta)
    hashes = '#' * int(precent * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|read/error %d/%d projects|Speed : %.4f |ETA: %s """ % (precent*100,hashes + spaces,counts,error_counts,speed,ETA))

    #sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects" % (counts,f2-f1))

    #sys.stdout.write("\rPercent: [%s] %d%%,remaining time: %.4f mins"%(hashes + spaces,precent,w))
    time.sleep(random.random())
    sys.stdout.flush()



class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            (rdir) = self.queue.get()
            yv=total_scan_recognization_regroup_process(rdir)
            #time.sleep(1/10)
            self.queue.task_done()

def daily_data_collection_main(rdirs,y):
    for j in xrange(y):
        t = ThreadClass(queue)
        t.setDaemon(True)
        t.start()
    for rdir in rdirs:
        queue.put(rdir)
    queue.join()

def multicoreprocess(rdirs):
    pool = mp.Pool()
    #for rdir in rdirs:
    yv=pool.map(total_scan_recognization_regroup_process,rdirs)
    return 1


def total_scan_recognization_regroup_process(rdir):

    error_di={}
    dailypledges_short_dict={}
    dailycomments_short_dict={}
    dailybackers_short_dict={}
    dailypledges_image_file=rdir['dailypledges']
    dailycomments_image_file=rdir['dailycomments']
    dailybackers_image_file=rdir['dailybackers']
    try:
        (dailypledges_word,dailycomments_word,dailybackers_word)=total_generation_process(dailypledges_image_file,dailycomments_image_file,dailybackers_image_file)
    except:

        #saving error project_id
        #print rdir['Project_ID']

        error_di = {'Project_ID':rdir['Project_ID'],'status':'Error'}

        move_file=path_a+'/file/%s'%rdir['Project_ID']

        shutil.move(move_file,error_file_collected)
        #error_counts+=1

        #print 'the imag_id = %s error, error has been recorded'%rdir['Project_ID']
    else:


        dailypledges_short_dict=dailypledges_dailycomments_dailybackers_collection(dailypledges_word,'dailypledges',rdir)
        #if len(list(dailypledges_short_dict))<=105:
        dailycomments_short_dict=dailypledges_dailycomments_dailybackers_collection(dailycomments_word,'dailycomments',rdir)
        dailybackers_short_dict=dailypledges_dailycomments_dailybackers_collection(dailybackers_word,'dailybackers',rdir)
            #collected.append({'Project_ID':rdir['Project_ID']})

        gc.collect()
    #    else:
            #error_ID.append({'Project_ID':rdir['Project_ID'],'status':'too long'})
            #saving error project_id

    #        move_file=path_a+'/file/%s'%rdir['Project_ID']

    #        shutil.move(move_file,error_file_collected)
    #        error_counts+=1


        #f2=time.time()
        #
        #time.sleep(random.random())
    result=(dailypledges_short_dict,dailycomments_short_dict,dailybackers_short_dict,error_di)
    #if error_di == {}:
    return result

def chunks(item,parts,model='equal_length'):

    lenitem=len(item)
    if model == 'equal_GAP' or model == 'GAP':
        n=lenitem//parts
    elif model == 'equal_length' or model == 'length':
        n=parts
    else:
        n=parts

    lis=[]
    #split item by n
    for i in xrange(0,lenitem,n):
        if i+n < lenitem:
            lis.append(item[i:i+n])
        else:
            lis.append(item[i:])
    return lis

def main_multi_core_recognise_process(status):
    global characteristiclibs
    global counts,collected,collected_file
    global error_ID,error_file,error_file_collected
    global path_a
    global dailypledges_dict_list,dailypledges_target_file
    global dailycomments_dict_list,dailycomments_target_file
    global dailybackers_dict_list,dailybackers_target_file
    global y,error_counts
    global lenfile,cooldown

    #error_ID=[]

    dict_path,path_a=inputsetting(status)

    dicttxt=dict_path+'/characteristic.txt'
    dictcsv=dict_path+'/characteristic.csv'
    error_counts=0

    error_file=path_a+'/target/error.csv'
    collected_file=path_a+'/target/collected.csv'
    error_file_collected=path_a+'/error'
    #'/Users/sn0wfree/Documents/imagedatakick/image/file/image12/error'

    dailypledges_target_file= path_a+'/target/dailypledges.csv'
    dailycomments_target_file=path_a+'/target/dailycomments.csv'
    dailybackers_target_file=path_a+'/target/dailybackers.csv'




    tasks_uncleaning=getDirList(path_a+'/file')
    #print type(tasks_uncleaning[1])
    collected_str=readacsv(dailypledges_target_file)['Project_ID'].tolist()
    #print collected_str[1]
    collected=[float(collected_str[x]) for x in xrange(len(collected_str)) ]
    #print collected[1]
    #error_list=readacsv(error_file)['Project_ID'].tolist()
    error_list=getDirList(path_a+'/error')
    error_ID=[]
    if error_list != []:
        for errors in error_list:
            error_ID.append({'Project_ID':errors,'status':'Error'})
    else:
        pass


    #collected=list(set(collected))


    #print collected
    #lencollected=len(collected)
    #lentasks_uncleaning=len(tasks_uncleaning)
    #tasks=scanfolderprocess(path_a+'/file')[0:50]

    tasks=list(set(tasks_uncleaning)-set(collected)-set(error_list))
    lenfile=len(tasks)
    #print tasks[0]
    print 'total file counts: %s'%lenfile
    #=list(set(tasks_uncleaning)-set(collected))
    characteristiclibs=read_characteristic_libs(dictcsv)


    rdirs=[]
    #print type(tasks[0])
    for task in tasks:
        if type(task)==float:
            temp={}
            dailypledges_image_file=path_a+'/file/%s/dailypledges.png' %task
            dailycomments_image_file=path_a+'/file/%s/dailycomments.png' %task
            dailybackers_image_file=path_a+'/file/%s/dailybackers.png' %task
            temp['Project_ID']=task
            #type_png=['dailypledges.png','dailybackers.png','dailycomments.png']
            #headers=['Project_ID','url']
            temp['dailypledges']=dailypledges_image_file
            temp['dailycomments']=dailycomments_image_file
            temp['dailybackers']=dailybackers_image_file
            rdirs.append(temp)

    #common_headers=['Project_ID',0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]
    #common_headers=['Project_ID','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100']
    gc.enable()


    #multicoreprocess(rdirs)
    pool = mp.Pool()
    rdirs_split = chunks(rdirs,y)
    for rdir in rdirs_split:
        #print type(ridr)
        f1=time.time()
        results=pool.map(total_scan_recognization_regroup_process,rdir)
        dailypledges_dict_list=[]
        dailycomments_dict_list=[]
        dailybackers_dict_list=[]
        error_ID=[]
        for (dailypledges_short_dict,dailycomments_short_dict,dailybackers_short_dict,error_di) in results:
            if len(list(dailypledges_short_dict))<=105 and dailypledges_short_dict !={}:
                dailypledges_dict_list.append(dailypledges_short_dict)

                dailycomments_dict_list.append(dailycomments_short_dict)

                dailybackers_dict_list.append(dailybackers_short_dict)

            elif len(list(dailypledges_short_dict))>105 and dailypledges_short_dict !={}:
                error_di={'Project_ID':dailypledges_short_dict['Project_ID'],'status':'too long'}


            if error_di !={}:
                error_ID.append(error_di)
                error_counts+=1
            else:
                counts+=1
    #if len(dailypledges_dict_list)>50:
        if dailypledges_dict_list !=[]:
            dict_list=(dailypledges_dict_list,dailycomments_dict_list,dailybackers_dict_list,error_ID)
            savingcsvprocessfordailydata(path_a,dict_list)
        else:
            pass
        #collected=[]
        if cooldown >= 100 and counts %3==1:
            time.sleep(30)
            cooldown=1
        elif counts >500:
            cooldown+=1
            time.sleep(random.random()+1)
        else:
            time.sleep(random.random())


        f2=time.time()
        w=(lenfile-counts)*(f2-f1)/y
        progress_test(counts,lenfile,f2-f1,w)

def recursionprocess(status):

    if type(status)== tuple :
        print 'enter multi-target collection model(multi-core)'
        for x in xrange(len(status)):
            print 'collect %s part'%status[x]
            main_multi_core_recognise_process(status[x])

    elif type(status)== int:
        print 'Enterring single-target collection model (multi-core)'
        #print 'Please enter following info.'
        main_multi_core_recognise_process(status)

        #print status



if __name__ == '__main__':
    global characteristiclibs
    global counts,collected,collected_file
    global error_ID,error_file,error_file_collected
    global path_a
    global dailypledges_dict_list,dailypledges_target_file
    global dailycomments_dict_list,dailycomments_target_file
    global dailybackers_dict_list,dailybackers_target_file
    global y,error_counts
    global lenfile,cooldown
    #queue = Queue.Queue()
    status=input('setup a status(0-99):')
    y=input('to choose the number of workers/parts for this tasks(8/50):')
    #core=input('multicore(0) or multithreading(1):')
    #y=2
    #mail = input('mail it?(1 or 0):')
    mail = 0
    counts=0
    cooldown=0
    if mail ==1:
        mail_password=input('please enter mail password:')
    else:
        pass
    #main_multi_core_recognise_process(status)
    recursionprocess(status)











    #savingcsvprocessfordailydata(path_a)

    print 'saving process completed'

    if mail== 1:

        target_files=[dailybackers_target_file,dailycomments_target_file,dailypledges_target_file]


        for target_file in target_files:
            target=  target_file
            now =  datetime.datetime.today()
            pathfile=publicpath+ '/%s.zip' % now
            print 'compress process completed'
            zipafilefordelivery(pathfile,target)

            print 'begin sending email'
            mail_username='linlu19920815@gmail.com'

            to_addrs="snowfreedom0815@gmail.com"
            attachmentFilePaths=pathfile
            sendmailtodelivery(mail_username,mail_password,to_addrs,attachmentFilePaths)
        print 'email sent'


    else:
        print 'collecting process completed'

    #print dailypledges_dict_list
    #print dailycomments_dict_list
    #print dailybackers_dict_list


    #['daily_pledged']
    #['daily_comments']
    #['daily_backers']
    #dailypledges
