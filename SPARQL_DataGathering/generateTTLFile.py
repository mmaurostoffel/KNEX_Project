import pandas as pd
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS

def getBaseData():
    QUERY = '''
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    SELECT DISTINCT ?main ?mainLabel ?type ?typeLabel
    WHERE{
        SERVICE <https://query.wikidata.org/sparql>{
          # 1 present in work Warhammer 40000 == Viele verschiedene Outputs
          {?main wdt:P1441 wd:Q209026.}
          UNION
          # 2 present in work Warhammer == Viele verschiedene Outputs
          {?main wdt:P1441 wd:Q928197.}
          UNION
          # 3 from_narrative universe == Viele verschiedene Outputs
          {?main wdt:P1080 wd:Q19595297.}
    
          ?main wdt:P31 ?type.
          ?main rdfs:label ?mainLabel filter (lang(?mainLabel) = "en").
          ?type rdfs:label ?typeLabel filter (lang(?typeLabel) = "en").
        }
    
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    '''

    g = Graph()

    WDT = Namespace("http://www.wikidata.org/prop/direct/")
    g.bind("wdt", WDT)

    for main, mainLabel, type, typeLabel in g.query(QUERY):
        print(main, mainLabel, type, typeLabel)
        g.add((main, WDT.P31, type))
        g.add((main, RDFS.label, mainLabel))
        g.add((type, RDFS.label, typeLabel))


    g.serialize('../results/base.ttl', format='ttl')

getBaseData()