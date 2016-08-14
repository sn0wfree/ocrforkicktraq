


def chunks(item,n):
    lenitem=len(item)
    dic=[]
    #split item by n
    for i in xrange(0,lenitem,n):
        if i+n < lenitem:
            dic.append(item[i:i+n])
        else:
            dic.append(item[i:])
    return dic


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
def getDirList( p ):
        p = str( p )
        if p=="":
              return [ ]
        #p = p.replace( "/","/")
        if p[-1] != "/":
             p = p+"/"
        a = os.listdir( p )
        b = [ float(x)   for x in a if os.path.isdir( p + x ) ]
        return b
#numpy int64 problem
#dot problem
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
            #error_ID.append(num)
            pass
    return f

    #shutil.move("oldpos","newpos")
def movedirprocess(single_dir,target_dir):

    import shutil,time

    shutil.move(single_dir,target_dir)
    #time.sleep(0.1)
    #print 'done'

class chunksplitdataintopart():
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


    def __init__(self,oringaldir,parts):
        import os
        fo=os.walk(oringaldir)
        f=[]
        for root,subfolder,files in fo:
            num=root.lstrip(oringaldir)
            #print num,type(num)
            statuscodefornum=Onlynum(num)
            if statuscodefornum == 0 and num !='':
                #print num
                number=oringaldir+'/'+num
                f.append(number)
        lenf=len(f)
        #print lenf
        chunksplitdataintopart.split=[]
        #split item by n
        n=lenf//parts
        for i in xrange(0,lenf,n):
            if i+n < lenf:
                chunksplitdataintopart.split.append(f[i:i+n])
            else:
                chunksplitdataintopart.split.append(f[i:])


def main(dirs,target_dirs):
    parts=5
    counts=0
    #define target_dirs
    f=chunksplitdataintopart(dirs,parts)
    part_from_f=len(f.split)
    #print len(f.split),f.split[0][1]
    for i in xrange(part_from_f):
        dir_temp=target_dirs+'/part%s'%i
        folders=f.split[i]
        for single_dir in folders:
            movedirprocess(single_dir,dir_temp)
            counts+=1
            if counts>20000:
                counts=0
                time.sleep(1)
        time.sleep(0.1)


if __name__=='__main__':
    import time
    import os,shutil
    dirs=       '/Users/sn0wfree/Documents/imagedatakick/file/imageforkick'
    target_dirs='/Users/sn0wfree/Documents/imagedatakick/file'
    parts=1
    targ='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image/testfile'
    erro_file = targ + '/error'
    oringaldir=targ+'/testpart2'
    #fo=os.walk(oringaldir)
    #oringaldir = os.getcwd()
    #print oringaldir
    #print oringaldir

    f=getDirList( oringaldir )

    move_file = oringaldir +'/%s'%f[1]
    #print move_file,type(move_file)
    target_path= targ+'/error'
    shutil.move(move_file,target_path)
    #oringaldir = os.getcwd()
    #print getDirList(oringaldir)


    #dirs='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image/file'
    #target_dirs='/Users/sn0wfree/Dropbox/BitTorrentSync/data/image/testfile'
    #f=chunksplitdataintopart(dirs,parts)











    #print len(f.split),f.split[1][1],type(f.split[1][1])
