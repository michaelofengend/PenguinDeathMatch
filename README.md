# Fall 2022 CS170 Project Skeleton
An attempt to solve/optimiza an NP-hard problem with a variety of algorithms.


TO OBTAIN INPUTS: Run solver.py. It goes through every possible algorithm that is in the
All outputs will be generated in the outputs folder. WARNING: This will overwrite existing outputs.

TO IMPROVE OUTPUTS: Run random_imp.py. It runs randomized algorithms a large number of times and overwrites existing outputs with improvements.

To generate MST stop outputs, call makeGraphs in algorithms.py.

To generate sample partitions,
Create a Neo4j Desktop instance with password 1234. Download APOC and GDS library plugins. Set apoc.import.file.enabled=true in configurations. In the database, move all graphs in graphml format (pre-generated in GMLinput) to $Database directory$/import. Then, run partition_generator.py.
