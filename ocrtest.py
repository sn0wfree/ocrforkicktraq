# coding:utf8

#from PIL import Image
import pytesseract,os,gc
from PIL import Image, ImageStat
import StringIO, cStringIO
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
#from matplotlib import pyplot as plt


def image_to_string(img, cleanup=True, plus=''):

    os.popen('tesseract ' + img + ' ' + img + ' ' + plus)
    with open(img + '.txt','r') as txt:
        text=txt.read()
    if cleanup:
        os.remove(img + '.txt')
    return text


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


def cropdailybar(dicts,dicts_axis,image):
    a=sorted(list(dicts))
    dayslabel=sorted(list(dicts_axis))
    daylabel={}
    for i in xrange(len(dayslabel)):
        daylabel[dayslabel[i]]=i
    #print a
    lena=len(a)
    counts=0
    line={}
    count=0
    for i in xrange(0,lena):
        if i <(lena-1):
            if  (a[i+1]-a[i])<=2:
                count+=1
            else:
                line[counts]=(a[i]-count,a[i])
                #gap.append(a[i+1]-a[i])
                count=0
                counts+=1
        else:
            if i==(lena-1):
                line[counts]=(a[i]-count,a[i])
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

def forsilceandsearchrowsandcolums(image,image_axis):
    dicts=scanrown(image)
    dicts_axis=scanaxis(image_axis)
    #print dicts_axis

    dailyimage=cropdailybar(dicts,dicts_axis,image)
    #dailyimage[0].show()
    pledged_dailyimage={}
    listdailyimage=list(dailyimage)
    lenlistdailyimage=len(listdailyimage)
    #for w in listdailyimage:
    #    day_character_pic=splitcolumtocharacter(dailyimage[w])
        #####


    #daily=dailyimage[4]
    #daily.show()
    #days=splitcolumtocharacter(daily)
    return dailyimage



def splitcolumtocharacter(dailydata5):
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
    a=sorted(list(character))
    #print a
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


def pledge_recognitionzeroloaction(image):
    #print type(image_file)
    lable_bottom=dailypledges_lable_confirm(image)
    #print type(lable_bottom_png)
    #lable_bottom.show()
    #lable_bottom.save('/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict/$0.tif')
    lable_bottom.save("temp.tif")
    temp=Image.open("temp.tif").convert("RGBA")
    os.remove("temp.tif")

    #temp_stringio = cStringIO.StringIO()
    #lable_bottom.save(temp_stringio,format='png')
    #temp_stringio.seek(0)
    #temp= temp_stringio.getvalue()
    #temp_stringio.close()
    #temp=temp.convert("RGBA")
    labledollarsymbol0=Image.open('/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict/pledgelabledollarsymbol0.tif').convert("RGBA")
    #print type(labledollarsymbol0)
    if temp== labledollarsymbol0:
        print 'coordinate axis is at bottom'
        location='bottom'
    else:
        print 'coordinate axis is at middle'
        location='middle'
    return location

def loading_characters_dictionary(path):
    characters_dict={}
    charactersdict=os.listdir(path)
    for files in charactersdict:
        #print files
        name=files.split('.')[0]

        files_image=path+'/'+files
        if name!='':
            dict_characters_image=Image.open(files_image)
            characters_dict[name]=dict_characters_image
        else:
            pass
    return characters_dict

#def loading_characteristic_library():




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

#def corealgotithm():


def read_whole_line(days):
    for i in xrange(sorted(list(days))):
        readline=''
        if charactersearchprocessforchart(days[i],characters_dict)!='cannot recognize':
            locals()['%sth_letter'%i]=charactersearchprocessforchart(days[i],characters_dict)
            readline+=locals()['%sth_letter'%i]
        else:
            readline+='meet Error'
    return realine





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



def characteristicfunction(character_image,setup=False,name='null',path='null'):
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

    pix=character_image.load()
    characteristicvalue={}
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
    characteristicvalue['the_number_of_pixel_in_each_row']=the_number_of_pixel_in_each_row
    characteristicvalue['the_number_of_pixel_in_each_column']=the_number_of_pixel_in_each_column
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

if __name__ == '__main__':
    gc.enable()
    image_file='dailypledges-5.png'
    #image_file = '/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict/pledgechart5.tif'
    image=Image.open(image_file).convert("RGBA")
    path='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict'

    #characters_dict=loading_characters_dictionary(path)
    #change the color
    image,axis=dailypledges_chart_bottom_confirm(image)
    #image=xxx(image)
    #image.show()

    roll = image.transpose(Image.ROTATE_270)
    roll_axis = axis.transpose(Image.ROTATE_270)
    print roll_axis.size[0],roll_axis.size[1]


    #roll.show()
    dailydata=forsilceandsearchrowsandcolums(roll,roll_axis)
    #print gap
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




def recogonize_char(image_dict,characteristiclibs):
    left_9=characteristiclibs['9']
    left_2=characteristiclibs['2']
    left_4=characteristiclibs['4']
    left_5=characteristiclibs['5']
    left_7=characteristiclibs['7']
    left_0=characteristiclibs['0']
    left_K=characteristiclibs['K']
    left_R=characteristiclibs['R']
    left_poundsymbol=characteristiclibs['poundsymbol']
    left_eurosymbol=characteristiclibs['eurosymbol']
    #left_0=characteristiclibs['0']
    # 2 4 5 6 7 0 euro pound KR
    if image_dict['the_number_of_columns']<=2:
        left_1=characteristiclibs['1']
        #
        left_comma=characteristiclibs['comma']
        if image_dict['the_number_of_columns']==left_1['the_number_of_columns']:
            if image_dict['the_number_of_pixel_in_each_row']=left_1['the_number_of_pixel_in_each_row'] and image_dict['the_number_of_pixel_in_each_column']=left_1['the_number_of_pixel_in_each_column']:
                return '1'
        elif image_dict['the_number_of_columns']==left_comma['the_number_of_columns']:

            if image_dict['the_number_of_pixel_in_each_row']=left_comma['the_number_of_pixel_in_each_row'] and image_dict['the_number_of_pixel_in_each_column']=left_comma['the_number_of_pixel_in_each_column']:
                return ','
    elif image_dict['the_number_of_columns']==3:
        left_minus=characteristiclibs['minus']
        if image_dict['the_number_of_pixel_in_each_row']=left_minus['the_number_of_pixel_in_each_row'] and image_dict['the_number_of_pixel_in_each_column']=left_minus['the_number_of_pixel_in_each_column']:
            return '-'
            break
    elif image_dict['the_number_of_columns']==5:
        left_dollarsymbol=characteristiclibs['dollarsymbol']
        if image_dict['the_number_of_pixel_in_each_row']=left_dollarsymbol['the_number_of_pixel_in_each_row'] and image_dict['the_number_of_pixel_in_each_column']=left_dollarsymbol['the_number_of_pixel_in_each_column']:
            return '$'
    elif image_dict['the_number_of_columns']==4:
        left_8=characteristiclibs['8']
        if image_dict['the_number_of_pixel_in_each_column']=left_8['the_number_of_pixel_in_each_column']:
            if image_dict['the_number_of_pixel_in_each_row']=left_8['the_number_of_pixel_in_each_row']:
                return '8'
            else:
                left_3=characteristiclibs['3']
                if image_dict['the_number_of_pixel_in_each_row']=left_3['the_number_of_pixel_in_each_row']:
                    return '3'
        elif image_dict['the_number_of_pixel_in_each_column']=left_9['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_9['the_number_of_pixel_in_each_row']:
                    return '9'
        elif image_dict['the_number_of_pixel_in_each_column']=left_2['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_2['the_number_of_pixel_in_each_row']:
                    return '2'
        elif image_dict['the_number_of_pixel_in_each_column']=left_4['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_4['the_number_of_pixel_in_each_row']:
                    return '4'
        elif image_dict['the_number_of_pixel_in_each_column']=left_6['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_6['the_number_of_pixel_in_each_row']:
                    return '6'
        elif image_dict['the_number_of_pixel_in_each_column']=left_5['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_5['the_number_of_pixel_in_each_row']:
                    return '5'
        elif image_dict['the_number_of_pixel_in_each_column']=left_7['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_7['the_number_of_pixel_in_each_row']:
                    return '7'
        elif image_dict['the_number_of_pixel_in_each_column']=left_0['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_0['the_number_of_pixel_in_each_row']:
                    return '0'
        elif image_dict['the_number_of_pixel_in_each_column']=left_K['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_K['the_number_of_pixel_in_each_row']:
                    return 'K'
        elif image_dict['the_number_of_pixel_in_each_column']=left_R['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_R['the_number_of_pixel_in_each_row']:
                    return 'R'
        elif image_dict['the_number_of_pixel_in_each_column']=left_poundsymbol['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_poundsymbol['the_number_of_pixel_in_each_row']:
                    return '£'
        elif image_dict['the_number_of_pixel_in_each_column']=left_eurosymbol['the_number_of_pixel_in_each_column']:
                if image_dict['the_number_of_pixel_in_each_row']=left_eurosymbol['the_number_of_pixel_in_each_row']:
                    return 'eur'




             # 2 4 5 6 7 0 euro pound KR








        #enter char recogonize
    ##recognize_process

    #print days
    #days[0].show()
    #print days[0].size[0],days[0].size[1]
