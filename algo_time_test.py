import json
import networkx as nx

from timeit import default_timer as timer
from networkx.algorithms import isomorphism

# Local imports
from algos.vf2 import vf2_isomorphism
from algos.bliss import bliss_isomorphism
from algos.color_refinement import color_refinement_isomorphism
from algos.weisfeiler_lehman import weisfeiler_lehman_isomorphism
from algos.laszlo_babai_simplified import laszlo_babai_simplified_isomorphism


def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'], label=node['label'])
    
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'])
    return G


def run_algorithm(name, algorithm_function, G1, G2):
    print("----------------------------------------------------------------")
    print(f"Running {name}...")
    start_time = timer()
    isomorphic = algorithm_function(G1, G2)
    end_time = timer()
    elapsed_time = end_time - start_time
    if isomorphic:
        print("The graphs ARE isomorphic.")
    else:
        print("The graphs ARE NOT isomorphic.")
    print(f"Time taken: {elapsed_time:.9f} seconds\n")


def run_algorithm_n_times(name, algorithm_function, G1, G2):
    n = 100
    print("----------------------------------------------------------------")
    print(f"Running {name}...")
    times = []
    for _ in range(n):
        start_time = timer()
        isomorphic = algorithm_function(G1, G2)
        end_time = timer()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
    average_time = sum(times) / len(times)
    if isomorphic:
        print("The graphs ARE isomorphic.")
    else:
        print("The graphs ARE NOT isomorphic.")
    print(f"Avg time taken over {n} runs: {average_time:.9f} seconds\n")


if __name__ == "__main__":
    graph1 = 'graphs/el_graph.json'
    graph2 = 'graphs/graph.json'
    
    G1 = load_graph_from_json(graph1)
    G2 = load_graph_from_json(graph2)
    
    run_algorithm_n_times("VF2 algo", vf2_isomorphism, G1, G2)
    run_algorithm_n_times("Bliss algo", bliss_isomorphism, G1, G2)
    run_algorithm_n_times("Color Refinement algo", color_refinement_isomorphism, G1, G2)
    run_algorithm_n_times("Weisfeiler Lehman algo", weisfeiler_lehman_isomorphism, G1, G2)
    run_algorithm_n_times("Laszlo Babai Simplified algo", laszlo_babai_simplified_isomorphism, G1, G2)