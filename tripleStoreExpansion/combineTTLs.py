from rdflib import Graph

g = Graph()
g.parse('../results/base.ttl', format='turtle')
g.parse('../results/files.ttl', format='turtle')
g.parse('../results/merged.ttl', format='turtle')
g.parse('../results/fuzzyMerged.ttl', format='turtle')
g.parse('../results/pages.ttl', format='turtle')
g.serialize('../results/fullTripleStore.ttl', format="turtle")


#graph = Graph()
#graph.parse('../results/fullTripleStore_vonHand.ttl', publicID="abc")


for row in g:
    print(row)

