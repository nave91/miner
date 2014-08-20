"""
#stats.py: Module supporting different stat tests

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

#Modules developed by Dr.Tim Menzies. refer http://menzies.us/cs472
import sys
sys.dont_write_bytecode = True
import random
from lib  import *

#---- Cool Classes ----------------------------

class Charmed:
  "Our objects are charming."
  def __repr__(i):
    """
    This Charmed object knows how to print
    all their slots, except for the private ones
    (those that start with "_").
    """
    args = []
    for key,val in vars(i).items(): 
      if key[0] != "_":
        args += ['%s=%s'% (key,val)]
    what = i.__class__.__name__
    return '%s(%s)' % (what, ', '.join(args)) 

class Thing(Charmed):
  """Norvig's shortcut for creating objects that 
  that holds data in several fields."""
  def __init__(self, **entries): 
    self.__dict__.update(entries)

class Sample(Charmed):
  "Keep a random sample of stuff seen so far."
  def __init__(i,size=64):
    i._cache, i.size, i.n = [],size, 0.0
    i._ordered=False
  def sorted(i):
    if not i._ordered:
      i._cache = sorted(i._cache)
      i._ordered=True
    return i._cache
  def seen(i,x):
    i.n += 1
    if len(i._cache) < i.size : 
      i._cache += [x]
      i._ordered=False
    else:
      if random.random() <= i.size/i.n:
        i._cache[int(random.random()*i.size)] = x
        i._ordered=False


def bootstrap(y0,z0,conf=0.05,b=1000):
    """The bootstrap hypothesis test from
    p220 to 223 of Efron's book 'An
    introduction to the boostrap."""
    class total():
        "quick and dirty data collector"
        def __init__(i,some=[]):
            i.sum = i.n = i.mu = 0 ; i.all=[]
            for one in some: i.put(one)
        def put(i,x):
            i.all.append(x);
            i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
        def __add__(i1,i2): return total(i1.all + i2.all)
    def testStatistic(y,z): 
        """Checks if two means are different, tempered
        by the sample size of 'y' and 'z'"""
        tmp1 = tmp2 = 0
        for y1 in y.all: tmp1 += (y1 - y.mu)**2 
        for z1 in z.all: tmp2 += (z1 - z.mu)**2
        s1    = float(tmp1)/(y.n - 1)
        s2    = float(tmp2)/(z.n - 1)
        delta = z.mu - y.mu
        if s1+s2:
            delta =  delta/((s1/y.n + s2/z.n)**0.5)
        return delta
    def one(lst): return lst[ int(any(len(lst))) ]
    def any(n)  : return random.uniform(0,n)
    y, z   = total(y0), total(z0)
    x      = y + z
    tobs   = testStatistic(y,z)
    yhat   = [y1 - y.mu + x.mu for y1 in y.all]
    zhat   = [z1 - z.mu + x.mu for z1 in z.all]
    bigger = 0.0
    for i in range(b):
        if testStatistic(total([one(yhat) for _ in yhat]),
                         total([one(zhat) for _ in zhat])) > tobs:
            bigger += 1
    return bigger / b < conf

def cohens(y,z):
    #cohens d=(x1-x2)/s
    x1 = sum(y)/len(y)
    x2 = sum(z)/len(z)
    yz = y+z
    avg = sum(yz)/len(yz)
    sums = 0
    for i in yz:
        sums += (avg-i)**2
    stdev = (sums/len(yz))**0.5
    return abs(x1-x2)/stdev
    
    
#############-- A12 TEST --##############

def a12old(lst1,lst2,rev=True):
  "how often is x in lst1 more than y in lst2?"
  more = same = 0.0
  for x in lst1:
    for y in lst2:
      if   x==y : same += 1
      elif rev     and x > y : more += 1
      elif not rev and x < y : more += 1
  return (more + 0.5*same) / (len(lst1)*len(lst2))

def a12(lst1,lst2, gt= lambda x,y: x > y):
  "how often is x in lst1 more than y in lst2?"
  def loop(t,t1,t2): 
    while t1.i < t1.n and t2.i < t2.n:
      h1 = t1.l[t1.i]
      h2 = t2.l[t2.i]
      if gt(h1,h2):
        t1.i  += 1; t1.gt += t2.n - t2.i
      elif h1 == h2:
        t2.i  += 1; t1.eq += 1; t2.eq += 1
      else:
        t2,t1  = t1,t2
    return t.gt*1.0, t.eq*1.0
  #--------------------------
  lst1 = sorted(lst1, cmp=gt)
  lst2 = sorted(lst2, cmp=gt)
  n1   = len(lst1)
  n2   = len(lst2)
  t1   = Thing(l=lst1,i=0,eq=0,gt=0,n=n1)
  t2   = Thing(l=lst2,i=0,eq=0,gt=0,n=n2)
  gt,eq= loop(t1, t1, t2)
  return gt/(n1*n2) + eq/2/(n1*n2)
