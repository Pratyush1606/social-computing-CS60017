import os
import snap
from PIL import Image

from config import CONFIG

dataset = os.path.join(CONFIG["DATASET_DIR"], "Email-EuAll.txt")
plot_dir = CONFIG["PLOT_DIR"]

class Network:

    def __init__(self, dataset):
        # Loading original (without removing any node) undirected graph from the dataset text file
        self.graph = snap.LoadEdgeList(snap.PUNGraph, dataset, 0, 1)
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
        self.graph.PlotOutDegDistr(self.network_name, "{} - degree distribution".format(self.network_name))

        '''
        Here all the files will be generated in this directory only. So the files have to moved to "plots"
        directory. Also files will be having default snap generated name with png format, so that also needs to be changed to 
        "deg-dist.jpg"
        '''
        for file in os.listdir(os.getcwd()):
            if((file.endswith(".png") or file.endswith(".plt") or file.endswith(".tab")) and (self.network_name in file)):
                file_location = os.path.join(os.getcwd(), file)
                file_format = file[file.rfind(".")+1:]

                # If file format is png, then save a copy in jpg format in plots dir
                if(file_format=="png"):
                    file_format = "jpg"
                    img = Image.open(file_location).convert('RGB')
                    file_name = "deg-dist.{}".format(file_format)
                    new_file_location = os.path.join(plot_dir, file_name)
                    img.save(new_file_location)
                
                # remove the files from the current directory
                os.remove(file_location)
    
    def get_avg_clustering_coeff(self):
        '''
        Get the average Clustering Coefficient
        '''
        return self.graph.GetClustCf()
    
    def get_num_edge_bridegs(self):
        '''
        Get the number of edge bridges
        '''
        list_edge_bridges = self.graph.GetEdgeBridges()
        return len(list_edge_bridges)


if __name__ == "__main__":
    print("## Question 2")
    print()

    # Creating network from the dataset
    network = Network(dataset=dataset)

    # Saving the network name as "Email-EuAll"
    network.network_name = "Email-EuAll"

    print("A.")
    print("  (a) Number of nodes: {}".format(network.get_num_of_nodes()))
    print("  (b) Number of edges: {}".format(network.get_num_of_edges()))

    print("B.")
    print("  (a) Number of nodes with degree=4: {}".format(network.get_num_nodes_with_degree_equal_4()))
    print("  (b) Plotting the Degree distribution...")
    network.plot_degree_distribution()
    print("      Plotting Done.")
    
    print("D. Average Clustering Coefficient: {:.4f}".format(network.get_avg_clustering_coeff()))

    print("F. Number of edge bridges: {}".format(network.get_num_edge_bridegs()))
