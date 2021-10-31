import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from networkx.algorithms import community
from collections import defaultdict
import os

# Configuring file locations of datasets, plots and output files
from config import CONFIG

# Datasets
FOOTBALL_DATASET = os.path.join(CONFIG["DATASET_DIR"], "football.gml")
POLBOOKS_DATASET = os.path.join(CONFIG["DATASET_DIR"], "polbooks.gml")

FOOTBALL_TRUE_COMMS_NUM = 12
POLBOOKS_TRUE_COMMS_NUM = 3

FOOTBALL_GROUND_TRUTH_COM_DATASET = os.path.join(CONFIG["DATASET_DIR"], "com-FOOTBALL.all.cmty.txt")
POLBOOKS_GROUND_TRUTH_COM_DATASET = os.path.join(CONFIG["DATASET_DIR"], "email-Eu-core-department-labels.txt")

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
FOOTBALL_DATASET_NAME = "FOOTBALL"
POLBOOKS_DATASET_NAME = "POLBOOKS"

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

def get_num_of_communities(methodname, datasetname, graph, true_comms_num=None):
    '''
    Calculates the number of communities generated

    Also returns the list of communities
    '''
    print("Dataset: {}".format(datasetname))

    if(methodname == NEWMAN_METHOD_NAME):
        communities = list(list(community.girvan_newman(graph))[true_comms_num-2])
        num_communities = len(communities)
        print("Number of communities using Newman-Girvan method: {}".format(num_communities))
        
    elif(methodname == CLAUSET_METHOD_NAME):
        communities = list(community.greedy_modularity_communities(graph))
        num_communities = len(communities)
        print("Number of communities using Clauset-Newman-Moore greedy modularity maximization method: {}".format(num_communities))
    
    print()
    return communities

###################################################

def plot_community_size_distribution(methodname, datasetname, communities):
    '''
    Plots the community size distribution for diff datasets and methods

    communities: List of communities
    '''
    print("Plotting Community Size distribution of {} graph using {} method".format(datasetname, methodname))
    points = []
    for c in communities:
        points.append(len(c))
    plt.hist(points, rwidth=0.2)
    plt.xlabel("Size of Communities")
    plt.ylabel("Frequency")
    plt.title("Community Size distribution of {} graph using {} method".format(datasetname, methodname))
    fig_destination = os.path.join(PLOT_DIR, f"{datasetname}_{methodname}_dist.png")
    plt.savefig(fig_destination)
    plt.close()
    print("Plotting Done")
    print()

###################################################

def plot_ground_truth_community_size_distribution(methodname, datasetname, graph):
    '''
    Plot the ground truth community size distribution
    
    Here the nodes with same `value` are being considered in the same true community.
    '''
    # Making the ground truth community
    communities = defaultdict(list)
    for node, value in list(graph.nodes(data="value")):
        communities[value].append(node)
    ground_truth_communities = list(communities.values())
    
    # Plotting the histogram
    plt.title("Plotting Ground Truth Community Size distribution of {} using {} method".format(datasetname, methodname))
    points = []
    for c in ground_truth_communities:
        points.append(len(c))
    plt.hist(points, rwidth=0.2)
    plt.xlabel("Size of Ground Truth Communities")
    plt.ylabel("Frequency")
    plt.title("Ground Truth Community Size distribution of {} using {} method".format(datasetname, methodname))
    fig_destination = os.path.join(PLOT_DIR, f"ground_truth_communities_dist_{datasetname}_{methodname}.png")
    plt.savefig(fig_destination)
    plt.close()
    print("Plotting Done")
    print()
    return ground_truth_communities
    
###################################################

def get_top_5_communities(communities):
    '''
    Get the top 5 communities based on the number of nodes from a list of communities'''
    return sorted(communities, key=lambda com: len(com), reverse=True)[:5]

###################################################

def get_top_communtiy(communities):
    '''
    Get the top community based on the number of nodes from a list of communities'''
    return sorted(communities, key=lambda com: len(com), reverse=True)[0]

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
    print()

###################################################

def get_community_coverage(graph, community):
    '''
    Get the coverage of a communtiy
    '''
    # Making a set of community nodes
    if(not isinstance(community, set)):
        community = set(community)
    
    intra_community_edges = 0
    # Iterating over the links to count intra community edges
    for e in graph.edges():
        if((e[0] in community) and (e[1] in community)):
            intra_community_edges += 1
    coverage = intra_community_edges / len(graph.edges)
    return coverage

###################################################

def get_top_5_community_coverage(methodname, datasetname, graph, communities):
    '''
    Get the coverage of the top 5 communities
    '''
    print("Method: {}".format(methodname))
    print("Dataset: {}".format(datasetname))
    for i in range(len(communities)):
        coverage = get_community_coverage(graph, communities[i])
        print("Coverage of community {} = {}".format(i+1, coverage))
    print()

###################################################

def get_jaccard_coefficient(methodname, datasetname, community1, community2):
    '''
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.jaccard_coefficient.html#networkx.algorithms.link_prediction.jaccard_coefficient

    https://stackoverflow.com/questions/50704439/python-jaccard-similartity-between-two-networks
    '''
    print("Method: {}".format(methodname))
    print("Dataset: {}".format(datasetname))
    union_size = len(set(community1) | set(community2))
    intersection_size = len(set(community1) & set(community2))
    coeff = 0
    if(union_size != 0):
        coeff = intersection_size / union_size
    print("jaccard coefficient = {}".format(coeff))
    print()

###################################################
print()
print("Question 1")
print("-----------")
print()

# Reading graphs
FOOTBALL_GRAPH = nx.read_gml(FOOTBALL_DATASET)
POLBOOKS_GRAPH = nx.read_gml(POLBOOKS_DATASET)

def run():
    ###################################################

    # Part A
    print("[a]")
    FOOTBALL_NEWMAN_COMMUNITIES = get_num_of_communities(NEWMAN_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_GRAPH, FOOTBALL_TRUE_COMMS_NUM)
    POLBOOKS_NEWMAN_COMMUNITIES = get_num_of_communities(NEWMAN_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_GRAPH, POLBOOKS_TRUE_COMMS_NUM)
    FOOTBALL_CLAUSET_COMMUNITIES = get_num_of_communities(CLAUSET_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_GRAPH)
    POLBOOKS_CLAUSET_COMMUNITIES = get_num_of_communities(CLAUSET_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_GRAPH)

    ###################################################

    # Part B
    print("[b]")
    plot_community_size_distribution(NEWMAN_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_NEWMAN_COMMUNITIES)
    plot_community_size_distribution(NEWMAN_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_NEWMAN_COMMUNITIES)
    plot_community_size_distribution(CLAUSET_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_CLAUSET_COMMUNITIES)
    plot_community_size_distribution(CLAUSET_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_CLAUSET_COMMUNITIES)

    ###################################################

    # Part C
    print("[c]")
    FOOTBALL_NEWMAN_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(NEWMAN_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_GRAPH)
    POLBOOKS_NEWMAN_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(NEWMAN_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_GRAPH)
    FOOTBALL_CLAUSET_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(CLAUSET_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_GRAPH)
    POLBOOKS_CLAUSET_GROUND_TRUTH_COMMUNITIES = plot_ground_truth_community_size_distribution(CLAUSET_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_GRAPH)

    ###################################################

    # Part D
    print("[d]")
    FOOTBALL_NEWMAN_TOP_5_COMMUNITIES = get_top_5_communities(FOOTBALL_NEWMAN_COMMUNITIES)
    POLBOOKS_NEWMAN_TOP_5_COMMUNITIES = get_top_5_communities(POLBOOKS_NEWMAN_COMMUNITIES)
    FOOTBALL_CLAUSET_TOP_5_COMMUNITIES =  get_top_5_communities(FOOTBALL_CLAUSET_COMMUNITIES)
    POLBOOKS_CLAUSET_TOP_5_COMMUNITIES = get_top_5_communities(POLBOOKS_CLAUSET_COMMUNITIES)

    FOOTBALL_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS = get_subragphs_from_communities(FOOTBALL_GRAPH, FOOTBALL_NEWMAN_TOP_5_COMMUNITIES)
    POLBOOKS_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS = get_subragphs_from_communities(POLBOOKS_GRAPH, POLBOOKS_NEWMAN_TOP_5_COMMUNITIES)
    FOOTBALL_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS =  get_subragphs_from_communities(FOOTBALL_GRAPH, FOOTBALL_CLAUSET_TOP_5_COMMUNITIES)
    POLBOOKS_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS = get_subragphs_from_communities(POLBOOKS_GRAPH, POLBOOKS_CLAUSET_TOP_5_COMMUNITIES)

    print_top_5_communities_size(NEWMAN_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS)
    print_top_5_communities_size(NEWMAN_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_NEWMAN_TOP_5_COMMUNITIES_SUBGRAPHS)
    print_top_5_communities_size(CLAUSET_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS)
    print_top_5_communities_size(CLAUSET_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_CLAUSET_TOP_5_COMMUNITIES_SUBGRAPHS)

    ###################################################

    # Part E
    print("[e]")
    get_top_5_community_coverage(NEWMAN_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_GRAPH, FOOTBALL_NEWMAN_TOP_5_COMMUNITIES)
    get_top_5_community_coverage(NEWMAN_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_GRAPH, POLBOOKS_NEWMAN_TOP_5_COMMUNITIES)
    get_top_5_community_coverage(CLAUSET_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_GRAPH, FOOTBALL_CLAUSET_TOP_5_COMMUNITIES)
    get_top_5_community_coverage(CLAUSET_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_GRAPH, POLBOOKS_CLAUSET_TOP_5_COMMUNITIES)

    ###################################################

    # Part F
    print("[f]")
    FOOTBALL_NEWMAN_TOP_COMMUNITY = FOOTBALL_NEWMAN_TOP_5_COMMUNITIES[0]
    POLBOOKS_NEWMAN_TOP_COMMUNITY = POLBOOKS_NEWMAN_TOP_5_COMMUNITIES[0]
    FOOTBALL_CLAUSET_TOP_COMMUNITY = FOOTBALL_CLAUSET_TOP_5_COMMUNITIES[0]
    POLBOOKS_CLAUSET_TOP_COMMUNITY = POLBOOKS_CLAUSET_TOP_5_COMMUNITIES[0]

    FOOTBALL_NEWMAN_GROUND_TRUTH_TOP_COMMUNITY = get_top_communtiy(FOOTBALL_NEWMAN_GROUND_TRUTH_COMMUNITIES)
    POLBOOKS_NEWMAN_GROUND_TRUTH_TOP_COMMUNITY = get_top_communtiy(POLBOOKS_NEWMAN_GROUND_TRUTH_COMMUNITIES)
    FOOTBALL_CLAUSET_GROUND_TRUTH_TOP_COMMUNITY = get_top_communtiy(FOOTBALL_CLAUSET_GROUND_TRUTH_COMMUNITIES)
    POLBOOKS_CLAUSET_GROUND_TRUTH_TOP_COMMUNITY = get_top_communtiy(POLBOOKS_CLAUSET_GROUND_TRUTH_COMMUNITIES)

    get_jaccard_coefficient(NEWMAN_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_NEWMAN_TOP_COMMUNITY, FOOTBALL_NEWMAN_GROUND_TRUTH_TOP_COMMUNITY)
    get_jaccard_coefficient(NEWMAN_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_NEWMAN_TOP_COMMUNITY, POLBOOKS_NEWMAN_GROUND_TRUTH_TOP_COMMUNITY)
    get_jaccard_coefficient(CLAUSET_METHOD_NAME, FOOTBALL_DATASET_NAME, FOOTBALL_CLAUSET_TOP_COMMUNITY, FOOTBALL_CLAUSET_GROUND_TRUTH_TOP_COMMUNITY)
    get_jaccard_coefficient(CLAUSET_METHOD_NAME, POLBOOKS_DATASET_NAME, POLBOOKS_CLAUSET_TOP_COMMUNITY, POLBOOKS_CLAUSET_GROUND_TRUTH_TOP_COMMUNITY)

run()