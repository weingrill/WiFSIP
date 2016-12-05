#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 18, 2016

@author: Joerg Weingrill <jweingrill@aip.de>
'''
import os
import config

class WiFSIPPressure():
    def __init__(self):
        import matplotlib
        matplotlib.use('Agg')
        
        self.plotpath = config.plotpath
        
        self.getdata()
        
    
    def getdata(self):
        import psycopg2
        
        database = psycopg2.connect(database=config.dbname, user=config.dbuser, host=config.dbhost, password=config.dbpassword) 
        self.plotpath = config.plotpath
        cursor = database.cursor()
        query = "SELECT datemeas, mbar, temp0, temp1, temp2, temp3 " \
                " FROM wifsippressure" \
                " WHERE datemeas>=current_timestamp-interval '1 day'" \
                " ORDER BY datemeas;"
        cursor.execute(query)
        result = cursor.fetchall()
        self.data = {}
        for i, c in enumerate(['datemeas', 'mbar', 'temp0', 'temp1', 'temp2', 'temp3']):
            self.data[c] = [r[i] for r in result]
        self.dates = self.data['datemeas']
    
    def plotpressure(self):
        import matplotlib.pylab as plt
        import matplotlib.dates as mdates
        
        plt.style.use('lcars.mplstyle')
        fig, ax = plt.subplots()
        
        ax.plot(self.dates, self.data['mbar'])

        lastdate = self.dates[-1]
        lastmbar = self.data['mbar'][-1]
        ax.text(lastdate, lastmbar, ' %.1e' % lastmbar)
        
        myFmt = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(myFmt)
        
        ax.grid()
        ax.minorticks_on()
        
        ax.set_xlabel('time')
        plt.ylabel('pressure [mbar]')
        ax.set_title('WiFSIP dewar pressure')
        plt.savefig(os.path.join(self.plotpath,'wifsippressure.png'))
        #plt.show()
        
    def plottemperatures(self):
        import matplotlib.pylab as plt
        import matplotlib.dates as mdates
        
        plt.style.use('lcars.mplstyle')
        fig, ax = plt.subplots()
        
        ax.plot(self.dates, self.data['temp0'], label='temp0')
        ax.plot(self.dates, self.data['temp1'], label='temp1')
        ax.plot(self.dates, self.data['temp2'], label='temp2')
        ax.plot(self.dates, self.data['temp3'], label='temp3')
        
        lastdate = self.dates[-1]
        lasttemp0 = self.data['temp0'][-1]
        lasttemp1 = self.data['temp1'][-1]
        lasttemp2 = self.data['temp2'][-1]
        lasttemp3 = self.data['temp3'][-1]
        ax.text(lastdate, lasttemp0, ' %.1f' % lasttemp0)
        ax.text(lastdate, lasttemp1, ' %.1f' % lasttemp1)
        ax.text(lastdate, lasttemp2, ' %.1f' % lasttemp2)
        ax.text(lastdate, lasttemp3, ' %.1f' % lasttemp3)
        
        myFmt = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(myFmt)
        
        try:
            ax.legend(loc=2, fontsize='small')
        except TypeError:
            ax.legend(loc=2)
        
        ax.grid()
        ax.minorticks_on()
        
        ax.set_xlabel('time')
        plt.ylabel(u"temperature \N{DEGREE SIGN}C")
        ax.set_title('WiFSIP temperatures')
        plt.savefig(os.path.join(self.plotpath,'wifsiptemperatures.png'))
        #plt.show()
        

if __name__ == '__main__':
    wp = WiFSIPPressure()
    wp.plotpressure()
    wp.plottemperatures()