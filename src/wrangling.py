import pandas as pd
from objects import CubicGraphs, BipartiteGraph, TriangleFreeGraphs
from utils import gpn


if __name__ == "__main__":

    df_data = []
    max_nodes = 10

    for num_u in range(1, max_nodes):
        for num_v in range(num_u, max_nodes - num_u + 1):
            for num_edges in range(num_u + num_v - 1, num_u * num_v + 1):
                try:
                    g = BipartiteGraph(num_u, num_v, num_edges)
                    graph = g.graph

                    name = g.label

                    df_data.append([
                        "bipartite",
                        name,
                        graph.number_of_nodes(),
                        graph.number_of_edges(),
                        gpn(graph),
                    ])
                except RuntimeError:
                    continue


    for n in range(4, max_nodes + 1, 2):
        try:
            cg = CubicGraphs(n)
        except RuntimeError:
            continue

        for i, graph in enumerate(cg.graphs, start=1):

            name = f"cubic_{n}_nodes_{i}"

            df_data.append([
                "cubic",
                name,
                graph.number_of_nodes(),
                graph.number_of_edges(),
                gpn(graph),
            ])


    for n in range(1, max_nodes + 1):
        try:
            tg = TriangleFreeGraphs(n)
        except RuntimeError:
            continue

        for i, graph in enumerate(tg.graphs, start=1):

            deg_seq = tg.degree_sequences[i - 1]
            deg_str = "_".join(map(str, deg_seq))
            name = f"tf_{deg_str}"

            df_data.append([
                "triangle-free",
                name,
                graph.number_of_nodes(),
                graph.number_of_edges(),
                gpn(graph),
            ])


    df = pd.DataFrame(
        df_data,
        columns=["type", "name", "num_nodes", "num_edges", "gpn_num"],
    )

    df.to_csv("gpn_class_data.csv", index=False)
