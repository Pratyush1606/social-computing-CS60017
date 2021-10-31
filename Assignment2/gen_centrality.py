from pathlib import Path
from collections import defaultdict, deque
import os

# Configuring file locations of datasets, plots and output files
from config import CONFIG

# Dataset
DATASET = os.path.join(CONFIG["DATASET_DIR"], "imdb_prodco.adj")

# Plot Directory
PLOT_DIR = CONFIG["PLOT_DIR"]

# Output Text File
OUTPUT_FILE = Path(".\output_2_closeness.txt")

# Making the blank output files
with open(OUTPUT_FILE, "w") as f:
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

def closeness_centrality(V, graph):
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

# Reading Dataset
with open(DATASET, "r") as file:
    data = file.readlines()

rows, columns = map(int, data[0].strip().split(","))

# adjacency_mat = [[float("inf") for _ in range(columns)] for _ in range(rows)]
# for line in data[1:]:
#     u, v, w = map(int, line.strip().split(","))
#     adjacency_mat[u][v] = w
#     adjacency_mat[v][u] = w

# # Making adjacency list
# graph = defaultdict(list)
# for i in range(rows):
#     for j in range(columns):
#         if(adjacency_mat[i][j]!=float("inf")):
#             graph[i].append((j, adjacency_mat[i][j]))

# Making adjacency list
graph = defaultdict(list)
for line in data[1:]:
    u, v, w = map(int, line.strip().split(","))
    graph[u].append((v, w))
    graph[v].append((u, w))

closeness_cenrality_list = closeness_centrality(rows, graph)

# Writing output to the output file
output = ""
for node_ID, centrality_value in enumerate(closeness_cenrality_list):
    output += "{} {}".format(node_ID, centrality_value)
    output += "\n"

with open(OUTPUT_FILE, "w") as f:
    f.write(output)

