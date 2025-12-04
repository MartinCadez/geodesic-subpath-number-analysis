import networkx as nx

def gpn(G: nx.Graph) -> int:
    n = G.number_of_nodes()
    total_paths = n 

    nodes = list(G.nodes())
    for i, u in enumerate(nodes):
        for v in nodes[i+1:]:
            total_paths += sum(1 for _ in nx.all_shortest_paths(G, source=u, target=v))

    return total_paths
