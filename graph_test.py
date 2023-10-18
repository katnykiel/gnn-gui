from pymatgen.core import Structure
import plotly.graph_objects as go
from collections import Counter
import networkx as nx


def visualize_structure_test():
    """
    This function reads in a structure file, creates a graph of the structure,
    and visualizes the graph using Plotly.

    Returns:
    None
    """
    # Read in the structure file
    structure = Structure.from_file("NaCl.cif")

    # Set the radius cutoff for identifying neighbors
    radius_cutoff = 5  # angstroms

    # Create a list of neighbors for each site in the structure
    neighbors_list = []
    elements = []
    for i, site in enumerate(structure):
        site_id = f"{site.specie}-{i}"
        neighbors = structure.get_sites_in_sphere(site.coords, radius_cutoff)
        neighbor_indices = list(
            set([f"{neighbor.specie}-{neighbor.index}" for neighbor in neighbors])
        )
        neighbors_list.append(neighbor_indices)
        elements.append(site_id)

    # Create a list of edges between neighboring sites
    edges = []
    for i in range(len(elements)):
        for j in range(len(neighbors_list[i])):
            edges.append([elements[i], neighbors_list[i][j]])

    # Flatten the list of lists
    flattened = [item for sublist in edges for item in sublist]

    # Count the occurrences of each element in the flattened list
    counts = Counter(flattened)

    # Get all elements that appear more than once
    duplicates = [element for element in counts if counts[element] > 1]

    # Filter the list of paired lists to only include items that appear more than once
    edges = [edge for edge in edges if edge[0] in duplicates and edge[1] in duplicates]

    # Create an empty graph
    G = nx.Graph()

    # Add nodes to the graph
    for sublist in edges:
        for node in sublist:
            G.add_node(node)

    # Add edges to the graph
    for sublist in edges:
        G.add_edge(sublist[0], sublist[1])

    # Give a random position to each node
    pos = nx.spring_layout(G)
    for node in G.nodes():
        G.nodes[node]["pos"] = pos[node].tolist()

    # Create a list of x and y coordinates for each edge
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Create a scatter plot of the edges
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Create a list of x and y coordinates for each node
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)

    # Assign colors to each node based on its element
    node_colors = []
    for node in G.nodes():
        if "Na" in node:
            node_colors.append("crimson")
        elif "Cl" in node:
            node_colors.append("goldenrod")
        else:
            node_colors.append("blue")

    # Create a scatter plot of the nodes
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        text=list(G.nodes()),
        hoverinfo="text",
        marker=dict(
            color=node_colors,
            size=20,
            line_width=2,
        ),
    )

    # Add the number of connections to each node's text
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(list(G.nodes)[node])

    node_trace.text = node_text

    # Create the final figure and display it
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Network graph of embedding",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            template="simple_white",
            font_size=20,
            # width=800,
            # height=800,
        ),
    )
    fig.show()


visualize_structure_test()
