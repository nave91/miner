"""
#_xy_dt.py: Support Module for xy_dt.py

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

import copy
import numpy as np
from sklearn import tree
from sklearn.tree import _tree

class Branch:
    def __init__(self):
        self.bid = 0
        self.clusters = []
        self.features = []
        self.conditions = [] #True if <=
        self.thresholds = []
        self.values = None
        self.samples = 0
    def __repr__(self):
        s = ""
        for i in range(0,len(self.features)):
            s+=" "+str(self.features[i])
            if self.conditions[i]:
                s+=" <= "
            else:
                s+=" > "
            s+=str(round(self.thresholds[i],2))
            s+=", "
        return str(self.clusters) + str(s) + "\n"
        
    def add_condition(self,feature,condition,threshold):
        from globfile import args,buckets
        if args['d']:
            self.features.append(feature)
            self.conditions.append(condition)
            buck_fea = [ i for i in buckets.keys() if feature == i[1:]][0]
            if condition:
                if int(threshold) in buckets[buck_fea].hi.keys():
                    self.thresholds.append(buckets[buck_fea].hi[int(threshold)])
                else:
                    self.thresholds.append(buckets[buck_fea].hi[0])
            else:
                if int(threshold) in buckets[buck_fea].lo.keys():
                    self.thresholds.append(buckets[buck_fea].lo[int(threshold)])
                else:
                    self.thresholds.append(buckets[buck_fea].lo[0])
        else:
            self.features.append(feature)
            self.conditions.append(condition)
            self.thresholds.append(threshold)

    def add_clusters(self,list):
        self.clusters = ["__"+str(i+1) for i in list]
    
    def add_samples(self,num):
        self.samples = num

    def remove_last_condition(self):
        self.features.pop(len(self.features)-1)
        self.conditions.pop(len(self.conditions)-1)
        self.thresholds.pop(len(self.thresholds)-1)

    def change_last_condition(self,condition):
        self.conditions[len(self.conditions)-1] = condition

    def get_condition(self,index):
        return [self.features[index],self.conditions[index],round(self.thresholds[index],1)]
        
class Branches:
    def __init__(branches):
        branches.collection = {}

    def __getitem__(branches,i):
        return branches.collection[i]

    def add(branches,branch):
        branch.bid = len(branches.collection.keys())
        branches.collection[branch.bid] = copy.deepcopy(branch)

    def difference(self,bid1,bid2):
        #bid1 is better than bid2,
        out = []
        branch1 = self.collection[bid1]
        branch2 = self.collection[bid2]
        for ind1,feature in enumerate(branch1.features):
            if feature in branch2.features:
                ind2 = branch2.features.index(feature)
                if branch1.thresholds[ind1] == branch2.thresholds[ind2]:
                    if branch1.conditions[ind1] != branch2.conditions[ind2]:
                        out.append(branch1.get_condition(ind1))
                    else: #adds similar conditions as well
                        if branch1.get_condition(ind1) not in out:
                            out.append(branch1.get_condition(ind1))
                else: out.append(branch1.get_condition(ind1))
            else:
                out.append(branch1.get_condition(ind1))
        return out
                
    def __repr__(branches):
        s = "\n\nBranches:\n"
        for key,i in branches.collection.items():
            s+=str(key)
            s+="---"
            s+=str(i)
        return s
