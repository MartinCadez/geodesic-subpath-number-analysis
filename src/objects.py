from sage.all import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random


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
        if num_nodes < 2:
            raise ValueError("star graph must have at least 2 nodes")

    def _build_graph(self):

        graph = nx.Graph()
        graph.add_edges_from([(0, node) for node in range(1, self.num_nodes)])
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
        return {f"v_{i+1}": list(neighbors) for i, (node, neighbors) in enumerate(self.graph.adjacency())}

    @property
    def degree_sequence(self) -> list:
        return [(node, degree) for node, degree in self.graph.degree()]

    def plot(self, filename: str | None = None) -> None:
        plt.figure(figsize=(8, 8))

        pos = {0: (0, 0)}

        angle_step = 2 * np.pi / (self.num_nodes - 1)
        for i in range(1, self.num_nodes):
            angle = i * angle_step
            pos[i] = (np.cos(angle), np.sin(angle))

        nx.draw_networkx(
            self.graph,
            pos=pos,
            labels={n: f"$v_{{{n + 1}}}$" for n in self.graph.nodes()},
            with_labels=True,
            node_color="#697ad1",
            edgecolors="#291a40",
            linewidths=2,
            node_size=2200,
            width=2,
            font_color="white",
            font_size=22
        )
        
        plt.axis("off")
        
        if filename:
            plt.savefig(filename, bbox_inches="tight")
            plt.close()
        else:
            plt.show()


class RandomBalancedBipartiteGraph:

    def __init__(
        self,
        num_nodes: int,
        edge_probability: float = 0.5,
        seed: int = None
    ):
        self.num_nodes = num_nodes
        self.edge_probability = edge_probability
        self.seed = seed
        
        self._validate_args(num_nodes, edge_probability)
        self.graph = self._build_graph()
        # self.graph.plot = lambda filename=None: plot(self.graph, filename)

    def __repr__(self) -> str:
        return f"RandomBalancedBipartiteGraph(num_nodes={self.num_nodes}, edge_probability={self.edge_probability})"

    def __str__(self) -> str:
        return f"{self.__repr__()}"

    @staticmethod
    def _validate_args(num_nodes: int, edge_probability: float) -> None:
        if not isinstance(num_nodes, int) or num_nodes < 2:
            raise ValueError("num_nodes must be an integer >= 2")
        if not (0 <= edge_probability <= 1):
            raise ValueError("edge_probability must be between 0 and 1")
    
    def _build_graph(self) -> nx.Graph:
        if self.seed is not None:
            random.seed(self.seed)
    
        # initializing BALANCED partition sets 
        u_set = list(range(self.num_nodes // 2)) # smaller partition; for odd `num_nodes`
        v_set = list(range(self.num_nodes // 2, self.num_nodes))
        
        # bp-connected structure; defined for consistency
        possible_edges = [(u, v) for u in u_set for v in v_set]
        max_possible_edges = len(possible_edges)

        graph = nx.Graph()
        graph.add_nodes_from(u_set, bipartite=0)
        graph.add_nodes_from(v_set, bipartite=1)

        # again for consistency; keep graph simple & connected
        # => tree will always have n-1 edges for graph with n nodes
        # which is the smallest num of edges to keep graph connected 
        # without forming a cycle
        spanning_tree_edges = [] 

        if u_set and v_set:
            # init graph construction process; 
            # random edge & already connected nodes var (span tree init)
            init_node_u, init_node_v = random.choice(u_set), random.choice(v_set)
            spanning_tree_edges.append((init_node_u, init_node_v))
            connected_u_nodes, connected_v_nodes = {init_node_u}, {init_node_v}

            # -> edge-side-init-build of spanning tree:

            # connect each unconnected node from the `u partition` 
            # to an already connected node in the `v partition` 
            # p.s. connections are done randomly
            for node in u_set:
                if node not in connected_u_nodes:
                    target_node = random.choice(list(connected_v_nodes))
                    spanning_tree_edges.append((node, target_node))
                    connected_u_nodes.add(node)

            # (vice versa): connect unconnected nodes in `v partition`
            for node in v_set:
                if node not in connected_v_nodes:
                    target_node = random.choice(list(connected_u_nodes))
                    spanning_tree_edges.append((target_node, node))
                    connected_v_nodes.add(node)

        graph.add_edges_from(spanning_tree_edges)

        # -> probability based edge assignment (increase graph density)

        # edge normalization (dealing with undirected graphs) 
        existing_edges = {
            (min(u, v), max(u, v)) for u, v in spanning_tree_edges
        }

        remaining_edges = [
            (u, v) for u, v in possible_edges
            if (min(u, v), max(u, v)) not in existing_edges
        ]

        # change order; aka create random sample
        random.shuffle(remaining_edges)

        # expected value of edges to be added stochastically
        expected_edges = int(self.edge_probability * max_possible_edges)

        # ensure connectivity; keep at least `num_nodes` - 1 edges
        remaining_to_add = max(self.num_nodes - 1, expected_edges) - len(spanning_tree_edges)
        # bound remaining number of edges between 0 and number of available candidate edges
        remaining_to_add = max(0, min(remaining_to_add, len(remaining_edges)))

        additional_edges = [
            e for e in remaining_edges
            if random.random() < self.edge_probability
        ][:remaining_to_add]

        graph.add_edges_from(additional_edges)

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
        return {f"v_{i+1}": list(neighbors) for i, (node, neighbors) in enumerate(self.graph.adjacency())}

    @property
    def degree_sequence(self) -> list:
        return [(node, degree) for node, degree in self.graph.degree()]

    def plot(self, filename: str | None = None) -> None:
        plt.figure(figsize=(12, 8))
        
        u_set, v_set = nx.bipartite.sets(self.graph)
        
        labels = {}
        for i, node in enumerate(sorted(u_set)):
            labels[node] = f"$u_{{{i}}}$"
        for i, node in enumerate(sorted(v_set)):
            labels[node] = f"$v_{{{i}}}$"
        
        nx.draw_networkx(
            self.graph,
            pos=nx.bipartite_layout(self.graph, u_set),
            labels=labels,
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

