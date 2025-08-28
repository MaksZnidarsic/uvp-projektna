


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

Seveda pa, če lahko podatke ekstrapolirajo oni, jih lahko tudi mi. To naredimo, saj se nikomur ne da čakati, da bi se naložili sami. Program za to uporabi zelo preprost algoritem. Ta gre takole. Program prej pridobljene izreke najprej preuredi v za branje prijaznejšo obliko. Vsak izrek v podatkovni bazi je oblike
```math
\bigwedge_i P_i \implies Q,
```
kjer so $`P_i`$-ji in $`Q`$ neke lastnosti. Sedaj se pri izbranem prostoru sprehodi čez vse izreke ter iz $`P_i`$-jev izpelje $`Q`$, kadar je to mogoče. Poleg tega mora preveriti še kontrapozicijo vsakega izreka, saj bi nam drugače ogromno lastnosti izviselo. Torej, če ve, da $`\neg Q`$, in ne pozna le nekega $`P_j`$-ja izmed $`P_i`$-jev, lahko iz $`\bigwedge_{i \neq j} P_i`$ izpelje $`\neg P_j`$. Ko s pomočjo izreka pridobi neko dodatno lastnost, ga program označi za uporabljenega. Program se tako ciklično sprehaja skozi še ne uporabljene izreke, dokler se število lastnosti za tisti prostor veča, nakar postopek zaključi ter se premakne na naslednji prostor.

Program pa še vseeno ne more izpeljati vseh lastnosti. Tistih nekaj, kar jih ostane, preprosto označi z 'ne vem' (v kodi označeno s Pythonovo vrednostjo `None`). Mislili bi si, da je to problem, ampak, če jih mi nismo sposobni izpeljati, jih tudi oni niso, kar se pokaže tudi na spletni strani.

Ko program enkrat zbere vse podatke, jih shrani v podano direktorijo. Analiza podatkov je bila narejena z uporabo Jupyter Notebooka in se nahaja v zgoraj omenjeni datoteki.
