import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def plot_network(
    df_nodes,
    df_links,
    door_nodes,
    X,
    Y,
    show_node_ids=True,
    show_link_ids=False,
    figsize=(8, 8),
    x=None,
    name="image/CE1.pdf",
):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("lightgrey")

    # ==========================
    # Draw links
    # ==========================

    if x is not None:
        flow_min = np.min(x)
        flow_max = np.max(x)
        norm = colors.Normalize(vmin=flow_min, vmax=flow_max)
        cmap = LinearSegmentedColormap.from_list(
            "evacuation", ["white", "orange", "darkred"]
        )

    if x is None:
        color = "black"
        lw = 1

    for idx, link in df_links.iterrows():
        if x is not None:
            # lw = 1 + 4 * (x[idx] - flow_min) / (max(flow_max - flow_min, 1e-9))
            color = cmap(norm(x[idx]))
            lw = 1 + 5 * norm(x[idx])
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
            fc=color,
            ec=color,
            linewidth=lw,
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
    door_nodes_df = df_nodes[df_nodes["node_id"].isin(door_nodes)]

    cap8 = df_nodes[
        (~df_nodes["node_id"].isin(door_nodes)) & (df_nodes["capacity"] == 4)
    ]

    cap2 = df_nodes[
        (~df_nodes["node_id"].isin(door_nodes)) & (df_nodes["capacity"] == 2)
    ]

    cap1 = df_nodes[
        (~df_nodes["node_id"].isin(door_nodes)) & (df_nodes["capacity"] == 1)
    ]

    ax.scatter(
        door_nodes_df["x_coord"] + 0.5,
        door_nodes_df["y_coord"] + 0.5,
        s=200,
        color="deepskyblue",
        edgecolor="black",
        label="Door",
    )

    ax.scatter(
        cap8["x_coord"] + 0.5,
        cap8["y_coord"] + 0.5,
        s=200,
        color="palegreen",
        edgecolor="black",
        label="Open",
    )

    ax.scatter(
        cap2["x_coord"] + 0.5,
        cap2["y_coord"] + 0.5,
        s=200,
        color="moccasin",
        edgecolor="black",
        label="Corridor",
    )

    ax.scatter(
        cap1["x_coord"] + 0.5,
        cap1["y_coord"] + 0.5,
        s=200,
        color="salmon",
        edgecolor="black",
        label="Seat",
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

    if x is not None:
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(
            sm,
            ax=ax,
            fraction=0.046,
            pad=0.04,
        )

        cbar.set_label("Link flow")
    ax.set_aspect("equal")

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    ax.grid(True, alpha=0.7)
    ax.set_facecolor("blue")
    plt.xlim([0, X])
    plt.ylim([0, Y])
    ax.invert_yaxis()
    ax.set_xticks(np.arange(X))
    ax.set_yticks(np.arange(Y))
    plt.axis("off")
    plt.savefig(name)

    plt.show()
