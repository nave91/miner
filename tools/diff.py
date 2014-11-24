"""
# diff.py: Module building decision tree and finding differences 
           between clusters/branches

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

#Module for checking differences between clusters
#Check diff()
import os
import reader
import properties
import xy_proj
from stats import *
from table import *
from xy_dt import xy_dt

class Diff: 
    def __init__(self,worse,diffs,pop):
        self.worse = worse
        self.diffs = diffs
        self.pop = pop
        
    def generate(self,function,model,verbose):
        return function(self.worse,self.diffs,
                        model,n=int(self.pop),verbose=verbose)
            
    def __str__(self):
        return ">diff for: "+str(self.worse)+\
            " is: "+str(self.diffs)+" <"

    def __repr__(self):
        return ">diff for: "+str(self.worse)+\
            " is: "+str(self.diffs)+" <"

def bettercheck(one,two,verbose = False):
    #both tests passed, similar
    better,similar,worse = 0,0,0
    for fea in dep[one]:
        index = colname[one].index(fea)
        y = []
        z = []
        for row in range(0,len(data[one])):
            y.append(data[one][row][index])
        for row in range(0,len(data[two])):
            z.append(data[two][row][index])
        if verbose: print fea,">>"
        a12_check = a12(y,z) < 0.6
        if a12_check:
            if verbose: print "a12 passed"
            similar += 1
        else:
            if verbose: print "a12 failed"
            #cohens_check = cohens(y,z) < 0.3
            bootstrap_check = bootstrap(y,z)
            check = bootstrap_check#cohens_check
            if check:
                if verbose: print "bootstrap passed"
                similar += 1
            else:
                if verbose: print "bootstrap failed"
                if verbose: print mu[one][fea],mu[two][fea]
                if one in more and two in more:
                    if fea in more[one]:
                        if mu[one][fea] > mu[two][fea]:
                            better += 1
                        else:
                            worse += 1
                if one in less and two in less:
                    if fea in less[one]:
                        if mu[one][fea] < mu[two][fea]:
                            better += 1
                        else:
                            worse += 1
    if verbose: print "b",better,"s",similar,"w",worse
    if better > 0 and worse == 0:
        return True #one is better than two


def closestbetter(cluster,bid,branches,better):
    #returns bid of branch having better cluster 
    #and the better cluster
    up = down = bid
    while up>=0 or down <len(branches.collection):
        if up >= 0:
            for ncluster in branches.collection[up].clusters:
                if ncluster in better:
                    return up,ncluster
            else: up -= 1
        if down < len(branches.collection):
            for ncluster in branches.collection[down].clusters:
                if ncluster in better:
                    return down,ncluster
            else: down += 1
    sys.stderr.write("WARNING: No best Branches around.\n")
    return -1,-1
            
def addotherdiffs(diffs,z):
    d = []
    dcols = []
    for i in diffs: 
        d.append(i)
        if i[0] not in dcols: dcols.append(i[0])
    for col in colname[z]:
        if col != 'C_id':
            if col not in dcols and col not in dep[z]: 
            #append new condition lo < col < high 
                mintemp = []
                mintemp.append(col)
                mintemp.append(False)
                mintemp.append(lo[z][col])
                maxtemp = []
                maxtemp.append(col)
                maxtemp.append(True)
                maxtemp.append(hi[z][col])
                d.append(mintemp)
                d.append(maxtemp)
    return d

def mutate(conds,wcluster,appender):
    #mutates wcluster wrt conds
    temp_data = []
    for c in conds:
        ind = colname[wcluster].index(c[0])
        for d in data[wcluster]:
            le = c[1]
            if le:
                if d[ind] <= c[2]:
                    if d not in temp_data: temp_data.append(d)
            else:
                if d[ind] > c[2]:
                    if d not in temp_data: temp_data.append(d)
    wced = wcluster+appender
    reader.makeTable(colname[wcluster],wced)
    for r in temp_data:
        reader.addRow(r,wced)
    return wced

def formatout(out):
    #Takes diff as arg and returns cleaned diff
    diffout = []
    #return only unique
    for i in out:
        if i not in diffout:
            diffout.append(i)
    out = diffout[:]
                
    #Return only non-contradicting conditions
    for i,r1 in enumerate(out):
        for j,r2 in enumerate(out):
            if r1[0] == r2[0] and r1[2] == r2[2] and r1[1] != r2[1]:
                out.pop(out.index(r1))
                out.pop(out.index(r2))
    return out

def diff(z,args,model=args['m'],verbose=False,checkeach=False):
    #Returns C1zlst as diffs added to z (main cluster) conditions
    #Returns C2zlst as diffs added to wclusters(local) conditions
    zlst,branches = xy_dt(z,args)
    #form better or worse on clusters in tree
    clus = [None]
    for _,b in branches.collection.items():
        for c in b.clusters:
            if c not in clus: clus.append(c)
    temp_zlst = zlst[:]
    zlst = clus[:]
    #Better on one if diff and less 
    #Worse on none if same
    scores = {}
    for zs in zlst[1:]:
        scores[zs] = 0
    for one in zlst[1:]:
        for two in zlst[1:]:
            if one != two:
                if bettercheck(one,two):
                    if one in scores: scores[one] += 1
                    else: scores[one] = 1
    zlst = temp_zlst[:]
    scorestuple = sorted(scores.iteritems(), key=lambda x:-x[1])
    nb = len(scores)**0.5 #Number of betters = sq_rt(len(scores)) 
    betterstuple = scorestuple[:int(nb)]
    betters,worses = [],[] #List of better and worse clusters
    for i in betterstuple:
        betters.append(i[0])
    worsestuple = scorestuple[int(nb):]
    for i in worsestuple:
        worses.append(i[0])
    if verbose or args['v']>1:
        print scorestuple
        print "better",betters
        print "worse",worses
        print branches
    
    outdiffs = []
    wclus = []
    Diffs = []
    for bid,branch in branches.collection.items():
        for cluster in branch.clusters:
            if cluster in worses:
                wbid = bid
                wcluster = cluster
                if wcluster not in wclus: wclus.append(wcluster)
                bbid,bcluster = closestbetter(cluster,bid,branches,betters)
                if verbose: print "b: "+str(bcluster),",","w: "+str(wcluster)
                if bbid > -1: 
                    diffs = branches.difference(bbid,wbid)
                    appender = "C2ced"
                    if args['d']:
                        C2diffs = diffs
                    else:
                        C2diffs = addotherdiffs(diffs,wcluster)
                    C2diffs = formatout(C2diffs) #changed from C2diffs to diffs
                    
                    C2wced = mutate(C2diffs,wcluster,appender) #before mutated
                    majclass_samples = branches.collection[wbid].samples
                    Diffs.append(Diff(C2wced,C2diffs,majclass_samples*10))

                        
    return Diffs,betters,zlst,branches


if __name__ == "__main__":
    name = os.path.basename(__file__).split('.')[0]
    properties.get_args(name,args)
    #Read csvfile
    csvfile = open('../data/'+args['ifile']+'.csv','r')
    #First table is initialized with name "main"
    z = "main"
    reader.readCsv(csvfile,z)
    if args['d']:
        import tshortener
        zlst = xy_proj.xy_proj(z,data,args) 
        zshort = tshortener.tshortener(z,zlst,colname,data,dep,indep,1.0)
        z = str(zshort)
    print diff(z,args,model=args['m'])
    if args['v'] > 2:
        print differs
