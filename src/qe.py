#!/usr/bin/python
'''
Created on Dec 4, 2014

@author: jwe
'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import array
from scipy import interpolate

wifsipqe = array([[300, 0.675],
[320, 0.725],
[340, 0.66],
[350, 0.62],
[360, 0.585],
[380, 0.63],
[400, 0.7],
[450, 0.787],
[500, 0.83],
[550, 0.91],
[600, 0.92],
[650, 0.89],
[700, 0.855],
[750, 0.775],
[800, 0.625],
[850, 0.45],
[900, 0.3],
[950, 0.155],
[1000, 0.07],
[1050, 0.03],
[1100, 0.04]])

def load_csv2(filename):
    csv = open(filename)
    csvlines = csv.readlines()
    csv.close()
    wv = []
    qe = []
    for l in csvlines[1:-2]:
        ls = l.split('\t')
        try:
            wv.append(float(ls[0]))
            qe.append(float(ls[2]))
        except ValueError:
            print ls
            
    wv = array(wv)
    qe = array(qe)
    return wv,qe


wv3,v =  load_csv2('/work2/jwe/stella/wifsip/doc/Bessel_V-1.txt')
wv4,b =  load_csv2('/work2/jwe/stella/wifsip/doc/Bessel_B-1.txt')
wv5,r =  load_csv2('/work2/jwe/stella/wifsip/doc/Bessel_R-1.txt')
wv1 = wifsipqe[:,0]
qe1 = wifsipqe[:,1]*100.

f = interpolate.interp1d(wv1, qe1, kind='cubic')

xnew = wv3[wv3>=300.0]
ynew = f(xnew) 


plt.scatter(wv1,qe1, label='WiFSIP Q.E.')
plt.plot(wv3, v,'g', label='Bessel V')
plt.plot(wv4, b,'b', label='Bessel B')
plt.plot(wv5, r,'r', label='Bessel R')
plt.plot(xnew, ynew,'k', label='WiFSIP Q.E. int.')
plt.plot(xnew, v[wv3>=300.0]*ynew/100,'g--', label='Bessel V eff')
plt.plot(xnew, b[wv3>=300.0]*ynew/100,'b--', label='Bessel B eff')
plt.plot(xnew, r[wv3>=300.0]*ynew/100,'r--', label='Bessel R eff')


plt.grid()
plt.xlim(300,1100)
plt.ylim(0,100)
plt.legend(fontsize='small')
plt.xlabel('wavelength [nm]')
plt.ylabel('%')
plt.savefig('WiFSIP_sensitivity.pdf')
plt.show()
#plt.close()
