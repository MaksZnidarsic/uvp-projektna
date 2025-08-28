


import pandas as pd
from glob import glob
from os.path import join, isfile
import re, json

DATOTEKE = [ 'prostori_*', 'prostori-lastnosti_*', 'rocno-pregledane-lastnosti_*',
        'lastnosti_*', 'izreki_*', 'protiprimeri_*', 'sklici_*' ]

def preberi():
    poti = [ [ y for y in glob(join('podatki', x)) if isfile(y) ][-1] for x in DATOTEKE ]
    for x in poti:
        if not len(re.findall('.json', x)): yield pd.read_csv(x); continue
        with open(x, 'r', encoding = 'utf-8') as f: yield json.load(f)
