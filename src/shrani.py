


import requests, re, json
from bs4 import BeautifulSoup as bs


STRAN = 'https://topology.pi-base.org'

class Izrek:
    def __init__(self, ime, leva, desna):
        self.ime = ime
        self.leva = leva # ((Px_1, 1|0), ..., (Px_n, 1|0))
        self.desna = desna # (Px, 1|0)

    def sledi(self, lastnosti):
        for x, y in self.leva:
            if lastnosti.get(x, None) != y: return False
        return True

    def slediIzKontrapozicije(self, lastnost, lastnosti):
        for x, y in filter(lambda x : x[0] != lastnost, self.leva):
            if 1 - y == lastnosti[x]: return False
        return True

class Prostor:
    def __init__(self, ime, indeks, lastnosti):
        self.ime = ime
        self.indeks = indeks
        self.lastnosti = lastnosti

    def seznam(self):
        lasnosti = [ x[1] for x in sorted(self.lastnosti.items(), key = lambda x : x[0]) ]
        return [ self.ime, self.indeks, *lasnosti ]

def izlusciPomen(s):
    return int(*re.findall('\\d{6}', s)), 1 - len(re.findall('¬', s))

def izlusciIzrek(ime_juha, leva_juha, desna_juha):
    pogoji_niz = leva_juha.decode_contents().split('â') # razcepi v "in" ($\land$, ∧)
    leva = tuple([ izlusciPomen(x) for x in pogoji_niz ])
    return Izrek(int(ime_juha.text[2:-1]), leva, izlusciPomen(desna_juha.decode_contents()))

def pridobiIzreke():
    juha = bs(requests.get(STRAN + '/theorems').text, features = 'html.parser')
    vrstice = juha.find('table').find_all('td')
    razvrscene_vrstice = zip(vrstice[::4], vrstice[1::4], vrstice[2::4])
    return [ izlusciIzrek(*x) for x in razvrscene_vrstice ]

def pridobiLastnostiInImenaProstorov():
    # v html-ju vsakega prostora je "baked in" json vseh lastnosti in prostorov
    juha = bs(requests.get(STRAN + '/spaces/S000001').text, features = 'html.parser')
    _json = json.loads(json.loads(juha.find('body').find('script').text)['body'])
    lastnosti = { int(x['uid'][1:]) : x['name'] for x in _json['properties'] }
    prostori = { int(x['uid'][1:]) : x['name'] for x in _json['spaces'] }
    return lastnosti, prostori

def najdiLastnost(s):
    vrednost, ime, _, __ =  s.find_all('td')
    return int(ime.text[2:-1]), len(re.findall('M173', vrednost.decode_contents()))

def preveriIzrek(izrek, lastnosti, uporabljen):
    if uporabljen[izrek]: return
    if izrek.desna[0] not in lastnosti and izrek.sledi(lastnosti):
        lastnosti[izrek.desna[0]] = izrek.desna[1]
        uporabljen[izrek] = True
        return
    if izrek.desna[0] not in lastnosti or izrek.desna[1] == lastnosti[izrek.desna[0]]: return
    lastnost = [ y for y, z in enumerate(izrek.leva) if z[0] not in lastnosti ]
    if len(lastnost) != 1: return
    if izrek.slediIzKontrapozicije(izrek.leva[lastnost[0]][0], lastnosti):
        lastnosti[izrek.leva[lastnost[0]][0]] = 1 - izrek.leva[lastnost[0]][1]
    uporabljen[izrek] = True

def dopolniLastnosti(lastnosti, izreki):
    dolzina_prejsnjic = len(lastnosti)
    uporabljen = { x : False for x in izreki }
    while True:
        for x in izreki: preveriIzrek(x, lastnosti, uporabljen)
        if dolzina_prejsnjic == len(lastnosti): break
        dolzina_prejsnjic = len(lastnosti)

def lastnostiProstora(indeks, izreki, vse_lastnosti):
    juha = bs(requests.get(STRAN + f'/spaces/S{indeks:06d}').text, features = 'html.parser')
    vrstice = juha.find('table').find('tbody').find_all('tr')
    lastnosti = {}
    for x in vrstice:
        ime, vrednost = najdiLastnost(x)
        lastnosti[ime] = vrednost
    dopolniLastnosti(lastnosti, izreki)
    for x in vse_lastnosti: lastnosti.setdefault(x, None)
    return lastnosti

def pridobiProstore(izreki, imena_prostorov, vse_lastnosti):
    prostori = []
    for x, y in imena_prostorov.items():
        lastnosti = lastnostiProstora(x, izreki, vse_lastnosti)
        prostori.append(Prostor(y, x, lastnosti))
        print('Prostor', x, y)
    return prostori

def jeProtiprimer(izrek, prostor):
    none = len([ x for x, y in izrek.leva if prostor.lastnosti[x] == None ])
    pregled = [ x for x, y in izrek.leva if prostor.lastnosti[x] == 1 - y ]
    protiprimer = izrek.desna[1] == prostor.lastnosti[izrek.desna[0]] and len(pregled)
    return 1 if protiprimer else ( None if none else 0)

def shrani(prostori_pot, protiprimeri_pot):
    izreki = pridobiIzreke()
    vse_lastnosti, imena_prostorov = pridobiLastnostiInImenaProstorov()
    prostori = pridobiProstore(izreki, imena_prostorov, vse_lastnosti.keys())
    with open(prostori_pot, 'w', encoding = 'utf-8') as f:
        lastnosti = sorted(vse_lastnosti.items(), key = lambda x : x[0])
        print('prostor', 'indeks', *[ x[1] for x in lastnosti ], sep = ',', file = f)
        print(None, None, *[ x[0] for x in lastnosti ], sep = ',', file = f)
        for x in prostori: print(*x.seznam(), sep = ',', file = f)
    with open(protiprimeri_pot, 'w', encoding = 'utf-8') as f:
        print('izrek', *imena_prostorov.values(), sep = ',', file = f)
        print(None, *imena_prostorov.keys(), sep = ',', file = f)
        for x in izreki: print(x.ime, *[ jeProtiprimer(x, y) for y in prostori ], sep = ',', file = f)
