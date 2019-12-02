#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on Mon Nov 25, 00:01:00 2019
@author jacek.kawa@radpoint.pl

gdcmanon provides a builder-wrapper to gdcm.Anonymizer()

# in non-dump mode:
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

# in dump mode: just omit key and cert, and use Remove(), Replace() or Empty() 
# methods od anonymizer

'''

import os
import sys
import warnings

# sorry for that, import custom GDCM (LD_LIBRARY_PATH to import shared libs
#sys.path.insert to import modules)
sys.path.insert(1, os.getenv('LD_LIBRARY_PATH'))

import gdcm

class Gdcmanon:
    
 
    def __init__(self, key = None, cert = None, deterministicUIDs = True, \
                 generateDummyNames = True, salt = None, \
                 removeTags = None, addTags = None):

        self.anonymizer = gdcm.Anonymizer()
        self.dummy = True

        # if key and cert is specified, encryption mode is enabled        
        if key is not None and cert is not None:
            # or OpenSSL or whatever
            self._cf = gdcm.CryptoFactory_GetFactoryInstance(gdcm.CryptoFactory.DEFAULT)
            self._cp = self._cf.CreateCMSProvider()

            if not self._cp.ParseKeyFile(key):
                raise ValueError('Key file{key} could not be read')
            if not self._cp.ParseCertificateFile(cert):
                raise ValueError('Certificate file{key} could not be read')

            # this one could be changes if necessary
            self._cp.SetCipherType(gdcm.CryptographicMessageSyntax.AES256_CIPHER)
            self.anonymizer.SetCryptographicMessageSyntax(self._cp)

            self.dummy = False

        elif key is None or cert is None:
            raise ValueError('Both key and cert must be specified to disable dummy mode')


        if self.dummy:
            # for the getters
            self.deterministicUIDs = None
            self.generateDummyNames = None
            self.salt = ''
        else:
            # extension of Radpoint GDCM
            self.setDeterminicticUIDs(deterministicUIDs)
            self.setGenerateDummyNames(generateDummyNames)
            self.setSalt(salt)
            
            self.removeTagsFromBALCPA(removeTags)
            self.addTagsToBALCPA(addTags)
            
        
    def getCurrentBALCPA(self):
        return self.anonymizer.GetBasicApplicationLevelConfidentialityProfileAttributes()

    def addTagsToBALCPA(self, tags):
        ''' add tags to a current/default set of tags that are encrypted
            during call to ano.BasicApplicationLevelConfidentialityProfile(True)
        '''
        if self.dummy:
            warnings.warn('BALCPA is only used in non-dummy mode')

        if tags is not None:
            self.anonymizer.AddTagsToBALCPA(list(tags))

    def removeTagsFromBALCPA(self, tags):
        if self.dummy:
            warnings.warn('BALCPA is only used in non-dummy mode')        
            
        if tags is not None:
            self.anonymizer.RemoveTagsFromBALCPA(list(tags))
        
    def setDeterminicticUIDs(self, deterministicUIDs):
        if self.dummy:
            warnings.warn('value assigned to deterministicUIDs is ignored in dummy mode')
        self.deterministicUIDs = deterministicUIDs
        self.anonymizer.SetDeterminicticUIDs(deterministicUIDs)
        
    def getDeterminicticUIDs(self):
        return self.deterministicUIDs
        
    def setGenerateDummyNames(self, generateDummyNames):
        if self.dummy:
            warnings.warn('value assigned to generateDummyNames is ignored in dummy mode')
        
        self.generateDummyNames = generateDummyNames
        self.anonymizer.SetGenerateDummyNames(generateDummyNames)
    
    def getGenerateDummyNames(self):
        return self.generateDummyNames
    
    def setSalt(self, salt):
        if self.dummy:
            warnings.warn('value assigned to salt is ignored in dummy mode')
        
        if salt is None or len(salt) == 0:
            warnings.warn("at the current version, salt cannot be empty, setting to '33'")
            salt = '33'
        
        self.salt = salt # before sanitization(!)
        _salt = bytearray(16)
        # sanitization
        if len(salt) > 16:
            salt = salt[0:16]
                    
        _salt[0:len(salt)] = salt.encode('ASCII')
        self.anonymizer.SetSalt(str(_salt, 'ASCII')) # stupid, yet works consistently with gdcmanon.exe
        
    def getSalt(self):
        return self.salt
        
    def clearInternalUIDS(self):
        if self.dummy:
            warnings.warn('Internal UIDS cache is only used in non-dummy mode')        
        self.anonymizer.ClearInternalUIDs()
    
    def getInstance(self):
        return self.anonymizer            
