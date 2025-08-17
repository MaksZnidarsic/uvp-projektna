


from os.path import join, isdir
from os import getcwd
import time, sys
from src.shrani import shrani


def main():
    direktorij = join(getcwd(), sys.argv[1] if len(sys.argv) >= 2 else '.')
    if not isdir(direktorij): return print('podana pot ne obstaja :/')
    cas = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
    shrani(
            join(direktorij, 'prostori_' + cas + '.csv'),
            join(direktorij, 'prostori-lastnosti_' + cas + '.csv'),
            join(direktorij, 'lastnosti_' + cas + '.csv'),
            join(direktorij, 'izreki_' + cas + '.csv'),
            join(direktorij, 'protiprimeri_' + cas + '.csv'),
            join(direktorij, 'sklici_' + cas + '.csv')
          )

if __name__ == '__main__': main()
