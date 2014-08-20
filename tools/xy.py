"""
#xy.py: Module supporting quad-clustering of data

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

from xy_lib import *

class row:
    """
    Stores rows and its (x,y) coordinates on projected
    2D pane
    """
    def __init__(i,row):
        i.row = row
        i.x = 0
        i.y = 0
    
    def __repr__(i):
        return "\n> x: "+str(i.x)+" y: "+str(i.y)+" "+str(i.row)

class xy:
    """
    Keeps all the data to recursively split 
    into 4 quadrants and yield them out
    """

    def __init__(i,z,pz,cols):
        """
        i.kept has all data that has to be clustered yet
        """
        i.xs=0
        i.ys=0
        i.kept=[]
        i.z = z
        i.Zofxy = "__Zofxy"
        makeTable(cols,i.z)
        i.sds = []
        i.cols = cols
        i.pz = pz

    def keep(i,xyz):
        """
        Keeps updating into upon adding new rows
        """
        i.kept+=[xyz]
        i.xs+=xyz.x
        i.ys+=xyz.y
        addRow(xyz.row,i.z)
        i.sds = i.getKeptSds(i.z)

    def getKeptSds(i,temp_z):
        sds = []
        for c in dep[temp_z]:
            if c in nump[temp_z]:
                sds.append(sd[temp_z][c])
        return sds

    
    def checkSds(i,old,new):
        #print [int(i) for i in old],[int(i) for i in new]
        #Checks std dev and if atleast one of dep has less sd than parent dont prune
        #if all of deps have more sds than parent then prune
        cnt = 0.0
        if len(old) == 0:
            sys.stderr.write("Error: No continuous dependent variable\n") 
            sys.exit()
        if len(old) != len(new): sys.stderr.write("Error: old != new, Check your dep's\n")   
        for i,j in zip(old,new):
            if i<j: cnt += 1
        if cnt > len(old)/2: return True
        else: return False
        

    def tiles(i,more,mini,oldn,spy,prune,verbose=True,lvl=0):
        """
        Yields recursively clustered data in form of Row objects
        """
        n = len(i.kept)
        repeat = True
        sdcheck = False
        if n != 0:
            xmu = i.xs*1.0/n
            ymu = i.ys*1.0/n
        #print n,xmu,ymu
        if spy and n!=0:
            print '|--'*lvl+str(n)#,"xmuymu:",xmu,ymu
        if int(n) == int(oldn) or int(n) == 0 :
            repeat = False
            if int(n) != 0:
                if verbose>0: print "repeat yielding",len(i.kept)
                if prune: 
                    if i.pz != '': 
                        sdcheck = i.checkSds(i.getKeptSds(i.pz),i.sds)
                    else: sdcheck = False
                else:
                    yield i.kept
                if sdcheck: 
                    if verbose > 0: print "Not yielded"
                    i.kept = []
                    n = 0
                    repeat = False
                else:
                    yield i.kept
        oldn = n
        if repeat == True:
            if n>mini:
                if n<more:
                    if verbose>0: print "actual yielding",len(i.kept)
                    if prune: 
                        if i.pz != '': 
                            sdcheck = i.checkSds(i.getKeptSds(i.pz),i.sds)
                        else: sdcheck = True
                        if sdcheck: 
                            if verbose > 0: print "Not yielded"
                            i.kept = []
                            n = 0
                        else:
                            yield i.kept
                    else:
                        yield i.kept
                else:
                    hh = i.__class__(i.z+str(lvl)+'hh',i.z,i.cols)
                    hl = i.__class__(i.z+str(lvl)+'hl',i.z,i.cols)
                    lh = i.__class__(i.z+str(lvl)+'lh',i.z,i.cols)
                    ll = i.__class__(i.z+str(lvl)+'ll',i.z,i.cols)
                    for xyz in i.kept:
                        if xyz.x < xmu:
                            if xyz.y < ymu:
                                what = ll
                            else:
                                what = lh
                        else:
                            if xyz.y < ymu:
                                what = hl
                            else:
                                what = hh
                        what.keep(xyz)
                    quads = [ll,lh,hl,hh]
                    for xy in quads:
                        for one in xy.tiles(more,mini,oldn,spy,prune,verbose,lvl+1):
                            yield one
            else:
                if verbose>0: print "else yielding",len(i.kept)
                if prune: 
                    if i.pz != '': 
                        sdcheck = i.checkSds(i.getKeptSds(i.pz),i.sds)
                    else: sdcheck = False
                    if sdcheck: 
                        if verbose > 0: print "Not yielded"
                        i.kept = []
                        n = 0
                        repeat = False
                    else:
                        yield i.kept
                else:
                    yield i.kept
