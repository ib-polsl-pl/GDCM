#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 01:07:08 2019

@author: jacek.kawa@radpoint.pl
"""

import sys
from gdcmanon import Gdcmanon
import gdcm

gdcm.Trace.DebugOn()
gdcm.Trace.WarningOn()
gdcm.Trace.ErrorOn()


b = Gdcmanon.Gdcmanon(key = 'openssl/key.key', cert = 'openssl/cert.pem')

anon = b.getInstance()

r = gdcm.Reader()
r.SetFileName('input.dcm')
r.Read()

anon.SetFile(r.GetFile())
if not anon.BasicApplicationLevelConfidentialityProfile(True): # False to decrypt
    print("Error during anonymization", file = sys.stderr)
else:
    w = gdcm.Writer()
    w.SetFileName('out.dcm')
    w.SetFile(anon.GetFile())
    w.Write()
    
