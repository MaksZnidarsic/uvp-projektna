


import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


DPI = 500

def velikostLastnost(lastnost, df):
    return 2 * len([ 1 for x in df[lastnost][1:] if x != x ]) / (df.shape[0] - 2)

def velikostProstor(prostor, df):
    indeks = list(df['prostor']).index(prostor)
    return 5 * len([ 1 for x in df[2:] if df[x][indeks] != df[x][indeks] ]) / (df.shape[1] - 2)

def narisiProstore(pot_podatki, slika_pot):
    df = pd.read_csv(pot_podatki)
    fig, ax = plt.subplots()
    G = nx.Graph()
    prostori = df['prostor']
    robovi = []
    for x in df[2:]: robovi += [ ( x, prostori[y] ) for y in range(1, len(prostori)) if df[x][y] ]
    G.add_edges_from(robovi)
    pos = nx.fruchterman_reingold_layout(G)
    barva = [ '#faa442' if x in df else '#516db6' for x in G ]
    velikosti = [ velikostLastnost(x, df) if x in df else velikostProstor(x, df) for x in G ]
    nx.draw_networkx_edges(G, pos, edge_color = 'white', width = 0.01)
    nx.draw_networkx_nodes(G, pos, node_size = velikosti, linewidths = 0, node_color = barva)
    ax.set_facecolor('#000919')
    plt.savefig(slika_pot, dpi = DPI, bbox_inches = 'tight', pad_inches = 0)

def velikostProtiprimer(protiprimer, df):
    return 3 * len([ 1 for x in df[protiprimer][1:] if x != x ]) / (df.shape[0] - 1)

def velikostIzrek(izrek, df):
    indeks = list(df['izrek']).index(izrek)
    return 3 * len([ 1 for x in df[1:] if df[x][indeks] == 1]) / (df.shape[1] - 1)

def narisiProtiprimere(pot_podatki, slika_pot):
    df = pd.read_csv(pot_podatki)
    fig, ax = plt.subplots()
    G = nx.Graph()
    izreki = df['izrek']
    robovi = []
    for x in df[1:]: robovi += [ ( x, izreki[y] ) for y in range(1, len(izreki)) if df[x][y] ]
    G.add_edges_from(robovi)
    pos = nx.spring_layout(G)
    barva = [ '#faa442' if x in df else '#517db6' for x in G ]
    velikost = [ velikostProtiprimer(x, df) if x in df else velikostIzrek(x, df) for x in G ]
    nx.draw_networkx_edges(G, pos, edge_color = 'white', width = 0.01)
    nx.draw_networkx_nodes(G, pos, node_size = velikost, linewidths = 0, node_color = barva)
    ax.set_facecolor('#000919')
    plt.savefig(slika_pot, dpi = DPI, bbox_inches = 'tight', pad_inches = 0)
