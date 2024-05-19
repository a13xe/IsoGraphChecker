import networkx as nx
from networkx.algorithms import isomorphism
import json
import time

def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'], label=node['label'])
    
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'])
    
    return G

if __name__ == "__main__":
    G1 = load_graph_from_json('graph/rand_graph_100000.json')
    G2 = load_graph_from_json('graph/rand_graph_100000.json')
    
    start_time = time.time()
    isomorphic = isomorphism.GraphMatcher(G1, G2)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    if isomorphic:
        print("The graphs are isomorphic.")
    else:
        print("The graphs are not isomorphic.")
    
    print(f"Time taken: {elapsed_time:.6f} seconds")
