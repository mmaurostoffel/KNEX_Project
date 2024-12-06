from pathlib import Path
import rdflib
from owlrl import DeductiveClosure, OWLRL_Semantics


# Step 1: Load the core dataset and extend it with the ontology
g = rdflib.Graph()
g.parse('results/fullTripleStore.ttl', format="turtle")
g.parse("ontology.ttl", format="turtle")

# Step 2: Apply reasoning using OWL RL rules
DeductiveClosure(OWLRL_Semantics).expand(g)

# Step 3: Save the expanded RDF graph
g.serialize("../results/fullTripleStore_expanded.ttl", format="turtle")