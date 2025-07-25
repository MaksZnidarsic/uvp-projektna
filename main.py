


import requests, re
from bs4 import BeautifulSoup as bs


STRAN = 'https://topology.pi-base.org'

class Izrek:
    def __init__(self, ime, leva, desna):
        self.ime = ime
        self.leva = leva # ((Px_1, 1|0), ..., (Px_n, 1|0))
        self.desna = desna # (Px, 1|0)

    def __str__(self):
        return f'Izrek {self.ime} {self.leva} {self.desna}'

    def __repr__(self):
        return f'Izrek({self.ime}, {self.leva}, {self.desna})'

    def sledi(self, lastnosti):
        for x, y in self.leva:
            if lastnosti.get(x, None) != y: return False
        return True

    def izpeljiIzObrata(self, lastnosti):
        n = [ y for y, z in enumerate(self.leva) if z[0] not in lastnosti ]
        if len(n) != 1: return False
        for x, y in self.leva:
            if x == self.leva[n[0]][0]: continue
            if 1 - y == lastnosti[x]: return False
        return self.leva[n[0]][0], 1 - self.leva[n[0]][1]

class Prostor:
    def __init__(self, ime, lastnosti):
        self.ime = ime
        self.lastnosti = lastnosti

    def seznam(self):
        return [ self.ime, *map(lambda x : x[1], sorted(self.lastnosti.items(), key = lambda x : x[0])) ]

def izlusciPomen(s):
    return int(*re.findall('\\d{6}', s)), 1 - len(re.findall('¬', s))

def izlusciIzrek(ime_juha, leva_juha, desna_juha):
    pogoji_niz = leva_juha.decode_contents().split('â') # razcepi v in ($\land$, ∧)
    leva = tuple([ izlusciPomen(x) for x in pogoji_niz ])
    return Izrek(int(ime_juha.text[2:-1]), leva, izlusciPomen(desna_juha.decode_contents()))

def pridobiIzreke():
    juha = bs(requests.get(STRAN + '/theorems').text, features = 'lxml')
    vrstice = juha.find('table').find_all('td')
    razvrscene_vrstice = zip(vrstice[::4], vrstice[1::4], vrstice[2::4])
    return [ izlusciIzrek(*x) for x in razvrscene_vrstice ]

def pridobiLastnosti():
    juha = bs(requests.get(STRAN + '/properties').text, features = 'lxml')
    vrstice = juha.find('table').find_all('td')[::3]
    return [ int(x.text[2:-1]) for x in vrstice ]

def najdiLastnost(s):
    vrednost, ime, _, __ =  s.find_all('td')
    return int(ime.text[2:-1]), len(re.findall('M173', vrednost.decode_contents()))

def preveriIzrek(izrek, lastnosti, uporabljen):
    if uporabljen[izrek][0]: return uporabljen
    if izrek.desna[0] not in lastnosti and izrek.sledi(lastnosti):
        lastnosti[izrek.desna[0]] = izrek.desna[1]
        uporabljen[izrek][0] = True
        return uporabljen
    if uporabljen[izrek][1] or izrek.desna[0] not in lastnosti: return uporabljen
    if izrek.desna[1] == lastnosti[izrek.desna[0]]:
        uporabljen[izrek][1] = True
        return uporabljen
    lastnost = izrek.izpeljiIzObrata(lastnosti)
    if not lastnost: return uporabljen
    lastnosti[lastnost[0]] = lastnost[1]
    uporabljen[izrek][0] = True
    return uporabljen

def dopolniLastnosti(lastnosti, izreki, vse_lastnosti):
    dolzina_prejsnjic = len(lastnosti)
    uporabljen = { x : [ False, False ] for x in izreki }
    while True:
        for x in izreki: uporabljen = preveriIzrek(x, lastnosti, uporabljen)
        if dolzina_prejsnjic == len(lastnosti): break
        dolzina_prejsnjic = len(lastnosti)
    for x in vse_lastnosti: lastnosti.setdefault(x, None)
    return lastnosti

def lastnostiProstora(ime, izreki, vse_lastnosti):
    juha = bs(requests.get(STRAN + f'/spaces/S{ime:06d}').text, features = 'lxml')
    vrstice = juha.find('table').find('tbody').find_all('tr')
    lastnosti = {}
    for x in vrstice:
        ime, vrednost = najdiLastnost(x)
        lastnosti[ime] = vrednost
    lastnosti = dopolniLastnosti(lastnosti, izreki, vse_lastnosti)
    return lastnosti

def pridobiProstore(izreki, vse_lastnosti):
    juha = bs(requests.get(STRAN + '/spaces/all').text, features = 'lxml')
    vrstice = juha.find('table').find_all('td')[::3]
    prostori = []
    for x in vrstice:
        ime = int(x.text[2:-1])
        lastnosti = lastnostiProstora(ime, izreki, vse_lastnosti)
        prostori.append(Prostor(ime, lastnosti))
        print(f'S{ime}')
    return prostori

def jeProtiprimer(izrek, prostor):
    none = len([ x for x, y in izrek.leva if prostor.lastnosti[x] == None ])
    pregled = [ x for x, y in izrek.leva if prostor.lastnosti[x] == 1 - y ]
    protiprimer = int(izrek.desna[1] == prostor.lastnosti[izrek.desna[0]] and len(pregled) > 0)
    return 1 if protiprimer else ( None if none else 0)

def main():
    izreki = pridobiIzreke()
    vse_lastnosti = pridobiLastnosti()
    prostori = pridobiProstore(izreki, vse_lastnosti)
    with open('prostori', 'w') as f:
        print('', *vse_lastnosti, sep = ',', file = f)
        for x in prostori: print(*x.seznam(), sep = ',', file = f)
    with open('protiprimeri', 'w') as f:
        print('', *[ x.ime for x in prostori ], sep = ',', file = f)
        for x in izreki: print(x.ime, *[ jeProtiprimer(x, y) for y in prostori ], sep = ',', file = f)

if __name__ == '__main__': main()
