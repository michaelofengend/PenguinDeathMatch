import json
import random

f = open('./i100.in', 'w')

graph = {}
graph["directed"] = False
graph["multigraph"] = False
graph["graph"] = {}
graph["nodes"] = [{"id": i} for i in range(100)]
group1 = [i for i in range(0, 11)]
group2 = [i for i in range(11, 39)]
group3 = [i for i in range(39, 54)]
group4 = [i for i in range(54, 72)]
group5 = [i for i in range(72, 83)]
group6 = [i for i in range(83, 91)]
group7 = [i for i in range(91, 100)]

edge1 = []
edge1.append({"weight" : random.randint(100, 300), "source" : 0, "target" : 5})
edge1.append({"weight" : random.randint(100, 300), "source" : 0, "target" : 7})
edge1.append({"weight" : random.randint(100, 300), "source" : 0, "target" : 9})
edge1.append({"weight" : random.randint(100, 300), "source" : 1, "target" : 3})
edge1.append({"weight" : random.randint(100, 300), "source" : 1, "target" : 4})
edge1.append({"weight" : random.randint(100, 300), "source" : 1, "target" : 10})
edge1.append({"weight" : random.randint(100, 300), "source" : 2, "target" : 3})
edge1.append({"weight" : random.randint(100, 300), "source" : 2, "target" : 9})
edge1.append({"weight" : random.randint(100, 300), "source" : 2, "target" : 10})
edge1.append({"weight" : random.randint(100, 300), "source" : 3, "target" : 6})
edge1.append({"weight" : random.randint(100, 300), "source" : 3, "target" : 7})
edge1.append({"weight" : random.randint(100, 300), "source" : 4, "target" : 1})
edge1.append({"weight" : random.randint(100, 300), "source" : 4, "target" : 2})
edge1.append({"weight" : random.randint(100, 300), "source" : 4, "target" : 10})
edge1.append({"weight" : random.randint(100, 300), "source" : 4, "target" : 2})
edge1.append({"weight" : random.randint(100, 300), "source" : 6, "target" : 7})
edge1.append({"weight" : random.randint(100, 300), "source" : 6, "target" : 1})
edge1.append({"weight" : random.randint(100, 300), "source" : 7, "target" : 1})
edge1.append({"weight" : random.randint(100, 300), "source" : 7, "target" : 0})
edge1.append({"weight" : random.randint(100, 300), "source" : 8, "target" : 0})
edge1.append({"weight" : random.randint(100, 300), "source" : 9, "target" : 6})
edge1.append({"weight" : random.randint(100, 300), "source" : 9, "target" : 7})
edge1.append({"weight" : random.randint(100, 300), "source" : 9, "target" : 5})
edge1.append({"weight" : random.randint(100, 300), "source" : 9, "target" : 1})
edge1.append({"weight" : random.randint(100, 300), "source" : 10, "target" : 0})

edge2 = []
for i in range(11, 37):
            edge2.append({"weight" : random.randint(8, 513), "source" : i, "target" : i + 2})

edge3 = []
temp_e3 = set()
num_edges3 = random.randint(12, 50)
for _ in range(num_edges3):
    a = random.randint(39, 53)
    b = random.randint(39, 53)
    if a == b:
        continue
    elif (a, b) in temp_e3 or (b, a) in temp_e3:
        continue
    else:
        temp_e3.add((a, b))
for u, v in temp_e3:
    edge3.append({"weight" : random.randint(100, 300), "source" : u, "target" : v})

edge4 = []
for i in range(55, 70):
    edge4.append({"weight" : random.randint(8, 621), "source" : i, "target" : i - 1})
    edge4.append({"weight" : random.randint(8, 621), "source" : i, "target" : i + 2})
    
edge5 = []
temp_e5 = set()
num_edges5 = random.randint(12, 90)
for _ in range(num_edges5):
    a = random.randint(72, 82)
    b = random.randint(72, 82)
    if a == b:
        continue
    elif (a, b) in temp_e5 or (b, a) in temp_e5:
        continue
    else:
        temp_e5.add((a, b))
for u, v in temp_e5:
    edge5.append({"weight" : random.randint(100, 300), "source" : u, "target" : v})

edge6 = []
edge6.append({"weight" : random.randint(100, 300), "source" : 83, "target" : 84})
edge6.append({"weight" : random.randint(100, 300), "source" : 83, "target" : 90})
edge6.append({"weight" : random.randint(100, 300), "source" : 84, "target" : 85})
edge6.append({"weight" : random.randint(100, 300), "source" : 84, "target" : 88})
edge6.append({"weight" : random.randint(100, 300), "source" : 85, "target" : 90})
edge6.append({"weight" : random.randint(100, 300), "source" : 86, "target" : 90})
edge6.append({"weight" : random.randint(100, 300), "source" : 87, "target" : 90})
edge6.append({"weight" : random.randint(100, 300), "source" : 88, "target" : 87})
edge6.append({"weight" : random.randint(100, 300), "source" : 89, "target" : 87})
edge6.append({"weight" : random.randint(100, 300), "source" : 90, "target" : 87})
edge6.append({"weight" : random.randint(100, 300), "source" : 90, "target" : 89})

edge7 = []
edge7.append({"weight" : random.randint(100, 300), "source" : 91, "target" : 96})
edge7.append({"weight" : random.randint(100, 300), "source" : 91, "target" : 95})
edge7.append({"weight" : random.randint(100, 300), "source" : 91, "target" : 99})
edge7.append({"weight" : random.randint(100, 300), "source" : 91, "target" : 93})
edge7.append({"weight" : random.randint(100, 300), "source" : 92, "target" : 94})
edge7.append({"weight" : random.randint(100, 300), "source" : 92, "target" : 93})
edge7.append({"weight" : random.randint(100, 300), "source" : 94, "target" : 95})
edge7.append({"weight" : random.randint(100, 300), "source" : 95, "target" : 92})
edge7.append({"weight" : random.randint(100, 300), "source" : 95, "target" : 93})
edge7.append({"weight" : random.randint(100, 300), "source" : 96, "target" : 94})
edge7.append({"weight" : random.randint(100, 300), "source" : 96, "target" : 93})
edge7.append({"weight" : random.randint(100, 300), "source" : 97, "target" : 91})
edge7.append({"weight" : random.randint(100, 300), "source" : 98, "target" : 94})
edge7.append({"weight" : random.randint(100, 300), "source" : 99, "target" : 93})

cross = []
num_edges_cross = random.randint(20000, 20000)
temp_cross = set()
groups = [group1, group2, group3, group4, group5, group6, group7]
count = 0
for _ in range(num_edges_cross):
    g1 = random.randint(0, 6)
    g2 = random.randint(0, 6)
    if g1 == g2:
        continue
    v = random.choice(groups[g1])
    w = random.choice(groups[g2])
    if (v, w) in temp_cross or (w, v) in temp_cross:
        continue
    else:
        temp_cross.add((v, w))
for u, v in temp_cross:
    cross.append({"weight" : random.randint(700, 989), "source" : u, "target" : v})

edges = edge1 + edge2 + edge3 + edge4 + edge5 + edge6 + edge7 + cross
graph["links"] = edges
print("edges: ", len(edges))
print("total weight: ", sum(map(lambda x: x["weight"], edges)))

json_object = json.dumps(graph)
with open("i100.in", "w") as outfile:
    outfile.write(json_object)