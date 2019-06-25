import networkx as nx
import graphOperations as graphOp
import flowAnalysis as flow
import pandas as pd
import dtmzUtils as utils
import simulation as sim
import datetime as dt
import numpy as np

days = ['2008-05-17','2008-05-18','2008-05-19','2008-05-20','2008-05-21','2008-05-22','2008-05-23','2008-05-24','2008-05-25','2008-05-26','2008-05-27','2008-05-28','2008-05-29','2008-05-30','2008-05-31','2008-06-01','2008-06-02','2008-06-03','2008-06-04','2008-06-05','2008-06-06','2008-06-07','2008-06-08','2008-06-09']
time_intervals = ['05:59:59','10:59:59','16:59:59','23:59:59']

n_regions = 128
n_mixzones = 8
k_anonymity = 2
flow_window = 50
nodes_file = "./../data/nodesByRegion.csv" 
edges_file = "./../data/edges2.csv"
log_file = "./log.txt"
region_flow_path = "./../flow/"
mixzones_path = "./../data/mixzones.csv"
G = graphOp.buildGraphFromCSV(nodes_file, edges_file)
kmeans = graphOp.clusterizingNodes(G,n_regions)
graphOp.calculateMixZonesByFlow(days, time_intervals, n_regions, n_mixzones, k_anonymity, flow_window, region_flow_path, G, kmeans,mixzones_path)

# mixzones = graphOp.selectMixZonesByEngenvectorAndRegion(n_mixzones,G,k_anonymity)
# sim.simulation(mixzones,mobile_entities,log_file)

# df = pd.read_csv(nodes_file,delimiter=',')
# df = df[df['node_id'].isin(list(nx.articulation_points(G)))]
# utils.visualizeMapBySpecificSet(df,"./../data/sf.geojson")

# graphOp.saveClusters(G,kmeans,"./../data/nodesByRegion.csv")
# graphOp.clusterizingNodes(G,n_regions,"./../data/nodesByRegion.csv")
# utils.visualizeMapByRegion(pd.read_csv(nodes_file, delimiter=","), n_regions, "./../data/sf.geojson")