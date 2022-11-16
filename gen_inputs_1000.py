import json
import random

f = open('./i1000.in', 'w')


json_object = json.dumps(graph)
with open("i1000.in", "w") as outfile:
    outfile.write(json_object)