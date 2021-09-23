import os
import sys
import snap

from config import CONFIG

dataset = os.path.join(CONFIG["DATASET_DIR"], "facebook_combined.txt")
plot_dir = CONFIG["PLOT_DIR"]
answer_loc = CONFIG["ANSWER_LOCATION"]

class Network:

    def __init__(self, dataset):
        # Loading original (without removing any node) undirected graph from the facebook dataset text file
        self.dataset = dataset
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
        
    def get_network_without_nodeids_divisible_by_3(self):
        # Making new graph after removing the specified nodes
        new_graph = snap.PUNGraph.New()

        # Adding all the nodes whose ids are not divisible by 3
        for node in self.graph.Nodes():
            node_id = node.GetId()
            if(node_id%3 != 0):
                # If the node is not already added to the graph
                if(not new_graph.IsNode(node_id)):
                    new_graph.AddNode(node_id)

        # Adding the corresponding edges in the new graph
        for edge in self.graph.Edges():
            source_node_id, dest_node_id = edge.GetId()

            # Checking if any node id is divisible by 3 or not
            if(source_node_id%3==0 or dest_node_id%3==0):
                continue

            # If the source node is not already added to the graph
            if(not new_graph.IsNode(source_node_id)):
                new_graph.AddNode(source_node_id)
            
            # If the dest node is not already added to the graph
            if(not new_graph.IsNode(dest_node_id)):
                new_graph.AddNode(dest_node_id)
            
            # Adding the edge
            new_graph.AddEdge(source_node_id, dest_node_id)
        
        return new_graph
    
    def get_nodes_with_highest_degree(self):
        '''
        Calculates the number of nodes with the highest degree and also get the node IDs with the highest degree in the network.

        Return:
        (num_nodes_with_highest_degree, list_of_nodeids_with_highest_deg)

        '''
        highest_deg = 0
        for node in self.graph.Nodes():
            highest_deg = max(highest_deg, node.GetDeg())
        
        num_nodes_with_highest_degree = 0
        list_of_nodeids_with_highest_deg = []
        for node in self.graph.Nodes():
            if(node.GetDeg() == highest_deg):
                num_nodes_with_highest_degree += 1
                list_of_nodeids_with_highest_deg.append(node.GetId())
        
        return (num_nodes_with_highest_degree, list_of_nodeids_with_highest_deg)
    
    def plot_shortest_path_distribution(self):
        '''
        Plot the distribution of the shortest path lengths in the network
        '''
        self.graph.PlotShortPathDistr(self.network_name, "{} - shortest path distribution".format(self.network_name))

        '''
        Here all the files will be generated in this directory only. So the files have to moved to "plots"
        directory. Also files will be having default snap generated name, so that also needs to be changed to 
        “shortest_path_<network_name>.png”
        '''
        for file in os.listdir(os.getcwd()):
            if((file.endswith(".png") or file.endswith(".plt") or file.endswith(".tab")) and (self.network_name in file)):
                file_location = os.path.join(os.getcwd(), file)
                file_format = file[file.rfind(".")+1:]

                # Only saving .png files and removing others
                if(file_format!="png"):
                    os.remove(file_location)
                    continue
                
                file_name = "shortest_path_{}.{}".format(self.network_name, file_format)
                new_file_location = os.path.join(plot_dir, file_name)
                os.replace(file_location, new_file_location)
    
    def get_num_articulation_points(self):
        '''
        Get the number of articulation points in the network'''
        list_articulation_points = self.graph.GetArtPoints()
        return len(list_articulation_points)
    
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
    
    def plot_connected_components_distribution(self):
        '''
        Plot the distribution of sizes of connected components in the network
        '''
        self.graph.PlotSccDistr(self.network_name, "{} - connected component distribution".format(self.network_name))

        '''
        Here all the files will be generated in this directory only. So the files have to moved to "plots"
        directory. Also files will be having default snap generated name, so that also needs to be changed to 
        “connected_comp_<network_name>.png”
        '''
        for file in os.listdir(os.getcwd()):
            if((file.endswith(".png") or file.endswith(".plt") or file.endswith(".tab")) and (self.network_name in file)):
                file_location = os.path.join(os.getcwd(), file)
                file_format = file[file.rfind(".")+1:]

                # Only saving .png files and removing others
                if(file_format!="png"):
                    os.remove(file_location)
                    continue

                file_name = "connected_comp_{}.{}".format(self.network_name, file_format)
                new_file_location = os.path.join(plot_dir, file_name)
                os.replace(file_location, new_file_location)
    
    def get_diameter(self, num_test_nodes=100):
        '''
        Get the diameter of the longest connected component
        '''
        return self.graph.GetBfsFullDiam(num_test_nodes)

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
    print("Question 1")
    print("-----------")
    print()

    # Part A
    print("A. Structure of the network")

    # Creating network from the dataset
    network = Network(dataset=dataset)

    # Saving the network name as "facebook"
    network.network_name = "facebook"

    print("1. Number of nodes present in the network: {}".format(network.get_num_of_nodes()))

    # Getting new network with all nodes with ids divisible by 3 removed
    new_network = network.get_network_without_nodeids_divisible_by_3()
    print("2. Number of nodes present in the new network after removing specified nodes: {}".format(new_network.GetNodes()))

    print("3. Number of edges present in the network: {}".format(network.get_num_of_edges()))

    print("4. Number of edges present in the new network after removing specified nodes: {}".format(new_network.GetEdges()))

    num_nodes_with_highest_degree, list_of_nodeids_with_highest_deg = network.get_nodes_with_highest_degree()
    print("5. Number of nodes with the highest degree in the network: {}".format(num_nodes_with_highest_degree))
    print("   The node IDs with the highest degree in the network is/are:", end=" ")
    print(*list_of_nodeids_with_highest_deg)

    print("6. Plotting the distribution of shortest path lengths...")
    network.plot_shortest_path_distribution()
    print("   Plotting Done.")

    print()

    # Part B
    print("B. Components of the network")

    print("1. The fraction of nodes in the largest connected component of the network: {:.4f}".format(network.graph.GetMxSccSz()))

    print("2. The number of articulation points in the network: {}".format(network.get_num_articulation_points()))

    print("3. The number of strongly connected components (SCC) in the network: {}".format(network.get_num_strongly_connected_comps()))
    print("   The number of weakly connected components (WCC) in the network: {}".format(network.get_num_weakly_connected_comps()))

    print("4. Plotting the distribution of sizes of connected components...")
    network.plot_connected_components_distribution()
    print("   Plotting Done.")

    print("5. The approximated diameter of the largest connected component of the network taking {} test nodes: {}".format(10, network.get_diameter(10)))
    print("   The approximated diameter of the largest connected component of the network taking {} test nodes: {}".format(100, network.get_diameter(100)))
    print("   The approximated diameter of the largest connected component of the network taking {} test nodes: {}".format(1000, network.get_diameter(1000)))
    
    print()
    print("#################")