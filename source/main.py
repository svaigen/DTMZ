import networkx as nx
import graphOperations as graphOp
import flowAnalysis as flow
import pandas as pd

nregions = 10
nodes_file = "./../data/nodesByRegion.csv" 
edges_file = "./../data/edges2.csv"
G = graphOp.buildGraphFromCSV(nodes_file, edges_file)
for c in nx.connected_components(G):
    print(len(c))
# graphOp.visualizeMap(pd.read_csv(nodes_file, delimiter=","), nregions, "./../data/sf.geojson")