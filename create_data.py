import numpy as np
import pandas as pd


def generate_nodes(width, height, nb_doors):
    """
    Generate the dataframe for the nodes

    Arguments:
        width: The size of the grid in the x-direction -> int
        height: The size of the grid in the y-direction -> int

    Returns:
        df_node: A dataframe with the columns 'node_id', 'x' coordinate and 'y' coordinate, 'links_out'
    """
    nb_node = width * height

    # NODE ID
    node_id = np.arange(nb_node)

    # DOORS ID
    top_contour = np.arange(width)
    left_contour = [width * i for i in range(1, height - 1)]
    right_contour = [width * i - 1 for i in range(2, height)]
    bot_contour = np.arange((height - 1) * width, nb_node)
    contour = np.sort(
        np.concatenate((top_contour, left_contour, right_contour, bot_contour))
    )

    idx_doors = np.sort(np.random.choice(contour, nb_doors, replace=False))

    # X_COORD / Y_COORD
    x_coord = []
    y_coord = []

    x = 0
    y = 0
    idx = 1
    while idx < nb_node + 1:
        x_coord.append(x)
        y_coord.append(y)
        if idx % (width) == 0:
            x = 0
            y += 1
        elif x < width:
            x += 1
        idx += 1

    # LINKS_OUT
    links_out = []
    idx_link = 0
    for i in range(nb_node):
        if i in idx_doors:
            links_out_i = []
        else:
            x = x_coord[i]
            y = y_coord[i]
            if y == 0:
                if (x == 0) or (x == (width - 1)):
                    link_1 = idx_link
                    link_2 = idx_link + 1
                    links_out_i = [link_1, link_2]
                    idx_link += 2
                else:
                    link_1 = idx_link
                    link_2 = idx_link + 1
                    link_3 = idx_link + 2
                    links_out_i = [link_1, link_2, link_3]
                    idx_link += 3

            elif y == (height - 1):
                if (x == 0) or (x == (width - 1)):
                    link_1 = idx_link
                    link_2 = idx_link + 1
                    links_out_i = [link_1, link_2]
                    idx_link += 2
                else:
                    link_1 = idx_link
                    link_2 = idx_link + 1
                    link_3 = idx_link + 2
                    links_out_i = [link_1, link_2, link_3]
                    idx_link += 3

            else:
                if (x == 0) or (x == (width - 1)):
                    link_1 = idx_link
                    link_2 = idx_link + 1
                    link_3 = idx_link + 2
                    links_out_i = [link_1, link_2, link_3]
                    idx_link += 3
                else:
                    link_1 = idx_link
                    link_2 = idx_link + 1
                    link_3 = idx_link + 2
                    link_4 = idx_link + 3
                    links_out_i = [link_1, link_2, link_3, link_4]
                    idx_link += 4

        links_out.append(links_out_i)

    # DATAFRAME
    data = {
        "node_id": node_id,
        "x_coord": x_coord,
        "y_coord": y_coord,
        "links_out": links_out,
    }

    df_node = pd.DataFrame(data)
    return df_node, idx_doors


def generate_links(df_node, speed, grid_size, idx_doors):
    """
    Generate the dataframe for the links

    Arguments:
        df_node: dataframe of the nodes -> Dataframe
        speed: speed people escape in [m/s] -> float
        grid_size: size of a grid in [m] -> float
        nb_doors: numbers of exit doors -> int

    Returns:
        df_link: A dataframe with the columns 'link_id', 'start_node', 'end_node', 't0'
    """
    link_per_node = df_node["links_out"].to_list()
    x_coord = df_node["x_coord"].to_list()
    y_coord = df_node["y_coord"].to_list()

    WIDTH = np.max(x_coord) + 1
    HEIGHT = np.max(y_coord) + 1

    idx_node = -1
    while len(link_per_node[idx_node]) == 0:
        idx_node -= 1
    nb_links = link_per_node[idx_node][-1] + 1
    nb_nodes = len(link_per_node)
    tt = grid_size / speed

    # LINK_ID
    link_id = np.arange(nb_links)

    # START_NODE / t0
    start_node = []
    t0 = []
    for i in range(nb_nodes):
        for j in range(len(link_per_node[i])):
            start_node.append(i)
            t0.append(tt)

    # END_NDOE
    end_node = []
    for i in range(nb_nodes):
        if i in idx_doors:
            pass
        else:
            x = x_coord[i]
            y = y_coord[i]
            if y == 0:
                if x == 0:
                    node_1 = i + 1
                    node_2 = WIDTH

                    end_node.append(node_1)
                    end_node.append(node_2)
                elif x == WIDTH - 1:
                    node_1 = i - 1
                    node_2 = 2 * WIDTH - 1

                    end_node.append(node_1)
                    end_node.append(node_2)
                else:
                    node_1 = i - 1
                    node_2 = i + 1
                    node_3 = WIDTH + x
                    end_node.append(node_1)
                    end_node.append(node_2)
                    end_node.append(node_3)

            elif y == HEIGHT - 1:
                if x == 0:
                    node_1 = i + 1
                    node_2 = (y - 1) * WIDTH

                    end_node.append(node_1)
                    end_node.append(node_2)
                elif x == WIDTH - 1:
                    node_1 = i - 1
                    node_2 = (HEIGHT - 1) * WIDTH - 1

                    end_node.append(node_1)
                    end_node.append(node_2)
                else:
                    node_1 = i - 1
                    node_2 = i + 1
                    node_3 = (y - 1) * WIDTH + x
                    end_node.append(node_1)
                    end_node.append(node_2)
                    end_node.append(node_3)

            else:
                if x == 0:
                    node_1 = i + 1
                    node_2 = (y - 1) * WIDTH
                    node_3 = (y + 1) * WIDTH
                    end_node.append(node_1)
                    end_node.append(node_2)
                    end_node.append(node_3)
                elif x == WIDTH - 1:
                    node_1 = i - 1
                    node_2 = y * WIDTH - 1
                    node_3 = (y + 2) * WIDTH - 1
                    end_node.append(node_1)
                    end_node.append(node_2)
                    end_node.append(node_3)
                else:
                    node_1 = i - 1
                    node_2 = i + 1
                    node_3 = (y - 1) * WIDTH + x
                    node_4 = (y + 1) * WIDTH + x
                    end_node.append(node_1)
                    end_node.append(node_2)
                    end_node.append(node_3)
                    end_node.append(node_4)

    # DATAFRAME
    data = {
        "link_id": link_id,
        "start_node": start_node,
        "end_node": end_node,
        "t0": t0,
    }

    df_node = pd.DataFrame(data)
    return df_node


def generate_demand(df_node, nb_people, type_dystrib):
    pass
