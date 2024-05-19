import json
import time
from collections import defaultdict

def weisfeiler_lehman_hash(graph, iterations=3):
    node_labels = {node: hash(str(data.get('label', ''))) for node, data in graph['nodes'].items()}
    
    for _ in range(iterations):
        new_labels = {}
        for node in graph['nodes']:
            neighbor_labels = sorted(node_labels[neighbor] for neighbor in graph['edges'][node])
            new_labels[node] = hash((node_labels[node], tuple(neighbor_labels)))
        node_labels = new_labels
    
    # Create a multiset label for the whole graph
    multiset_label = hash(tuple(sorted(node_labels.values())))
    return multiset_label

def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    G = {'nodes': {}, 'edges': defaultdict(list)}
    for node in data['nodes']:
        G['nodes'][node['id']] = {'label': node['label']}
    
    for edge in data['edges']:
        G['edges'][edge['source']].append(edge['target'])
        G['edges'][edge['target']].append(edge['source'])
    
    return G

def weisfeiler_lehman_isomorphism(G1, G2, iterations=3):
    G1_hash = weisfeiler_lehman_hash(G1, iterations)
    G2_hash = weisfeiler_lehman_hash(G2, iterations)
    return G1_hash == G2_hash

if __name__ == "__main__":
    G1 = load_graph_from_json('graph/rand_graph_100000.json')
    G2 = load_graph_from_json('graph/rand_graph_100000.json')
    
    start_time = time.time()
    isomorphic = weisfeiler_lehman_isomorphism(G1, G2)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    if isomorphic:
        print("The graphs are isomorphic.")
    else:
        print("The graphs are not isomorphic.")
    
    print(f"Time taken: {elapsed_time:.6f} seconds")