


import requests, json, csv, re, random
from bs4 import BeautifulSoup as bs


STRAN = 'https://topology.pi-base.org/'

def link():
    r = random.choice(( '', 'spaces', 'spaces/all', 'properties', 'theorems', 'questions', 'dev' ))
    if r in ( '', 'spaces', 'questions', 'dev' ): return STRAN + r
    u = { 'spaces/all' : ( 3, 'S' ), 'properties' : ( 3, 'P' ), 'theorems' : ( 4, 'T' ) }
    juha = bs(requests.get(STRAN + r).text, features = 'html.parser')
    pot = random.choice(juha.find('table').find_all('td')[::u[r][0]])
    return STRAN + r.split('/')[0] + '/' + re.findall(u[r][1] + '\\d{6}', str(pot))[0]

def preurediPogoj(pogoj):
    return { 'lastnost' : pogoj['property'], 'vrednost' : pogoj['value'] }

def preurediIzreke(podatki):
    izreki = []
    for x in podatki:
        izrek = {}
        izrek['uid'] = x['uid']
        if x['when']['kind'] == 'atom': izrek['pogoj'] = [ preurediPogoj(x['when']) ]
        else: izrek['pogoj'] = [ preurediPogoj(y) for y in x['when']['subs'] ]
        izrek['posledica'] = preurediPogoj(x['then'])
        izrek['opis'] = x['description']
        izreki.append(izrek)
    return izreki

def preberiLastnosti(podatki):
    lastnosti = dict()
    for x in podatki:
        lastnosti.setdefault(x['space'], dict())[x['property']] = x['value']
    return lastnosti

def sledi(izrek, lastnosti):
    return all([ lastnosti.get(x['lastnost']) == x['vrednost'] for x in izrek['pogoj'] ])

def slediIzKontrapozicije(izrek, lastnost, lastnosti):
    return all([ not (1 - x['vrednost'] == lastnosti[x['lastnost']])
                for x in izrek['pogoj'] if x['lastnost'] != lastnost ])

def preveriIzrek(izrek, lastnosti):
    if sledi(izrek, lastnosti):
        lastnosti[izrek['posledica']['lastnost']] = izrek['posledica']['vrednost']
        return True
    if izrek['posledica']['lastnost'] not in lastnosti: return False
    if izrek['posledica']['vrednost'] == lastnosti[izrek['posledica']['lastnost']]: return True
    n = [ x for x, y in enumerate(izrek['pogoj']) if y['lastnost'] not in lastnosti ]
    if not len(n): return True
    if len(n) > 1: return False
    lastnost, vrednost = [ *izrek['pogoj'][n[0]].values() ]
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

def preberiSklice(podatki):
    sklici = dict()
    prevod = { 'spaces' : 'prostori', 'traits' : 'prostori-lastnosti',
            'theorems' : 'izreki', 'properties' : 'lastnosti' }
    for x in list(podatki.keys())[:-1]:
        for y in podatki[x]:
            for z in y['refs']:
                sklici.setdefault(z['name'], dict())['vrsta'] = list(z.keys())[-1]
                sklici[z['name']]['ekstra'] = z[sklici[z['name']]['vrsta']]
                sklici[z['name']].setdefault('št. v ' + prevod[x], 0)
                sklici[z['name']]['št. v ' + prevod[x]] += 1
    for x in sklici.values():
        x['skupaj'] = sum([ x.setdefault('št. v ' + y, 0) for y in prevod.values() ])
    return sklici

def jeProtiprimer(izrek, lastnosti):
    none = len([ x for x in izrek['pogoj'] if lastnosti[x['lastnost']] == None ])
    pregled = [ x['lastnost'] for x in izrek['pogoj']
            if lastnosti[x['lastnost']] == 1 - x['vrednost'] ]
    protiprimer = (izrek['posledica']['vrednost'] == lastnosti[izrek['posledica']['lastnost']]
            and len(pregled))
    return None if none else bool(protiprimer)

def shrani(
        prostori_pot,
        prostori_lastnosti_pot,
        rocno_pregledane_lastnosti_pot,
        lastnosti_pot,
        izreki_pot,
        protiprimeri_pot,
        sklici_pot
          ):
    juha = bs(requests.get(pot := link()).text, features = 'html.parser')
    podatki = json.loads(json.loads(juha.find('body').find('script').text)['body'])
    print('pobrano iz', pot)

    izreki = preurediIzreke(podatki['theorems'])
    vse_lastnosti = [ x['uid'] for x in podatki['properties'] ]
    vsi_prostori = [ x['uid'] for x in podatki['spaces'] ]
    lastnosti_prostorov = preberiLastnosti(podatki['traits'])
    for x in lastnosti_prostorov.values(): dopolniLastnosti(x, izreki, vse_lastnosti)
    sklici = preberiSklice(podatki)

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

    with open(rocno_pregledane_lastnosti_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'prostor', 'lastnost', 'vrednost', 'št. sklicev', 'opis' ))
        for x in podatki['traits']: w.writerow(( x['space'], x['property'], x['value'],
                len(x['refs']), x['description'] ))

    with open(lastnosti_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'lastnost', 'uid', 'št. aliasov', 'št. sklicev', 'opis' ))
        for x in podatki['properties']: w.writerow(( x['name'], x['uid'],
                len(x.get('aliases', [])), len(x.get('refs', [])), x['description'] ))

    with open(izreki_pot, 'w', encoding = 'utf-8') as f:
        print(json.dumps(izreki, indent = 2), file = f)

    with open(protiprimeri_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        w.writerow(( 'izrek', *vsi_prostori ))
        for x in izreki: w.writerow(( x['uid'],
                *[ jeProtiprimer(x, lastnosti_prostorov[y]) for y in vsi_prostori ] ))

    with open(sklici_pot, 'w', encoding = 'utf-8', newline = '') as f:
        w = csv.writer(f)
        macke = ( 'vrsta', 'ekstra', 'št. v prostori', 'št. v prostori-lastnosti',
                'št. v lastnosti', 'št. v izreki', 'skupaj' )
        w.writerow(( 'ime', *macke ))
        for x in sklici.keys(): w.writerow(( x, *[ sklici[x][y] for y in macke ] ))

if __name__ == '__main__':
    juha = bs(requests.get(pot := link()).text, features = 'html.parser')
    podatki = json.loads(json.loads(juha.find('body').find('script').text)['body'])

    print(podatki['traits'][30])
