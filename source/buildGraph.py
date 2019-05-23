import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def buildNodeAttributeDict(nodes,id,attr):
    attr_dict = {}
    for indices, row in nodes.iterrows():
        attr_dict[row[id]] = row[attr]
    return attr_dict


edges_file = "./../data/edges.csv"
nodes_file = "./../data/nodes.csv"

nodes = pd.read_csv(nodes_file, error_bad_lines=False)
edges = pd.read_csv(edges_file, header=0, delimiter=",", usecols=["edge_id","source","target"])

G = nx.from_pandas_edgelist(df=edges, source="source", target="target")
#nx.set_node_attributes(G, buildNodeAttributeDict(nodes,"node_id","latitude") , "latitude")

dictAttr = buildNodeAttributeDict(nodes,"node_id","latitude")
for item in dictAttr:
    print(item['latitude'])

#print(G.nodes.data())

#print(pd.Series(nodes["latitude"], index=nodes.node_id))
#print("building a visual representation of G")
#nx.draw_networkx(G,pos=nx.circular_layout(G))
#plt.draw()
#plt.show()
#print("exiting...")