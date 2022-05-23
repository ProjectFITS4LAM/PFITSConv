# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:43:06 2022

@author: giuliano giuffrida
"""
import numpy
import sys
import os
from PIL import Image
from PIL.TiffTags import TAGS
from astropy.io import fits
from datetime import datetime
from pathlib import Path


with Image.open(sys.argv[1]) as img:
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}        
    r, g, b = img.split()
    data = numpy.array([numpy.array(r), numpy.array(g), numpy.array(b)])
    hdu = fits.PrimaryHDU(data=data)
    hdr = hdu.header
    now = datetime.now()
    hdr.remove('EXTEND')
    hdr.set('UNIKEY',True,'Compliant with UNI 11845:2022')
    hdr.set('EXTEND',True)
    hdr.set('LONGSTRN','OGIP 1.0','The OGIP long string convention may be used')
    hdr.set('CREATOR','PFITSConv v1.0','Software that created this FITS file')
    hdr.set('INSTRUME',meta_dict['Make'][0] + " " + meta_dict['Model'][0]  ,'Maker and model of the device')
    hdr.set('PROGRAM',meta_dict['Software'][0], 'Software that created the image')
    datetag=meta_dict['DateTime'][0].split()  
    hdr.set('DATE-OBS',datetag[0].replace(":","-") +"T"+datetag[1], 'Date and time of acquisition')   
    hdr.set('DATE',now.strftime("%Y-%m-%dT%H:%M:%S"), 'Date and time of FITS file creation')
    hdr.set('ORIGIN',meta_dict['Copyright'][0], 'Copyright notice')
    hdr.set('OBJECT',Path(sys.argv[1]).stem, 'Item identification')
    hdr.set('COLORMAP','RGB','Colors mapping')
    hdr.set('CTYPE1',' ','Linear transformation on axis 1')
    hdr.set('CTYPE2',' ','Linear transformation on axis 2')
    hdr.set('CTYPE3','RGB','Name of the coordinate represented by axis 3')
    hdr.set('CRPIX1',0.0,'Location of reference point along axis 1')
    hdr.set('CRPIX2',0.0,'Location of reference point along axis 2')
    hdr.set('CRPIX3',0.0,'Location of reference point along axis 3')
    hdr.set('CRVAL1',0.0,'Location of reference point along axis 1')
    hdr.set('CRVAL2',0.0,'Location of reference point along axis 2')
    hdr.set('CRVAL3',0.0,'Location of reference point along axis 3')
    hdr.set('CUNIT1','mm','Units of CRVAL1 and CDELT1')
    hdr.set('CUNIT2','mm','Units of CRVAL2 and CDELT2')
    hdr.set('CUNIT3',' ','Units of CRVAL3 and CDELT3')
    hdr.set('CDELT1',25.4/(meta_dict['XResolution'][0][0]/meta_dict['XResolution'][0][1]),'Coordinate increment at reference point')
    hdr.set('CDELT2',25.4/(meta_dict['YResolution'][0][0]/meta_dict['YResolution'][0][1]),'Coordinate increment at reference point')
    hdr.set('CDELT3',1.0,'Coordinate increment at reference point')
    hdu.add_datasum()
    hdu.add_checksum()
    hdr.remove('EXTEND')
    # in the following lines there is a workaround to put the UNIKEY key before EXTEND
    hdr.set('EXTAND',True, after='UNIKEY')
    if os.path.exists(sys.argv[2]):
        os.remove(sys.argv[2])
    hdu.writeto(sys.argv[2])
    with open(sys.argv[2], 'rb+') as f:
        f.seek(563)
        f.write(b'\x45')
