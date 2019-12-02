#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 10:08:40 2019

Provides functionality close to a command-line gdcmanon, i.e. anonymize one file or one dir.

strategy object: gdcmanon.AnonWrapper(gdcm.Anonymizer()) provides the process() method that does the job,
yet one may implement logic in _anonymizeOneFile() as well


@author: jacek.kawa@radpoint.pl
"""

import gdcm
from gdcmanon import Gdcmanon
import os
#import sys

class anon:
    def __init__(self, anonymizer):

        self.anonymizer = anonymizer
        # apparently no possibility of reuse these two
        #self.reader = gdcm.Reader()
        #self.writer = gdcm.Writer()
        
    def _anonymizeOneFile(self, file):
        self.anonymizer.SetFile(file)
        
        #ret = self.anonymizer.BasicApplicationLevelConfidentialityProfile(True)
        ret = self.anonymizer.process()
    
        # here you can do some magick removing
        
        if ret:
            fout = self.anonymizer.GetFile()
        else:
            fout = None
        
        return (ret, fout)
        
    
    def anonymizeOneFile(self, fin, fout):
        reader = gdcm.Reader()
        reader.SetFileName(fin)
        ret = reader.Read()
        
        if not ret:
            return (False, "File could not been read")
        
        (ar, af) = self._anonymizeOneFile(reader.GetFile())
        
        if not ar:
            return (False, "Error while anonymizing")
        
        writer = gdcm.Writer()
        writer.SetFileName(fout)
        writer.SetFile(af)
        writer.Write()
        return (True, "OK")
        

    def anonimizeDir(self, dirIn, dirOut):
        if not os.path.isdir(dirIn):
            raise ValueError(f'dirIn={dirIn} must be a directory')
        if os.path.exists(dirOut) and not os.path.isdir(dirOut):
            raise ValueError(f'dirOut={dirOut} must not exist or be a directory')

        status = list()
        ok = 0
        fail = 0
        skipped = 0
        
        #walk it out
        for root, subdirs, files in os.walk(dirIn):
            directory_ = os.path.relpath(root, dirIn)
            directory = os.path.join(dirOut, directory_)
            os.makedirs(directory, exist_ok = True)
            
            for f in files:
                if f == 'DICOMDIR':
                    skipped = skipped + 1
                    continue
                fin = os.path.join(root, f)
                fout = os.path.join(directory, f)
                ret, msg = self.anonymizeOneFile(fin, fout)
                if not ret:
                    fail = fail + 1
                    #print(f'error while anonymizing {fin}: {msg}', file=sys.stderr)
                else:
                    ok = ok + 1

                status.append({'file' : fin, 'status' : ret, 'msg' : msg})

        obj = {"ok" : ok, "fail" : fail, "skipped" : skipped}
        return (obj, status)