import networkx as nx
import graphOperations as graphOp
import flowAnalysis as flow
import pandas as pd
import dtmzUtils as utils
import simulation as sim
import datetime as dt
import numpy as np
import sys
import os 
import operator

days = ['2008-05-17','2008-05-18','2008-05-19','2008-05-20','2008-05-21','2008-05-22','2008-05-23','2008-05-24','2008-05-25','2008-05-26','2008-05-27','2008-05-28','2008-05-29','2008-05-30','2008-05-31','2008-06-01','2008-06-02','2008-06-03','2008-06-04','2008-06-05','2008-06-06','2008-06-07','2008-06-08','2008-06-09']
time_intervals = ['05:59:59','10:59:59','16:59:59','23:59:59']

n_regions = 128
n_mixzones = int(sys.argv[1])
k_anonymity = int(sys.argv[2])
radius_mixzone = int(sys.argv[3])
flow_window = 50
print("number mz: {} - k_anom: {} - radius_coverage: {}".format(n_mixzones,k_anonymity,radius_mixzone))
nodes_file = "./../data/nodesByRegion.csv" 
edges_file = "./../data/edges2.csv"
sim_file = "./simulation.csv"
region_flow_path = "./../flow/"
mobile_entities_path="./../data/tripsPerDay/"
mixzones_path = "./../data/mixzones.csv"
metric = utils.EIGENVECTOR_METRIC
# G = graphOp.buildGraphFromCSV(nodes_file, edges_file)
# kmeans = graphOp.clusterizingNodes(G,n_regions)

path = "./simulations_day_range/eigenvector/m9_k14_r500/"

hist_days = [None] * len(days) 
fr = open(path+"resume.csv","w")
fr.write("coverage,pseudonymisation,flow\n")
for day_file in os.listdir(path):
    if day_file.endswith(".txt"):
        cov_dict = {} 
        anon_dict = {}
        flow = 0        
        # cover_list = []
        # anon_list = []
        f = open(path+day_file,"r")
        for row in f.readlines():
            coverages = row.split("<->")[0].replace(" ","")
            if len(coverages) > 1:
                coverages = coverages[0:len(coverages)-1]
            anonimyzeds = row.split("<->")[1].replace(" \n","")
            if len(anonimyzeds) > 1:
                anonimyzeds = anonimyzeds[0:len(coverages)-1]
            # cov_dict = {}            
            for cover in coverages.split(","):
                if not cover == '':
                    cov_dict[cover] = 1
            # cover_list.append(len(cov_dict))
            # anon_dict = {}
            for anon in anonimyzeds.split(","):
                if not anon == '':
                    anon_dict[anon] = 1
            # anon_list.append(len(anon_dict))
        f.close()
        df = pd.read_csv(path+day_file.replace(".txt","")+".csv", delimiter=',', header=None)
        fr.write("{},{},{}\n".format(len(cov_dict),len(anon_dict),df[3][0]))
fr.close()
        # df = pd.read_csv(path+day_file.replace(".txt","")+".csv", delimiter=',', header=None)
        # df[1] = cover_list
        # df[2] = anon_list
        # df.to_csv(path+"fixed-"+day_file.replace(".txt","")+".csv", header=None, index=None)

# sim.simulation(G, n_mixzones, k_anonymity, mobile_entities_path,sim_file,mixzones_path, days, time_intervals, radius_mixzone, metric)
# graphOp.calculateMixZonesByFlow(days, time_intervals, n_regions, n_mixzones, k_anonymity, flow_window, region_flow_path, G, kmeans,mixzones_path, metric)
# mixzones = graphOp.selectMixZonesByEngenvectorAndRegion(n_mixzones,G,k_anonymity)
# df = pd.read_csv(nodes_file,delimiter=',')
# df = df[df['node_id'].isin(list(nx.articulation_points(G)))]
# utils.visualizeMapBySpecificSet(df,"./../data/sf.geojson")

# graphOp.saveClusters(G,kmeans,"./../data/nodesByRegion.csv")
# graphOp.clusterizingNodes(G,n_regions,"./../data/nodesByRegion.csv")
# utils.visualizeMapByRegion(pd.read_csv(nodes_file, delimiter=","), n_regions, "./../data/sf.geojson")