import numpy as np
import networkx as nx
from networkx.algorithms import bipartite

import networkx as nx
import matplotlib.pyplot as plt


class BipartiteGraph:
    U_NODE_COLOR = "#698ad1"
    V_NODE_COLOR = "#b5dcff"

    def __init__(
        self,
        num_u: int,
        num_v: int,
        num_edges: int,
    ):
        self.num_u = num_u
        self.num_v = num_v
        self.num_edges = num_edges
        self.label = f"G({num_u}, {num_v}, {num_edges})"
        self.graph = self._build_graph()
    
    def __repr__(self) -> str:
        return f"BipartiteGraph(num_u={self.num_u}, num_v={self.num_v}, num_edges={self.num_edges})"

    def __str__(self) -> str:
        return f"{self.__repr__()}"

    @staticmethod
    def _validate_args(num_u: int, num_v: int, num_edges: int) -> None:
        if not all(isinstance(x, int) for x in [num_u, num_v, num_edges]):
            raise ValueError("all parameters must be integers.")

        if not all(x > 0 for x in [num_u, num_v, num_edges]):
            raise ValueError("all parameters must be positive integers.")

        if not (num_u + num_v - 1 <= num_edges <= num_u * num_v):
            raise ValueError(
                f"Invalid number of edges; for given parameters: "
                f"num_u={num_u}, num_v={num_v} (cardinality of each disjoint set) "
                f"For given number of vertecies, number of edges"
                f"must be between {num_u + num_v - 1} "
                f"(minimal connected tree) and {num_u * num_v} "
                f"(complete bipartite graph)."
            )

    def _build_graph(self) -> nx.Graph:
        self._validate_args(self.num_u, self.num_v, self.num_edges)

        U = [f"u{i + 1}" for i in range(self.num_u)]
        V = [f"v{i + 1}" for i in range(self.num_v)]

        G = nx.Graph()
        G.add_nodes_from(U, bipartite=0)
        G.add_nodes_from(V, bipartite=1)

        edges = []
        for i, u_node in enumerate(U):
            v_node = V[i % len(V)]
            edges.append((u_node, v_node))

        for i, v_node in enumerate(V):
            u_node = U[i % len(U)]
            if (u_node, v_node) not in edges:
                edges.append((u_node, v_node))

        possible_edges = [(u, v) for u in U for v in V if (u, v) not in edges]
        possible_edges.sort()
        edges += possible_edges[: self.num_edges - len(edges)]

        G.add_edges_from(edges)

        if not nx.is_bipartite(G):
            raise RuntimeError("Error: graph is not bipartite")
        if not nx.is_connected(G):
            raise RuntimeError("Generated graph is not connected.")

        return G
    
    @property
    def u_nodes(self) -> list[str]:
        return [n for n, d in self.graph.nodes(data=True) if d["bipartite"] == 0]

    @property
    def v_nodes(self) -> list[str]:
        return [n for n, d in self.graph.nodes(data=True) if d["bipartite"] == 1]

    @property
    def degree_sequence(self) -> dict[str, tuple[int, ...]]:
        U_degrees = tuple(dict(self.graph.degree(self.u_nodes)).values())
        V_degrees = tuple(dict(self.graph.degree(self.v_nodes)).values())
        return {"U": U_degrees, "V": V_degrees}

    @property
    def edges(self):
        return list(self.graph.edges())
    
    @property
    def adj_matrix(self) -> np.ndarray:
        return nx.to_numpy_array(self.graph, nodelist=list(self.graph.nodes()))
    
    @property
    def incidence_matrix(self) -> np.ndarray:
        return nx.incidence_matrix(self.graph, oriented=False).toarray()

    def plot(self, filename: str | None = None) -> None:
        plt.figure(figsize=(12, 8))

        nx.draw_networkx(
            self.graph,
            pos=nx.bipartite_layout(
                self.graph,
                [n for n, d in self.graph.nodes(data=True) if d["bipartite"] == 0],
            ),
            labels = {
                n: f"$u_{{{n[1:]}}}$" if n.startswith("u") else f"$v_{{{n[1:]}}}$"
                for n in self.graph.nodes()
            },
            node_color=[
                self.U_NODE_COLOR if d["bipartite"] == 0 else self.V_NODE_COLOR
                for _, d in self.graph.nodes(data=True)
            ],
            edgecolors="#292a40",
            linewidths=2,
            node_size=4000,
            width=2,
            font_color="white",
            font_size=30
        )

        plt.axis("off")
        plt.title(self.label)

        if filename:
            plt.savefig(filename, bbox_inches="tight", facecolor="white")
            plt.close()
        else:
            plt.show()

if __name__ == "__main__":
    G = BipartiteGraph(num_u=3, num_v=2, num_edges=4)
    print(G)
    print(G.u_nodes)
    print(G.v_nodes)
    print(G.edges)
    print(G.degree_sequence)
    print(G.adj_matrix)
    print(G.incidence_matrix)
    G.plot()
