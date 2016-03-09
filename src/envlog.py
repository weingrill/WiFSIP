#!/usr/bin/python
'''
Created on Nov 18, 2014

@author: jwe
'''
import psycopg2
import matplotlib
matplotlib.use('Agg')

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
        columns = ['pressure', 'dettemp','cryotemp', 'telfocus', 'ambtemp', 'relhum', 'maxwind', 'tempm1', 'tempm2', 'avrgwind','atmpress', 'dewpoint']
        colstring = ', '.join(columns)
        query = """SELECT %s 
        FROM obs 
        WHERE instrument=%d
        ORDER BY dateobs DESC 
        LIMIT 1;""" % (colstring, instrument) 
        cursor.execute(query)
        result = cursor.fetchall()
        
        self.data = {}
        
        for i, c in enumerate(columns):
            self.data[c] = result[0][i]
        
        self.data['pressure'] *= 1e7
        
        from matplotlib import rcParams
        params = {'backend': 'Agg',
              'savefig.dpi' : 100,
              'figure.figsize': [6, 6]}
        rcParams.update(params)

    def plot(self, value):
        from gauge import gauge
        unit = ''
        if value in ['dettemp','cryotemp', 'ambtemp', 'tempm1', 'tempm2', 'dewpoint']:
            unit = u"\N{DEGREE SIGN}C"
        if value == 'telfocus': unit = 'mm'
        if value in ['maxwind', 'avrgwind']:
            unit = 'm/s'
        if value == 'atmpress': unit = 'mBar'
        if value == 'relhum': unit = '%'
        if value == 'pressure': unit = '1e-7 bar'
        titles = {'pressure': 'pressure', 
                  'dettemp': 'det. temp.',
                  'cryotemp': 'cryo temp.', 
                  'telfocus': 'focus', 
                  'ambtemp': 'amb. temp.', 
                  'relhum': 'rel. hum.', 
                  'maxwind': 'max. wind', 
                  'tempm1': 'M1 temp.', 
                  'tempm2': 'M2 temp.', 
                  'avrgwind': 'wind speed',
                  'atmpress': 'atm. press.', 
                  'dewpoint': 'dewpoint'}
        minmaxes = {'pressure': [0.0, 100.0], 
                  'dettemp': [-120.0, -100.0],
                  'cryotemp': [-160.0, -130.0], 
                  'telfocus': [40.0, 50.0], 
                  'ambtemp':[-10.0, 30.0], 
                  'relhum': [0.0, 100.0], 
                  'maxwind': [0.0, 20.0], 
                  'tempm1': [0.0, 25.0], 
                  'tempm2':   [0.0, 25.0], 
                  'avrgwind': [0.0, 20.0],
                  'atmpress': [750.0, 780.0], 
                  'dewpoint': [-30.0, 10.0]}
        
        if value in minmaxes:
            minmax = minmaxes[value]
        else:
            minmax = [0.0, 100.0]
        nticks = {'pressure': 10, 
                  'dettemp': 2,
                  'cryotemp': 3, 
                  'telfocus': 10, 
                  'ambtemp': 4, 
                  'relhum': 10, 
                  'maxwind': 2, 
                  'tempm1': 5, 
                  'tempm2': 5, 
                  'avrgwind': 2,
                  'atmpress': 3, 
                  'dewpoint': 4}
        filename = '%s_%d.png' % (value, self.instrument)
        gauge(self.data[value], minmax=minmax, nticks=nticks[value],title=titles[value], units=unit, filename = filename)

if __name__ == '__main__':
    envlog2 = EnvironmentLog(2)
    for value in ['pressure', 'dettemp','cryotemp', 'telfocus', 'ambtemp', 'relhum', 'maxwind', 'tempm1', 'tempm2', 'avrgwind','atmpress', 'dewpoint']:
        envlog2.plot(value)
    