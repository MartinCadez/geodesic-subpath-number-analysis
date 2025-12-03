from sage.all import *
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
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

class CubicGraphs:
    NODE_COLOR = "#698ad1"

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.label = f"CubicGraphs({num_nodes})"
        self.graphs = self._build_graphs()
    
    def __repr__(self) -> str:
        return f"CubicGraphs(num_nodes={self.num_nodes}, num_graphs={len(self.graphs)})"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def _validate_args(num_nodes: int) -> None:
        if not isinstance(num_nodes, int):
            raise ValueError("num_nodes must be an integer.")
        if num_nodes < 4:
            raise ValueError("Cubic graph must have at least 4 nodes.")
        if num_nodes % 2 != 0:
            raise ValueError("Cubic (3-regular) graph must have an even number of nodes.")

    def _build_graphs(self):
        self._validate_args(self.num_nodes)
        
        nx_graphs = [graph.networkx_graph() for graph in graphs(self.num_nodes)
                     if graph.is_regular(3) and graph.is_connected()]

        if not nx_graphs:
            raise RuntimeError

        return nx_graphs

    @property
    def edges(self) -> list[list[tuple[int, int]]]:
        return [list(graph.edges()) for graph in self.graphs]

    @property
    def adj_matrices(self) -> list[np.ndarray]:
        return [nx.to_numpy_array(graph, nodelist=sorted(graph.nodes())) for graph in self.graphs]

    @property
    def incidence_matrices(self) -> list[np.ndarray]:
        return [nx.incidence_matrix(graph, oriented=False).toarray() for graph in self.graphs]

    def plot(self, index: int | None = None, filename: str | None = None) -> None:
        if index is not None:
            self._plot_single(self.graphs[index], index, filename)
        else:
            for i, graph in enumerate(self.graphs):
                self._plot_single(graph, i)

    def _plot_single(self, graph: nx.Graph, index: int, filename: str | None = None):
        plt.figure(figsize=(10, 8))
        pos = nx.circular_layout(graph)
        
        nx.draw_networkx(
            graph,
            pos=pos,
            labels={n: f"$v_{{{n+1}}}$" for n in graph.nodes()},
            node_color=self.NODE_COLOR,
            edgecolors="#292a40",
            linewidths=2,
            node_size=3000,
            width=2,
            font_color="white",
            font_size=30
        )
        plt.axis("off")
        plt.title(f"{self.label} - Graph {index+1}")
        if filename:
            plt.savefig(filename, bbox_inches="tight", facecolor="white")
            plt.close()
        else:
            plt.show()


if __name__ == "__main__":
    # G = BipartiteGraph(num_u=3, num_v=2, num_edges=4)
    # print(G)
    # print(G.u_nodes)
    # print(G.v_nodes)
    # print(G.edges)
    # print(G.degree_sequence)
    # print(G.adj_matrix)
    # print(G.incidence_matrix)
    # G.plot()

    cg6 = CubicGraphs(4)
    print("Number of graphs:", len(cg6.graphs))
    cg6.plot(index=0, filename="test.png")
    cg6.plot(index=1, filename="test1.png")

