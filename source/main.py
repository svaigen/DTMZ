import networkx as nx
import graphOperations as graphOp
import flowAnalysis as flow
import pandas as pd
import dtmzUtils as utils
import simulation as sim

n_regions = 32
n_mixzones = 8
k_anonymity = 2
nodes_file = "./../data/nodesByRegion.csv" 
edges_file = "./../data/edges2.csv"
log_file = "./log.txt"
G = graphOp.buildGraphFromCSV(nodes_file, edges_file)

mixzones = graphOp.selectMixZonesByEngenvectorAndRegion(n_mixzones,G,k_anonymity)
mobile_entities = utils.generateMobileEntitiesByFolder("./../data/tripsPerDay/2008-05-17/")
sim.simulation(mixzones,mobile_entities,log_file)

# df = pd.read_csv(nodes_file,delimiter=',')
# df = df[df['node_id'].isin(list(nx.articulation_points(G)))]
# utils.visualizeMapBySpecificSet(df,"./../data/sf.geojson")

# graphOp.clusterizingNodes(G,n_regions,"./../data/nodesByRegion.csv")
# utils.visualizeMapByRegion(pd.read_csv(nodes_file, delimiter=","), n_regions, "./../data/sf.geojson")