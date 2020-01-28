#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on Mon Nov 25, 00:01:00 2019
@author jacek.kawa@radpoint.pl
'''

import os
import sys

# sorry for that, import custom GDCM (LD_LIBRARY_PATH to import shared libs
#sys.path.insert to import modules)
if not os.getenv('LD_LIBRARY_PATH') in sys.path:
    sys.path.insert(1, os.getenv('LD_LIBRARY_PATH'))

import gdcm

#gdcm.Trace.DebugOn()
#gdcm.Trace.WarningOn()
#gdcm.Trace.ErrorOn()


def setup():
    gg = gdcm.Global.GetInstance()
    pth = os.getenv('GDCM_RESOURCES_PATH')
    #pth = '/usr/share/gdcm-3.0/XML/'
    if pth is not None:
        gg.Prepend(pth)
    gg.LoadResourcesFiles()


setup()
