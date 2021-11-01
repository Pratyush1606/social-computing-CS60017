from pathlib import Path
from collections import defaultdict, deque
import os
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import centrality

# Configuring file locations of datasets, plots and output files
from config import CONFIG

# Dataset
DATASET = os.path.join(CONFIG["DATASET_DIR"], "imdb_prodco.adj")

# Plot Directory
PLOT_DIR = CONFIG["PLOT_DIR"]

# Output Text File
OUTPUT_FILE_1 = Path(".\output_2_closeness.txt")
OUTPUT_FILE_2 = Path(".\output_2.txt")

# Making the blank output files
with open(OUTPUT_FILE_1, "w") as f:
    f.write("")
# Making the blank output files
with open(OUTPUT_FILE_2, "w") as f:
    f.write("")

###################################################

def get_shortest_length_path_from_source(node, graph):
    '''
    Get the shortest path lengths to all the accessible nodes from the given node

    Returns a list of shortest distances to accessible nodes from given node
    '''
    dist = []
    visited = defaultdict(bool)
    visited[node] = True
    q = deque()
    q.append((node, 0))
    while(q):
        curr_node, curr_dist = q.popleft()
        for neigh, weight in graph[curr_node]:
            if(not visited[neigh]):
                visited[neigh] = True
                neigh_dist = curr_dist + 1
                q.append((neigh, neigh_dist))
                dist.append(neigh_dist)
    return dist

def get_closeness_centrality(V, graph):
    '''
    Calculate closeness_centrality of a graph

    Inputs:
    V: Number of total nodes in the graph
    graph: Adjacency List

    Returns:
    closeness_centrality: List of all the closeness_centrality of the nodes
    '''
    closeness_centrality = [0]*V
    
    for node in range(V):
        shortest_path_lengths = get_shortest_length_path_from_source(node, graph)
        tot_shortest_paths = sum(shortest_path_lengths)
        len_shortest_paths = len(shortest_path_lengths)
        node_closeness_centrality = 0
        if(tot_shortest_paths>0 and V>1):
            node_closeness_centrality = (len_shortest_paths - 1)/tot_shortest_paths
            # Normalizing with respect to unconnected components
            node_closeness_centrality *= (len_shortest_paths - 1)/(V - 1)
        closeness_centrality[node] = node_closeness_centrality
    return closeness_centrality

def make_graph_from_dataset(data):
    # Returns a graph (adjacency list) from data read from dataset
    graph = defaultdict(list)
    for line in data:
        u, v, w = map(int, line.strip().split(","))
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph

def get_top_50_nodes(centrality_list):
    '''
    Returns the list of top 50 nodes with respect to closeness centrality
    '''
    top_50_nodes_value_list = sorted(list(enumerate(centrality_list)), key=lambda x: x[1], reverse=True)[:50]
    top_50_nodes = [node for node, _ in top_50_nodes_value_list]
    return top_50_nodes

###################################################
print()
print("Question 2")
print("-----------")
print()

# Reading Dataset
with open(DATASET, "r") as file:
    data = file.readlines()

rows, columns = map(int, data[0].strip().split(","))
data = data[1:]     # Removing the first line containing the rows and columns

###################################################

print("Part A")
# Making adjacency list
graph = make_graph_from_dataset(data)
closeness_centrality_list = get_closeness_centrality(rows, graph)

# Writing output to the output 1 file
output = ""
for node_ID, centrality_value in enumerate(closeness_centrality_list):
    output += "{} {}".format(node_ID, centrality_value)
    output += "\n"
with open(OUTPUT_FILE_1, "w") as f:
    f.write(output)

###################################################

print("Part B")
# Making an undirected graph from the data read from dataset
G = nx.Graph()
for line in data:
    u, v, w = map(int, line.strip().split(","))
    G.add_edge(u, v)

print("a.")
closeness_centrality_dict_from_nx = centrality.closeness_centrality(G)
closeness_centrality_list_from_nx = [0]*rows
for key, value in closeness_centrality_dict_from_nx.items():
    closeness_centrality_list_from_nx[key] = value

# Plotting the histogram
print("Plotting Closeness Centrality Values")
plt.title("Normalized Closeness Centrality")
plt.hist(closeness_centrality_list_from_nx, rwidth=0.2)
plt.xlabel("Closeness Centrality Values")
plt.ylabel("Frequency")
fig_destination = os.path.join(PLOT_DIR, "closeness_dist.png")
plt.savefig(fig_destination)
plt.close()
print("Plotting Done")
print()

print("b.")
top_50_nodes = get_top_50_nodes(closeness_centrality_list)
top_50_nodes_from_nx = get_top_50_nodes(closeness_centrality_list_from_nx)
overlapping_nodes = list(set(top_50_nodes) & set(top_50_nodes_from_nx))

# Writing output to the output 2 file
output = "#overlaps for Closeness Centrality: {}".format(len(overlapping_nodes))
with open(OUTPUT_FILE_2, "w") as f:
    f.write(output)