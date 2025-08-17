


from os.path import join, isdir
from os import getcwd, makedirs
import time, sys
from src.shrani import shrani


def main():
    direktorij = join(getcwd(), sys.argv[1] if len(sys.argv) >= 2 else '.')
    makedirs(direktorij, exist_ok = True)
    cas = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
    shrani(
            join(direktorij, 'prostori_' + cas + '.csv'),
            join(direktorij, 'prostori-lastnosti_' + cas + '.csv'),
            join(direktorij, 'lastnosti_' + cas + '.csv'),
            join(direktorij, 'izreki_' + cas + '.json'),
            join(direktorij, 'protiprimeri_' + cas + '.csv'),
            join(direktorij, 'sklici_' + cas + '.csv')
          )

if __name__ == '__main__': main()
