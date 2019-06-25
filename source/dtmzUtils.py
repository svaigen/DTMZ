import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import networkx as nx
from sklearn.cluster import KMeans
import random
import mixZone as mz
import mobileEntity as me
import os
import datetime as dt
import string

def removingNoiseFromNodes(nodes_file,G):
    nodes = pd.read_csv(nodes_file, delimiter=",")
    first = True
    nodes = nodes.set_index("node_id")
    for component in sorted(nx.connected_components(G), key=len, reverse=True):
        if not first:                      
            for node in component:                
                nodes = nodes.drop(node,axis=0)                
        first = False
    nodes.to_csv(nodes_file)
    return None


def getColors(n):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    name_colors = []
    for name, c in colors.items():
        name_colors.append(name)
    random.shuffle(name_colors)
    return name_colors[0:n]

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

def visualizeMapBySpecificSet(nodes_df, region_file):
    points = buildMapPoints(nodes_df)
    region = buildMapRegion(region_file)
    fig, ax = plt.subplots(1, subplot_kw=dict(alpha=0.3))
    map = region.plot(ax=ax, color='gray')
    colors = getColors(1)
    points.plot(ax=map, marker="o", markersize=15, alpha=0.5, color=colors[0])
    ax.set_title("Map visualization")
    plt.show()
    return None

def visualizeMapByRegion(nodes_df, nregions, region_file):
    points_list = []
    for i in range(nregions):
        nodes = nodes_df[nodes_df['region'] == i]
        points_list.append(buildMapPoints(nodes))
    region = buildMapRegion(region_file)
    fig, ax = plt.subplots(1, subplot_kw=dict(alpha=0.3))
    map = region.plot(ax=ax, color='gray')
    i = 0
    colors = getColors(nregions)
    for points in points_list:
        points.plot(ax=map, marker="o", markersize=5, alpha=0.5, color=colors[i])
        i += 1
    ax.set_title("Map visualization")
    plt.show()
    return None

def visualizeMapByGraphComponent(nodes_df, G, region_file):
    points_list = []
    comp_dict = {}
    components = []
    c_index = 0
    for component in nx.connected_components(G):       
        for node in component:
            comp_dict[node] = c_index
        c_index += 1
    for i, row in nodes_df.iterrows():
        components.append(comp_dict[row['node_id']])
    nodes_df['component'] = components    
    for i in range(nodes_df['component'].max()+1):
        filter = nodes_df[nodes_df['component'] == i]
        points_list.append(buildMapPoints(filter))
    region = buildMapRegion(region_file)
    fig, ax = plt.subplots(1, subplot_kw=dict(alpha=0.3))
    map = region.plot(ax=ax, color='gray')
    colors = getColors(nodes_df['component'].max()+1)
    i=0
    for points in points_list:
        points.plot(ax=map, marker="o", markersize=5, alpha=0.5, color=colors[i])
        i += 1
    ax.set_title("Map visualization")
    plt.show()
    return None

def generateMixZonesObjects(mixzones_ID,G,k_anonimity):
    mixzones = []
    for id in mixzones_ID:
        mixzones.append(mz.mixZone(id,k_anonimity,G.nodes[id]['latitude'],G.nodes[id]['longitude'],100))
    return mixzones

def generateMobileEntitiesByFolder(path):
    mobileEntities = []
    for trip_file in os.listdir(path):
        trip_df = pd.read_csv("{}{}".format(path,trip_file), delimiter=',')
        firstRow = True
        mobile_entity = {}
        for i, data in trip_df.iterrows():            
            if firstRow:
                mobile_entity = me.mobileEntity(data['name'],(data['lat'],data['lon'],data['time']),data['id_trace'])
                firstRow = False
            else:
                mobile_entity.addTrace((data['lat'],data['lon'],data['time']))
        mobileEntities.append(mobile_entity)
    return mobileEntities

def formatTimestamp(timestamp, format):
    return (dt.datetime.fromtimestamp(timestamp) - dt.timedelta(hours=7)).strftime(format)

def generatingRandomPseudonym(size):
    samples = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m","1","2","3","4","5","6","7","8","9","0"]
    pseudonym = ""
    for i in range(size):
        pseudonym += random.choice(samples)
    return pseudonym

def initializeRegionsFlowHistory(n_regions,rows,cols):
    regions_flow_history = {}
    for r in range(n_regions):
        df = pd.DataFrame(columns=cols)
        df.set_index('day')
        df['day'] = rows
        for col_id in range(1,len(cols)):
            df[cols[col_id]] = 0
        regions_flow_history[r] = df
    return regions_flow_history

def getIndexDay(day):
    days = ['2008-05-17','2008-05-18','2008-05-19','2008-05-20','2008-05-21','2008-05-22','2008-05-23','2008-05-24','2008-05-25','2008-05-26','2008-05-27','2008-05-28','2008-05-29','2008-05-30','2008-05-31','2008-06-01','2008-06-02','2008-06-03','2008-06-04','2008-06-05','2008-06-06','2008-06-07','2008-06-08','2008-06-09']
    for i in range(len(days)):
        if days[i] == day:
            return i
    return -1