


# Analiza podatkovne baze [$`\pi`$-base](https://topology.pi-base.org)

Program pobere podatke iz spletne strani [$`\pi`$-base](https://topology.pi-base.org) ter jih shrani. Analiza podatkov se nahaja v direktoriji [`analiza`](analiza).


## Uporaba

Repozitorij [klonirano](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) ter se [prestavimo](https://man.cx/cd) v pravkar ustvarjeno direktorijo, kjer ustvarimo [pythonovo virtualno okolje](https://docs.python.org/3/library/venv.html) ter ga aktiviramo. Preden program prvič uporabimo, [naložimo](https://pip.pypa.io/en/stable/user_guide/) potrebne knjižnice, ki se nahajajo v datoteki [`requirements.txt`](requirements.txt).
Program zaženemo s klicem
```
python main.py <pot>
```
kjer `<pot>` predstavlja pot do direktorije, v katero želimo shraniti podatke. V primeru, da poti ne podamo, program vse datoteke shrani v `cwd`. Če direktorija ne obstaja, jo ustvari.

Analiza podatkov se nahaja v direktoriji [`analiza`](analiza). V primeru, da Jupyter Notebooka ne bi znali uporabljati, se navodila nahajajo v [dokumentaciji](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html).


## Kako

Po podrobnem pregledu [$`\pi`$-base](https://topology.pi-base.org)a ugotovimo, da se v vsaki datoteki na spletni strani nahaja celotna podatkovna baza zapakirana v nekem nizu globoku v kodi, kjer je podana v formatu JSON. Program to s pridom izkoristi in celotno bazo podatkov pobere z enim samim klicem knjižnice `requests`, ki ga opravi na naključno izbrani strani v [$`\pi`$-base](https://topology.pi-base.org)u. (Kot lahko vidimo v starejših verzijah napisanih pred odkritjem tega dejstva, je moral program včasih obiskati stran vsakega izmed prostorov, da bi iz nje pridobil vse lastnosti le-tega. To je bilo seveda zelo zamudno.)

Tukaj pa se program ne ustavi, saj še ni ugotovil, katere lastnosti veljajo za kateri prostor. Primarno lahko v podatkovni bazi za dani prostor izvemo le peščico ročno pregledanih lastnosti, ki zanj veljajo, ostale pa podatkovna baza dopolni s pomočjo v njen shranjenih izrekov. Ker uporabljamo le knjižnico `requests`, teh dodatnih lastnosti ne dobimo, saj so v HTML dodane šele naknadno s pomočjo JavaScripta.

Seveda pa, če lahko podatke ekstrapolirajo oni, jih lahko tudi mi. To naredimo, saj se nikomur ne da čakati, da bi se naložili sami. Program za to uporabi zelo preprost algoritem. Ta gre takole. Program najprej vse prej pridobljene izreke preuredi v za branje prijaznejšo obliko, nato pa pri vsakem prostoru ponovi naslednje. Ciklično se sprehaja skozi vse izreke, kjer iz vsakega izpelje tiste lastnosti, ki se jih da. Ker so vsi izreki oblike $`\bigwedge P_i \implies Q`$, kjer so $`P_i`$-ji in $`Q`$ vrednosti nekih lastnosti, program najprej preveri, če velja $`P_i`$ $`\forall i`$, od koder lahko očitno izpelje $`Q`$. Poleg tega pa mora preveriti še kontrapozicijo izreka, saj bi nam drugače ogromno lastnosti izviselo. Vemo, da velja
```math
\left( \bigwedge P_i \implies Q \right) \iff \left( \neg Q \implies \bigvee \neg P_i \right).
```
Torej, če $`\neg Q`$ in ne pozna le nekega $`P_j`$-ja izmed $`P_i`$-jev, lahko iz $`P_i`$ $`\forall i \neq j`$ izpelje $`\neg P_j`$. Program ta proces ponavlja, dokler se število poznanih lastnosti prostora veča in mu ostajajo še ne uporabljeni izreki, nato pa se premakne na naslednji prostor.

Program pa še vseeno ne more izpeljati vseh lastnosti danega prostora, zato tistih nekaj, kar jih ostane, preprosto označi z 'ne vem' (v kodi označeno s Pythonovo vrednostjo `None`). Mislili bi si, da bi to lahko bil problem, ampak, če jih mi nismo sposobni izpeljati, jih tudi oni niso, kar se pokaže tudi na spletni strani.

Ko program enkrat zbere vse podatke, jih v zanje izbranem formatu (tj. JSON ali CSV) shrani v podano direktorijo. Vse datoteke so shranjene v formatu
```
<ime-podatkov>_<leto>-<mesec>-<dan>-<ura>-<minuta>.<format>
```
kjer uporabimo datum in čas shranjevanja. Analiza podatkov je bila narejena z uporabo Jupyter Notebooka in se nahaja v zgoraj omenjeni datoteki.
