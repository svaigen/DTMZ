import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans

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

def clusterizingNodes(G, nclusters,file_path):
    coordinates = []
    for node in G.nodes():
        coordinates.append([G.node[node]['latitude'],G.node[node]['longitude']])
    coordinates = np.asarray(coordinates)
    kmeans = KMeans(n_clusters=nclusters, max_iter=500, precompute_distances='auto', random_state=1, n_jobs=-1).fit(coordinates)    
    f = open(file_path,'w')
    f.write("node_id,latitude,longitude,region\n")
    index = 0
    for node in G.nodes():
        f.write("{},{},{},{}\n".format(node, G.node[node]['latitude'], G.node[node]['longitude'], kmeans.labels_.item(index)))
        index += 1
    f.close()
    return None

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

def buildMapPoints(nodes):
    points = pd.DataFrame()
    points['geometry'] = nodes.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
    geo_points = gpd.GeoDataFrame(points, geometry='geometry')
    geo_points.crs = {'init':'epsg:3395'}
    return geo_points

def buildMapRegion(region_file):
    region = gpd.read_file(region_file)
    region.crs = {'init': 'epsg:3395'}
    region = region.rename(columns={'geometry': 'geometry'}).set_geometry('geometry')
    return region

def visualizeMap(nodes_df, nregions, region_file):
    points_list = []
    for i in range(nregions):
         #SG = G.subgraph([n for n, attrdict in G.node.items() if attrdict['region'] == i])
        nodes = nodes_df[nodes_df['region'] == i]
        points_list.append(buildMapPoints(nodes))
    region = buildMapRegion(region_file)
    fig, ax = plt.subplots(1, subplot_kw=dict(alpha=0.3))
    map = region.plot(ax=ax, color='gray')
    i = 0
    colors=['black','yellow','red','white','orange','blue','purple','pink','brown','green']
    for points in points_list:
        points.plot(ax=map, marker="o", markersize=5, alpha=0.5, color=colors[i])
        i += 1
    ax.set_title("Map visualization")
    plt.show()
    return None