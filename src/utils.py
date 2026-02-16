import networkx as nx
from collections import deque


def gpn(
    G: nx.Graph,
    count_trivial: bool = True
    ) -> int:
    """total number of shortest paths between all unordered pairs of nodes on a graph"""
    
    gpn = G.number_of_nodes() if count_trivial else 0
    nodes = list(G.nodes())

    # source to BFS
    for source_index, source_node in enumerate(nodes):

        dist = {source_node: 0}
        sigma = {source_node: 1} # number of shortest paths to each node
        queue = deque([source_node]) # bfs init

        # BFS traversal
        while queue:
            current_node = queue.popleft()

            for neighbor in G[current_node]:
                
                # if: no visit to neighbor
                if neighbor not in dist:
                    dist[neighbor] = dist[current_node] + 1
                    sigma[neighbor] = sigma[current_node]
                    queue.append(neighbor)

                # if: neighbor already discovered at shortest distance
                elif dist[neighbor] == dist[current_node] + 1:
                    sigma[neighbor] += sigma[current_node]

        # count number of shortest paht of source node
        for target_node in nodes[source_index + 1:]:
            gpn += sigma.get(target_node, 0)

    return gpn