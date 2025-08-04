


from src.shrani import shrani
from src.narisi import narisiProstore, narisiProtiprimere
import time, sys
from os.path import join, basename


def kliciShrani():
    if len(sys.argv) >= 4: return shrani(sys.argv[2], sys.argv[3])
    cas = time.strftime("%Y-%m-%H-%M", time.localtime())
    mapa = sys.argv[2] if len(sys.argv) == 3 else './'
    shrani(join(mapa, 'prostori_' + cas + '.csv'), join(mapa, 'protiprimeri_' + cas + '.csv'))

def kliciNarisi():
    if len(sys.argv) < 4: return print('https://github.com/maksznidarsic/uvp-projektna')
    mapa = sys.argv[4] if len(sys.argv) == 5 else './'
    narisiProstore(sys.argv[2], join(mapa, 'vizualizacija-' + basename(sys.argv[2]) + '.png'))
    narisiProtiprimere(sys.argv[3], join(mapa, 'vizualizacija-' + basename(sys.argv[3]) + '.png'))

def main():
    if not len(sys.argv) - 1: return print('https://github.com/maksznidarsic/uvp-projektna')
    if sys.argv[1] == 'shrani': return kliciShrani()
    if sys.argv[1] == 'narisi': return kliciNarisi()

if __name__ == '__main__': main()
