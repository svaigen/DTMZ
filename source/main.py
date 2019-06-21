import networkx as nx
import graphOperations as graphOp
import flowAnalysis as flow
import pandas as pd
import dtmzUtils as utils

n_regions = 32
n_mixzones = 8
nodes_file = "./../data/nodesByRegion.csv" 
edges_file = "./../data/edges2.csv"
G = graphOp.buildGraphFromCSV(nodes_file, edges_file)

selected_mixzones = graphOp.selectMixZonesByEngenvectorAndRegion(n_mixzones,G)
df = pd.read_csv(nodes_file,delimiter=',')
df = df[df['node_id'].isin(selected_mixzones)]
utils.visualizeMapBySpecificSet(df,"./../data/sf.geojson")

# df = pd.read_csv(nodes_file,delimiter=',')
# df = df[df['node_id'].isin(list(nx.articulation_points(G)))]
# utils.visualizeMapBySpecificSet(df,"./../data/sf.geojson")

# graphOp.clusterizingNodes(G,n_regions,"./../data/nodesByRegion.csv")
# utils.visualizeMapByRegion(pd.read_csv(nodes_file, delimiter=","), n_regions, "./../data/sf.geojson")