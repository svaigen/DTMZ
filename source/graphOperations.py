import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans
import dtmzUtils as utils
import copy
import operator

def buildGraphFromCSV(nodes_file, edges_file):
    nodes = pd.read_csv(nodes_file, delimiter=",")
    edges = pd.read_csv(edges_file, engine="python", usecols=["edge_id","source","target"])
    G = nx.empty_graph(0)
    G = buildNodesAndEdges(G, nodes, edges)
    nx.set_node_attributes(G, buildNodeAttributeDict(nodes,"node_id","latitude") , "latitude")
    nx.set_node_attributes(G, buildNodeAttributeDict(nodes,"node_id","longitude") , "longitude")
    nx.set_node_attributes(G, buildNodeAttributeDict(nodes,"node_id","region") , "region")
    print("Graph info:")
    print("Number of nodes: {}".format(len(G.nodes)))
    print("Number of edges: {}".format(len(G.edges)))  
    return G

def buildNodeAttributeDict(nodes,id,attr):
    attr_dict = {}
    for indices, row in nodes.iterrows():
        attr_dict[row[id]] = row[attr]
    return attr_dict


def buildNodesAndEdges(G, nodes, edges):    
    for i, n in nodes.iterrows():
        G.add_node(n["node_id"])
    counter = 0
    f = open('./../data/ignored_edges.csv','w')
    f.write("edge_id,source,target\n")
    for i, e in edges.iterrows():
        if (G.has_node(e["source"]) and G.has_node(e["target"])):
            G.add_edge(e["source"], e["target"])            
        else:
            f.write("{},{},{}\n".format(e["edge_id"],e["source"],e["target"]))
            counter = counter + 1            
    f.close()    
    return G

def clusterizingNodes(G, nclusters):
    coordinates = []
    for node in G.nodes():
        coordinates.append([G.node[node]['latitude'],G.node[node]['longitude']])
    coordinates = np.asarray(coordinates)
    kmeans = KMeans(n_clusters=nclusters, max_iter=500, precompute_distances='auto', random_state=1, n_jobs=-1).fit(coordinates)        
    return kmeans

def saveClusters(G, kmeans, file_path):
    f = open(file_path,'w')
    f.write("node_id,latitude,longitude,region\n")
    index = 0
    for node in G.nodes():
        f.write("{},{},{},{}\n".format(node, G.node[node]['latitude'], G.node[node]['longitude'], kmeans.labels_.item(index)))
        index += 1
    f.close()
def showGraph(G):
    print("building a visual representation of G")
    nx.draw_networkx(G,pos=nx.circular_layout(G))
    plt.draw()
    plt.show()
    return None

def saveNodesDegrees(G,pathFile):
    f = open (pathFile,'w')
    f.write("node,degree\n")
    for node in G.nodes:
        f.write("{},{}\n".format(node,G.degree[node]))        
    f.close()
    return None

def removingNodesDegreeZeroFromFile(nodes_file, G):
    nodes_df = pd.read_csv(nodes_file, delimiter=",")
    nodes_df = nodes_df.set_index("node_id")
    for node in G.nodes:
        if (G.degree[node] == 0):
            nodes_df = nodes_df.drop(node,axis=0)
            print("Node removed: {}".format(node))
    nodes_df.to_csv(nodes_file)
    return None

def saveArticulationNodesInfo(G,output_file):
    f = open(output_file,'w')
    f.write("node_id,number_of_components,length_of_components\n")
    print("Processing Articulations...")
    total_artic = len(list(nx.articulation_points(G)))
    i = 1
    for articulation in nx.articulation_points(G):
        print("{}/{}".format(i,total_artic))
        i+=1   
        GA = copy.deepcopy(G)
        GA.remove_node(articulation)
        f.write("{},{},(".format(articulation, len(list(nx.connected_components(GA)))))
        for component in nx.connected_components(GA):
            f.write("{}-".format(len(component)))
        f.write(")\n")
    f.close()
    return None

def selectMixZonesByEngenvectorAndRegion(n_mixzones,G,k_anonymity):
    centrality = nx.eigenvector_centrality(G,max_iter=1000)
    nodes_ordered = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
    regions_placement = {}
    selected_mixzones = []
    number_of_mixzones_placed = 0
    for node, center_value in nodes_ordered:
        if not (G.node[node]["region"] in regions_placement.keys()):
            regions_placement[G.node[node]["region"]] = 1
            selected_mixzones.append(node)
            number_of_mixzones_placed += 1
        if number_of_mixzones_placed == n_mixzones:
            return utils.generateMixZonesObjects(selected_mixzones,G,k_anonymity)
