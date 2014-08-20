"""
#tshortener.py: Module supporting pruning of 
                Decision Trees

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

import table,reader
import xy_lib

from lib import *
from _xy_dt import Branches,Branch,_tree,np


def tshortener(z,zlst,colname,data,dep,indep,patt=1.0,discretize=True):
    #The infogain techniques of pruning columns and discretization
    class Bucket:
        #class for each column with splitted pairs of data
        def __init__(self,name):
            self.pairs = [] #unsorted row pairs
            self.name = name
            self.wsum = 0
            self.dinds = {} #sorted split indexs
            self.lo = {}
            self.hi = {}
            
        def addpairs(self,pairs):
            self.pairs.append(pairs)
        def addwsum(self,wsum):
            self.wsum = wsum
        def __repr__(self):
            s = 'n: '+str(self.name)+":"
            s += ' l: '+str(len(self.pairs))
            s += ' e: '+str(self.wsum)+'\n'
            return s

    from globfile import buckets
    outcols = []

    for key,value in buckets.items():
        buckets[key] = None

    for Z in zlst[1:]:
        for c in indep[Z]:
            if c == 'C_id': continue
            if c not in buckets.keys():
                buckets[c] =  Bucket(c)
            elif buckets[c] is None:
                buckets[c] = Bucket(c)
            ind = colname[Z].index(c)
            cind = colname[Z].index('C_id')
            for r in data[Z]:
                buckets[c].addpairs((r[ind],str(r[cind])))
        reader.removeTable(Z)
    buckets = weighted_entropies(buckets)
    vals = buckets.values()[:]
    vals.sort(key=lambda x: x.wsum,reverse=False)
    for i in range(0,int(len(vals)*patt)):
        outcols.append(vals[i].name)
    zshort = 'shortenedz'
    outcols = [i for i in colname[z] if i in outcols]
    print outcols,"#infogained"
    #Convert outcols to discrete attributes
    if discretize:
        outcols = [c[1:] for c in outcols]
        print outcols,"#discretized"

    reader.makeTable(outcols+dep[z],zshort)
    for r in data[z]:
        temp = []
        for i,c in enumerate(colname[z]):
            if discretize:
                if c[1:] in outcols or c in dep[z]:
                    temp.append(r[i])
            else:
                if c in outcols+dep[z]:
                    temp.append(r[i])
        reader.addRow(temp,zshort)
    if discretize: discretizer(zshort,buckets)
    for Z in zlst:
        reader.removeTable(Z)
    #discretizer(zshort,buckets)
    return zshort

def discretizer(z,buckets):
    #discretizes data in z and updates buckets
    if args['v'] > -1:
        sys.stderr.write("\n#Discretiziing data.\n")
    for b_ind,b in buckets.items():
        if b.name[1:] in colname[z]:
            cind = indexOf(z,b.name[1:])
            for key,value in b.dinds.items():
                for v in value:
                    if key in b.lo.keys():
                        if data[z][v][cind] < b.lo[key]:
                            b.lo[key] = data[z][v][cind]
                    else:
                        b.lo[key] = data[z][v][cind]
                    if key in b.hi.keys():
                        if data[z][v][cind] > b.hi[key]:
                            b.hi[key] = data[z][v][cind]
                    else:
                        b.hi[key] = data[z][v][cind]
                    data[z][v][cind] = key
    #table.outCsv([z])
    
def distance_pruner(zlst):
    #Prunes cluster tree i.e. zlst with distance between their centroids
    

    if args['v'] > -1:
        sys.stderr.write("\n#Pruning data based on eucledian distance between clusters.\n")
        print zlst," #Old zlst before distprune"
    
    import dist
    z0 = zlst[0]
    pairs = []
    for _i,i in enumerate(data[z0]):
        for _j,j in enumerate(data[z0]):
            if i != j:
                if dist.dist(i,j,z0,indep,nump) < 0.3:
                    if [_i,_j] not in pairs and [_j,_i] not in pairs:
                        pairs.append(['__'+str(_i+1),'__'+str(_j+1)])
                    
    def repaired(pairs):
        for i in pairs:
            for j in pairs:
                if i != j :
                    if i[0] in j or i[1] in j:
                        pairs = [list(set(i+j))]+\
                        [k for k in pairs if k not in [i,j]]
                        return repaired(pairs)
        return pairs
    
    repairs = repaired(pairs)
    ps = []
    for i in repairs:
        ps+=i
    for i in zlst[1:]:
        if i not in ps:
            repairs.append([i])
    temp_row = {}
    
    for ind,p in enumerate(repairs):
        temp_row[ind] = []
        for i in p:
            temp_row[ind] += data[i]
    col = colname[z0]
    for Z in zlst:
        reader.removeTable(Z)
    zlst = [None]
    for ind,value in enumerate(temp_row.values()):
        Z = '__'+str(ind+1)
        reader.makeTable(col,Z)
        for r in value:
            reader.addRow(r[:len(r)-1]+[ind],Z)
        zlst.append(Z)
    xy_lib.buildzero(zlst,'',args['e'])

    if args['v'] > -1:
        print zlst," #New zlst after distprune"
    return zlst


def weighted_entropies(buckets):
    #calculates weighted entropies of items in buckets
    import ediv,math
    for c,b in buckets.items():
        ps = sorted(b.pairs)
        org_pairs = b.pairs[:]
        dinds = {}
        dvals = {}
        ds = ediv.ediv(ps)
        vs = [i[0] for i in ps]
        total = 0
        wsum = 0
        ls = []
        for ind,d in enumerate(ds):
            ls.append(len(d[1])*1.0)
            dinds[ind] = []
            dvals[ind] = d[1]
        for ind,o in enumerate(org_pairs):
            for key,value in dvals.items():
                if o in value:
                    dinds[key].append(ind)
                    dvals[key].pop(value.index(o))
        b.dinds = dinds
        #weighted sum of entropies based on indexes
        for l in ls:
            if l!= 0:
                e = -(l/len(ps))*math.log(l/len(ps),2)
            else: e = 0.0
            wsum += e*1/l
            total += 1/l
            buckets[c].wsum = wsum/total
    return buckets
    



def prune_similar(decision_tree,args,feature_names=None,
                         max_depth=None,delete_more=False,prune=False):
    #Prunes sub trees in dtree with similar majority class
    #delete_more deletes leaves with more than one majority class

    if args['v'] > -1:
        sys.stderr.write("\n#Pruning similar trees.\n\n")

    def branching(tree, left, node_id, criterion, parent):
        value = tree.value[node_id]
        if tree.n_outputs == 1:
            value = value[0, :]
        if tree.children_left[node_id] == _tree.TREE_LEAF and tree.children_right[node_id] == _tree.TREE_LEAF:
            #temp = np.where(value!=0)[0].tolist()
            temp = np.where(value==max(value))[0].tolist()
            temp = ['__'+str(i+1) for i in temp]
            more = '---> more' if len(temp)>1 else ''
            samples = tree.n_node_samples[node_id]
            if delete_more:
                if len(temp) > 1:
                    if left:
                        if tree.children_right[parent] != _tree.TREE_LEAF:
                            tree.children_left[parent] = _tree.TREE_LEAF
                        else:
                            r = tree.value[tree.children_right[parent]][0].tolist()
                            l = value.tolist()
                            tree.value[node_id][0] = np.array([i+j for i,j in zip(l,r)])
                            
                    else:
                        if tree.children_left[parent] != _tree.TREE_LEAF:
                            tree.children_right[parent] = _tree.TREE_LEAF
                        else:
                            l = tree.value[tree.children_left[parent]][0].tolist()
                            r = value.tolist()
                            tree.value[node_id][0] = np.array([i+j for i,j in zip(l,r)])
                            
            return "%s  # samples = %s #  %s"  \
                % (temp,
                   samples,
                   more)
        else:
            if feature_names is not None:
                feature = feature_names[tree.feature[node_id]]
            else:
                feature = "X[%s]" % tree.feature[node_id]
            
            #add condition at node to current branch
            return "%s <= %.4f samples = %s" \
                   % (feature,
                      tree.threshold[node_id],
                      tree.n_node_samples[node_id])
    
    def recurse(tree, left, node_id, criterion, parent=None, depth=0, spy=args['spy']):
        
        lclus = []
        rclus = []
        
        def collect(clus,t,l,n_id,c,p):
            val = t.value[n_id]
            if t.n_outputs == 1:
                val = val[0,:]
            
            test_for_exclusives = np.equal(val,np.array([0.0]*len(val)))
            if False in test_for_exclusives:
                clu = np.where(val==max(val))[0].tolist()
                for i in clu:
                    if i not in clus: clus.append(i)
            return clus

        if node_id == _tree.TREE_LEAF:
            raise ValueError("Invalid node_id %s" % _tree.TREE_LEAF)

        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]

        # Add node with description
        if max_depth is None or depth <= max_depth:
            str = branching(tree, left, node_id, criterion, parent)
            clus= []
            clus = collect(clus,tree, left, node_id, criterion, parent)
            if spy:
                print depth*"|-"+" "+str
            if left_child != _tree.TREE_LEAF:
                left = True
                lclus =recurse(tree, left, left_child, criterion=criterion, parent=node_id,depth=depth + 1)
                left = False
                rclus = recurse(tree, left, right_child, criterion=criterion, parent=node_id,depth=depth + 1)
        if lclus == rclus and lclus and rclus and prune:
            tree.value[node_id] = tree.value[left_child]
            tree.children_left[node_id] = _tree.TREE_LEAF
            tree.children_right[node_id] = _tree.TREE_LEAF
            print "--"*25,"This Tree"
        return clus
        
    left = None
    if isinstance(decision_tree, _tree.Tree):
        recurse(decision_tree, left, 0, criterion=args['c'])
    else:
        recurse(decision_tree.tree_, left, 0, criterion=args['c'])
    
    return None
