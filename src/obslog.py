#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import numpy as np


class ObservationLog():
    def __init__(self, instrument=1):
        database  = 'stella'
        user = 'guest'
        host = 'pera.aip.de'
        password='IwmDs!'
        
        self.instrument = instrument
        database = psycopg2.connect(database=database, 
                                    user=user, 
                                    host=host, 
                                    password=password) 
        cursor = database.cursor()
        query = """SELECT object, min(dateobs) 
        from obs 
        where dateobs>=current_timestamp-interval '1 day'
        AND instrument=%d
        group by object
        order by min;""" % instrument 
        cursor.execute(query)
        result = cursor.fetchall()
        self.objects = [r[0] for r in result]
        query = """SELECT date, dateobs, exptime, object, "FILTER" 
        from obs 
        where date>=current_timestamp-interval '1 day' 
        AND instrument=%d 
        order by date;""" % instrument 
        cursor.execute(query)
        result = cursor.fetchall()
        
        columns = ['date', 'dateobs', 'exptime', 'object', 'filter']
        
        self.data = {}
        for c in columns:
            i = columns.index(c)
            self.data[c] = [r[i] for r in result]
        from matplotlib import rcParams
        params = {'backend': 'Agg',
              'savefig.dpi' : 100,
              'figure.figsize': [9.6, 6]
              }
        rcParams.update(params)

    def plot(self):
        filters = {'V': 'g', 'B':'b', 'R': 'r', 'y': 'y', 
                   'I':'#7F0000', 'U': '#6C2DC7', 'hbn':'c','hbw':'c',
                   'han':'#A00000','haw':'#A00000',
                   'rp':'#FF3030',
                   'ThAr night': 'orange','ThAr day': 'orange',
                   'ThAr bad weather': 'orange', 'Bias STELLA2':'b',
                   'Flat Field long': 'g'}
        
        plt.subplot(1,1,1)
        obj_pos = np.arange(len(self.objects))
        objarray = list(self.objects)
        for i in range(len(self.data['object'])):
            width = self.data['exptime'][i]/86400.0
            left = self.data['dateobs'][i]
            obj = self.data['object'][i]
            
            ypos = objarray.index(obj)
            cfilter = str(self.data['filter'][i]).rstrip()
            if cfilter in filters:
                filtercol = filters[cfilter]
            elif obj in filters:
                filtercol = filters[obj]
            else:
                print '"%s" "%s"' % (cfilter, obj)
                filtercol= 'm'
            
            plt.barh(ypos, width, left=left, align='center', color=filtercol, edgecolor=filtercol)
        plt.yticks(obj_pos, self.objects)
        plt.xlabel('Performance')
        if self.instrument==1:
            plt.title('Observation Log STELLA2')
        elif self.instrument==2:
            plt.title('Observation Log STELLA1')
        plt.subplots_adjust(top = 0.90,left=0.22, bottom=0.10,right=0.95)
        
        start = self.data['dateobs'][0]
        end = self.data['dateobs'][-1] + datetime.timedelta(hours=2)
        hours = []
        labels = []
        start = start.replace(minute=0,second=0,microsecond=0)
        current = start + datetime.timedelta(hours=1)
        while current<end:
            hours.append(current)
            labels.append('%02dh' % current.hour)
            current += datetime.timedelta(hours=2)
        plt.xticks(hours, labels)
        plt.xlabel('time')
        plt.ylim(-1,len(self.objects))
        plt.grid()
        plt.savefig('obslog%d.png' % self.instrument)
        #plt.show()
        plt.close()


if __name__ == '__main__':
    obslog2 = ObservationLog(2)
    obslog2.plot()
    obslog1 = ObservationLog(1)
    obslog1.plot()
