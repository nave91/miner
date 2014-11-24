"""
#lib.py: Library Module for all tools

Copyright (c) 2014 rekojtoor@gmail.com

._____.___ .___ .______  ._______.______  
:         |: __|:      \ : .____/: __   \ 
|   \  /  || : ||       || : _/\ |  \____|
|   |\/   ||   ||   |   ||   /  \|   :  \ 
|___| |   ||   ||___|   ||_.: __/|   |___\
      |___||___|    |___|   :/   |___|    
                                          
Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and
associated documentation files (the "Software"), to
deal in the Software without restriction, including
without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to
whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission
notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE."""                                           
                                          
import sys
sys.dont_write_bytecode = True

import re
import random
from globfile import *
from math import *
PI = 3.1415926535
EE = 2.7182818284 

def indexOf(Z,col):
    return colname[Z].index(col)

def medianOf(z,c):
    median = -100000000
    ind = indexOf(z,c)
    values = []
    if len(data[z]) == 1:
        return round(data[z][0][ind],2)
    for i in data[z]:
        values.append(i[ind])
    values = [i for i in values if i != '?']
    l = len(values)*1.0
    if l == 0: return -1
    values = sorted(values)
    md = (l+1)/2 - 1 #index of median
    if l%2 != 0: #odd
        median = values[int(md)]
    else: #even
        median = (values[int(md-0.5)]+values[int(md+0.5)])/2
    if median == '?': return -1
    return round(median*1.0,2)

def resetSeed(seed):
    if seed:
        random.seed(seed)
    else:
        random.seed(1)

def line(csvfile): #returns formatted line from the csvfile 
    l = csvfile.readline()
    endcommare = re.compile('.*,$')
    if l != '':
        l = l.split('#')[0]
        l = l.replace('\t','')
        l = l.replace('\n','')
        l = l.replace('\r','')
        l = l.replace(' ','')
        endcomma = endcommare.match(l)
        if endcomma:
            ltemp = line(csvfile)
            if ltemp != -1:
                return l+ltemp
            else:
                return l
        else:
            return l
    else:
        return -1

def anyi(lst):
    resetSeed(1)
    tmp = random.random()
    return int(tmp*len(lst)) + 1

def ptile(lst,chops):
    n = len(lst)-1
    sorte = sorted(lst)
    ptile = {}
    for p in chops:
        ptile[p] = round(sorte[int(float(p)*n)],1)
    return ptile

def depsptile(z,chops):
    #returns ptile of dep's
    p = {}
    ptiles = {}
    for col in dep[z]:
        ind = colname[z].index(col)
        for d in data[z]:
            if col in p.keys(): p[col].append(d[ind])
            else: p[col] = [d[ind]]
        ptiles[col] = ptile(p[col],chops)
    return ptiles

def chopsptiles(ptiles,chops):
    rowchops ={}
    for col,ptile in ptiles.items():
        for chop in chops:
            if chop in rowchops.keys(): 
                rowchops[chop].append(ptile[chop])
            else:
                rowchops[chop] = [ptile[chop]]
    return rowchops

def printptiles(z,ptiles,chops,title='title'):
    print str(title)+': '+str(z),"len:",len(data[z])
    header = ["percentile"]
    for i in ptiles.keys():
        header.append(str(i))
    print rowprint(header)
    rowchops = chopsptiles(ptiles,chops)
    for key,value in rowchops.items():
        out = [str(int(key*100))]
        for i in value:
            out.append(str(i))
        print rowprint(out)
    
def depsptiles(befz,aftz,chops,verbose=False):
    ptiles1 = depsptile(befz,chops)
    ptiles2 = depsptile(aftz,chops)
    rowchops1 = chopsptiles(ptiles1,chops)
    rowchops2 = chopsptiles(ptiles2,chops)
    dec,inc,same = 0,0,0 
    for chop in chops:
        for ind,col in enumerate(ptiles1.keys()):
            if rowchops1[chop][ind] > rowchops2[chop][ind]:
                dec += 1
            elif rowchops1[chop][ind] < rowchops2[chop][ind]: 
                inc += 1
            else:
                same += 1

    if verbose: 
        printptiles(befz,ptiles1,chops,"before")
        printptiles(aftz,ptiles2,chops,"after")
        print "---"*27
        print "dec:",dec,"inc:",inc,"same:",same
        print "---"*27       
    return dec,inc,same


def calcMre(z,col):
    #calculate mre with median
    cind = indexOf(z,col)
    med = medianOf(z,col)
    for r,d in enumerate(data[z]):
        actual = d[cind]
        if actual != '?':
            mre[z][r] = abs((actual-med)/actual)
    return mre

def normalizelist(list):
    maxi = max(list)
    mini = min(list)
    temp = []
    for l in list:
        temp.append(((maxi-l)/(maxi-mini))*100)
    return temp

def median(lst):
    return np.median(np.array(lst))

def spread(lst):
    return np.percentile(np.array(lst),75) - \
        np.percentile(np.array(lst),25)

def mqw(lst):
    m,q,w = -1,-1,-1
    lst = sorted(lst)
    m = median(lst)
    q = spread(lst)
    w = max(lst)
    return m,q,w

def indepdata(z):
    cinds = []
    for c in indep[z]:
        cinds.append(colname[z].index(c))
    indata = []
    for d in data[z]:
        _tmp = []
        for i in cinds:
            _tmp.append(d[i])
        indata.append(_tmp)
    return indata
    
if __name__ == '__main__':
    import random
    print mqw([random.randint(1,10) for i in range(10)])
