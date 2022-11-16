import json
import random

f = open('./i1000.in', 'w')

graph = {}
graph["directed"] = False
graph["multigraph"] = False
graph["graph"] = {}
graph["nodes"] = [{"id": i} for i in range(1000)]

edges = []
num_edges_cross = random.randint(7000, 10000)
temp_edges = set()
for _ in range(num_edges_cross):
    v = random.randint(0, 999)
    w = random.randint(0, 999)
    if w == v:
        continue
    if (v, w) in temp_edges or (w, v) in temp_edges:
        continue
    else:
        temp_edges.add((v, w))
for u, v in temp_edges:
    edges.append({"weight" : random.randint(1, 999), "source" : u, "target" : v})

graph["links"] = edges
print("edges: ", len(edges))
print("total weight: ", sum(map(lambda x: x["weight"], edges)))

json_object = json.dumps(graph)
with open("i1000.in", "w") as outfile:
    outfile.write(json_object)

print()