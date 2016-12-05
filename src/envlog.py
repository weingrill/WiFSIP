#!/usr/bin/python
'''
Created on Nov 18, 2014

@author: jwe
'''
import psycopg2
import matplotlib
matplotlib.use('Agg')

class EnvironmentLog():
    def __init__(self, instrument=1, devel = False):
        database  = 'stella'
        user = 'guest'
        host = 'pera.aip.de'
        password='IwmDs!'
        
        self.instrument = int(instrument)
        self.devel = devel
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
        
        self.data['pressure'] *= 1e6
        
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
        if value == 'pressure': unit = '1e-6 bar'
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
        minmaxes = {'pressure': [0.0, 10.0], 
                  'dettemp': [-120.0, -100.0],
                  'cryotemp': [-160.0, -130.0], 
                  'telfocus': [43.0, 45.0], 
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
        nticks = {'pressure':10, 
                  'dettemp':  2,
                  'cryotemp': 3, 
                  'telfocus':10, 
                  'ambtemp':  4, 
                  'relhum':  10, 
                  'maxwind':  2, 
                  'tempm1':   5, 
                  'tempm2':   5, 
                  'avrgwind': 2,
                  'atmpress': 3, 
                  'dewpoint': 4}
        
        ranges = {'pressure': [{'color': 'g', 'from': 1.4, 'to': 4.40},
                               {'color': 'y', 'from': 4.4, 'to': 6.40}], 
                  'dettemp':  [{'color': 'g', 'from': -113.2, 'to': -112.0}],
                  'cryotemp': [{'color': 'g', 'from': -148.0, 'to': -141.0}], 
                  'telfocus': [{'color': 'g', 'from': 43.6, 'to': 43.88}], 
                  'ambtemp':  [{'color': 'g', 'from': 0.2, 'to': 8.4}], 
                  'relhum':   [{'color': 'g', 'from': 0.0, 'to': 35.0},
                               {'color': 'y', 'from': 35.0, 'to': 78.0}], 
                  'maxwind':  [{'color': 'g', 'from': 0.0, 'to': 7.2},
                               {'color': 'y', 'from': 7.2, 'to': 9.53}],
                  'tempm1':   [{'color': 'g', 'from': 6.6, 'to': 15.6}],
                  'tempm2':   [{'color': 'g', 'from': 6.7, 'to': 15.3}],
                  'avrgwind': [{'color': 'g', 'from': 0.0,   'to': 5.4},
                               {'color': 'y', 'from': 5.4,   'to': 6.4}],
                  'atmpress': [{'color': 'y', 'from': 758.5, 'to': 762.0},
                               {'color': 'g', 'from': 762.0, 'to': 774.5}], 
                  'dewpoint': [{'color': 'g', 'from': -30.0, 'to': 2.0},
                               {'color': 'y', 'from': 2.0,   'to': 6.2}]
                  }
        if self.devel:
            filename = '../www/%s_%d.png' % (value, self.instrument)
        else:
            filename = '%s_%d.png' % (value, self.instrument)
        gauge(self.data[value], minmax=minmax, nticks=nticks[value],title=titles[value], units=unit, filename = filename, ranges = ranges[value])

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='produces gauges for the STELLA web gui')
    parser.add_argument('-devel', action='store_true', default=False, help='use development path')
    parser.add_argument('instrument', type = int, default=2, help='1 = SES, 2 = WiFSIP')
    
    args = parser.parse_args()

    envlog = EnvironmentLog(args.instrument, devel = args.devel)
    for value in ['pressure', 'dettemp','cryotemp', 'telfocus', 'ambtemp', 'relhum', 'maxwind', 'tempm1', 'tempm2', 'avrgwind','atmpress', 'dewpoint']:
        envlog.plot(value)
    