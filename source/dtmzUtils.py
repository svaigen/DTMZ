import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import networkx as nx
from sklearn.cluster import KMeans
import random

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