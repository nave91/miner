#Module to define arguments and properties
import sys
import os
import argparse
sys.do_not_write_bytecode=True

def get_args(name,args):
    desc = {
        "reader" : "Reads ifile into table like structure",
        "dist" : "Calculates distance between 2 rows of table",
        "xy_proj" : "XY module that uses xy.py to cluster rows spectrally and project it on 2D space as rows",
        "xy_dt" : "Builds CART tree with cluster id's as outcomes and attributes as decisions",
        "diff" : "Uses xy_dt to use differences between various branches and shows techniques C1-C3 and C2-C3",        
    }

    if name in desc:
        parser = argparse.ArgumentParser(description=desc[name])
    else:
        parser = argparse.ArgumentParser()

    #Adding arguements
    parser.add_argument("ifile", type=str,
                        help="input file to load into table")
    parser.add_argument("-v","--verbose",type=int,
                        help="increase output verbosity")
    parser.add_argument("-e","--evaluate",type=str,
                        help="default is median, can change to mean")
    parser.add_argument("-p","--prune",
                        help="default is false, can change to true to prune childs having sd > parent in spec clu",
                        action="store_true")
    parser.add_argument("-n","--near",type=int,
                        help="default is all, can change to nth percent, returns clusters with n nearest neighbors to centroid")
    parser.add_argument("-l","--leaf",type=int,
                        help="default is 20, can change to n, sets min_samples_leaf of dtree")
    parser.add_argument("-c","--criterion",type=str,
                        help="default is entropy, can change to gini")
    parser.add_argument("-s","--size",type=str,
                        help="range of cluster size, default is sq_rt(total)<2*sq_rt(total), specify as 1,2")
    parser.add_argument("-t","--title",type=str,
                        help="Specify title of graph, avoid spaces-use underscores. default is \'graphed_output\'") 
    parser.add_argument("--spy",
                        help="default is false, can change to true to see trees",
                        action="store_true")
    parser.add_argument("--dtreeprune",
                        help="default is false, can change to true to prune decision trees",
                        action="store_true")
    parser.add_argument("-d","--discretize",
                        help="discretizes data. Default is false.",
                        action="store_true")
    parser.add_argument("-i","--infogain",
                        help="Uses infogain to prune columns. Default is 0.5, can change to .XX value.")
    parser.add_argument("--distprune",
                        help="Prunes cluster tree with distance between centroids.(0.3)", 
                        action="store_true")
    a = parser.parse_args()
    
    #Handling arguements
    if a.verbose > -1:
        sys.stderr.write("Note: Verbose level set to "+str(a.verbose)+"\n")
        args['v'] = a.verbose
    if a.ifile:
        args['ifile'] = a.ifile
    if a.evaluate:
        if a.evaluate in ['mean','median']:
            sys.stderr.write("Note: Evaluate is set to "+str(a.evaluate)+"\n")
            args['e'] = a.evaluate
        else:
            sys.stderr.write("Error: Measure can be either mean or median\n")
            sys.exit()
    if a.prune:
        args['p'] = a.prune 
    if a.spy:
        args['spy'] = a.spy
    if a.near > -1:
        sys.stderr.write("Note: Returns only "+str(a.near)+" percent nearest to the centroid\n")
        args['n'] = a.near
    if a.leaf != 20 and a.leaf > 0:
        sys.stderr.write("Note: Min samples per leaf is set to "+str(a.leaf)+"\n")
        args['l'] = a.leaf
    if a.criterion:
        if a.criterion in ['entropy','gini']:
            sys.stderr.write("Note: "+str(a.criterion)+" is used as criterion\n")
            args['c'] = a.criterion
        else:
            sys.stderr.write("Error: Criterion can be entropy or gini")
    if a.size:
        sys.stderr.write("Note: Standard cluster size is set to ("+str(a.size)+")\n")
        temp = a.size.split(',')
        args['smin'] = int(min(temp))
        args['smax'] = int(max(temp))
    if a.title:
        sys.stderr.write("Note: Title set to "+str(a.title)+"\n")
        args['t'] = a.title
    if a.dtreeprune:
        sys.stderr.write("Note: Pruning leaves with more than one cluster and sub-trees with same majority class\n")
        args['dtreeprune'] = a.dtreeprune
    if a.discretize:
        sys.stderr.write("Note: Discretizing data\n")
        args['d'] = a.discretize
    if a.infogain:
        args['i'] = float(a.infogain)
        sys.stderr.write("Note: Taking only top "+str(args['d'])+" of columns and pruning rest\n")
    if a.distprune:
        args['distprune'] = True
