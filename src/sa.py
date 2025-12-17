import random
import logging
import networkx as nx
from simanneal import Annealer
from utils import gpn

logging.basicConfig(level=logging.INFO)


class GPNOptimizer(Annealer):

    def __init__(self, initial_graph: nx.Graph):
        if not nx.is_bipartite(initial_graph):
            raise ValueError("Initial graph must be bipartite")
        if not nx.is_connected(initial_graph):
            raise ValueError("Initial graph must be connected")

        self.u_set, self.v_set = nx.bipartite.sets(initial_graph)
        super().__init__(initial_graph)

    def energy(self) -> float:
        return -gpn(self.state)

    def move(self):
        G = self.state
        u_set, v_set = self.u_set, self.v_set

        max_attempts = 50
        for _ in range(max_attempts):
            new_G = G.copy()
            move_type = random.choice(["add", "remove", "swap"])

            if move_type == "add":
                u = random.choice(tuple(u_set))
                v = random.choice(tuple(v_set))
                if not new_G.has_edge(u, v):
                    new_G.add_edge(u, v)

            elif move_type == "remove":
                if new_G.number_of_edges() > new_G.number_of_nodes() - 1:
                    u, v = random.choice(list(new_G.edges()))
                    new_G.remove_edge(u, v)

            elif move_type == "swap":
                existing = list(new_G.edges())
                missing = [
                    (u, v) for u in u_set for v in v_set
                    if not new_G.has_edge(u, v)
                ]
                if existing and missing:
                    u1, v1 = random.choice(existing)
                    u2, v2 = random.choice(missing)
                    new_G.remove_edge(u1, v1)
                    new_G.add_edge(u2, v2)

            if nx.is_bipartite(new_G) and nx.is_connected(new_G):
                self.state = new_G
                return

        return