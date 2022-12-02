from neo4j import GraphDatabase
import logging
from starter import *
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def get_k_cut(self, name):
        with self.driver.session(database="neo4j") as session:
            # Do not combine methods; the session executes them in parallel and causes data race if done so
            session.execute_write(self._clear_nodes)
            session.execute_write(self._delete_graph)
            session.execute_write(self._load_graphml, name)
            session.execute_write(self._label_nodes)
            session.execute_write(self._create_graph)
            for k in range(2, 13):
                result = session.execute_write(self._max_k_cut, k)
                dump = []
                for record in result:
                    dump.append(record.data())
                with open("./sample_partition_3/" + name[:-8] + "_part" + str(k) + ".in", "w") as outfile:
                    json.dump(dump, outfile)

    @staticmethod
    def _clear_nodes(tx):
        clear = ("MATCH (n) DETACH DELETE n")
        tx.run(clear)

    @staticmethod
    def _delete_graph(tx):
        delete = ("CALL gds.graph.drop('g', false)")
        tx.run(delete) 
    
    @staticmethod
    def _load_graphml(tx, fname):
        query = ("CALL apoc.import.graphml('file://" + fname + "', {readLabels: TRUE, storeNodeIds: TRUE})")
        tx.run(query)

    @staticmethod
    def _label_nodes(tx):
        label = "MATCH (n) set n:node"
        tx.run(label)

    @staticmethod
    def _create_graph(tx):
        create = "CALL gds.graph.project('g', 'node',{RELATED : {properties:  'weight', orientation: 'UNDIRECTED'}})"
        tx.run(create)

    @staticmethod
    def _max_k_cut(tx, k):
        query = ("CALL gds.alpha.maxkcut.stream('g', {k:" + str(k) + ", relationshipWeightProperty:'weight', iterations : 30, vnsMaxNeighborhoodOrder : 50}) YIELD nodeId, communityId")
        result = tx.run(query)
        return [row for row in result]

    #EXAMPLE
    @staticmethod
    def _create_and_return(tx, person1_name, person2_name):
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                     for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                            query=query, exception=exception))
            raise

def main(size, num):
    app = App("bolt://localhost:7687", "neo4j", "1234")
    app.get_k_cut("{s}{n}.graphml".format(s = size, n = num))
    app.close()

# Terminal call
if __name__ == "__main__":
    import sys
    args = sys.argv
    main(args[0], args[1], args[2])


