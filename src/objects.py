from sage.all import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class BipartiteGraphs:
    
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
            raise ValueError("num_nodes must be an integer")
        if num_nodes < 1:
            raise ValueError("bipartiteGraph graph must have at least 1 node")

    def _build_graphs(self):
        self._validate_args(self.num_nodes)

        nx_graphs = [g.networkx_graph() for g in graphs.nauty_geng(f"{self.num_nodes} -b -c")]

        if not nx_graphs:
            raise RuntimeError(f"no bipartite graphs generated for n={self.num_nodes}")

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
            node_size=3000,
            width=2,
            font_color="white",
            font_size=30
        )
        
        plt.axis("off")

        if filename:
            plt.savefig(filename, bbox_inches="tight", facecolor="white")
            plt.close()
        else:
            plt.show()

class CubicGraphs:

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
            raise ValueError("num_nodes must be an integer")
        if num_nodes < 4:
            raise ValueError("cubic graph must have at least 4 nodes")
        if num_nodes % 2 != 0:
            raise ValueError("cubic (3-regular) graph must have an even number of nodes")

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
        
        nx.draw_networkx(
            graph,
            pos=nx.circular_layout(graph),
            labels={n: f"$v_{{{n+1}}}$" for n in graph.nodes()},
            node_color="#698ad1",
            edgecolors="#292a40",
            linewidths=2,
            node_size=3000,
            width=2,
            font_color="white",
            font_size=30
        )

        plt.axis("off")

        if filename:
            plt.savefig(filename, bbox_inches="tight", facecolor="white")
            plt.close()
        else:
            plt.show()

class StarGraph:

    def __init__(
            self,
            num_nodes: int
        ):
        self.num_nodes = num_nodes
        self._validate_args(num_nodes)
        self.graph = self._build_graph()

    def __repr__(self) -> str:
        return f"StarGraph(num_nodes={self.num_nodes})"

    def __str__(self) -> str:
        return f"{self.__repr__()}"

    @staticmethod
    def _validate_args(num_nodes: int) -> None:
        if not isinstance(num_nodes, int):
            raise ValueError("num_nodes must be an integer")
        if num_nodes < 1:
            raise ValueError("star graph must have at least 1 nodes")

    def _build_graph(self):
        graph = nx.Graph()
        
        graph.add_nodes_from(range(self.num_nodes))
        graph.add_edges_from((-1, node) for node in range(1, self.num_nodes))

        return graph

    @property
    def edges(self) -> list:
        return list(self.graph.edges())

    @property
    def adj_matrix(self) -> np.ndarray:
        return nx.to_numpy_array(self.graph, nodelist=sorted(self.graph.nodes()))

    @property
    def incidence_matrix(self) -> np.ndarray:
        return nx.incidence_matrix(self.graph, oriented=False).toarray()

    @property
    def nodes(self) -> dict:
        return {f"v_{i+0}": list(neighbors) for i, (node, neighbors) in enumerate(self.graph.adjacency())}

    @property
    def degree_sequence(self) -> list:
        return [(node, degree) for node, degree in self.graph.degree()]

    def plot(self, filename: str | None = None) -> None:
        plt.figure(figsize=(7, 8))
        pos = {-1: (0, 0)}
        
        angle_step = 1 * np.pi / (self.num_nodes - 1)
        for i in range(0, self.num_nodes):
            angle = i * angle_step
            pos[i] = (np.cos(angle), np.sin(angle))

        nx.draw_networkx(
            self.graph,
            pos=pos,
            labels={n: f"$v_{{{n+0}}}$" for n in self.graph.nodes()},
            with_labels=True,
            node_color="#697ad1",
            edgecolors="#291a40",
            linewidths=1,
            node_size=2199,
            width=1,
            font_color="white",
            font_size=22
        )
        
        plt.axis("off")
        
        if filename:
            plt.savefig(filename, bbox_inches="tight")
            plt.close()
        else:
            plt.show()