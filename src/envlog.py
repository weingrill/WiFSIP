'''
Created on Nov 18, 2014

@author: jwe
'''
import psycopg2
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import numpy as np

class EnvironmentLog():
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
        columns = ['date', 'dateobs', 'tempm1', 'tempm2', 'dewpoint','cryotemp', 'dettemp']
        colstring = ', '.join(columns)
        query = """SELECT %s 
        FROM obs 
        WHERE instrument=%d 
        ORDER BY date 
        LIMIT 288;""" % (colstring, instrument) 
        cursor.execute(query)
        result = cursor.fetchall()
        #where date>=current_timestamp-interval '1 day' 
        
        
        self.data = {}
        for c in columns:
            i = columns.index(c)
            self.data[c] = [r[i] for r in result]
            
        self.dates = self.data['date']
        from matplotlib import rcParams
        params = {'backend': 'Agg',
              'savefig.dpi' : 100,
              'figure.figsize': [9.6, 6]}
        rcParams.update(params)

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


    def plot(self):
        """
        plot the humidities
        """
        ax = plt.subplot(1,1,1)
        plt.title('Humidities')
        plt.plot(self.dates, self.data['tempm1'],'b', label='tempm1')
        plt.plot(self.dates, self.data['tempm2'],'g', label='tempm2')
        plt.plot(self.dates, self.data['dewpoint'],'r', label='dewpoint')
        plt.scatter(self.dates, self.data['dettemp'], label='dettemp', facecolor='m', edgecolor='none')
        plt.scatter(self.dates, self.data['cryotemp'], label='cryotemp', facecolor='c', edgecolor='none')
        try:
            ax.legend(loc=2, fontsize='small')
        except TypeError:
            ax.legend(loc=2)
        self.plot_xticks()
        plt.grid()
        plt.ylabel('C')
        plt.savefig('tempm1.png')
        #plt.show()
        plt.close()

if __name__ == '__main__':
    envlog2 = EnvironmentLog(2)
    envlog2.plot()
