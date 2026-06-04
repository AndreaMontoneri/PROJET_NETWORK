import matplotlib.pyplot as plt
import numpy as np


def plot_network(
    df_nodes,
    df_links,
    door_nodes,
    X,
    Y,
    show_node_ids=True,
    show_link_ids=False,
    figsize=(8, 8),
):
    fig, ax = plt.subplots(figsize=figsize)

    # ==========================
    # Draw links
    # ==========================
    for _, link in df_links.iterrows():
        start = link["start_node"]
        end = link["end_node"]

        x1 = df_nodes.loc[df_nodes["node_id"] == start, "x_coord"].values[0]
        y1 = df_nodes.loc[df_nodes["node_id"] == start, "y_coord"].values[0]

        x2 = df_nodes.loc[df_nodes["node_id"] == end, "x_coord"].values[0]
        y2 = df_nodes.loc[df_nodes["node_id"] == end, "y_coord"].values[0]

        ax.arrow(
            x1 + 0.5,
            y1 + 0.5,
            0.9 * (x2 - x1),
            0.9 * (y2 - y1),
            length_includes_head=True,
            head_width=0.08,
            head_length=0.12,
            fc="gray",
            ec="gray",
            alpha=0.7,
        )

        # Link ID
        if show_link_ids:
            xm = (x1 + x2) / 2
            ym = (y1 + y2) / 2

            ax.text(xm, ym, str(link["link_id"]), color="blue", fontsize=8)

    # ==========================
    # Draw nodes
    # ==========================
    normal_nodes = df_nodes[~df_nodes["node_id"].isin(door_nodes)]
    door_nodes_df = df_nodes[df_nodes["node_id"].isin(door_nodes)]

    ax.scatter(
        normal_nodes["x_coord"] + 0.5,
        normal_nodes["y_coord"] + 0.5,
        s=300,
        color="lightblue",
        edgecolor="black",
        label="Normal cell",
    )

    ax.scatter(
        door_nodes_df["x_coord"] + 0.5,
        door_nodes_df["y_coord"] + 0.5,
        s=300,
        color="red",
        edgecolor="black",
        label="Door",
    )

    # ==========================
    # Node IDs
    # ==========================
    if show_node_ids:
        for _, node in df_nodes.iterrows():
            ax.text(
                node["x_coord"] + 0.5,
                node["y_coord"] + 0.5,
                str(node["node_id"]),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
            )

    # ==========================
    # Plot formatting
    # ==========================
    ax.set_aspect("equal")

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    ax.grid(True, alpha=0.7)
    plt.xlim([0, X])
    plt.ylim([0, Y])
    ax.invert_yaxis()
    ax.set_xticks(np.arange(X))
    ax.set_yticks(np.arange(Y))
    # plt.axis("off")

    plt.show()
