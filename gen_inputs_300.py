import json
import random

f = open('./i300.in', 'w')

graph = {}
graph["directed"] = False
graph["multigraph"] = False
graph["graph"] = {}
graph["nodes"] = [{"id": i} for i in range(300)]

group = []
group.append([i for i in range(0, 21)])
group.append([i for i in range(21, 42)])
group.append([i for i in range(42, 63)])
group.append([i for i in range(63, 85)])
group.append([i for i in range(85, 106)])
group.append([i for i in range(106, 128)])
group.append([i for i in range(128, 149)])
group.append([i for i in range(149, 170)])
group.append([i for i in range(170, 191)])
group.append([i for i in range(191, 212)])
group.append([i for i in range(212, 233)])
group.append([i for i in range(233, 255)])
group.append([i for i in range(255, 278)])
group.append([i for i in range(278, 300)])

all_edges = []

for g in group:
    edge = []
    temp_e = set()
    num_edges = random.randint(14, len(g) * (len(g) + 1) / 2)
    for _ in range(num_edges):
        a = random.randint(g[0], g[-1])
        b = random.randint(g[0], g[-1])
        if a == b:
            continue
        elif (a, b) in temp_e or (b, a) in temp_e:
            continue
        else:
            temp_e.add((a, b))
    for u, v in temp_e:
        all_edges.append({"weight" : random.randint(8, 182), "source" : u, "target" : v})


cross = []
num_edges_cross = 10000
temp_cross = set()
for _ in range(num_edges_cross):
    g1 = random.choice(group)
    g2 = random.choice(group)
    if g1 == g2:
        continue
    v = random.choice(g1)
    w = random.choice(g2)
    if (v, w) in temp_cross or (w, v) in temp_cross:
        continue
    else:
        temp_cross.add((v, w))
for u, v in temp_cross:
    cross.append({"weight" : random.randint(800, 989), "source" : u, "target" : v})

edges = all_edges + cross
graph["links"] = edges
print("edges: ", len(edges))
print("total weight: ", sum(map(lambda x: x["weight"], edges)))

json_object = json.dumps(graph)
with open("i300.in", "w") as outfile:
    outfile.write(json_object)