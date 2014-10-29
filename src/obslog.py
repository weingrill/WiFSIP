#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Oct 24, 2014

@author: jwe
   Column   |            Type             | Modifiers 
------------+-----------------------------+-----------
 date       | timestamp without time zone | not null
 dateobs    | timestamp without time zone | not null
 instrument | smallint                    | 
 iversion   | smallint                    | 
 exptime    | real                        | 
 amplmode   | character(8)                | 
 pressure   | real                        | 
 dettemp    | real                        | 
 cryotemp   | real                        | 
 austatus   | smallint                    | 
 auseeing   | real                        | 
 domestat   | boolean                     | 
 observer   | smallint                    | 
 transfered | boolean                     | 
 online     | boolean                     | 
 filename   | character varying(255)      | 
 path       | character varying(255)      | 
 imagetyp   | smallint                    | 
 object     | character varying(255)      | 
 telfocus   | real                        | 
 objname    | character varying(255)      | 
 ambtemp    | real                        | 
 relhum     | real                        | 
 maxwind    | real                        | 
 telescop   | character(8)                | 
 naquire    | smallint                    | 
 guideloss  | real                        | 
 tempm1     | real                        | 
 tempm2     | real                        | 
 avrgwind   | real                        | 
 winddir    | real                        | 
 atmpress   | real                        | 
 dewpoint   | real                        | 
 aumiss     | real                        | 
 seseff     | real                        | 
 snest      | real                        | 
 aulight    | real                        | 
 aulign     | real                        | 
 objid      | character varying(255)      | 
 ADU_av     | real[]                      | 
 ADU_var    | real[]                      | 
 ADU_CNM3   | real[]                      | 
 ADU_CNM4   | real[]                      | 
 ADU_CNM5   | real[]                      | 
 ADU_CNM6   | real[]                      | 
 FILTER     | character(8)                | 
 TELDEROT   | real                        | 
 EXPID      | integer                     | 
 TARGETID   | character varying(255)      | 

'''

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

        database = psycopg2.connect(database=database, user=user, host=host, password=password) 
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
        query = """SELECT date, dateobs, exptime, object 
        from obs 
        where date>=current_timestamp-interval '1 day' 
        AND instrument=%d 
        order by date;""" % instrument 
        cursor.execute(query)
        result = cursor.fetchall()
        
        columns = ['date', 'dateobs', 'exptime', 'object']
        
        self.data = {}
        for c in columns:
            i = columns.index(c)
            self.data[c] = [r[i] for r in result]

    def plot(self):
        plt.subplot(1,1,1)
        obj_pos = np.arange(len(self.objects))
        objarray = list(self.objects)
        for i in range(len(self.data['object'])):
            width = self.data['exptime'][i]/86400.0
            left = self.data['dateobs'][i]
            obj = self.data['object'][i]
            
            ypos = objarray.index(obj)
            plt.barh(ypos, width, left=left, align='center')
        plt.yticks(obj_pos, self.objects)
        plt.xlabel('Performance')
        plt.title('Observation log')
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
