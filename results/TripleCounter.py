from rdflib import Graph, URIRef, Namespace, RDFS, Literal

g = Graph()
g.parse("results/expandedFiltered.ttl", format="turtle")

COUNTER = 0
for s, p, o in g:
    COUNTER += 1

print(COUNTER)