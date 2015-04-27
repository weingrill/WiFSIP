#!/usr/bin/python    
# -*- coding: utf-8 -*-
'''
Created on Jan 16, 2015

@author: Joerg Weingrill <jweingrill@aip.de>
'''

class Landolt(object):
    '''
    The famous Landolt class
    '''


    def __init__(self):
        '''
        Constructor
        '''
        from datasource import DataSource
    
        self.table = DataSource(database='wifsip', user='sro', host='pina.aip.de')
        self.data = []

    def fromfile(self, filename='table2.dat'):
        """
        load data from file
        
        filename: string, table2.dat
        """
        from astropy.coordinates import SkyCoord
        from astropy import units as u
        
        def nfloat(s):
            from numpy import nan
            try:
                result = float(s)
            except ValueError:
                return nan
            return result

        def nint(s):
            from numpy import nan
            try:
                result = int(s)
            except ValueError:
                return nan
            return result

        f = open(filename)
        lines = f.readlines()
        f.close
        
        for l in lines:
            coords = l[12:38] 
            c = SkyCoord(coords, 'icrs', unit=(u.hourangle, u.deg))  # @UndefinedVariable
            record = {'name':   l[0:12].rstrip(),
                      'ra':   c.ra.degree,
                      'dec':  c.dec.degree,
                      'vmag': nfloat(l[38:45]),
                      'bv':  nfloat(l[46:51]),
                      'ub':  nfloat(l[52:59]),
                      'vr':  nfloat(l[59:66]),
                      'ri':  nfloat(l[66:73]),
                      'vi':  nfloat(l[73:79]),
                      'nobs': nint(l[80:83]),
                      'nnig': nint(l[84:87]),
                      'e_vmag': nfloat(l[88:94]),
                      'e_bv': nfloat(l[95:101]),
                      'e_ub': nfloat(l[102:108]),
                      'e_vr': nfloat(l[109:115]),
                      'e_ri': nfloat(l[116:122]),
                      'e_vi': nfloat(l[123:129]),
                      'coord': '(%f,%f)' % (c.ra.degree, c.dec.degree)}
            #print record
            self.data.append(record)
            
    def todatabase(self):
        """
        write the imported data to the database
        """
        from StringIO import StringIO
        
        def nstr(s):
            if len(str(s).strip())==0: return '\N'
            elif type(s) is str: return str(s) 
            else: return str(s)
            
        values = ''
        
        for record in self.data:
            valline = '\t'.join([nstr(v) for v in record.values()])
            valline = valline.replace('nan', '\N')
            print valline
            values += valline + '\n'

        columns = record.keys()
        f = StringIO(values)
        cur = self.table.cursor
        try:
            cur.copy_from(f,'landolt', columns=columns)
        finally:
            self.table.commit()
    
    def calibrate(self):
        query = """SELECT frames.datesend, MAX(airmass) "airmass", COUNT(star) "nstar", AVG(mag_auto-vmag) "o-c mag", STDDEV_POP(mag_auto-vmag) "sigma"
            FROM frames, phot, landolt
            WHERE object LIKE 'Landolt%'
            AND filter='V'
            AND frames.objid=phot.objid
            AND circle(phot.coord,3./3600.) @> circle(landolt.coord,0)
            AND frames.objid like '2014%'
            AND phot.flags=0
            GROUP BY frames.datesend
            ORDER BY frames.datesend;"""
        result = self.table.query(query)

        import numpy as np
        for r in result: print '%s %.2f %2d %+6.3f %.3f' % r
        
        import matplotlib.pyplot as plt
        x = np.array([r[0] for r in result])
        n = np.array([r[2] for r in result])
        y = np.array([r[3] for r in result])
        yerr = np.array([r[4] for r in result])
        
        #print len(x),len(y),len(yerr)
        plt.scatter(y,yerr, s=n*5, edgecolor='none')
        plt.show()
        plt.errorbar(x, y, yerr)
        plt.minorticks_on()
        plt.grid()
        plt.show()
       
       
if __name__ == '__main__':
    l = Landolt()
    #l.fromfile('/work1/jwe/Landolt/table2.dat') 
    #l.todatabase()
    l.calibrate()   