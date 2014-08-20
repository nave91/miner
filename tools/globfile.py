"""
#globfile.py: Module containing global variables to
              be used across all modules

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

#
#Properties for table
#
name = ""
z = "main"
args = {'v' : -1,
        'ifile' : '',
        'e' : 'median',
        'p' : False,
        'n' : -1,
        'spy': False,
        'l' : 20,
        'c' : 'entropy',
        'smin' : -1,
        'smax' : -1,
        'm' : 'flight',
        't' : 'graphed_output',
        'chops' : [0.25,0.5,0.75,1],
        'out': 'effrange',
        'jmoo':'_',
        'dtreeprune': False,
        'i' : 0.5,
        'd' : False,
        'distprune': False
        }
#
#Info for table
#
csvindex = -1 #initialized to -1 as lists start at zero
colname = {k: [] for k in range(1)} #stores dict of names of columns
data = {k: [] for k in range(1)} #stores dict of list of lists containing each row
test = [] #stores test data
#
#metadata
#
order = {k:dict.fromkeys(colname) for k in range(1)} #stores colnames and index of column in csv
klass = {k: [] for k in range(1)} #dict of list of klass columns
more = {k: [] for k in range(1)} #dict of list of more columns
less = {k: [] for k in range(1)} #dict of list of less columns
num = {k: [] for k in range(1)} #dict of list of num columns
term = {k: [] for k in range(1)} #dict of list of term columns
dep = {k: [] for k in range(1)} #dict of list of dependent columns
indep = {k: [] for k in range(1)} #dict of list of independent columns
nump = {k: [] for k in range(1)} #dict of list containing nump column names
wordp = {k: [] for k in range(1)} #dict of list containing wordp column names
#
#for nump values
#
hi = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing highest values of nump columns 
lo = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing lowest values of nump columns
mu = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing mean values of nump columns
m2 = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing m2 values of nump columns
sd = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing std dev of nump columns
#
#for wordp values
#
mode = {k:dict.fromkeys(wordp) for k in range(1)} #dictionary containing mode of wordp columns
most = {k:dict.fromkeys(wordp) for k in range(1)} #dictionary containing most occured item of wordp columns
count = {k:dict(dict.fromkeys(wordp)) for k in range(1) }#dictionary of dictionaries of count of each item in each wordp column
#
#for all
#
n = {k:dict.fromkeys(colname) for k in range(1)} #stores number of elements in each column
isnum = True
#
#for the zeror
#
hypotheses = {}
#
#Number of unfilled columns
nulls= {k: {} for k in range(1)}
#
#For dependent variables the MRE values of ONE dep can be stored in 
mre = {}
#For shortened tree discretizer
buckets = {}
