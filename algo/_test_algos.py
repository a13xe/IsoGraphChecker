import json
import networkx as nx
from timeit import default_timer as timer
from networkx.algorithms import isomorphism
from color_refinement import color_refinement_isomorphism
from weisfeiler_lehman import weisfeiler_lehman_isomorphism

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
    # RANDOM
    graph1 = 'graph/rand_graph_100000.json'
    graph2 = 'graph/rand_graph_100000.json'
    # INV
    graph1 = 'graph/el_graph_inv.json'
    graph2 = 'graph/graph_inv.json'
    # AND
    graph1 = 'graph/el_graph_and.json'
    graph2 = 'graph/graph_and.json'
    # SCHEME
    graph1 = 'graph/el_graph.json'
    graph2 = 'graph/graph.json'
    
    G1 = load_graph_from_json(graph1)
    G2 = load_graph_from_json(graph2)
    
    print("----------------------------------------------------------------")
    print("Running VF2 algo...")
    start_time = timer()
    isomorphic = isomorphism.GraphMatcher(G1, G2)
    end_time = timer()
    elapsed_time = end_time - start_time
    if isomorphic:
        print("The graphs ARE isomorphic.")
    else:
        print("The graphs ARE NOT isomorphic.")
    print(f"Time taken: {elapsed_time:.9f} seconds\n")
    
    print("----------------------------------------------------------------")
    print("Running color refinement algo...")
    start_time = timer()
    isomorphic = color_refinement_isomorphism(G1, G2)
    end_time = timer()
    elapsed_time = end_time - start_time
    if isomorphic:
        print("The graphs ARE isomorphic.")
    else:
        print("The graphs ARE NOT isomorphic.")
    print(f"Time taken: {elapsed_time:.9f} seconds\n")
    
    print("----------------------------------------------------------------")
    print("Running Weisfeiler Lehman algo...")
    start_time = timer()
    isomorphic = weisfeiler_lehman_isomorphism(G1, G2)
    end_time = timer()
    elapsed_time = end_time - start_time
    if isomorphic:
        print("The graphs ARE isomorphic.")
    else:
        print("The graphs ARE NOT isomorphic.")
    print(f"Time taken: {elapsed_time:.9f} seconds\n")