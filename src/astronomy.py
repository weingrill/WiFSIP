'''
Created on Jan 24, 2013

@author: jwe
'''

def now():
    """returns the current time in UT"""
    import datetime
    return datetime.datetime.utcnow()

def airmass(h):
    """
    calulates the airmass as a function of height h in degrees
    taken fom Wikipedia, Pickering (2002)
    """
    from numpy import sin, pi,array
    
    h = array(h)
    if type(h)=='float':
        if h < 0.0: h = 0.0
        if h > 90.0: h = 90.0
    if h.ndim==1:
        h[h > 90.0] = 90.0
        h[h < 1.0] = 1.0
    
    #if min(h) < 0.0 or max(h) > 90.0:
    #    raise ValueError('h = %s must be in [0.,90.]' % h)
        
    return 1.0/sin((h + 244/(165 + 47*h**1.1))*pi/180)

def height(a):
    """
    returns the height from a given airmass a,
    since inversion of airmass function is difficult.
    """
    from scipy.optimize import newton
    from numpy import array, searchsorted
    
    # we define predefined table since Newton's method is
    # poor with bad x0 
    airtable = array([38.75, 26.64, 19.64, 15.26, 12.36, 10.33, 8.85, 7.73, 6.85, 
               6.15, 5.58, 5.1, 4.7, 4.36, 4.07, 3.81, 3.58, 3.38, 3.20,
               3.04, 2.9, 2.77, 2.65, 2.54, 2.44, 2.35, 2.27, 2.19, 2.12, 
               2.06, 1.99, 1.94, 1.88, 1.83, 1.78, 1.74, 1.7, 1.66, 1.62,
               1.59, 1.55, 1.52, 1.49, 1.46, 1.44, 1.41, 1.39, 1.37, 1.34, 
               1.32, 1.3, 1.29, 1.27, 1.25, 1.24, 1.22, 1.21, 1.19, 1.18, 
               1.17, 1.15, 1.14, 1.13, 1.12, 1.11, 1.1, 1.09, 1.09, 1.08, 
               1.07, 1.06, 1.06, 1.05, 1.05, 1.04, 1.04, 1.03, 1.03, 1.02, 
               1.02, 1.02, 1.01, 1.01, 1.01, 1.01, 1., 1., 1., 1., 1., 1.])
    
    x0 = 90. - searchsorted(airtable[::-1], a)
    f = lambda h, a: airmass(h) - a
    return newton(f, x0 = x0, args = (a,))
    

def mag_distance(d):
    """
    calculates the magnitude of a solar like star
    at the given distance d in parsec
    """
    from numpy import log10
    return 5.0*log10(d) - 5.0 + 4.83
    
def jd(epoch):
    """
    returns the Julian Day of a given time. 
    datetime must be a datetime object
    http://en.wikipedia.org/wiki/Julian_day
    """
    
    import datetime
    from math import floor
    if not type(epoch) is datetime.datetime:
        raise TypeError('datetime must be of type datetime')
    
    a = floor((14 - epoch.month)/12)
    y = epoch.year + 4800 - a
    m = epoch.month + 12*a - 3
    
    d = epoch.day
    h = epoch.hour/24. + epoch.minute/1440. + epoch.second/86400. # microsecond might be added here?
    
    if [epoch.year,epoch.month,d] >= [1582,10,15]:
        jdn = epoch.day + floor((153*m + 2)/5) + 365*y + floor(y/4) - floor(y/100) + floor(y/400) - 32045
    elif [epoch.year,epoch.month,d] <= [1582,10,4]:
        jdn = epoch.day + floor((153*m + 2)/5) + 365*y + floor(y/4) - 32083
    return jdn + (epoch.hour-12)/24. + epoch.minute/1440. + epoch.second/86400.

def hms2dd(hms):
    """convert hours, minutes seconds to degrees"""
    if type(hms) is str:
        if hms.find(':')>0: 
            hms = hms.split(':')
        else:
            hms = hms.split(' ')
    hms = [float(h) for h in hms]
    if len(hms)==2: hms.append(0.0)
    return (abs(hms[0]) + hms[1]/60. + hms[2]/3600.)*15.

def hms2hh(hms):
    """convert hours, minutes seconds to decimal hours"""
    if type(hms) is str:
        if hms.find(':')>0: 
            hms = hms.split(':')
        else:
            hms = hms.split(' ')
    hms = [float(h) for h in hms]
    if len(hms)==2: hms.append(0.0)
    return (hms[0] + hms[1]/60. + hms[2]/3600.)


def dms2dd(dms):
    """convert degrees, minutes seconds to degrees"""
    from functions import sign
    if type(dms) is str:
        if dms.find(':')>0: 
            dms = dms.split(':')
        else:
            dms = dms.split(' ')
    dms = [float(d) for d in dms]
    if len(dms)==2: dms.append(0.0)
    return sign(dms[0])*(abs(dms[0]) + dms[1]/60. + dms[2]/3600.)

def dd2dms(degrees):
    """convert degrees to degrees, minutes, seconds"""
    from math import trunc
    d = trunc(degrees)
    m = trunc((degrees-d)*60.)
    s = ((degrees-d)*60.-m)*60. 
    return (d,m,s)

def dd2hms(degrees):
    """convert degrees to hours, minutes, seconds"""
    from math import trunc
    h = trunc(degrees/15.)
    frac_hours = degrees/15. - h
    m = trunc(frac_hours*60.)
    frac_minutes=(frac_hours)*60. - m
    s = frac_minutes*60. 
    return (h,m,s)

def mjd(datetime):
    """returns the modified Julian date (MJD) of a given time."""
    return jd(datetime)-2400000.5

def caldat(mjd):
    """returns the datetime value of the given MJD mjd"""
    from datetime import datetime
    from math import floor
    a = int(mjd + 2400001.0)
    if a < 2299161:
        b = 0
        c = a + 1524
    else:
        b = int((a-1867216.25)/36524.25)
        c = a + b - (b/4) + 1525
    d = int((c-122.1)/365.25)
    e = 365*d + d/4
    f = int((c-e)/30.6001)
    day = c - e - int(30.6001*f)
    month = f - 1 - 12*(f/14)
    year = d - 4715 - ((7+month)/10)
    fracofday = mjd - floor(mjd)
    hour = int(fracofday*24)
    minute = int(fracofday*24*60) - hour*60
    second = int(fracofday*24*60*60) - hour*3600 - minute*60
    #TODO: microseconds
    return datetime(year, month, day, hour, minute, second)

def ecl2equ(coords, jd):
    from math import pi, sin, cos, asin
    l = coords[0]
    b = coords[1]
    t = (jd-2451545.0) / 36525 
    dtor = pi/180. # degrees to radians
    eps = 23.439291*dtor-t*0.013004*dtor
    delta = asin(sin(eps)*cos(b)*sin(l)+cos(eps)*sin(b))
    alpha = cos(b)*cos(l)/cos(delta)
    return((alpha,delta))      

def equ2ecl(coords, jd):
    from math import pi, sin, cos, asin
    alpha = coords[0]
    delta = coords[1]
    t = (jd-2451545.0) / 36525 
    dtor = pi/180. # degrees to radians
    eps = 23.439291*dtor-t*0.013004*dtor
    b = asin(cos(eps)*sin(delta)-sin(eps)*cos(delta)*sin(alpha))
    l = cos(delta)*cos(alpha)/cos(b)
    return((l,b))

    
class celestialobject(object):
    def __init__(self, observer):
        self.ra = 0.0
        self.dec = 0.0
        self.observer = observer
        

class moon(celestialobject):
    def phase(self):
        """returns the phase of the moon"""
        return 0

class sun(celestialobject):
    """solar object"""
    def __init__(self, time=now()):
        self.diameter = 1.3927e9 # meters
        self.mass = 1.989e30 # kilograms
        self.distance = 1.496e11 # meters
        
    def ecliptic(self):
        """return the ecliptic coordinates (lambda, beta) of the sun"""
        from math import pi, sin
        from numpy import polyval
        dtor = pi/180. # degrees to radians
        stor = dtor/3600. # arcseconds to radians
        t = (self.observer.time-2451545.0) / 36525
        
        dlp = (1.866*stor - 0.016*stor*t)*sin((207.51 + 150.27*t)*dtor) + \
                                 6.4*stor*sin((251.39 + 20.208*t)*dtor) + \
                               0.266*stor*sin((150.80 + 119.00*t)*dtor)
                          
        # mean anomaly, degree
        g = polyval([0.54/3600.,35999.+179.02/3600.,357.525433]*dtor,t) + dlp
        
        dl = ((6892.817 - 17.240*t)/3600)*sin(g) + \
             ((  71.977 -  0.361*t)/3600)*sin(2*g) + \
             (1.054/3600)*sin(3*g)
        # mean longitude, degree
        l0 = polyval([1.089/3600.,(36000+2770.308/3600.),280.465905]*dtor,t)
        # true longitude, degree
        b = 0. # b < 1 arcsec
        return l0 + dl,b   
          
    def ra(self):
        """convert ecliptic longitude L to right ascension RA and declination delta
        (the ecliptic latitude of the Sun is assumed to be zero)"""
        from math import sqrt,sin,cos,atan
        # number of Julian centuries since Jan 1, 2000, 12 UT
        t = (self.time-2451545.0) / 36525
        l,b = self.ecliptic()
        # obliquity eps of ecliptic:
        eps = 23.0 + 26.0/60.0 + 21.448/3600.0 - \
            (46.8150*t + 0.00059*t**2 - 0.001813*t**3)/3600.
        x = cos(l)
        y = cos(eps)*sin(l)
        z = sin(eps)*sin(l)
        r = sqrt(1.0-z**2)

        return (24/180)*atan(y/(x+r)) # in hours

    def dec(self):
        """convert ecliptic longitude L to right ascension RA and declination delta
        (the ecliptic latitude of the Sun is assumed to be zero)"""
        from math import sqrt,sin,atan
        # number of Julian centuries since Jan 1, 2000, 12 UT
        t = (self.time-2451545.0) / 36525
        l,b = self.ecliptic()
        # obliquity eps of ecliptic:
        eps = 23.0 + 26.0/60.0 + 21.448/3600.0 - \
            (46.8150*t + 0.00059*t**2 - 0.001813*t**3)/3600.

        z = sin(eps)*sin(l)
        r = sqrt(1.0-z**2)

        return atan(z/r) # in degrees
    
    def altitude(self):
        """convert tau, delta to horizon coordinates of the observer 
        (altitude h, azimuth az)"""
        from math import sin, asin,cos
        beta = 0
        delta = 0
        tau = 0
        return asin(sin(beta )*sin(delta) + cos(beta)*cos(delta)*cos(tau))

    def azimuth(self):
        """convert tau, delta to horizon coordinates of the observer 
        (altitude h, azimuth az)"""
        from math import sin, atan,cos, tan
        beta = 0
        delta = 0
        tau = 0
        return atan(-sin(tau) / (cos(beta)*tan(delta) - sin(beta)*cos(tau)))
#class planet(celestialobject):
    

class observer(object):
    '''
    classdocs
    '''

    def __init__(self, latitude, longitude, height, time=now()):
        '''
        Constructor
        longitude, latitude in degrees
        longitude: west is negative
        height in meters
        time in jd
        '''
        self.longitude = longitude
        self.latitude = latitude
        self.height = height
        self.time = time
    
    def gmst(self):
        """returns the Greenwich mean stellar time"""
        t = (self.time - 2451545.0)/36525.
        return (100.46061837 + 36000.770053608*t + 0.000387933*t**2 - (t**3/38710000.) + self.latitude)
    
    def hjd(self, star):
        from math import sin,cos
        s = sun()
        r = s.distance
        c = 299792458.0
        return jd(self.time)-(r/c)*(sin(star.dec)*sin(s.dec)+cos(star.dec)*cos(s.dec)*cos(star.ra-s.ra))
    
    def siderialtime(self):
        # compute sidereal time at Greenwich (according to: Jean Meeus: Astronomical Algorithms)
        t = (self.time - 2451545.0)/36525.
        return 280.46061837 + 360.98564736629*(self.time-2451545.0) + \
               0.000387933*t**2 - t**3/38710000.0
if __name__ == '__main__':
    n = now()
    print n
    print jd(n),mjd(n),caldat(mjd(n))
    