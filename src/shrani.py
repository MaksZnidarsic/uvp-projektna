


import requests, json, csv, re, random
from bs4 import BeautifulSoup as bs


STRAN = 'https://topology.pi-base.org/'

def link():
    r = random.choice(( '', 'spaces', 'spaces/all', 'properties', 'theorems', 'questions', 'dev' ))
    if r in ( '', 'spaces', 'questions', 'dev' ): return STRAN + r
    u = { 'spaces/all' : ( 3, 'S' ), 'properties' : ( 3, 'P' ), 'theorems' : ( 4, 'T' ) }
    juha = bs(requests.get(STRAN + r).text, features = 'html.parser')
    pot = random.choice(juha.find('table').find_all('td')[::u[r][0]])
    return STRAN + r + '/' + re.findall(u[r][1] + '\\d{6}', str(pot))[0]

def preurediIzreke(izreki):
    for x in izreki:
        atom = { 'kind' : 'atom', 'property' : x['when'].get('property'), 'value' : x['when'].get('value') }
        x['when'] = x['when'].get('subs', [ atom ])
    return izreki

def preberiLastnosti(podatki):
    lastnosti = dict()
    for x in podatki:
        lastnosti.setdefault(x['space'], dict())[x['property']] = x['value']
    return lastnosti

def sledi(izrek, lastnosti):
    return all([ lastnosti.get(x['property']) == x['value'] for x in izrek['when'] ])

def slediIzKontrapozicije(izrek, lastnost, lastnosti):
    return all([ not (1 - x['value'] == lastnosti[x['property']])
                for x in izrek['when'] if x['property'] != lastnost ])

def preveriIzrek(izrek, lastnosti):
    if sledi(izrek, lastnosti):
        lastnosti[izrek['then']['property']] = izrek['then']['value']
        return True
    if izrek['then']['property'] not in lastnosti: return False
    if izrek['then']['value'] == lastnosti[izrek['then']['property']]: return True
    n = [ x for x, y in enumerate(izrek['when']) if y['property'] not in lastnosti ]
    if not len(n): return True
    if len(n) > 1: return False
    _, lastnost, vrednost = [ *izrek['when'][n[0]].values() ]
    if slediIzKontrapozicije(izrek, lastnost, lastnosti): lastnosti[lastnost] = bool(1 - vrednost)
    return True


def dopolniLastnosti(lastnosti, izreki, vse_lastnosti):
    dolzina = len(lastnosti)
    uporabljen = { x['uid'] : False for x in izreki }
    while True:
        for x in izreki:
            if not uporabljen[x['uid']]: uporabljen[x['uid']] = preveriIzrek(x, lastnosti)
        if dolzina == (dolzina := len(lastnosti)): break
    for x in vse_lastnosti: lastnosti.setdefault(x)
    return lastnosti

def jeProtiprimer(izrek, lastnosti):
    none = len([ x for x in izrek['when'] if lastnosti[x['property']] == None ])
    pregled = [ x['property'] for x in izrek['when'] if lastnosti[x['property']] == 1 - x['value'] ]
    protiprimer = (izrek['then']['value'] == lastnosti[izrek['then']['property']]) and len(pregled)
    return None if none else bool(protiprimer)

def shrani(
        prostori_pot,
        prostori_lastnosti_pot,
        lastnosti_pot,
        izreki_pot,
        protiprimeri_pot,
        sklici_pot
          ):
    juha = bs(requests.get(link()).text, features = 'html.parser')
    podatki = json.loads(json.loads(juha.find('body').find('script').text)['body'])

    izreki = preurediIzreke(podatki['theorems'].copy())
    vse_lastnosti = [ x['uid'] for x in podatki['properties'] ]
    vsi_prostori = [ x['uid'] for x in podatki['spaces'] ]
    lastnosti_prostorov = preberiLastnosti(podatki['traits'])
    for x in lastnosti_prostorov.values(): dopolniLastnosti(x, izreki, vse_lastnosti)

    with open(prostori_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'prostor', 'uid', ' aliasov', 'št. sklicev', 'opis' ))
        for x in podatki['spaces']: w.writerow(( x['name'], x['uid'],
                len(x.get('aliases', [])), len(x.get('refs', [])), x['description'] ))

    with open(prostori_lastnosti_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'prostor', *vse_lastnosti ))
        for x in vsi_prostori: w.writerow(( x,
                *[ lastnosti_prostorov[x][y] for y in vse_lastnosti ] ))

    with open(lastnosti_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'lastnost', 'uid', 'št. aliasov', 'št. sklicev', 'opis' ))
        for x in podatki['properties']: w.writerow(( x['name'], x['uid'],
                len(x.get('aliases', [])), len(x.get('refs', [])), x['description'] ))

    with open(izreki_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'izrek', 'če', 'potem', 'št. sklicev', 'opis' ))
        for x in izreki: w.writerow(( x['uid'], repr(x['when']), repr(x['then']),
                len(x.get('refs', [])), x['description'] ))

    with open(protiprimeri_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'izrek', *vsi_prostori ))
        for x in izreki: w.writerow(( x['uid'],
                *[ jeProtiprimer(x, lastnosti_prostorov[y]) for y in vsi_prostori ] ))

    #with open(reference_pot, 'w', encoding = 'utf-8', newline = '') as f:
        #w = csv.writer(f)
        #w.writerow(( 'referenca', ))
