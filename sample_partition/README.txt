SAMPLE PARTITIONS OF INPUT GRAPHS

Description:
File {size}{n}_part{k}.in corresponds to an approximate maximum k-partition of the nth input graph of the given size.
e.g. small1_part3.in is a list of dictionaries that describe team assignments of nodes in small1.in into 3 teams.
To update the a networkx graph G according to these assignments, call:
    read_partition(G, path: str)
where str is the filepath of the partition file.
To get all nodes assigned to each team, call:
    team_vector(path: str, num_teams)
which returns a vector where a list of all nodes belonging to an indexed team number.

Todo:
Keep generating these for medium and large graphs.
Need to generate multiple possibilities for each k and graph, since the algorithm used to produce these assignments is not deterministic.

Also note: part30 and onwards are unnecessary. The cost function for k >= 30 is so large that they do not need to be considered.
They are kept here for purely research purposes.