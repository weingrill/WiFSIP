'''
Created on Feb 26, 2013

@author: jwe <jweingrill@aip.de>
'''

def wifsipguider():
    import optics
    from math import pi
    stella = optics.telescope(1.2, 1.2*8)
    basler = optics.detector([2048, 1088], 5.5e-6)
    print('depth of focus: %.3f mm' % (basler.focusdepth(stella)*1e3))
    fov, fovx, fovy = basler.fieldofview(stella)
    print('field of view: %.2f (%.2f x %.2f) arcmin' % (60*fov*180/pi, 60*fovx*180/pi, 60*fovy*180/pi))
    print('1 pixel == %.2f arcsec' % (basler.pixelfov(stella)*3600*180/pi))
    
if __name__ == '__main__':
    wifsipguider()
    pass