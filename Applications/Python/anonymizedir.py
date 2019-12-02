#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:43:01 2019

@author: jacek.kawa@radpoint.pl
"""


from gdcmanon import Gdcmanon
from gdcmanon import anon as an

import sys
import gdcm
import json
import sqlite3
import random
from cachetools import LRUCache


class radAnonimizer(Gdcmanon.AnonWrapper):
    malenames = ['ANASTAZY', 'BONIFACY', 'CECYL', 'DOBROMIR', 'EUSTACHY', 'FABIUSZ', 'GERWAZY', 'HIACYNT', 'IDZI', 'JACENTY', 'KASJAN', 'LAMBERT', 'MAKARY', 'NEPOMOUCEN', 'ONUFRY', 'PONCYLIUSZ', 'RAJMUND', 'SERWACY', 'TEOBALD', 'URBAN', 'WIT', 'ZACHARIASZ', 'LETO', 'TWOFLOWER', 'RUMCAJS', 'HAVELOCK', 'ELVIS', 'RAJMUND', 'BILL', 'CLIVE', 'BUTCH', 'PETER', "ALEXANDRE", "ALFRED", "ARNOLD", "AURELIUSZ", "BARNABA", "BEN", "DMYTRO", "DYMITR", "ELIJAH", "EMMANUEL", "FINN", "FRANCIS", "GEORGE", "GROMOSLAW", "HORACY", "JOHANNES", "JOSEPH", "KONSTANTYN", "LUBOMIR", "LUCA", "MASON", "NICO", "RAFAEL", "RICHARD", "ROBIN", "ROGER", "SALOMON", "SASZA", "SIEMOWIT", "STANISLAW", "TIM", "TIMOTHY", "TYMUR", "VOLODYMYR", "YASIN", "YASSIN", "ZACHAR", "ZAHAR", "AMIN", "ANGELO", "BORIS", "BRANDON", "CASPIAN", "DENNIS", "DIONIZY", "EGOR", "EUZEBIUSZ", "FABIO", "HENRIK", "ILYA", "ISMAEL", "JASPER", "JAYDEN", "JURIJ", "KONSTANTIN", "KSAVIER", "LENART", "LEONID", "LESLAW", "LEVI", "LUDWIG", "MARCELLO", "MAXIME", "MAXIMILIANO", "MELCHIOR", "MILOSZ", "MODEST", "NATANEL", "NIKLAS", "OLEH", "OLEKSII", "OMAR", "PAUL", "RAJAN", "RODRIGO", "RUDOLF", "SAM", "THIAGO", "TOMMY", "TRISTAN", "VITALI", "XAVERY", "ZAWISZA", "ABDULLAH", "ADNAN", "AIDAN", "AIDEN", "ALEJANDRO", "ALEKSANDR", "ALEKSIEJ", "ALESSIO", "ANDREAS", "ANDREI", "ANDRIY", "ANTONIUSZ", "ARYAN", "AUGUSTIN", "BALTAZAR", "BJORN", "CHARLES", "CRISTIAN", "CZCIBOR", "DANIL", "DEXTER", "DMITRIJ", "ELLIOT", "ENES", "ENZO", "ESTEBAN", "FREDERICK", "GERALD", "GIOVANNI", "GUSTAV", "HAMZA", "HERBERT", "IBRAHIM", "IDZI", "ILIAN", "ILIAS", "ISAAC", "JAROSLAW", "JEGOR", "JOSEF", "JOZUE", "JUSTIN", "KENAN", "KIRILL", "KRISTIAN", "KSAVERY", "LIONEL", "MALIK", "MARCELL", "MARIO", "MARSEL", "MASSIMO", "MATEI", "MATTHIAS", "MATVIY", "MIKE", "MIKHAIL", "MILOSLAW", "MIRAN", "MIROSLAW", "MUSA", "NATANAEL", "NESTOR", "NHAT", "OKTAWIUSZ", "ORLANDO", "PAVLO", "RADOSZ", "RAJMUND", "RAMI", "ROMEO", "SEMEN", "SWIATOSLAW", "TIAGO", "TIMON", "TOBY", "TOMMASO", "UMAR", "VALENTINO", "VITALII", "VLADIMIR", "WALERY", "WIESLAW", "WITALIJ", "WLADYSLAW", "XANDER", "YAROSLAV", "ZAC", "ZACK", "ZBYSZKO", "AAYAN", "ADRIEN", "AKIM", "ALBANO", "ALEC", "ALEKSEJ", "ALEN", "ALEXANDROS", "ALEXY", "ALPER", "ALVARO", "AMINE", "ANDRE", "ANGEL", "ARCHIBALD", "ARIS", "ARMANDO", "ARSENIUSZ", "ARTEMIJ", "ASEN", "ASHER", "ATANAZY", "ATHARVA", "ATTILA", "AYAN", "AYAZ", "BOZYDAR", "CHARLIE", "COLLIN", "CONAN", "CRISTIANO", "CZAREK", "DAGMAR", "DANG", "DANTE", "DARIAN", "DARIO", "DASTIN", "DAVIDE", "DAVINCI", "DAVIT", "DEMIAN", "DEMJAN", "DENIEL", "DENIZ", "DRAGOMIR", "EDUARD", "EINAR", "EKAM", "ELI", "ELIOTT", "ELYAS", "EREN", "EUSTACHY", "EZEL", "FARES", "FERENC", "FRANCISCO", "FRANCO", "FRANKIE", "FRANKO", "GABRIELE", "GAGIK", "GAWEL", "GERALT", "GIA", "GIUSEPPE", "GLEB", "GOR", "GORAN", "GWIDON", "HAI", "HARIS", "HARUN", "HAYK", "HENDRIK", "HOANG", "HOANG", "HOANG", "IDRIS", "ILJA", "ILLIA", "IMRAN", "JAMAL", "JANUARY", "JAROSLAV", "JAVIER", "JOAN", "JOHANN", "JONAS", "JOSE", "JOSZKO", "JOZEF", "JUAN", "JUDA", "JULIEN", "JULIO", "JULIUS", "JUNHAO", "JURII", "KAMIL", "KEITH", "KENZO", "KEREM", "KHALID", "KIRIL", "KORAY", "KOSTEK", "KOSTIANTYN", "LARGO", "LEO", "LEON", "LINUS", "LIO", "LIVIAN", "LLOYD", "LONGIN", "LOTAR", "LUCIAN", "MACIEK", "MALAKAI", "MARCELIN", "MARCELINO", "MATEUSH", "MATHEO", "MATIAS", "MATTIA", "MATVEJ", "MATVEY", "MATWIEJ", "MATWIJ", "MAURICE", "MAXIMILIEN", "MAXIMILLIAN", "MAXWELL", "MERGEN", "MICHEL", "MIHAIL", "MIKEL", "MINH", "MINH", "MINH", "MIROSLAV", "MOHAMED", "MORGAN", "MUSTAFA", "MYKOLA", "MYRON", "NAREK", "NAWOJ", "NAZARII", "NIKOLAI", "NORMAN", "OCTAVIAN", "ORHAN", "OSTAP", "OTTO", "PAULO", "PAVEL", "PAWEL", "PEDRO", "PHAN", "PHILIPPE", "QUENTIN", "RAPHAEL", "RAUL", "RAVI", "REMI", "REYANSH", "RICARDO", "ROBERTO", "ROHAN", "RONALD", "RUDRA", "RUFIN", "RUSLAN", "SALAH", "SALVADOR", "SAMSON", "SELIM", "SELIM", "SEMIR", "SERGIO", "SERHII", "SHER", "SHIVANSH", "SINAN", "SLAWOJ", "SOBIESLAW", "STANISLAS", "STANLEY", "STEVEN", "SULEIMAN", "SVEN", "SVIATOSLAV", "SCIBOR", "TADEJ", "TARAS", "TEOMAN", "THEO", "TIGRAN", "TIMO", "TIMOFEI", "TOM", "TOMEK", "TOMIR", "TONI", "TRAIAN", "TUAN", "VENIAMIN", "WADIM", "WALENTY", "WALTER", "WITEK", "WITOSZ", "WLADIMIR", "WOJMIR", "WOLFGANG", "YAKUB", "YAREMA", "YEHOR", "YURI", "YUVAAN", "ZAID", "ZAKARIYA", "ZAYAN", "ZBYSZEK"]
    femalenames = ['ALFREDA', 'BIANKA', 'CECYLIA', 'DELFINA', 'EUFEMIA', 'FILOMENA', 'GERTRUDA', 'IMELDA', 'JOLENTA', 'KLOTYLDA', 'LUTGARDA', 'MECHTYLDA', 'NIKODEMA', 'ODYLIA', 'OKTAWIA', 'PELAGIA', 'RUTA', 'SCHOLASTYKA', 'TEKLA', 'UMA', 'WERIDIANA', 'ZYTA', 'ELEANOR', 'ARWEN', 'PERSEFONA', 'NIKODEZJA', 'ROZA', 'STOKROTKA', 'CIRI', 'ALEXANDRA', "ELA", "GRACJA", "GRACJANA", "INGRID", "IVANKA", "JENNIFER", "JESIKA", "KAMELIA", "KATERYNA", "KRISTINA", "LATIKA", "LEOKADIA", "LINA", "LINDA", "MAIA", "MANUELA", "MARIIA", "MARYAM", "MELODY", "MICHAELA", "MIKA", "NAWOJKA", "PAMELA", "PETRA", "ROSE", "SCARLETT", "SLAWA", "SOLOMIIA", "SUSANNA", "TETIANA", "TINA", "ULIANA", "VALENTINA", "YASMINA", "AIDA", "ALANA", "ALDONA", "ALENA", "ANATOLIA", "ATHENA", "AUDREY", "BERNADETTA", "BOGUSLAWA", "CHANEL", "CYNTIA", "ELEANOR", "ELSA", "EMILI", "EVELINA", "GEORGIA", "GIULIA", "JAGIENKA", "JULIE", "KAYLA", "LEONIE", "LIANA", "MADELEINE", "MALENA", "MARIAM", "MARIANA", "MELA", "MILLA", "MILA", "MOLLY", "NATASHA", "NELLI", "OLENA", "RAISA", "ROSALIA", "SAMANTHA", "SAVANNAH", "SELIN", "SUSANNE", "TESSA", "VERA", "VERONICA", "WALENTYNA", "YASMINE", "YEVA", "ZARINA", "ZOEY", "ADEL", "AILA", "ALEKSA", "ALISHA", "ALYA", "AMBER", "ANABELLA", "ANGELICA", "ANNABELLE", "ASYA", "AYLIN", "BERNADETA", "BOGDANA", "BRONISLAWA", "CARLOTTA", "CATTLEYA", "CIRILLA", "DAMROKA", "DANIELLA", "DINA", "DONATA", "ELINA", "ELISE", "ELLIE", "ESMERALDA", "FABIOLA", "FLAWIA", "FREJA", "GRACE", "ILIA", "INDIA", "ISABEL", "ISLA", "ISMENA", "IVA", "IVY", "KAJRA", "KAMILLA", "KATRINA", "LAJLA", "LAURENCJA", "LEIA", "LEONA", "LENA", "LILIAN", "LILLIAN", "MAGNOLIA", "MARGARET", "MARGARYTA", "MARISA", "MASZA", "MELANI", "MIRELA", "NATALIIA", "NEYLA", "NIKOLETA", "NIKOLINA", "NILA", "OTOLIA", "PELAGIA", "PIA", "POLIANA", "PRISHA", "RACHELA", "ROSALIE", "ROZALINA", "RUBY", "RUT", "RUTA", "SASHA", "SELMA", "SOFIYA", "TAIDA", "VALERIIA", "VITTORIA", "VIVIAN", "WIERA", "XENIA", "AAHANA", "AALIYAH", "ADELIA", "AIMEE", "AISZA", "AJSZA", "ALESSANDRA", "ALESSIA", "ALEXIA", "ALISSIA", "ALITA", "ALVIRA", "ALYSSA", "AMAIA", "AMALIA", "AMARACHI", "AMELA", "AMELIA", "ANABEL", "ANABELA", "ANABELL", "ANABELLE", "ANELIA", "ANETTA", "ANGEL", "ANIA", "ANYA", "ARLENA", "ARLETTA", "ARLO", "ARNIKA", "ASEL", "ASHLEY", "ASIYA", "ASTEJA", "AUGUSTYNA", "AURIKA", "AYESHA", "AYSE", "BAO", "CAMILA", "CANSU", "CARLA", "CAROLINA", "CAROLINE", "CELIA", "CELINE", "CLAIRE", "CLARISSA", "CYNTHIA", "DANA", "DARINA", "DORA", "ELENI", "ELIZABET", "ELMIRA", "EMA", "EMANUELA", "EMILIANA", "EMILIIA", "EMINE", "ERIN", "ESTELLE", "EULALIA", "FLORENTINA", "FRIDA", "GABI", "GABRYJELA", "GEMMA", "GIA", "HELEN", "HOAI", "ILARIA", "IMAN", "INES", "IRINA", "IRIS", "IRMA", "IVANNA", "IWA", "IWANKA", "JAGA", "JEWA", "JOZEFA", "JUDITH", "KAMILIA", "KARLA", "KATHRIN", "KHLOE", "KIM", "KLARYSA", "KLEOPATRA", "KORDELIA", "LANA", "LEJLA", "LENNA", "LETI", "LEA", "LILLIANA", "LIUBOV", "LIA", "LORA", "LOUISA", "LOUISE", "LUCIA", "LUCJA", "LUSI", "MADLEN", "MALVINA", "MARCELINE", "MARGOT", "MARIJA", "MARYNA", "MASHA", "MAURA", "MELEK", "MIGLENA", "MINH", "MIYA", "NADIN", "NADIYA", "NADJA", "NAILA", "NARE", "NELLIE", "NGOC", "NORA", "PHOEBE", "QIANYU", "RAMONA", "ROZA", "SABRINA", "SAIDA", "SAWA", "SCARLET", "SELINA", "SEMILIANA", "SERAFINA", "SIENNA", "SIMONE", "SOFI", "SOFII", "SOFIKO", "SOFIA", "SOLOMIA", "SOLOMIJA", "SORAYA", "SUMAYA", "SUSAN", "SUZAN", "SUZANNA", "SYNTIA", "SZYMON", "TALIA", "TALITA", "TEODOZJA", "TEOFILA", "THANH", "THEA", "THIEN", "TIANTIAN", "TUE", "ULJANA", "ULLA", "VANESA", "VARVARA", "VIKTORIE", "VIRA", "VIRGINIA", "VLADYSLAVA", "WARWARA", "WERA", "YELYZAVETA", "ZELIA", "ZLATOSLAVA", "ZORA", "ZORIA", "ZUZANA", "ZAKLINA"]
    
    surnames = ['PODOLSKI', 'DUDA', 'WAWELSKI', 'MAZOWSKI', 'CHORTEKS', 'OLSZA', \
                'SMITH', 'SCHMIDT', 'KOWALSKI', 'KALVIS', 'KOVAC', 'FABER', \
                'NIEWIEM', 'KOVOTEPEC', 'TUMELO', 'HERRERO', 'SEPPA', 'HAMPO', \
                'SMID', 'IMANI', 'BAGGINS', 'TUK', 'GAMGEE', 'BRANDYBUCK', \
                'BOLGER', 'DELVING', 'BANKS', 'TOOK', 'ATREIDES', 'HARKONNEN', \
                'CORRINO', 'TUEK', 'KYNES', 'MAPES', 'DE VRIES', 'HALLECK', \
                'IDAHO', 'HAWAT', 'IRONFUNDERSON', 'VIMES', 'GARLIC', \
                'WETHERWAX', 'OGG', 'STOLAT', 'SPULDING', 'VETINARI', \
                'HERBATA', 'BIGOS', 'WIERZCHON', 'KOZLOWSKI', 'NUTTER']

    def __init__(self, anonymizer, dbfile):
        super().__init__(anonymizer)

        # cache name substitutions
        self.cache = LRUCache(maxsize = 100)
        
        # handle DB
        self.dbfile = dbfile
        self.cursor = None
        self.conn = None
        self.reinitialize()
        
    def reinitialize(self):
        self.conn = sqlite3.connect(self.dbfile)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS mapping " \
                            "(anonID TEXT, fakeID TEXT)" )
        self.cursor.execute("CREATE INDEX IF NOT EXISTS ai ON mapping(anonID)")
        self.conn.commit()
        
    def process(self):
        
        # main part
        ret = self.anonymizer.RemovePrivateTags()
        if not ret:
            return False
        ret = self.anonymizer.BasicApplicationLevelConfidentialityProfile(True)
        if not ret:
            return False
        
        # reinvent PatientName
        f = self.anonymizer.GetFile()
        ds = f.GetDataSet()

	# this fields for some reason have the space on the rightmost position, so rstrip()
        pid = str((ds.GetDataElement(gdcm.Tag(0x10, 0x20))).GetValue()).rstrip()
        psex = str((ds.GetDataElement(gdcm.Tag(0x10, 0x40))).GetValue()).rstrip()

        #print(f"pid={pid}, psex={psex}")
        pName = self._findAlias(pid, psex)
        
        return self.anonymizer.Replace(gdcm.Tag(0x10, 0x10), pName)
    
    def _findAlias(self, pid, psex):
        
        #L1 cache to easy find most recent substitutions
        name = self.cache.get(pid)
        if name is not None:
            return name

        #then seek in the DB
        self.cursor.execute("SELECT fakeID FROM mapping " \
                            "WHERE anonID = ?", (pid, ))
        ret = self.cursor.fetchone()
        if ret is None:
            # previously unseen
            name = radAnonimizer._generateName(psex)
            self.cursor.execute("INSERT INTO mapping VALUES (?,?)", (pid, name))
            self.conn.commit()
        else:
            # seen
            name = ret[0]

        # one way or another: cache it
        self.cache[pid] = name
        return name
        
    def _generateName(sex):
        #print(f"sex=|{sex}|")
        if sex == 'F':
            Name = random.choice(radAnonimizer.femalenames)
        else:
            Name = random.choice(radAnonimizer.malenames)
            
        Surname = random.choice(radAnonimizer.surnames)
        PatientName = "%s^%s^^^" % (Surname, Name)
        return PatientName
        
    def finalize(self):
        self.conn.close()
        
       
        
def main(src, dst, mapping, salt):
    # setup gdcm anonymizer        
    # key = None, cert = None, deterministicUIDs = True, \
    #                 generateDummyNames = True, salt = None, \
    #                 removeTags = None, addTags = None):
    
    b = Gdcmanon.Gdcmanon(key = 'openssl/key.key', cert = 'openssl/cert.pem', \
                          salt = salt, deterministicUIDs = True, \
                          generateDummyNames = True)
    #Sex, Study/Series Description, Weight
    b.removeTagsFromBALCPA(list((gdcm.Tag(0x10,0x40), gdcm.Tag(0x8,0x1030), \
                                gdcm.Tag(0x8,0x103e), gdcm.Tag(0x10, 0x1030), \
                                gdcm.Tag(0x10, 0x1010))))
    
    # create wrapper with custom anonymization procedure coded in process()
    # and open connections to db
    wrapper = radAnonimizer(b.getInstance(), mapping)
    
    # create the crawler/tool
    anonymizer = an.anon(wrapper)
    stat, ret = anonymizer.anonimizeDir(src, dst)

    return (stat, ret)

if __name__ == '__main__':

    gdcm.Trace.DebugOff()
    gdcm.Trace.WarningOff()
    gdcm.Trace.ErrorOff()    
    
    if len(sys.argv) < 3:
        print(f"invoke: {sys.argv[0]} srcDir destDir")
        sys.exit(1)
        
    src = sys.argv[1]
    dst = sys.argv[2]
    mapping = "mapping.db" # sqlite3 db with patientID (after deterministic anonymization) <-> fake name/surname mappings
    salt = '55'
    
    stat, ret = main(src, dst, mapping, salt)

    print(f'OK={stat["ok"]}, FAILED={stat["fail"]}, SKIPPED={stat["skipped"]}', file = sys.stderr)
    print(json.dumps(ret))
    
