#!/usr/bin/env python3

# Impulse: Ontology Reasoning with Python

from pathlib import Path
import rdflib
from owlrl import DeductiveClosure, OWLRL_Semantics

TURTLE_DIR = Path("ttl")

# Step 1: Load the core dataset and extend it with the ontology
g = rdflib.Graph()
g.parse(TURTLE_DIR / "core-dataset.ttl", format="turtle")
g.parse(TURTLE_DIR / "ontology.ttl", format="turtle")

# Step 2: Apply reasoning using OWL RL rules
DeductiveClosure(OWLRL_Semantics).expand(g)

# Step 3: Save the expanded RDF graph
g.serialize("core-dataset_expanded.ttl", format="turtle")