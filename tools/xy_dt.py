"""
#xy_dt.py: Module for building decision trees

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

import tshortener
import sklearn as sk

from xy_proj import *
from xy_lib import *
from _xy_dt import *
from sklearn import tree
from sklearn.tree import _tree

def xy_dt0(decision_tree,feature_names=None,
           max_depth=None):

    if args['v'] > -1:
        sys.stderr.write("\n#Decision Tree. Generated using CART of scikit-learn.\n")

    #Create new Branches Object
    branches = Branches()
    
    def branching(tree, branches, cur_branch, left, node_id, criterion):
        
        value = tree.value[node_id]
        if tree.n_outputs == 1:
            value = value[0, :]
        if tree.children_left[node_id] == _tree.TREE_LEAF and tree.children_right[node_id] == _tree.TREE_LEAF:
            branches.leaves += 1
            temp = np.where(value==max(value))[0].tolist()
            cur_branch.add_clusters(temp)
            cur_branch.add_samples(tree.n_node_samples[node_id])
            branches.add(cur_branch)
            if left:
                #If its a leaf then change last condition
                cur_branch.change_last_condition(False)
            temp = ['__'+str(i+1) for i in temp]
            return "%s  # samples = %s # branch_id = %s"  \
                % (temp,
                   tree.n_node_samples[node_id], 
                   str(len(branches.collection.keys())-1))
        else:
            branches.nodes += 1
            if feature_names is not None:
                feature = feature_names[tree.feature[node_id]]
            else:
                feature = "X[%s]" % tree.feature[node_id]
            
            #add condition at node to current branch
            
            cur_branch.add_condition(feature,True,tree.threshold[node_id])
            return "%s <= %.1f samples = %s" \
                   % (feature,
                      tree.threshold[node_id],
                      tree.n_node_samples[node_id])
       
    def recurse(tree, branches, cur_branch, left, node_id, criterion, parent=None, depth=0, spy=args['spy']):
        
        
        if node_id == _tree.TREE_LEAF:
            raise ValueError("Invalid node_id %s" % _tree.TREE_LEAF)

        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]

        # Add node with description
        if max_depth is None or depth <= max_depth:
            str = branching(tree, branches, cur_branch, left, node_id, criterion)
            if spy:
                print depth*"|-"+" "+str
            if left_child != _tree.TREE_LEAF:
                left = True
                recurse(tree, branches, cur_branch, left, left_child, criterion=criterion, parent=node_id,
                        depth=depth + 1)
            if right_child != _tree.TREE_LEAF:
                # Changed last condtion as we are now on right side of condition
                cur_branch.change_last_condition(False)
                left = False
                recurse(tree, branches, cur_branch, left, right_child, criterion=criterion, parent=node_id,
                        depth=depth + 1)
                # Removed the condition as it exited out of that condition
                cur_branch.remove_last_condition()
    cur_branch = Branch()
    left = None
    if isinstance(decision_tree, _tree.Tree):
        recurse(decision_tree, branches, cur_branch, left, 0, criterion=args['c'])
    else:
        recurse(decision_tree.tree_, branches, cur_branch, left, 0, criterion=args['c'])
    
    return branches

           
def xy_dt(z,args,pdffile=False):
        
    zlst = xy_proj(z,data,args)
    if args['distprune']:
        zlst = tshortener.distance_pruner(zlst)
    
    clustered_data = regroup(zlst,"data")
    clustered_target = regroup(zlst,"target")
    #Convert lists to np.ndarrays
    clustered_target = np.asarray(np.float_(clustered_target))
    cd_temp = []
    for row in clustered_data:
        row_temp = []
        for item in row:
            row_temp.append(np.float_(item))
        cd_temp.append(row_temp)
    clustered_data = np.asarray(cd_temp)
    #Build Classifier
    clf = tree.DecisionTreeClassifier(min_samples_leaf=args['l'],criterion=args['c'])#,max_depth=5)
    clf = clf.fit(clustered_data,clustered_target)
    if pdffile:
        from sklearn.externals.six import StringIO
        with open(z+"iris.dot", 'w') as f:
            f = tree.export_graphviz(clf, out_file=f,feature_names=colname[z])
    
    if args['dtreeprune']:
        branches = tshortener.prune_similar(clf,args,colname[zlst[1]],delete_more=True,prune=True)
        print "\n","#"*25,"New Tree","#"*25
    
    branches = xy_dt0(clf,colname[zlst[1]])
    return zlst,branches


if __name__ == "__main__":
    sys.do_not_write_bytecode = True
    name = os.path.basename(__file__).split('.')[0]
    get_args(name,args)
    #Read csvfile
    csvfile = open('../data/'+args['ifile']+'.csv','r')
    #First table is initialized with name "main"
    z = "main"
    readCsv(csvfile,z)
    
    import tshortener
    zlst = xy_proj(z,data,args) 
    zshort = tshortener.tshortener(z,zlst,colname,data,dep,indep,0.50)
    z = str(zshort)
    
    zlst,branches = xy_dt(z,args)


    if args['v'] > -1:
        print branches
        needmore = False
        if needmore:
            for key,branch in branches.collection.items():
                print 'Group:',key,branch.clusters
                outCsv(branch.clusters)
 
            
