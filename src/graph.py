import matplotlib.pyplot as plt
import numpy as np
import sys
import math
sys.do_dot_write_bytecode = True

def graph2d(listx,listy,labelx,labely,legend,out='out.png'):
    sys.stderr.write('NOTE: Graph is generated with title \"'
                     +str(out)+'\"'
                     +'\n legend: '
                     +str(legend) 
                     +'\n labels'
                     +'\n x: '+str(labelx)
                     +'\n y: '+str(labely))
    sys.stderr.write('\nNOTE: Check \"'+str(out)+'\" for the graph\n')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(listy,label = labely)
    xtics = [listx[int(0.1*i*len(listx))] for i in range(0,10)] 
    ax.xaxis.set_ticks(xtics)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    ax.legend()    
    plt.savefig(out)

def graph2dmultiple_withlog(listx,dicty,nldicty,labelx,labely,legend,out='out.png',ticks=-1):
    sys.stderr.write('NOTE: Graph is generated with title \"'
                     +str(out)+'\"'
                     +'\n legend: '
                     +str(legend) 
                     +'\n labels'
                     +'\n x: '+str(labelx)
                     +'\n y: '+str(labely))
    sys.stderr.write('\nNOTE: Check \"'+str(out)+'\" for the graph\n')
    fig = plt.figure(dpi=80)
    ax = fig.add_subplot(111)
    ax.set_title(out)
    colors = ['b','r','y','c']
    lstyle = ['-','--','-.',':']
    i = 0
    for key,value in dicty.items():
        ax.plot(value,label = key,color=colors[i],linestyle='-')#,linestyle=lstyle[i])
        i+=1
    xtics = [listx[int(0.1*i*max(listx))] for i in range(0,10)] 
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    if legend: ax.legend(loc=2,prop={'size':8})
    
    ax2 = ax.twinx()
    i = 0
    for key,value in nldicty.items():
            ax2.plot(value,label = 'log('+str(key)+')',color=colors[i],linestyle='--')#,linestyle=lstyle[i])
            i+=1
    if ticks>0:
        #plt.xticks(np.arange(min(listx),max(listx),ticks))
        #get max listy
        listy =[]
        for key,value in nldicty.items():
            listy += value
        plt.yticks(np.arange(math.floor(min(listy)),math.ceil(max(listy)),ticks))
    if legend: ax2.legend(loc=1,prop={'size':8})
    plt.savefig(out)
    
def graph2dmultiple(listx,dicty,labelx,labely,legend,out='out.png',ticks=-1):
    sys.stderr.write('NOTE: Graph is generated with title \"'
                     +str(out)+'\"'
                     +'\n legend: '
                     +str(legend) 
                     +'\n labels'
                     +'\n x: '+str(labelx)
                     +'\n y: '+str(labely))
    sys.stderr.write('\nNOTE: Check \"'+str(out)+'\" for the graph\n')
    fig = plt.figure(dpi=80)
    ax = fig.add_subplot(111)
    ax.set_title(out)
    colors = ['b','r','y','c']
    lstyle = ['-','--','-.',':']
    i = 0
    for key,value in dicty.items():
        ax.plot(value,label = key,color=colors[i],linestyle=lstyle[i])
        i+=1
    xtics = [listx[int(0.1*i*max(listx))] for i in range(0,10)] 
    #ax.xaxis.set_ticks(xtics)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    if legend: ax.legend(loc=2)
    if ticks>0:
        #plt.xticks(np.arange(min(listx),max(listx),ticks))
        #get max listy
        listy =[]
        for key,value in dicty.items():
            listy += value
        plt.yticks(np.arange(math.floor(min(listy)),math.ceil(max(listy)),ticks))
    plt.savefig(out)
