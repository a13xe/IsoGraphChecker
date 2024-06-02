import networkx as nx

def color_refinement_isomorphism(graph1, graph2):
    def color_refine(graph):
        color_map = {node: 1 for node in graph.nodes()}
        stable = False

        while not stable:
            stable = True
            new_color_map = {}
            for node in graph.nodes():
                neighbors_colors = sorted([color_map[neighbor] for neighbor in graph.neighbors(node)])
                new_color_map[node] = (color_map[node], tuple(neighbors_colors))

            color_count = {}
            for node, color in new_color_map.items():
                if color not in color_count:
                    color_count[color] = len(color_count) + 1
                new_color_map[node] = color_count[color]

            if color_map != new_color_map:
                stable = False
                color_map = new_color_map

        return sorted(color_map.values())

    return color_refine(graph1) == color_refine(graph2)