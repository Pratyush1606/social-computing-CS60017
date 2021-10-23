import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from networkx.algorithms import community
from collections import defaultdict
import os

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
        '''
        Dataset is in the form of
        Com1_Node1 Com1_Node2 Com1_Node3 ....
        .....       .....
        '''
        ground_truth_communities = []
        # Reading the ground truth dataset
        with open(dataset, "r") as f:
            comm_list = f.readlines()
        
        for t in comm_list:
            ground_truth_communities.append(list(map(int, t.strip().split())))

    elif(datasetname == EUCORE_DATASET_NAME):
        '''
        Dataset is in the form of
        NodeId      Department
        .....       .....
        '''
        data = defaultdict(list)

        # Reading the ground truth dataset
        with open(dataset, "r") as f:
            node_id_dept_list = f.readlines()
        
        for t in node_id_dept_list:
            node_id, dept = map(int, t.strip().split())
            data[dept].append(node_id)
        ground_truth_communities = list(data.values())

    # Calculating the frequency of the communities
    freq = defaultdict(int)
    for comm in ground_truth_communities:
        freq[len(comm)] += 1

    x, y = [], []
    for key, val in freq.items():
        x.append(key)
        y.append(val)
        
    plt.plot(x, y)
    plt.xlabel("Size of Ground Truth Communities")
    plt.ylabel("Frequency")
    plt.title("Ground Truth Community Size distribution of {} using {} method".format(datasetname, methodname))
    fig_destination = os.path.join(PLOT_DIR, f"ground_truth_communities_dist_{datasetname}_{methodname}.png")
    plt.savefig(fig_destination)
    return ground_truth_communities
    
###################################################

def get_top_5_communities(communities):
    '''
    Get the top 5 communities based on the number of nodes from a list of communities'''
    return sorted(communities, key=lambda com: len(com), reverse=True)[:5]

###################################################

def get_subragphs_from_communities(graph, communities):
    '''
    Get a list of subgraphs from a list of community nodes and the original graph
    '''
    communities_subgraphs = []
    for com in communities:
        subgraph = graph.subgraph(com).copy()
        communities_subgraphs.append(subgraph)
    
    return communities_subgraphs

###################################################

def print_top_5_communities_size(methodname, datasetname, community_subgraphs):
    '''
    Print the size of the top 5 communities in the form of  (number of nodes, number of edges)
    '''
    print("Method: {}".format(methodname))
    print("Dataset: {}".format(datasetname))
    for i in range(len(community_subgraphs)):
        community_subgraph = community_subgraphs[i]
        number_of_nodes = community_subgraph.number_of_nodes()
        number_of_edges = community_subgraph.number_of_edges()
        print(f"Community {i+1}: (number_of_nodes = {number_of_nodes}, number_of_edges = {number_of_edges})")

###################################################

def get_community_coverage(methodname, datasetname, graph, communities):
    '''
    Get the coverage of the top 5 communities
    '''
    print("Method: {}".format(methodname))
    print("Dataset: {}".format(datasetname))
    for i in range(len(communities)):
        com = communities[i]
        coverage, performance = community.partition_quality(graph, [com])
        print("Coverage of community {} = {}".format(i+1, coverage))


def get_jaccard_coefficient(methodname, datasetname, graph1, graph2):
    '''
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.jaccard_coefficient.html#networkx.algorithms.link_prediction.jaccard_coefficient

    https://stackoverflow.com/questions/50704439/python-jaccard-similartity-between-two-networks
    '''
    pass

###################################################
print()
print("Question 1")
print("-----------")
print()

# Making undirected graph from DBLP Dataset
Graphtype = nx.Graph()   # for undirected graph
DBLP_GRAPH = nx.read_edgelist(DBLP_DATASET, create_using=Graphtype, nodetype=int)

# Making directed graph from EUCORE Dataset
Graphtype = nx.DiGraph()   # for directed graph
EUCORE_GRAPH = nx.read_edgelist(EUCORE_DATASET, create_using=Graphtype, nodetype=int)

###################################################

def run():
    # Part A
    print("[a]")

    DBLP_NEWMAN_COMMUNITIES = get_num_of_communities(NEWMAN_METHOD_NAME, DBLP_DATASET_NAME, DBLP_GRAPH)
    EUCORE_NEWMAN_COMMUNITIES = get_num_of_communities(NEWMAN_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_GRAPH)
    DBLP_CLAUSET_COMMUNITIES = get_num_of_communities(CLAUSET_METHOD_NAME, DBLP_DATASET_NAME, DBLP_GRAPH)
    EUCORE_CLAUSET_COMMUNITIES = get_num_of_communities(CLAUSET_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_GRAPH)

    print()

    ###################################################

    # Part B
    print("[b]")

    plot_community_size_distribution(NEWMAN_METHOD_NAME, DBLP_DATASET_NAME, DBLP_NEWMAN_COMMUNITIES)
    plot_community_size_distribution(NEWMAN_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_NEWMAN_COMMUNITIES)
    plot_community_size_distribution(CLAUSET_METHOD_NAME, DBLP_DATASET_NAME, DBLP_CLAUSET_COMMUNITIES)
    plot_community_size_distribution(CLAUSET_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_CLAUSET_COMMUNITIES)

    print()

    ###################################################

    # Part C
    print("[c]")

    DBLP_NEWMAN_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(NEWMAN_METHOD_NAME, DBLP_DATASET_NAME, DBLP_GROUND_TRUTH_COM_DATASET)
    EUCORE_NEWMAN_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(NEWMAN_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_GROUND_TRUTH_COM_DATASET)
    DBLP_CLAUSET_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(CLAUSET_METHOD_NAME, DBLP_DATASET_NAME, DBLP_GROUND_TRUTH_COM_DATASET)
    EUCORE_CLAUSET_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(CLAUSET_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_GROUND_TRUTH_COM_DATASET)

    print()

    ###################################################

    # Part D
    print("[d]")

    DBLP_NEWMAN_TOP_5_COMMUNITIES = get_top_5_communities(DBLP_NEWMAN_COMMUNITIES)
    EUCORE_NEWMAN_TOP_5_COMMUNITIES = get_top_5_communities(EUCORE_NEWMAN_COMMUNITIES)
    DBLP_CLAUSET_TOP_5_COMMUNITIES =  get_top_5_communities(DBLP_CLAUSET_COMMUNITIES)
    EUCORE_CLAUSET_TOP_5_COMMUNITIES = get_top_5_communities(EUCORE_CLAUSET_COMMUNITIES)

    DBLP_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS = get_subragphs_from_communities(DBLP_GRAPH, DBLP_NEWMAN_TOP_5_COMMUNITIES)
    EUCORE_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS = get_subragphs_from_communities(EUCORE_GRAPH, EUCORE_NEWMAN_TOP_5_COMMUNITIES)
    DBLP_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS =  get_subragphs_from_communities(DBLP_GRAPH, DBLP_CLAUSET_TOP_5_COMMUNITIES)
    EUCORE_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS = get_subragphs_from_communities(EUCORE_GRAPH, EUCORE_CLAUSET_TOP_5_COMMUNITIES)


    print_top_5_communities_size(NEWMAN_METHOD_NAME, DBLP_DATASET_NAME, DBLP_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS)
    print_top_5_communities_size(NEWMAN_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS)
    print_top_5_communities_size(CLAUSET_METHOD_NAME, DBLP_DATASET_NAME, DBLP_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS)
    print_top_5_communities_size(CLAUSET_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS)

    print()

    ###################################################

    # Part E
    print("[e]")

    get_community_coverage(NEWMAN_METHOD_NAME, DBLP_DATASET_NAME, DBLP_GRAPH, DBLP_NEWMAN_TOP_5_COMMUNITIES)
    get_community_coverage(NEWMAN_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_GRAPH, EUCORE_NEWMAN_TOP_5_COMMUNITIES)
    get_community_coverage(CLAUSET_METHOD_NAME, DBLP_DATASET_NAME, DBLP_GRAPH, DBLP_CLAUSET_TOP_5_COMMUNITIES)
    get_community_coverage(CLAUSET_METHOD_NAME, EUCORE_DATASET_NAME, EUCORE_GRAPH, EUCORE_CLAUSET_TOP_5_COMMUNITIES)

    print()

    ###################################################

    # Part F
    print("[f]")




    print()


def check():
    DBLP_NEWMAN_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(NEWMAN_METHOD_NAME, DBLP_DATASET_NAME, DBLP_GROUND_TRUTH_COM_DATASET)

check()