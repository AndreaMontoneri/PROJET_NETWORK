import queue

import numpy as np


def shortest_path_tree(t, org, df_node, df_link):
    """
    Generate shortest path tree from a given origin node
    using label correction

    :param t: link cost
    :param org: origin

    :return u: node label
    :return p: previous link on shortest path for each node
    """
    # Extract data
    node_ids = df_node["node_id"].to_numpy()
    links_out = df_node["links_out"].to_numpy()

    end_node = df_link["end_node"].to_numpy()

    n_node = node_ids.shape[0]

    # Initialize
    u = np.inf * np.ones(n_node)
    u[org] = 0
    p = -1 * np.ones(n_node)
    Q = queue.Queue()
    Q.put(org)

    # Algorithm
    while Q.qsize() > 0:
        i = Q.get()
        list_out_node = links_out[i]
        for candidate in list_out_node:
            j = end_node[candidate]
            if u[j] > u[i] + t[candidate]:
                u[j] = u[i] + t[candidate]
                p[j] = candidate
                if j not in Q.queue:
                    Q.put(j)
    return u, p


def construct_shortest_path(r, s, u, p, df_links):
    """
    Construct shortest path using the outputs of labeling algorithm

    :param r: origin node
    :param s: destination node
    :param u: node labels
    :param p: previous link on shortest path for each node
    :param df_links: dataframe of links

    :return sp_node: shortest path as a sequence of nodes
    :return sp_link: shortest path as a sequence of links

    """
    # Initialize
    start_node = df_links["start_node"].to_numpy()

    sp_node = [s]
    link = int(p[s])
    sp_link = [link]
    node_i = start_node[link]

    while node_i != r:
        sp_node.append(int(node_i))
        link = int(p[node_i])
        sp_link.append(link)
        node_i = start_node[link]

    sp_node.append(r)
    sp_node.reverse()
    sp_link.reverse()

    return sp_node, sp_link


def print_sp(sp_node):
    """
    Print the shortest path in a clean and readable way

    :param sp_node: list of node in shortest path
    """
    sp_str = " -> ".join([str(node) for node in sp_node])
    print(sp_str)


def all_or_nothing_assignment(t, df_od, df_links, df_node):
    """
    All-or-nothing assignment: load traffic flows on shortest paths

    :param t: link cost

    :return x: link flow
    """
    # Extract data
    od_id = df_od["od_id"].to_numpy()
    origin = df_od["origin"].to_numpy()
    destination = df_od["destination"].to_numpy()
    q = df_od["demand"].to_numpy()

    x = np.zeros(t.shape)

    for id in od_id:
        org = origin[id]
        dest = destination[id]

        u, p = shortest_path_tree(t, org, df_node, df_links)

        sp_node, sp_link = construct_shortest_path(org, dest, u, p, df_links)

        x[sp_link] += q[id]
    return x


def line_search(x, y, max_gap, link_cost_function: callable, df_links):
    """
    Determine step size by bisection line search

    :param x: current link flows
    :param y: target link flows
    :param max_gap: gap threshold
    :param link_cost_function: link cost for the current opti pb

    :return step: optimal step size
    """
    alpha_L = 0
    alpha_U = 1
    while alpha_U - alpha_L > max_gap:
        alpha = (alpha_L + alpha_U) / 2
        grad = link_cost_function(x + alpha * (y - x), df_links) @ (y - x)
        if grad > 0:
            alpha_U = alpha
        else:
            alpha_L = alpha
    return alpha


def FW(
    max_iter,
    max_gap,
    max_gap_ls,
    link_cost_function: callable,
    objective_function: callable,
    df_od,
    df_link,
    df_nodes,
):
    """
    Solve static traffic assignment
    using Frank-Wolfe algorithm

    :param max_iter: max number of iterations of main loop
    :param max_gap: gap threshold of main loop
    :param max_gap_ls: gap threshold of line search
    :param link_cost_function: link cost for the current opti pb
    :param objective_function: objective for the current opti pb

    :return x_star: equilibrium link flow
    :return gap: gap over iterations
    :return obj: objective value over iterations
    """
    t0 = df_link["t0"].to_numpy()

    gap = []
    obj = []
    x = []
    x.append(all_or_nothing_assignment(t0, df_od, df_link, df_nodes))

    for i in range(max_iter):
        if (i + 1) % 500 == 0:
            print(f"Iteration : {i + 1} / {max_iter}")

        t = link_cost_function(x[-1], df_link)
        y = all_or_nothing_assignment(t, df_od, df_link, df_nodes)
        d = y - x[-1]
        alpha = line_search(x[-1], y, max_gap_ls, link_cost_function, df_link)
        x.append(x[-1] + alpha * d)
        gap.append(np.dot(t, -d) / np.dot(t, x[-1]))
        obj.append(objective_function(x[-1], df_link))
        if gap[-1] < max_gap:
            break

    if i != max_iter - 1:
        print(f"Converged after {i + 1} iterations")

    x_star = x[-1]

    return x_star, gap, obj
