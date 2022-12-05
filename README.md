# Fall 2022 CS170 Project Skeleton

TO OBTAIN INPUTS: Run solver.py. It goes through every possible algorithm that is in the
All outputs will be generated in the outputs folder. WARNING: This will overwrite existing outputs.

TO IMPROVE OUTPUTS: Run random_imp.py. It runs randomized algorithms a large number of times and overwrites existing outputs with improvements.

To generate MST stop outputs, call makeGraphs in algorithms.py.

To generate sample partitions,
Create a Neo4j Desktop instance. In the database, move all graphs in graphml format (pre-generated in GMLinput) to $Database directory$/import. Then, run partition_generator.py.