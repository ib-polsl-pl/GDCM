#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 01:07:08 2019

@author: jacek.kawa@radpoint.pl
"""

import sys
from gdcmanon import Gdcmanon
from gdcmanon import anon as an
import gdcm
import json

#gdcm.Trace.DebugOn()
#gdcm.Trace.WarningOn()
#gdcm.Trace.ErrorOn()


def example1():

    b = Gdcmanon.Gdcmanon(key = 'openssl/key.key', cert = 'openssl/cert.pem', \
                          salt = '55')
    
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
        
# benchmark it over a MRI dir with ~10 000 files:
# gdcmanon:
#
# real    1m3,193s
# user    0m22,734s
# sys     0m4,481s
#
# gdcmanonexample::example2:
#
#real    1m4,707s
#user    0m44,960s
#sys     0m4,318s
        
        
def example2():

    b = Gdcmanon.Gdcmanon(key = 'openssl/key.key', cert = 'openssl/cert.pem', \
                          salt = '55')
    #anon = b.getInstance()
    anon = b.getAnonWrapper('BALCPA')
    
    anonymizer = an.anon(anon)
    
    stat, ret = anonymizer.anonimizeDir('/tmp/input', '/tmp/output')
    print(f'OK={stat["ok"]}, FAILED={stat["fail"]}, SKIPPED={stat["skipped"]}')
    return ret


ret = example2()
