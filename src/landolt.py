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
        self.data = []
        for l in lines:
            coords = l[12:38] 
            c = SkyCoord(coords, 'icrs', unit=(u.hourangle, u.deg))  # @UndefinedVariable
            record = {'name':   l[0:12].rstrip(),
                      'ra':   c.ra.degree,
                      'dec':  c.dec.degree,
                      'Vmag': nfloat(l[38:45]),
                      'B-V':  nfloat(l[46:51]),
                      'U-B':  nfloat(l[52:59]),
                      'V-R':  nfloat(l[59:66]),
                      'R-I':  nfloat(l[66:73]),
                      'V-I':  nfloat(l[73:79]),
                      'Nobs': nint(l[80:83]),
                      'Nnig': nint(l[84:87]),
                         
                      'coord': '(%f,%f)' % (c.ra.degree, c.dec.degree)}
            print record
            self.data.append(record)
       
if __name__ == '__main__':
    l = Landolt()
    l.fromfile('/work1/jwe/Landolt/table2.dat')    