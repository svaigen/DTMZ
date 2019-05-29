import networkx as nx
import graphOperations as graphOp
import flowAnalysis as flow

nodes_file = "./../data/nodes.csv" 
edges_file = "./../data/edges2.csv"

G = graphOp.buildGraphFromCSV(nodes_file, edges_file)