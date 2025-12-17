from simanneal import Annealer
from utils import gpn
import logging
import random
import networkx as nx

logging.basicConfig(level=logging.INFO)

class GPNOptimizer(Annealer):
    def __init__(
            self,
            state,
            initial_partition
        ):
        self.partition_A, self.partition_B = initial_partition
        super().__init__(state)
    
    def energy(self, graph):
        return -gpn(graph)

    def move(
            current_graph: nx.Graph,
            max_attempts=100
        ):
        if not nx.is_bipartite(current_graph):
            logging.error("input graph is not bipartite.")
            return current_graph.copy()
        
        u_set, v_set = nx.bipartite.sets(current_graph)
        
        if not u_set or not v_set:
            logging.error("bipartite graph has no valid partition, returning the original graph.")
            return current_graph.copy()
        
        attempt = 0
        while attempt < max_attempts:
            attempt += 1
            move_type = random.choice(['add_edge', 'remove_edge', 'swap_edge'])
            
            new_graph = current_graph.copy()
            changed = False
            
            if move_type == 'add_edge':
                u = random.choice(list(u_set))
                v = random.choice(list(v_set))
                if not new_graph.has_edge(u, v):
                    new_graph.add_edge(u, v)
                    changed = True
                    
            elif move_type == 'remove_edge':
                edges = list(new_graph.edges())
                if edges:
                    u, v = random.choice(edges)
                    new_graph.remove_edge(u, v)
                    changed = True
            
            elif move_type == 'swap_edge':
                cross_edges = [(u, v) for u in u_set for v in v_set if new_graph.has_edge(u, v)]
                possible_new = [(u, v) for u in u_set for v in v_set if not new_graph.has_edge(u, v)]
                
                if cross_edges and possible_new:
                    rem_u, rem_v = random.choice(cross_edges)
                    add_u, add_v = random.choice(possible_new)
                    new_graph.remove_edge(rem_u, rem_v)
                    new_graph.add_edge(add_u, add_v)
                    changed = True
            
            elif changed and nx.is_connected(new_graph) and nx.is_bipartite(new_graph):
        return new_graph
