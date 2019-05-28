import networkx as nx
import graphOperations as graphOp

nodes_file = "./../data/nodes.csv" 
edges_file = "./../data/edges2.csv"

G = graphOp.buildGraphFromCSV(nodes_file, edges_file)