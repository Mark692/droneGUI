'''
Created on Oct 25, 2018
This module is used to manage animations via matplotlib

*Link for guide and download: https://matplotlib.org/
*Link for Python + MatPlotLib tutorial: https://pythonprogramming.net/embedding-live-matplotlib-graph-tkinter-gui/?completed=/how-to-embed-matplotlib-graph-tkinter-gui/

@author: mark
'''

# import matplotlib.animation as animation
from matplotlib.figure import Figure

from matplotlib import style

import matplotlib.pyplot as plt

style.use('ggplot')

myFigure = Figure(figsize=(5, 4), dpi=100)
a = myFigure.add_subplot(111)  # f.add_subplot(ijk): i-th plot, j rows, k columns


def animate(i):
    '''
    src = Log file to graph live
    '''
    
    src = 'live_Data.txt'
    pullData = open(src, 'r').read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    a.clear()
    a.plot(xar, yar)
    

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animatePlot(i):
    
# Non si aggiorna live. 
# Richiede un pyplot.show() alla fine per mostrare il grafico

    pullData = open("live_Data.txt", "r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar, yar)
    
    
