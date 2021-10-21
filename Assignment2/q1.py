import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from networkx.algorithms import community
from collections import defaultdict
import os
import sys

# Configuring file locations of datasets, plots and output files
from config import CONFIG

# Datasets
DBLP_DATASET = os.path.join(CONFIG["DATASET_DIR"], "com-dblp.ungraph.txt")
EUCORE_DATASET = os.path.join(CONFIG["DATASET_DIR"], "email-Eu-core.txt")
DBLP_GROUND_TRUTH_COM_DATASET = os.path.join(CONFIG["DATASET_DIR"], "com-dblp.all.cmty.txt")
EUCORE_GROUND_TRUTH_COM_DATASET = os.path.join(CONFIG["DATASET_DIR"], "email-Eu-core-department-labels.txt")

# Plot Directory
PLOT_DIR = CONFIG["PLOT_DIR"]

# Output Text Files
NEWMAN_OUTPUT_FILE = Path(".\output_1_NEWMAN.txt")
CLAUSET_OUTPUT_FILE = Path(".\output_1_CLAUSET.txt")

# Making the blank output files
with open(NEWMAN_OUTPUT_FILE, "w") as f:
    f.write("")

with open(CLAUSET_OUTPUT_FILE, "w") as f:
    f.write("")

# NEWMAN_OUTPUT = open(NEWMAN_OUTPUT_FILE, "a")
# CLAUSET_OUTPUT = open(CLAUSET_OUTPUT_FILE, "a")

NEWMAN_METHOD_NAME = "NEWMAN"
CLAUSET_METHOD_NAME = "CLAUSET"
DBLP_DATASET_NAME = "DBLP"
EUCORE_DATASET_NAME = "EUCORE"

###################################################

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
    def flush(self):
        pass

# Configuring script to print to stdout as well as to different output files
# backup = sys.stdout

###################################################

# Making undirected graph from DBLP Dataset
Graphtype = nx.Graph()   # for undirected graph
DBLP_GRAPH = nx.read_edgelist(DBLP_DATASET, create_using=Graphtype, nodetype=int)

# Making directed graph from EUCORE Dataset
Graphtype = nx.DiGraph()   # for directed graph
EUCORE_GRAPH = nx.read_edgelist(EUCORE_DATASET, create_using=Graphtype, nodetype=int)

###################################################

def get_num_of_communities(methodname, datasetname, graph):
    '''
    Calculates the number of communities generated

    Also returns the list of communities
    '''
    # Setting output file to be written into
    # sys.stdout = Tee(sys.stdout, output_file)
    print("Dataset: {}".format(datasetname))

    if(methodname == NEWMAN_METHOD_NAME):
        communities = community.girvan_newman(graph)
        num_communities = len(list(communities))
        print("Number of communities using Newman-Girvan method: {}".format(num_communities))
        
    elif(methodname == CLAUSET_METHOD_NAME):
        communities = community.greedy_modularity_communities(graph)
        num_communities = len(list(communities))
        print("Number of communities using Clauset-Newman-Moore greedy modularity maximization method: {}".format(num_communities))
        
    print()
    return communities

###################################################

def plot_community_size_distribution(methodname, datasetname, communities):
    '''
    Plots the community size distribution for diff datasets and methods

    communities: List of communities
    '''
    data = defaultdict(int)
    for c in communities:
        data[len(c)] += 1
    
    x, y = [], []
    for key, val in data.items():
        x.append(key)
        y.append(val)
    
    plt.plot(x, y)
    plt.xlabel("Size of Communities")
    plt.ylabel("Frequency")
    plt.title("Community Size distribution of {} graph using {} method".format(datasetname, methodname))
    fig_destination = os.path.join(PLOT_DIR, f"{datasetname}_{methodname}_dist.png")
    plt.savefig(fig_destination)

###################################################

def plot_ground_truth_community_size_distribution(methodname, datasetname, dataset):
    '''
    Plots the ground truth community size distribution for diff datasets and methods
    '''
    if(datasetname == DBLP_DATASET_NAME):
        pass

    elif(datasetname == EUCORE_DATASET_NAME):
        data = defaultdict(list)

        # Reading the ground truth dataset
        with open(dataset, "r") as f:
            node_id_dept_list = f.readlines()
        
        for t in node_id_dept_list:
            node_id, dept = map(int, t.strip().split())
            data[dept].append(node_id)
        
        x, y = [], []
        for key, val in data.items():
            x.append(key)
            y.append(len(val))
        
    plt.plot(x, y)
    plt.xlabel("Size of Ground Truth Communities")
    plt.ylabel("Frequency")
    plt.title("Ground Truth Community Size distribution of {} graph using {} method".format(datasetname, methodname))
    fig_destination = os.path.join(PLOT_DIR, f"ground_truth_communities_dist_{datasetname}_{methodname}.png")
    plt.savefig(fig_destination)
    


