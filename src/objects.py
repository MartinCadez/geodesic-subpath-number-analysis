from sage.all import *
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt


class BipartiteGraphs:
    U_NODE_COLOR = "#698ad1"
    V_NODE_COLOR = "#b5dcff"

    def __init__(
        self,
        num_nodes: int
    ):
        self.num_nodes = num_nodes
        self.graphs = self._build_graphs()
    
    def __repr__(self) -> str:
        return f"BipartiteGraphs(num_nodes={self.num_nodes}, num_graphs={len(self.graphs)})"

    def __str__(self) -> str:
        return f"{self.__repr__()}"

    @staticmethod
    def _validate_args(num_nodes: int) -> None:
        if not isinstance(num_nodes, int):
            raise ValueError("num_nodes must be an integer.")
        if num_nodes < 1:
            raise ValueError("BipartiteGraph graph must have at least 1 node.")

    def _build_graphs(self):
        self._validate_args(self.num_nodes)

        nx_graphs = [g.networkx_graph() for g in graphs.nauty_geng(f"{self.num_nodes} -b -c")]

        if not nx_graphs:
            raise RuntimeError(f"No bipartite graphs generated for n={self.num_nodes}")

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


    @property
    def nodes(self) -> list[dict[str, list[str]]]:
        node_sets = []
        for graph in self.graphs:
            u_set, v_set = nx.bipartite.sets(graph)
            graph_dict = {
                "U": sorted(list(u_set)),
                "V": sorted(list(v_set))
            }
            node_sets.append(graph_dict)
    
        return node_sets


    @property
    def degree_sequences(self) -> list[dict[str, tuple[int, ...]]]:
        return [
            {
                "U": tuple(dict(graph.degree(u_set)).values()),
                "V": tuple(dict(graph.degree(v_set)).values())
            }
            for graph in self.graphs
            for u_set, v_set in [nx.bipartite.sets(graph)]
        ]

    def plot(self, index: int | None = None, filename: str | None = None) -> None:
        if index is not None:
            self._plot_single(self.graphs[index], index, filename)
        else:
            for i, graph in enumerate(self.graphs):
                self._plot_single(graph, i)


    def _plot_single(self, graph: nx.Graph, index: int, filename: str | None = None):
        plt.figure(figsize=(12, 8))
        
        u_set, v_set = nx.bipartite.sets(graph)
        
        labels = {}
        for i, node in enumerate(sorted(u_set)):
            labels[node] = f"$u_{{{i}}}$"
        for i, node in enumerate(sorted(v_set)):
            labels[node] = f"$v_{{{i}}}$"
        
        nx.draw_networkx(
            graph,
            pos=nx.bipartite_layout(graph, u_set),
            labels=labels,
            node_color = "#698ad1",
            edgecolors="#292a40",
            linewidths=2,
            node_size=4000,
            width=2,
            font_color="white",
            font_size=30
        )

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

        nx_graphs = [g.networkx_graph() for g in graphs.nauty_geng(f"{self.num_nodes} -d3 -D3 -c")]

        # nx_graphs = [graph.networkx_graph() for graph in graphs(self.num_nodes)
        #              if graph.is_regular(3) and graph.is_connected()]

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


class TriangleFreeGraphs:
    NODE_COLOR = "#f08c4f"

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.label = f"TriangleFreeGraphs({num_nodes})"
        self.graphs = self._build_graphs()
    
    def __repr__(self) -> str:
        return f"TriangleFreeGraphs(num_nodes={self.num_nodes}, num_graphs={len(self.graphs)})"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def _validate_args(num_nodes: int) -> None:
        if not isinstance(num_nodes, int):
            raise ValueError("num_nodes must be an integer.")
        if num_nodes < 1:
            raise ValueError("Triangle-free graph must have at least 1 node.")

    def _build_graphs(self):
        self._validate_args(self.num_nodes)

        nx_graphs = [g.networkx_graph() for g in graphs.nauty_geng(f"{self.num_nodes} -t -c")]

        if not nx_graphs:
            raise RuntimeError(f"No triangle-free graphs generated for n={self.num_nodes}")

        return nx_graphs

    @property
    def degree_sequences(self) -> list[tuple[int, ...]]:
        sequences = []
        for graph in self.graphs:
            deg_seq = tuple(d for n, d in sorted(graph.degree(), key=lambda x: x[0]))
            sequences.append(deg_seq)
        return sequences


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


# class LineGraph:
#     NODE_COLOR = "#e08e45"

#     def __init__(
#             self,
#             num_nodes: int
#     ):
#         self.num_nodes = num_nodes
#         self.label = f"L({self.num_nodes})"
#         self.graph = self._build_graphs()

#     def __repr__(self) -> str:
#         return f"LineGraph(num_nodes={self.graph.number_of_nodes()}, num_edges={self.graph.number_of_edges()})"

#     @staticmethod
#     def _validate_args(num_nodes: int) -> None:
#         if not isinstance(num_nodes, int):
#             raise ValueError("num_nodes must be an integer.")
#         if num_nodes < 1:
#             raise ValueError("Line graph must have at least 1 node.")

#     def _build_graphs(self):
#         self._validate_args(self.num_nodes)
#         G = nx.Graph()
#         G.add_edges_from((i, i + 1) for i in range(self.num_nodes - 1))
#         return G

#     @property
#     def nodes(self) -> list[str]:
#         return list(self.graph.nodes())

#     @property
#     def edges(self) -> list[tuple[str, str]]:
#         return list(self.graph.edges())

#     @property
#     def degree_sequence(self) -> tuple[int, ...]:
#         return tuple(dict(self.graph.degree()).values())

#     @property
#     def adj_matrix(self) -> np.ndarray:
#         return nx.to_numpy_array(self.graph, nodelist=list(self.graph.nodes()))

#     @property
#     def incidence_matrix(self) -> np.ndarray:
#         return nx.incidence_matrix(self.graph, oriented=False).toarray()

#     def plot(self, filename: str | None = None) -> None:
#         plt.figure(figsize=(8, 2))  # horizontal layout

#         nx.draw_networkx(
#             self.graph,
#             pos={i: (i, 0) for i in self.graph.nodes()},
#             labels={n: f"$v_{n}$" for n in self.graph.nodes()},
#             node_color=self.NODE_COLOR,
#             edgecolors="#292a40",
#             linewidths=2,
#             node_size=1000,
#             width=2,
#             font_color="white",
#             font_size=16
#         )

#         plt.axis("off")
#         plt.title(self.label)

#         if filename:
#             plt.savefig(filename, bbox_inches="tight", facecolor="white")
#             plt.close()
#         else:
#             plt.show()


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

    # cg6 = CubicGraphs(6)
    # print("Number of graphs:", len(cg6.graphs))
    # cg6.plot(index=0, filename="nauthy.png")
    # cg6.plot(index=1, filename="nauthy1.png")

