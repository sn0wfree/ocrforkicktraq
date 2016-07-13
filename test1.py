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

#def corealgotithm():








    #characters_dict['pledgechart5'].show()



    #if location =='bottom':

    #    wholedecompositionprocess(image,path)

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
    the_number_of_column=dataset.shape[1]
    #thenumber_of_row=dataset.shape[1]
    sum_row = dataset.sum(axis=1) #the characteristic for each row
    sum_column = dataset.sum(axis=0) #the characteristic for each column
    the_number_of_pixel_in_each_row=sumacharacteristicforsingleroworcolumn(sum_row)
    the_number_of_pixel_in_each_column=sumacharacteristicforsingleroworcolumn(sum_column)
    characteristicvalue['the_number_of_columns']=the_number_of_column
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



if __name__ == '__main__':
    gc.enable()
    path='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/ocrforkicktraq/dict'
    #d='eurodollarsymbol'
    #image_file = path+'/'+'pledgechart%s.tif'%d
    image_file='dailypledges-6.png'
    image=Image.open(image_file).convert("RGBA")

    #print a["8"]



    #print characteristicvalue['the_number_of_pixel_in_each_row']
    #print characteristicvalue['the_number_of_pixel_in_each_column'],tuple(characteristicvalue['the_number_of_pixel_in_each_column'])
    #print characteristicvalue['the_number_of_columns']















#def resizesearch(roll,columnp,rowp):
#    counts={}
#    resss=(roll.size[0]/columnp,roll.size[1]/rowp)
#    roll_resized=roll.resize(resss)
#    pixel=roll_resized.load()
    #print roll_resized.size[0]
    #data = np.zeros((roll_resized.size[1],roll_resized.size[0]))
#    for i in xrange(roll_resized.size[1]):
#        for j in xrange(roll_resized.size[0]):
#            if pixel[j,i][0]==0:
#                counts[i]='has'
#    #print list(counts),len(list(counts))
#    return list(counts)

    #data = pd.DataFrame(data)




#rows=resizesearch(roll,1,rowp)
#counts={}
#pixels=roll.load()
#for row in rows:
#    for i in xrange(roll.size[0]):#
#        count=0
#        if pixels[i,row-3][0] ==0:
#            count+=1
#        counts[i]=count


#print rows






#print image_to_string("hz.font.exp0.tif")
