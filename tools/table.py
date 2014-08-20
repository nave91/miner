"""
#table.py: Module for different table operations

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

from globfile import *
from lib import *

def expected(z,e): #returns expected outcome in str
    out = [c for c in colname[z]]
    if e == 'mean':
        for c in colname[z]:
            if c in wordp[z]:
                out[colname[z].index(c)] = str(mode[z][c])
            else:
                out[colname[z].index(c)] = str('%0.2f' % round(mu[z][c],2))
        return out
    if e == 'median':
        for c in colname[z]:
            if c in wordp[z]:
                out[colname[z].index(c)] = str(mode[z][c])
            else:
                out[colname[z].index(c)] = str(round(float(medianOf(z,c)),2))
        return out
    sys.stderr.write("Expected1 did not return anything. Fix it. Bye Bye.\n")
    sys.exit()


def expected1(z,e): #returns expected outcome
    out = [c for c in colname[z]]
    if e == 'mean':
        for c in colname[z]:
            if c in wordp[z]:
                out[colname[z].index(c)] = mode[z][c]
            else:
                out[colname[z].index(c)] = round(mu[z][c],2)
        return out
    if e == 'median':
        for c in colname[z]:
            if c in wordp[z]:
                out[colname[z].index(c)] = mode[z][c]
            else:
                out[colname[z].index(c)] = round(float(medianOf(z,c)),2)
        return out
    sys.stderr.write("Expected1 did not return anything. Fix it. Bye Bye.\n")
    sys.exit()

def rowprint(row,sp=20): #returns neat rows
    c = "%"+str(sp)+"s"
    columns = [ c % cell for cell in row]
    columns.append("%4s" % '#')
    return ' '.join(columns)

def tableprint(z,e): #prints table with the summary
    sys.stderr.write("tableprint prints expected with mean by default\n")
    try:
        print rowprint(colname[z]),'%10s' % 'notes'
        print rowprint(expected(z,e)), '%10s' % 'expected'
        temp = [ c for c in range(len(colname[z]))]
        for c in colname[z]:
            #print c
            if c in nump[z]:
                temp[colname[z].index(c)] = str('%0.2f' % round(sd[z][c],2))
            else:
                if n[z][c] > 0:
                    temp[colname[z].index(c)] = str('%0.2f' % round(float(most[z][c])/float(n[z][c]),2))
                else:
                    temp[colname[z].index(c)] = 0.0
        print rowprint(temp),'%10s' % 'certainity'
        for row in data[z]:
            print rowprint(row)
    except KeyError:
        print "Empty Table or Table missing"
        return

def tableprint1(z):
    print rowprint(colname[z])
    for row in data[z]:
        print rowprint(row)

def klass1(data, z):
    for k in klass[z]:
        return data[colname[z].index(k)]

def klassAt(z):
    for k in klass[z]:
        return colname[z].index(k)

def fromHell(row,z,more,less):
    m = 0
    out = 0
    aLittle = 0.001
    if z in more:
        for c in more[z]:
            ind = colname[z].index(c)
            if row[ind] != '?':
                m+=1
                print ind,z
                out += ((row[ind] - hi[z][c]) / (hi[z][c] - lo[z][c] + aLittle))**2
    if z in less:
        for c in less[z]:
            ind = colname[z].index(c)
            if row[ind] != '?':
                m+=1
                out += ((row[ind] - hi[z][c])/ (hi[z][c] - lo[z][c] + aLittle))**2
    return out**0.5/m**5 if m == 1 else 1

def printCsv(z,rounding=False):
    comma = ','
    for d in data[z]:
        items = ''
        for item in d:
            if rounding:
                if isinstance(item,(float,int)):
                    items+=str(int(item))+comma
                else:
                    items+=str(item)+comma
            else:
                items+=str(item)+comma        
        if items[len(items)-1] is comma:
            print items[:len(items)-1]
        else:
            print items
        
def printColCsv(z):
    items = ''
    for c in colname[z]:
        if colname[z].index(c) != (len(colname[z])-1):
            comma = ','
        else:
            comma = ''
        items += str(c)+comma
    print items

    
def outCsv(zlst,rounding=False):
    printColCsv(zlst[0])
    for Z in zlst:
        printCsv(Z,rounding)

def outCsvCols(z,cols,rounding=True):
    items = ''
    comma = ','
    inds  = []
    for c in colname[z]:
        if c in cols:
            inds.append(colname[z].index(c))
            items += str(c)+comma
    print items
    for d in data[z]:
        items = ''
        for i_item,item in enumerate(d):
            if i_item in inds:
                if rounding:
                    if isinstance(item,(float,int)):
                        items+=str(int(item))+comma
                    else:
                        items+=str(item)+comma
                else:
                    items+=str(item)+comma        
        print items
    
