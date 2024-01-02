import pandas as pd
import networkx as nx
from networkx.classes.graph import Graph
from itertools import combinations
import numpy as np

def distance_index(index1: int, index2: int, df: pd.DataFrame) -> float:
    return ((df.loc[index1]['x']-df.loc[index2]['x'])**2+(df.loc[index1]['y']-df.loc[index2]['y'])**2+(df.loc[index1]['z']-df.loc[index2]['z'])**2)**0.5

def get_distance_threshold(atom1, atom2):
    atom_pairs = {
        ('H', 'H'): 0.7,
        ('C', 'C'): 1.65,
        ('O', 'O'): 1.4,
        ('N', 'N'): 1.45,
        ('C', 'H'): 1.14,
        ('C', 'O'): 1.5,
        ('H', 'O'): 1.019,
        ('C', 'N'): 1.51,
        ('H', 'N'): 1.15,
        ('O', 'S'): 1.75,
        ('C', 'Cl'): 1.80,
        ('C', 'F'): 1.45,
        ('C', 'S'): 1.85,
        ('N', 'S'): 1.85,
    }
    return atom_pairs.get(tuple(sorted([atom1, atom2])), 0)

def plot_G(coordinate_result: pd.DataFrame) -> Graph:
    size = len(coordinate_result.index)
    link = [[0] * size for _ in range(size)]

    for index_1 in coordinate_result.index:
        for index_2 in coordinate_result.index[index_1:]:
            atom_1 = coordinate_result.loc[index_1]['atom']
            atom_2 = coordinate_result.loc[index_2]['atom']
            threshold = get_distance_threshold(atom_1, atom_2)
            distance = distance_index(index_1, index_2, coordinate_result)
            if distance < threshold:
                link[index_1 - 1][index_2 - 1] = link[index_2 - 1][index_1 - 1] = 1

    G = nx.from_numpy_array(np.array(link))
    mapping = {i: i + 1 for i in range(len(link))}
    G = nx.relabel_nodes(G, mapping)
    for i in coordinate_result.index:
        G.nodes[i]["label"] = coordinate_result.loc[i]['atom']
    return G

def return_Enediyne(G: Graph) -> list:
    valid_subgraphs = []
    nodes_with_label_C = [node for node, attr in G.nodes(data=True) if attr.get('label') == 'C']
    for nodes in combinations(nodes_with_label_C, 6):
        if is_valid_subgraph(G, nodes):
            valid_subgraphs.append(nodes)
    if len(valid_subgraphs)==1:return valid_subgraphs
    else :return False
def is_valid_subgraph(G: Graph, nodes) -> bool:
    subgraph = G.subgraph(nodes)
    if not nx.is_tree(subgraph):
        return False
    degree_total=[]
    # Check if each node has label 'C'
    for node in nodes:
        degree_total.append(G.degree(node))
        if G.nodes[node].get('label') != 'C':
            return False
    degree_total.sort()
    if degree_total!=[2,2,2,2,3,3]:
        return  False
    return True