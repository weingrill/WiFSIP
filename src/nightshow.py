#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2014

@author: jwe

 date     | timestamp without time zone | not null
 tbay     | real                        | 
 tspec    | real                        | 
 telectr  | real                        | 
 ttable   | real                        | 
 taussen  | real                        | 
 hbay     | real                        | 
 hspec    | real                        | 
 helectr  | real                        | 
 haussen  | real                        | 
 solz     | real                        | 
 paussen  | real                        | 
 wind     | real                        | 
 windpeak | real                        | 
 winddir  | real                        | 
 windbay  | real                        | 
 lx       | real                        | 
 rain     | real                        | 
 good     | character(1)                | 
 dust     | real                        | 
 tlounge  | real                        | 
 tlab     | real                        | 
 toil1    | real                        | 
 toil2    | real                        | 


'''
import psycopg2
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import numpy as np

class NightShow():
    def __init__(self):
        database  = 'stella'
        user = 'guest'
        host = 'pera.aip.de'
        password='IwmDs!'

        database = psycopg2.connect(database=database, user=user, host=host, password=password) 
        cursor = database.cursor()
        query = "SELECT * from env where date>=current_timestamp-interval '1 day' order by date;" 
        cursor.execute(query)
        result = cursor.fetchall()
        
        columns = [ 'date', 'tbay', 'tspec', 'telectr', 'ttable', 'taussen', 'hbay', \
                   'hspec', 'helectr', 'haussen', 'solz', 'paussen', 'wind' , \
                   'windpeak', 'winddir', 'windbay', 'lx',  'rain', 'good' , 'dust', \
                   'tlounge', 'tlab', 'toil1', 'toil2']
        
        self.data = {}
        for c in columns:
            i = columns.index(c)
            self.data[c] = [r[i] for r in result]
        
        
        self.dates = self.data['date']
    
    def plot_bar(self, axis):
        """
        plot agreen vertical bar for every five minute where the conditions are 
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
        plot agreen vertical bar for every five minute where the conditions are 
        good
        """
        
        # width of the bar is 5 minutes (= datainterval)
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
            plt.xlabel('time')
    
    def temperatures(self):
        """
        plot the temperatures
        """
        ax = plt.subplot(3,1,1)
        plt.title('Temperatures')
        plt.plot(self.dates, self.data['tbay'],'b', label='bay')
        plt.plot(self.dates, self.data['taussen'],'r', label='outside')
        plt.plot(self.dates, self.data['tlounge'],'g', label='lounge')
        ax.legend(fontsize='small')
        self.plot_bar(ax)
        self.plot_xticks(nolabels=True)
        plt.ylabel(u"\N{DEGREE SIGN}C")
    
        ax = plt.subplot(3,1,2)
        plt.plot(self.dates, self.data['tspec'],'r', label='spec')
        plt.plot(self.dates, self.data['ttable'],'g', label='table')
        ax.legend(fontsize='small')
        self.plot_bar(ax)
        self.plot_xticks(nolabels=True)
        plt.ylabel(u"\N{DEGREE SIGN}C")
        
        ax = plt.subplot(3,1,3)
        plt.plot(self.dates, self.data['telectr'],'r', label='electr')
        plt.plot(self.dates, self.data['tlab'],'b', label='lab')
        plt.plot(self.dates, self.data['toil1'],'c', label='oil1')
        plt.plot(self.dates, self.data['toil2'],'m', label='oil2')
        ax.legend(fontsize='small')
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel(u"\N{DEGREE SIGN}C")
        plt.savefig('temperatures.png')
        #plt.show()
        plt.close()

    def humidities(self):
        ax = plt.subplot(1,1,1)
        plt.title('Humidities')
        plt.plot(self.dates, self.data['hbay'],'b', label='bay')
        plt.plot(self.dates, self.data['haussen'],'r', label='outside')
        plt.plot(self.dates, self.data['helectr'],'g', label='electr')
        plt.plot(self.dates, self.data['hspec'],'orange', label='spectr')
        ax.legend(loc=2, fontsize='small')
        plt.ylim(0,100)
        self.plot_rain(ax)
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel('rel. %')
        plt.savefig('humidities.png')
        #plt.show()
        plt.close()

    def pressure(self):
        import scipy.interpolate as spyint
        from astronomy import mjd, caldat
        from numpy import array,power
        #p0 = array(self.data['paussen'])/0.769584
        t0 = array(self.data['taussen'])+ 273.15 
        p0 = array(self.data['paussen'])/power(1.0-(0.0065*2200.0/t0),5.255)
        mdates = np.array([mjd(d) for d in self.dates])
        sp = spyint.splrep(mdates, p0,s=0.5)
        x = np.linspace(mdates[0], mdates[-1], 500)
        xdates = [caldat(xi) for xi in x]
        int_paussen = spyint.splev(x, sp)

        ax = plt.subplot(1,1,1)
        plt.title('Pressure')
        #plt.plot(self.dates, self.data['paussen'],'g')
        plt.plot(xdates, int_paussen,'k')
        yticks = array(plt.yticks()[0])
        plt.yticks(yticks,['%4.0f' % y for y in yticks])
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel('mbar at sealevel')
        plt.savefig('pressure.png')
        #plt.show()
        plt.close()

    def winds(self):
        ax = plt.subplot(111)
        plt.title('Wind speeds')
        plt.plot(self.dates, self.data['wind'],'r', label='outside')
        plt.plot(self.dates, self.data['windbay'],'b', label='bay')
        plt.plot(self.dates, self.data['windpeak'],'#F75D59', label='peak')
        ax.legend(loc=2,fontsize='small')
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel('m/s')
        #theta = np.array(self.data['winddir']) * np.pi / 180.0
        #r = self.data['wind']
        #c = plt.scatter(theta, r)
        #c.set_alpha(0.75)
        plt.savefig('winds.png')
        #plt.show()
        plt.close()

    def brightness(self):
        ax = plt.subplot(1,1,1)
        plt.title('Brightness')
        plt.semilogy(self.dates, self.data['lx'],'k')
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel('lux')
        plt.savefig('brightness.png')
        #plt.show()
        plt.close()

    def dust(self):
        ax = plt.subplot(1,1,1)
        plt.title('Dust')
        plt.semilogy(self.dates, self.data['dust'],'k')
        self.plot_bar(ax)
        self.plot_xticks()
        plt.ylabel('dust')
        plt.savefig('dust.png')
        #plt.show()
        plt.close()

nightshow = NightShow()
nightshow.temperatures()
nightshow.humidities()
nightshow.pressure()
nightshow.brightness()
nightshow.dust()
nightshow.winds()
