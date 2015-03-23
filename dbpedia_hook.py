__author__ = "bediegilmez"

import rdflib
import logging
from rdflib.graph import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory

# configuring logging
logging.basicConfig()
print("-------------------------------------------------------------------------------------------------------------------")
print("         _           _                    _        _ _             _ _     \n ___ _ _| |_ ___ ___| |_ ___ ___ ___    _| |_    _| | |_ ___ ___ _| |_|___ \n| . | | |  _| -_|   | . | -_|  _| . |  |_   _|  | . | . | . | -_| . | | .| \n|_  |___|_| |___|_|_|___|___|_| |_  |    |_|    |___|___|  _|___|___|_|__,| \n|___|                           |___|                   |_|                "),__author__
print("-------------------------------------------------------------------------------------------------------------------")

# configuring the end-point and constructing query
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
construct_query="""
      PREFIX gb: <http://bedilico.us/ontologies/gutenbuch.owl#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
      PREFIX dbpprop: <http://dbpedia.org/property/>
      PREFIX dc:<http://purl.org/dc/elements/1.1/>
      PREFIX foaf:<http://xmlns.com/foaf/0.1/>
      PREFIX dcterms: <http://purl.org/dc/terms/>

      CONSTRUCT {
      ?book rdf:type gb:Book .
      ?book gb:titled_as ?name.
      gb:Title rdf:type ?name.
      ?book gb:written_by ?author.
      ?author rdf:type gb:Author.
      ?book gb:author_name ?authorName.
      gb:Author rdf:type ?authorName.
      gb:AuthorName rdf:type ?authorName.
      ?book gb:released ?firstPublished.
      ?firstPublished rdf:type gb:PublishDate.
      ?book gb:writtenInCountry ?country .
      ?country rdf:type gb:Country.
      ?book gb:writtenIn ?lang .
      ?lang rdf:type gb:Language.
      ?book gb:summary ?abstract.
      gb:Absratct rdf:type ?abstract.
      ?book gb:identified_with ?isbn .
      gb:ISBN rdf:type ?isbn.
      ?book gb:publish_tpe ?mediaType .
      ?mediaType rdf:type gb:Media .
      ?book gb:has_pagenumber ?pages.
      gb:Pages rdf:type ?pages.
      ?book gb:genre ?genre

      }WHERE{?book rdf:type dbpedia-owl:Book .
       ?book foaf:name ?name.
       OPTIONAL {?book dbpedia-owl:author ?author}
       OPTIONAL {?author dbpprop:name ?authorName}
       OPTIONAL {?book dbpedia-owl:releaseDate ?firstPublished}
       OPTIONAL {?book dbpedia-owl:country ?country}
       OPTIONAL {?book dbpedia-owl:language ?lang}
       OPTIONAL {?book dbpedia-owl:abstract ?abstract}
       OPTIONAL {?book dbpedia-owl:isbn ?isbn}
       OPTIONAL {?book dbpedia-owl:numberOfPages ?pages}
       OPTIONAL {?book dbpedia-owl:mediaType ?mediaType}
       OPTIONAL {?book dbpprop:genre ?genre}
       FILTER ( regex(str(?author), "Franz_Kafka") || regex(str(?author), "Mark_Twain") )
       FILTER (LANG(?abstract)="en")
      }"""



sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graph_id=URIRef("http://bedilico.us/store/book")
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store

g = sparql.query().convert()

g.parse("gutenbuch.owl")
g.serialize("bookShelf_from_dbpedia.owl", "xml")
execfile("gb_hook.py")