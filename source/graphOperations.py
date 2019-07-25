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
import os
from haversine import haversine

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

def selectMixZonesByMetricAndRegion(n_mixzones,G,k_anonymity, radius_mixzone,metric):
    regions_placement = {}
    selected_mixzones = []
    number_of_mixzones_placed = 0
    if metric == utils.EIGENVECTOR_METRIC:
        centrality = nx.eigenvector_centrality(G,max_iter=1000)
        nodes_ordered = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
        for node, center_value in nodes_ordered:
            if not (G.node[node]["region"] in regions_placement.keys()):
                regions_placement[G.node[node]["region"]] = 1
                selected_mixzones.append(node)
                number_of_mixzones_placed += 1
            if number_of_mixzones_placed == n_mixzones:
                return utils.generateMixZonesObjects(selected_mixzones,G,k_anonymity, radius_mixzone)
    else:
        nodes_ordered = nx.voterank(G,max_iter=1000)
        for node in nodes_ordered:
            if not (G.node[node]["region"] in regions_placement.keys()):
                regions_placement[G.node[node]["region"]] = 1
                selected_mixzones.append(node)
                number_of_mixzones_placed += 1
            if number_of_mixzones_placed == n_mixzones:
                return utils.generateMixZonesObjects(selected_mixzones,G,k_anonymity, radius_mixzone)

def calculateMixZonesByFlow(days, time_intervals, n_regions, n_mixzones, k_anonymity, flow_window, region_flow_path, G, kmeans, mixzones_path, metric):
    # total_intervals = len(time_intervals) * len(days)
    total_intervals = len(days)
    regions_flow_history = [None] * n_regions
    for csv in os.listdir(region_flow_path):
        regions_flow_history[int(csv.split("region-")[1].split(".")[0])] = pd.read_csv("{}{}".format(region_flow_path,csv),delimiter=',')           
    regions_flow_arrays = generateFlowAsArray(regions_flow_history, days, time_intervals)
    regions_ewma = []
    for region_flow in regions_flow_arrays:
        regions_ewma.append(utils.calculateEWMA(region_flow,len(region_flow)))
    ewma_matrix = regions_ewma[0]
    for i in range(1,len(regions_ewma)):
        ewma_matrix = np.vstack((ewma_matrix, regions_ewma[i]))
    sum_ewma = np.sum(ewma_matrix,axis=0)
    mixzones_demand = []
    for i in range(total_intervals):
        mixzones_demand.append(calculateRegionsAndNumberOfMixZonesByFlowRate(ewma_matrix[:,i],sum_ewma[i], n_mixzones, n_regions))
    regions_ordered_nodes = getOrderedNodesByMetric(G,n_regions,metric)
    fmz = open(mixzones_path,'w')
    for demand in mixzones_demand:
        line = ""
        for key in demand:
            number_of_mixzones = demand[key]
            line += getMixZonesByDemand(number_of_mixzones,regions_ordered_nodes[key],G)
        fmz.write(line[:-1])
        fmz.write("\n")
    fmz.close()
    return None

def getMixZonesByDemand(number_of_mixzones, nodes_ordered, G):
    distance_min = 1000
    remaining_mixzones = number_of_mixzones
    places = []
    for node in nodes_ordered:
        if remaining_mixzones == number_of_mixzones:
            places.append(node)
            remaining_mixzones -= 1
        else:
            distance_ok = True
            for place in places:
                distance = haversine((G.node[place]['latitude'],G.node[place]['longitude']),(G.node[node]['latitude'],G.node[node]['longitude'])) * 1000
                if(distance < distance_min):
                    distance_ok = False
            if distance_ok:
                places.append(node)
                remaining_mixzones -= 1
        if remaining_mixzones == 0:
            break;
    response = ""
    for place in places:
        response = response + "{},".format(place)
    return response

def getOrderedNodesByMetric(G, n_regions,metric):
    regions_ordered_nodes = [None] * n_regions
    if metric == utils.EIGENVECTOR_METRIC:
        centrality = nx.eigenvector_centrality(G,max_iter=1000)
        nodes_ordered = sorted(centrality.items(), key = operator.itemgetter(1), reverse = True)
        for node, c in nodes_ordered:
            if regions_ordered_nodes[int(G.node[node]['region'])] is None:
                regions_ordered_nodes[int(G.node[node]['region'])] = [node]
            else:
                regions_ordered_nodes[int(G.node[node]['region'])].append(node)
    else:
        nodes_ordered = nx.voterank(G,max_iter=1000)
        for node in nodes_ordered:
            if regions_ordered_nodes[int(G.node[node]['region'])] is None:
                regions_ordered_nodes[int(G.node[node]['region'])] = [node]
            else:
                regions_ordered_nodes[int(G.node[node]['region'])].append(node)
    return regions_ordered_nodes

def calculateRegionsAndNumberOfMixZonesByFlowRate(ewma_values, ewma_sum, n_mixzones, n_regions):
    limiar = n_mixzones / n_regions
    regions_rate = {}
    for i in range(len(ewma_values)):
        regions_rate[i] = ewma_values[i] / ewma_sum
    rates_ordered = sorted(regions_rate.items(), key = operator.itemgetter(1), reverse = True)
    mixzones_remaining = n_mixzones
    regions_mixzones = {}
    for rateID in rates_ordered:
        if mixzones_remaining == 0:
            return regions_mixzones
        attributed_mixzones = (rateID[1] // limiar) + 1
        if attributed_mixzones < mixzones_remaining:
            regions_mixzones[rateID[0]] = attributed_mixzones
            mixzones_remaining -= attributed_mixzones
        else:
            regions_mixzones[rateID[0]] = mixzones_remaining
            mixzones_remaining = 0
    print(regions_mixzones)
    return regions_mixzones

def generateFlowAsArray(regions_flow_history, days, time_intervals):
    regions_flows =[None] * len(regions_flow_history)
    counter = 0
    for region in regions_flow_history:
        flows = []
        for day in days:
            sum = 0 
            for interval in time_intervals:
                sum+= region.ix[utils.getIndexDay(day),interval]
                # flows.append(region.ix[utils.getIndexDay(day),interval])
            flows.append(sum)                
        regions_flows[counter] = flows
        counter += 1
    return regions_flows