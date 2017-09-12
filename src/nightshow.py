#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2014

@author: jwe

produce graphs for the environmental plots of stella
'''
import psycopg2
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import numpy as np
import config
import os

class NightShow():
    def __init__(self):
        """
        get the values for the last 24 hours from the database
        """
        
        database = psycopg2.connect(database=config.dbname, user=config.dbuser, host=config.dbhost, password=config.dbpassword) 
        self.plotpath = config.plotpath
        cursor = database.cursor()
        columns = [ 'date', 'tbay', 'tspec', 'telectr', 'ttable', 'taussen', 'hbay', \
                   'hspec', 'helectr', 'haussen', 'solz', 'paussen', 'wind' , \
                   'windpeak', 'winddir', 'windbay', 'lx',  'rain', 'good' , 'dust', \
                   'tlounge', 'tlab', 'toil1', 'toil2']
        colstring = ', '.join(columns)
        query = """SELECT %s 
        FROM env 
        WHERE date>=current_timestamp-interval '1 day' 
        ORDER BY date;""" % colstring
        cursor.execute(query)
        result = cursor.fetchall()
        
        self.data = {}
        for c in columns:
            i = columns.index(c)
            self.data[c] = [r[i] for r in result]
        
        
        self.dates = self.data['date']
        from matplotlib import rcParams
        params = {'backend': 'Agg',
              'savefig.dpi' : 100,
              'figure.figsize': [9.6, 6]
              }
        rcParams.update(params)
     
    def plot_bar(self, axis):
        """
        plot a green vertical bar for every five minute where the conditions are 
        good
        """
        
        # width of the bar is 5 minutes (= datainterval)
        barwidth = 5.0/(24*60)
        gdates=[]
        for i in range(len(self.dates)):
            if self.data['good'][i]=='y': gdates.append(self.dates[i])
        heights = np.repeat(axis.get_ylim()[1]-axis.get_ylim()[0], len(gdates))
        bottoms = np.repeat(axis.get_ylim()[0], len(gdates))
        plt.bar(gdates, heights, barwidth, bottoms, color='g', alpha=0.25, linewidth=0)

    def plot_rain(self, axis):
        """
        plot a green vertical bar for every five minute where the conditions are 
        good
        """
        
        # width of the bar is 5 minutes (= data interval)
        barwidth = 5.0/(24*60)
        raindates=[]
        for i in range(len(self.dates)):
            if self.data['rain'][i]>0.002: raindates.append(self.dates[i])
        heights = np.repeat(axis.get_ylim()[1]-axis.get_ylim()[0], len(raindates))
        bottoms = np.repeat(axis.get_ylim()[0], len(raindates))
        plt.bar(raindates, heights, barwidth, bottoms, color='b', alpha=0.25, linewidth=0)

    
    def plot_xticks(self, nolabels=False):
        """
        plot the xticks every two hours (08h 10h 12h)
        """
        start = self.data['date'][0]
        end = self.data['date'][-1]
        hours = []
        labels = []
        start = start.replace(minute=0,second=0,microsecond=0)
        current = start + datetime.timedelta(hours=1)
        while current<end:
            hours.append(current)
            labels.append('%02dh' % current.hour)
            current += datetime.timedelta(hours=2)
        if nolabels: 
            plt.xticks(hours,'')
        else:
            plt.xticks(hours, labels)
            plt.xlabel('time '+str(end))
    
    def temperatures(self):
        """
        plot the temperatures
        """
        ax = plt.subplot(3,1,1)
        plt.title('Temperatures')
        plt.plot(self.dates, self.data['tbay'],'b', label='bay')
        plt.plot(self.dates, self.data['taussen'],'r', label='outside')
        self.splplot(self.dates, self.data['tlounge'],'g', label='lounge')
        try:
            ax.legend(loc=2, fontsize='small')
        except TypeError:
            ax.legend(loc=2)
        self.plot_bar(ax)
        self.plot_xticks(nolabels=True)
        plt.ylabel(u"\N{DEGREE SIGN}C")
    
        ax = plt.subplot(3,1,2)
        plt.plot(self.dates, self.data['tspec'],'r', label='spec')
        self.splplot(self.dates, self.data['ttable'],'g', label='table')
        try:
            ax.legend(loc=2, fontsize='small')
        except TypeError:
            ax.legend(loc=2)
        self.plot_bar(ax)
        self.plot_xticks(nolabels=True)
        plt.ylabel(u"\N{DEGREE SIGN}C")
        
        ax = plt.subplot(3,1,3)
        self.splplot(self.dates, self.data['telectr'], 'r', label='electr', smooth=4)
        self.splplot(self.dates, self.data['tlab'],'b', label='lab')
        self.splplot(self.dates, self.data['toil1'],'c', label='oil1', smooth=1)
        self.splplot(self.dates, self.data['toil2'],'m', label='oil2', smooth=1)
        try:
            ax.legend(loc=2, fontsize='small')
        except TypeError:
            ax.legend(loc=2)
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel(u"\N{DEGREE SIGN}C")
        plt.savefig(os.path.join(self.plotpath,'temperatures.svg'))
        plt.close()

    def humidities(self):
        """
        plot the humidities
        """
        ax = plt.subplot(1,1,1)
        plt.title('Humidities')
        plt.plot(self.dates, self.data['hbay'],'b', label='bay')
        plt.plot(self.dates, self.data['haussen'],'r', label='outside')
        plt.plot(self.dates, self.data['helectr'],'g', label='electr')
        plt.plot(self.dates, self.data['hspec'],'orange', label='spectr')
        try:
            ax.legend(loc=2, fontsize='small')
        except TypeError:
            ax.legend(loc=2)
        plt.ylim(0,100)
        self.plot_rain(ax)
        self.plot_bar(ax)
        self.plot_xticks()
        plt.grid()
        plt.ylabel('rel. %')
        plt.savefig(os.path.join(self.plotpath,'humidities.svg'))
        plt.close()

    def splplot(self, x, y, color, label='', smooth=0.5):
        """
        plot a spline interpolated (smoothed) version of the data
        """
        try:
            import scipy.interpolate as spyint
        except ImportError:
            plt.plot(x, y, color, label=label)
        else:
            from astronomy import mjd, caldat
            
            mdates = np.array([mjd(d) for d in x])
            sp = spyint.splrep(mdates, y, s=smooth)
            x1 = np.linspace(mdates[0], mdates[-1], 288)
            xdates = [caldat(xi) for xi in x1]
            y1 = spyint.splev(x1, sp)
            plt.plot(xdates, y1, color, label=label)

    def pressure(self):
        """
        plot the pressure in mbar
        calculate the pressure at sealevel corrected by temperature
        """
        #from numpy import array,power
        #p0 = array(self.data['paussen'])/0.769584
        t0 = np.array(self.data['taussen'])+ 273.15 
        p0 = np.array(self.data['paussen'])/np.power(1.0-(0.0065*2200.0/t0),5.255)
        
        ax = plt.subplot(1,1,1)
        plt.title('Pressure')
        #plt.plot(self.dates, self.data['paussen'],'g')
        self.splplot(self.dates, p0,'k')
        yticks = np.array(plt.yticks()[0])
        plt.yticks(yticks,['%4.0f' % y for y in yticks])
        self.plot_bar(ax)
        self.plot_xticks()
        plt.grid()
        plt.ylabel('mbar at sealevel')
        plt.savefig(os.path.join(self.plotpath,'pressure.svg'))
        plt.close()

    def winds(self):
        ax = plt.subplot(111)
        plt.title('Wind speeds')
        plt.plot(self.dates, self.data['wind'],'r', label='outside')
        plt.plot(self.dates, self.data['windbay'],'b', label='bay')
        plt.plot(self.dates, self.data['windpeak'],'#F75D59', label='peak')
        try:
            ax.legend(loc=2, fontsize='small')
        except TypeError:
            ax.legend(loc=2)
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel('m/s')
        #theta = np.array(self.data['winddir']) * np.pi / 180.0
        #r = self.data['wind']
        #c = plt.scatter(theta, r)
        #c.set_alpha(0.75)
        plt.grid()
        plt.savefig(os.path.join(self.plotpath,'winds.svg'))
        plt.close()

    def brightness(self):
        ax = plt.subplot(1,1,1)
        plt.title('Brightness')
        if np.max(self.data['lx']<0):
            plt.semilogy(self.dates, self.data['lx'],'k')
        else:
            plt.plot(self.dates, self.data['lx'],'k')
        self.plot_bar(ax)
        self.plot_xticks()
        plt.grid()
        plt.ylabel('lux')
        plt.savefig(os.path.join(self.plotpath,'brightness.svg'))
        plt.close()

    def dust(self):
        ax = plt.subplot(1,1,1)
        plt.title('Dust')
        if np.max(self.data['dust'])/np.min(self.data['dust'])>10.0:
            plt.semilogy(self.dates, self.data['dust'],'k', drawstyle='steps')
        else:
            plt.plot(self.dates, self.data['dust'],'k', drawstyle='steps')
        self.plot_bar(ax)
        self.plot_xticks()
        plt.grid()
        plt.ylabel('dust')
        plt.savefig(os.path.join(self.plotpath,'dust.svg'))
        plt.close()

def removefile(filename):
    try:
        os.remove(filename)
    except OSError:
        # can't remove file
        print("Can't remove %s" % filename)
    return

if __name__ == '__main__':
    nightshow = NightShow()
    try:
        nightshow.temperatures()
    except:
        removefile('temperatures.svg')
    try:
        nightshow.humidities()
    except:
        removefile('humidities.svg')
    try:
        nightshow.pressure()
    except ValueError:
        removefile('pressure.svg')
    try:
        nightshow.brightness()
    except ValueError:
        removefile('brightness.svg')
    try:
        nightshow.dust()
    except ValueError:
        removefile('dust.svg')
    try:
        nightshow.winds()
    except ValueError:
        removefile('winds.svg')
    
