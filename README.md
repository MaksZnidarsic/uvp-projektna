


# Analiza in vizualizacija [$`\pi`$-base](topology.pi-base.org)a

Program pobere podatke iz spletne strani [$`\pi`$-base](topology.pi-base.org) ter jih vizualizira. Analiza se nahaja v direktoriji `analiza`.


## Uporaba

Preden program prvič zaženemo, naložimo potrebne knjižnice (`pip install -r requirements.txt`). Podatke shranimo z ukazom
```
$ python main.py shrani <pot-prostori> <pot-protiprimeri>
```
Namesto dveh poti lahko podamo tudi samo pot do direktorije, v katero naj program shrani datoteke. V primeru, da poti ne podamo, program datoteke shrani v `cwd`. Podatke nato vizualiziramo z ukazom
```
$ python main.py narisi <podatki-prostori> <podatki-protiprimeri> <direktorija-slik>
```
kjer `<podatki-prostori>` in `<podatki-protiprimeri>` predstavljata poti do prej shranjenih datotek. V primeru, da `<direktorija-slik>` ni podana, jih program shrani v `cwd`.

Ukaza delujeta pod predpostavko, da podane direktorije oz. datoteke obstajajo in sledijo zgoraj opisanemu formatu.


## Kako

Program naprej presene in uredi podatke o [izrekih](topology.pi-base.org/theorems). Za podatke o prostorih in lastnostih lahko 'poscrapa' stran enega izmed prostorov, saj so imena vseh zapisana v JSONu, ki se nahaja vsaki izmed njih. Sedaj, ko je dobil imena vseh prostorov in lastnosti, se program sprehodi po straneh prostorov ter za vsakega posebej zbere vse njegove lastnosti.

Tukaj naletimo na težavo, saj ima izvorna koda, ki nam jo poda knjižnica `requests`, le nekaj izmed lastnosti danega prostora, preostale pa so kasneje dodane z uporabo javascripta. Lastnosti, ki jih ne moremo direktno prebrati, program zato ekstrapolira s pomočjo prej dobljenih izrekov (to je tudi razlog, da najprej poišče izreke). Algoritem za ekstrapolacijo je zelo preprost. Ker so vsi izreki oblike
```math
\bigwedge_i P_i \implies Q,
```
kjer so $`P_i`$ in $`Q`$ neke lastnosti, lahko, če velja $`P_i`$ $`\forall i`$, preprosto izpeljemo $`Q`$. Poleg tega pa moramo preveriti tudi kontrapozicijo, saj drugače ne bomo dobili vseh lastnosti podanih v podatkovni bazi. Torej če velja $`\neg Q`$ in izmed vseh $`P_i`$ ne poznamo samo nekega $`P_j`$, potem iz $`\neg P_i`$ $`\forall i \neq j`$ lahko izpeljemo $`\neg P_j`$.

Ko enkrat ima vse podatke, program ugotovi, kateri prostori so protiprimeri za obrate katerih izrekov ter jih shrani v podani datoteki.

Vizualizacija je zelo standardna.
