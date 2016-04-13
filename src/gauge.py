#!/usr/bin/env python
#import os, sys
#import matplotlib

# http://nicolasfauchereau.github.io/climatecode/posts/drawing-a-gauge-with-matplotlib/

#from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np

from matplotlib.patches import Circle, Wedge

def degree_range(n): 
    start = np.linspace(0,270,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,270,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points

def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

def scaleto(value, fromrange, torange):
    x0,x1 = fromrange
    y0,y1 = torange
    return (((value - x0) * (y1 - y0)) / (x1 - x0)) + y0
    
def deg(pos, minmax):
    return scaleto(pos, minmax, [225.0, -45.0])
    #return 225 - 270.0*(pos-minmax[0])/minmax[1]

def gauge(position=0.0, minmax=[0.0, 100.0], nticks=10, units='[1]', title='value',filename = None, ranges=None):
    #from matplotlib import rcParams
    #params = {'backend': 'Agg',
    #      'savefig.dpi' : 100,
    #      'figure.figsize': [6, 6]}

    _, ax = plt.subplots()
    #rcParams.update(params)
    # plot the outer circle
    ax.add_patch(Circle((0, 0), radius=0.5, edgecolor='k', facecolor='w'))
    
    # plot the inner arc
    #ax.add_patch(Arc((0, 0), 0.9, 0.9, angle=-45.0, theta1=0.0, theta2=270.0))
    
    #plot range wedges
    for r in ranges:
        theta1 = deg(r['to'], minmax)
        theta2 = deg(r['from'], minmax)
        ax.add_patch(Wedge((0, 0), 0.5, theta1, theta2, width=0.05, alpha=0.4, color=r['color']))
    position = max(minmax[0],position)
    position = min(minmax[1],position)
    pos = deg(position, minmax)
    
    
    """
    plot ticks and labels
    """
    minortickspos = np.linspace(deg(minmax[0],minmax),deg(minmax[1],minmax), nticks*10+1)
    ticklabels = np.linspace(minmax[0], minmax[1], nticks+1)
    for i, tickpos in enumerate(minortickspos):
        c = np.cos(np.radians(tickpos))
        s = np.sin(np.radians(tickpos))
        if i % 5 <> 0 and i % 10 <> 0:
            ax.plot([0.48*c, 0.5*c], [0.48*s, 0.5*s],'k')
        # plot 5 ticks    
        if i % 5 == 0 and i % 10 <> 0:
            ax.plot([0.46*c, 0.5*c], [0.46*s, 0.5*s],'k')
            
        if i % 10 == 0:
            ax.plot([0.45*c, 0.5*c], [0.45*s, 0.5*s],'k', linewidth=2)
            ax.text(0.4*c, 0.4*s,ticklabels[i/10], ha='center', va='center', fontsize=14)
        
    
    """
    plot the arrow
    """
    pinlength = 0.35 # plus headlength of 0.1 gives 0.45
    ax.arrow(0, 0, pinlength * np.cos(np.radians(pos)), pinlength * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.04, head_length=0.1, fc='orange', ec='orange')
    
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='orange'))
    
    
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='k', zorder=11))

    ax.text(0.0, -0.15, units, ha='center', va='center', fontsize=24)
    ax.text(0.0, -0.35, title, ha='center', va='center', fontsize=36)
    
    """
    removes frame and ticks, and makes axis equal and tight
    """
    
    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.set_aspect(1.)
    #ax.axis('equal')
    plt.tight_layout()
    
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename, dpi=70, bbox_inches='tight')
    plt.close()
    

        
if __name__ == '__main__':
    gauge(-135.964, minmax=[-160,-130.0],nticks=3,title='Cryo Temp', units=u"\N{DEGREE SIGN}C", ranges=[{'color':'g', 'from':-140, 'to':-145}])
    #gauge(-155.64, minmax=[-130.0,-80.0])