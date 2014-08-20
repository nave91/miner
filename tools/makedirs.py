"""
#makedirs.py: Module to build structured directories 

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
import os
import datetime
import getopt

def usage():
    print 'Usage: python makedirs.py [-h][-v]'
    print '-h --help','Print help out'
    print '-v --verbose','Show verbose'
    print '-d --data','Build data folders'
    print '-o --out','Build out folders'
    print '-s --subdir','Build out subfolders, used with -o'

def makedirs():
    #Load arguements into a{}
    a = {'verbose': False,
         'data': False,
         'out': False,
         'subdir':False
         }
    #Fill 'em up
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                  'hvdos', 
                                   ['help', 
                                    'verbose',
                                    'data',
                                    'out',
                                    'subdir'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    #What if no arguments are given
    if not opts: 
        usage()
        sys.exit(2)
    #Handle arguements
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        if opt in ('-v', '--verbose'):
            a['verbose'] = True
        if opt in ('-d','--data'):
            a['data'] = True
        if opt in ('-o','--out'):
            a['out'] = True
        if opt in ('-s','--subdir'):
            a['subdir'] = True
    #Call function makedir
    makedir(a)


def makedir(a):
    parent = '../'
    out = 'out/'
    data = 'data/'
    out_names = ['csvs/','graphs/','dats/']
    date = datetime.date.today().strftime("%d_%B_%Y")+'/'
    
    if a['verbose']: print date
    if a['data']:
        ensure_dir(parent+data)
        ensure_dir(parent+data+date)
    if a['out']:
        ensure_dir(parent+out)
        ensure_dir(parent+out+date)
        if a['subdir']:
            for i in out_names:
                ensure_dir(parent+out+date+i)
    

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        sys.stderr.write('NOTE: Created '+d+' directory.\n')
        os.makedirs(d)
    else:
        sys.stderr.write('NOTE: Directory '+d+' already present.\n')

if __name__ == "__main__":
    sys.do_not_write_bytecode = True
    makedirs()


