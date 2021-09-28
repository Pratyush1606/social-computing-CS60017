import os
import snap
import sys
import matplotlib.pyplot as plt

from config import CONFIG

dataset = os.path.join(CONFIG["DATASET_DIR"], "email-Eu-core.txt")
plot_dir = CONFIG["PLOT_DIR"]
answer_loc = CONFIG["ANSWER_LOCATION"]

class Network:

    def __init__(self, dataset):
        # Loading original (without removing any node) directed graph from the dataset text file
        self.dataset = dataset
        self.graph = snap.LoadEdgeList(snap.PNGraph, dataset, 0, 1)
        
        # Getting an undirected version of the graph
        self.undirected_graph = snap.LoadEdgeList(snap.PUNGraph, dataset, 0, 1)
        self.network_name = ""
    
    def get_num_of_nodes(self):
        try:
            return self.graph.GetNodes()
        except Exception as e:
            print(e)

    def get_num_of_edges(self):
        try:
            return self.graph.GetEdges()
        except Exception as e:
            print(e)
    
    def get_num_nodes_with_degree_equal_4(self):
        '''
        Calculates the number of nodes which have degree = 4 in the network.

        '''
        num_nodes_with_deqree_4 = 0
        for node in self.graph.Nodes():
            if(node.GetDeg() == 4):
                num_nodes_with_deqree_4 += 1
        
        return num_nodes_with_deqree_4
    
    def get_num_weakly_connected_comps(self):
        '''
        Get the number of weakly connected components of the network'''
        list_weakly_connected_comps = self.graph.GetWccs()
        return len(list_weakly_connected_comps)

    def get_num_strongly_connected_comps(self):
        '''
        Get the number of strongly connected components of the network'''
        list_strongly_connected_comps = self.graph.GetSccs()
        return len(list_strongly_connected_comps)
    
    def plot_degree_distribution(self):
        '''
        Plot the degree distribution
        '''

        deg_dist = self.graph.GetDegCnt()
        x, y = [], []
        for elem in deg_dist:
            x.append(elem.GetVal1())
            y.append(elem.GetVal2())

        plt.plot(x, y)
        plt.xlabel("Degree")
        plt.ylabel("Frequency")
        plt.title("Degree distribution of {} network".format(self.network_name))
        fig_destination = os.path.join(plot_dir, "deg-dist.jpg")
        plt.savefig(fig_destination)
    
    def get_avg_clustering_coeff(self):
        '''
        Get the average Clustering Coefficient
        '''
        return self.graph.GetClustCf()
    
    def get_num_edge_bridges(self):
        '''
        Get the number of edge bridges
        '''
        
        '''
        An edge is a bridge if, when removed, increases the number of connected components. 
        Here only the strong edges are considered which when removed, increase the number of strongly connected components
        '''
        count = 0
        scc_count = self.get_num_strongly_connected_comps()
        for edge in self.graph.Edges():
            src, dest = edge.GetId()
            self.graph.DelEdge(src, dest)
            if(self.get_num_strongly_connected_comps() > scc_count):
                count += 1
            self.graph.AddEdge(src, dest)
        return count

    def get_num_triangles(self):
        '''
        Get the number of triangles
        '''

        '''
        Here the different directions are not being considered
        '''
        return self.graph.GetTriads()

    def get_num_rectangles(self):
        '''
        Get the number of rectangles
        '''

        '''
        Using the same concept of getting the number of triangles, this function is being implemented without considering the direction.

        '''
        # Making a copy of the graph
        graph_copy = snap.LoadEdgeList(snap.PNGraph, self.dataset, 0, 1)
        count_rectangles = 0
        tot_nodes = graph_copy.GetNodes()

        for node1_id in range(tot_nodes):
            for node2_id in range(node1_id+1, tot_nodes):

                # Getting the common neighbours of this diagonal containing nodes (node1, node2)
                numNbrs = graph_copy.GetCmnNbrs(node1_id, node2_id)

                # Counting all the rectangles being formed from all the other diagonal pairs
                count_rectangles += (numNbrs*(numNbrs-1))//2

            # Since node1 has been visited, so it has to be removed from the
            # graph otherwise, it will be recounted in any other rectangle
            graph_copy.DelNode(node1_id)

        return count_rectangles

    def get_largest_wcc(self):
        '''
        Get a graph representing the largest weakly connected component in the original graph
        '''
        return self.graph.GetMxWcc()
    
    def get_largest_scc(self):
        '''
        Get a graph representing the largest strongly connected component in the original graph
        '''
        return self.graph.GetMxScc()
    
    def print_graph_info(self):
        self.graph.PrintInfo("Python type TUNGraph", "q2-graph-info.txt", False)        


class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
    def flush(self):
        pass

if __name__ == "__main__":
    # Configuring script to print to stdout as well as answers.txt
    f = open(answer_loc, 'a')
    backup = sys.stdout
    sys.stdout = Tee(sys.stdout, f)

    print()
    print("Question 2")
    print("-----------")
    print()

    # Creating network from the dataset
    network = Network(dataset=dataset)

    # Saving the network name as "email-Eu-core"
    network.network_name = "email-Eu-core"

    print("A.")
    print("  (a) Number of nodes: {}".format(network.get_num_of_nodes()))
    print("  (b) Number of edges: {}".format(network.get_num_of_edges()))

    print("B.")
    print("  (a) Number of nodes with degree=4: {}".format(network.get_num_nodes_with_degree_equal_4()))
    print("  (b) Plotting the Degree distribution...")
    network.plot_degree_distribution()
    print("      Plotting Done.")

    # Get the Largest WCC and SCC
    wcc = network.get_largest_wcc()
    scc = network.get_largest_scc()
    print("C.")
    print("  (a) Number of nodes in largest weakly connected component (WCC): {}".format(wcc.GetNodes()))
    print("      Number of edges in largest weakly connected component (WCC): {}".format(wcc.GetEdges()))
    print("  (b) Number of nodes in largest strongly connected component (SCC): {}".format(scc.GetNodes()))
    print("      Number of edges in largest strongly connected component (SCC): {}".format(scc.GetEdges()))
    
    print("D. Average Clustering Coefficient: {:.4f}".format(network.get_avg_clustering_coeff()))

    print("E. Number of triangles: {}".format(network.get_num_triangles()))
    print("   Number of rectangles: {}".format(network.get_num_rectangles()))

    print("F. Number of edge bridges: {}".format(network.get_num_edge_bridges()))
    
    print()
    print("#################")