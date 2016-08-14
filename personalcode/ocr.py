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

def chart_confirm(chartimage,type):
    target_pixel=(0,114,104,99,105,109,113,112,111,108,103,106)
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

    #mianchart_day = image.crop(mainchart_day_box)
    mainchart_without_day=image.crop(mainchart_without_day_box)

    #mianchart_day_b=chart_confirm(mianchart_day,'day')
    mainchart_without_day_b=chart_confirm(mainchart_without_day,'mainchart')
    return mainchart_without_day_b

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

def forsilceandsearchrowsandcolums(image):
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
    a=sorted(list(dicts))
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
                count=0
                counts+=1
        else:
            if i==(lena-1):
                line[counts]=(a[i]-count,a[i])
                #return a dict
    dailyimage={}
    listline=list(line)
    for i in listline:
        (y1,y2)=line[i]
        box=(0,y1-1,image.size[0],y2+2)
        locals()['data%s'%i]=image.crop(box)
        dailyimage[i]=locals()['data%s'%i]
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
    labledollorsymbol0=Image.open('/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict/pledgelabledollorsymbol0.tif').convert("RGBA")
    #print type(labledollorsymbol0)
    if temp== labledollorsymbol0:
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

def charactersearchprocessforchart(image,characters_dict,opt = True,imagetype='pledge'):
    characters_dict_value=characters_dict.values()
    dd='cannot recognize'
    #opt dict
    if opt == True and imagetype=='pledge':
        keys={}
        del characters_dict['pledgelabledollorsymbol0']
        del characters_dict['pledgechartdollorsymbol0']
        characters_dict_keys=characters_dict.keys()
        for key in characters_dict_keys:
            if 'chart' in key:
                key_drop=key.split('chart')[1]
                if key_drop =='dollorsymbol':
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

    if opt == True:
        characters_dict=keys
    else:
        pass
    characters_dict_value=characters_dict.values()
    #print image
    #print characters_dict['pledgechartdollorsymbol']
    for value in characters_dict_value:
        if image== value:
            print value
            dd=characters_dict.keys()[characters_dict.values().index(value)]
            break
    return dd



def read_whole_line(days):
    for i in xrange(sorted(list(days))):
        readaline=''
        if charactersearchprocessforchart(days[i],characters_dict)!='cannot recognize':
            locals()['%sth_letter'%i]=charactersearchprocessforchart(days[i],characters_dict)
            readaline+=locals()['%sth_letter'%i]
        else:
            readaline+='meet Error'
    return readline


def wholedecompositionprocess(image_file,path):
    image=dailypledges_chart_bottom_confirm(image_file)
    #loading characters dictionary
    path='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict'
    characters_dict=loading_characters_dictionary(path)
    #characters_dict['pledgechartdollorsymbol0'].show()

    #print tif0.size
    #rotate all zeros
    #roll=rollallzero(image,tif0)
    #roll = roll.transpose(Image.ROTATE_270)
    roll = image.transpose(Image.ROTATE_270)
    #roll.show()
    #spilt all bar to each line
    dailydata=forsilceandsearchrowsandcolums(roll)
    #dailydata[5].show()
    pledged_dailydata={}
    listdailydata=list(dailydata)
    #lenlistdailydata=len(listdailydata)
    for w in listdailydata:
        daily=dailydata[w]
        days=splitcolumtocharacter(daily)

        if days[0]==characters_dict['pledgechartdollorsymbol']:
            readline=read_whole_line(days)
        else:
            daily_rotate=daily.transpose(Image.ROTATE_90)
            days=splitcolumtocharacter(daily_rotate)
            #need rotate

        pledged_dailydata[w]=readline
        readline=''



if __name__ == '__main__':
    gc.enable()
    image_file = 'dailypledges1.png'
    image=Image.open(image_file).convert("RGBA")
    #location=pledge_recognitionzeroloaction(image)
    characters_dictionart_path='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict'
    characters_dict=loading_characters_dictionary(characters_dictionart_path)

    a=characters_dict['pledgechartdollorsymbol']
    #a.show()
    text=charactersearchprocessforchart(a,characters_dict)
    print text
