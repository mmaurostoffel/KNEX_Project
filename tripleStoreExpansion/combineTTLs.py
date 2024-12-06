from rdflib import Graph



g = Graph()
g.parse('../results/base.ttl', format='turtle')
g.parse('../results/files.ttl', format='turtle')
g.parse('../results/merged.ttl', format='turtle')
g.parse('../results/fuzzyMerged.ttl', format='turtle')
g.parse('../results/relations.ttl', format='turtle')
g.parse('../results/pages.ttl', format='turtle')
g.serialize('../results/fullTripleStore.ttl', format="turtle")


for row in g:
    print(row)

