from math import sqrt


def v_add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]


def v_mul(k, v):
    return [v[0] * k, v[1] * k]


def edge_to_arrow(ax, edge, color="k"):
    ax.arrow(
        edge[0][0],
        edge[0][1],
        edge[1][0] - edge[0][0],
        edge[1][1] - edge[0][1],
        head_width=0.05,
        head_length=0.1,
        length_includes_head=True,
        fc=color,
        ec=color,
    )


def plot_edge_set(ax, edges, color):
    for e1 in edges:
        edge_to_arrow(ax, e1, color=color)


u = [1, 0]
v = [1 / 2, sqrt(3) / 2]


def generate_triangular_edges_from_origin(origins):
    u = [1, 0]
    v = [1 / 2, sqrt(3) / 2]

    edge_1 = [1 / 2, sqrt(3) / 2]
    edges_type_1 = [(v_add(o, edge_1), o) for o in origins]
    edge_2 = [1, 0]
    edges_type_2 = [(o, v_add(o, edge_2)) for o in origins]

    # For edge 3 we need a shift of origin to get the whole set.
    edge_3 = [1 / 2, -sqrt(3) / 2]
    shift = [1 / 2, sqrt(3) / 2]
    origins_shifted = [v_add(shift, o) for o in origins]
    edges_type_3 = [(v_add(os, edge_3), os) for os in origins_shifted]

    return (edges_type_1, edges_type_2, edges_type_3)
