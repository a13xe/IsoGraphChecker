import json
import time
from collections import defaultdict, deque

class Graph:
    def __init__(self):
        self.adj = defaultdict(set)
        self.nodes = set()

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, source, target):
        self.adj[source].add(target)
        self.adj[target].add(source)

def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    G = Graph()
    for node in data['nodes']:
        G.add_node(node['id'])
    
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'])
    
    return G

class VF2:
    def __init__(self, G1, G2):
        self.G1 = G1
        self.G2 = G2
        self.mapping = {}
        self.inverse_mapping = {}
        self.core_1 = {}
        self.core_2 = {}
        self.in_1 = defaultdict(int)
        self.in_2 = defaultdict(int)
        self.out_1 = defaultdict(int)
        self.out_2 = defaultdict(int)

    def is_isomorphic(self):
        if len(self.G1.nodes) != len(self.G2.nodes) or len(self.G1.adj) != len(self.G2.adj):
            return False
        return self.match()

    def match(self):
        if len(self.mapping) == len(self.G1.nodes):
            return True

        candidate_pairs = self.candidate_pairs()
        for n, m in candidate_pairs:
            if self.is_feasible(n, m):
                self.add_pair(n, m)
                if self.match():
                    return True
                self.remove_pair(n, m)

        return False

    def candidate_pairs(self):
        if not self.mapping:
            return [(n, m) for n in self.G1.nodes for m in self.G2.nodes]

        pairs = []
        for n in self.G1.nodes:
            if n in self.mapping:
                continue
            for m in self.G2.nodes:
                if m in self.inverse_mapping:
                    continue
                pairs.append((n, m))

        return pairs

    def is_feasible(self, n, m):
        return (self.in_1[n] == self.in_2[m] and 
                self.out_1[n] == self.out_2[m] and 
                len(self.G1.adj[n]) == len(self.G2.adj[m]))

    def add_pair(self, n, m):
        self.mapping[n] = m
        self.inverse_mapping[m] = n
        self.core_1[n] = m
        self.core_2[m] = n

        for neighbor in self.G1.adj[n]:
            self.in_1[neighbor] += 1
            self.out_1[neighbor] -= 1

        for neighbor in self.G2.adj[m]:
            self.in_2[neighbor] += 1
            self.out_2[neighbor] -= 1

    def remove_pair(self, n, m):
        del self.mapping[n]
        del self.inverse_mapping[m]
        del self.core_1[n]
        del self.core_2[m]

        for neighbor in self.G1.adj[n]:
            self.in_1[neighbor] -= 1
            self.out_1[neighbor] += 1

        for neighbor in self.G2.adj[m]:
            self.in_2[neighbor] -= 1
            self.out_2[neighbor] += 1

if __name__ == "__main__":
    G1 = load_graph_from_json('graph/rand_graph_100000.json')
    G2 = load_graph_from_json('graph/rand_graph_100000.json')
    
    vf2 = VF2(G1, G2)
    
    start_time = time.time()
    isomorphic = vf2.is_isomorphic()
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    if isomorphic:
        print("The graphs are isomorphic.")
    else:
        print("The graphs are not isomorphic.")
    
    print(f"Time taken: {elapsed_time:.6f} seconds")
