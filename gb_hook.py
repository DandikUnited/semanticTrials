__author__ = "bediegilmez"
import rdflib
from rdflib import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory


# configuring logging
print("-------------------------------------------------------------------------------------------------------------------")
print("Filling ontology from Gutenberg Project endpoint...")
print("-------------------------------------------------------------------------------------------------------------------")
# configuring the end-point and constructing query
# the given construct query will add the data to the existing individuals 
# it will rather add new individual movies to the graph with the data from linkedmdb
# this is not an ideal solution but works fine with the Sparql query in the query_bonus.py.
# If you open the full_example.owl in Protege you will find out that the individuals 
# 1236,1237,1238,1239 are the movie data from linkedmdb.
sparql = SPARQLWrapper("http://wifo5-04.informatik.uni-mannheim.de/gutendata/sparql")
construct_query="""
      PREFIX gb: <http://bedilico.us/ontologies/gutenbuch.owl#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
      PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
      PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
      PREFIX dc: <http://purl.org/dc/terms/>
      prefix owl: <http://www.w3.org/2002/07/owl#>
      PREFIX dc:<http://purl.org/dc/elements/1.1/>
      PREFIX foaf:<http://xmlns.com/foaf/0.1/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      
      CONSTRUCT {
      ?book rdf:type gb:Book .
      ?book gb:title ?bookTitle .
      ?book gb:written_by ?author.
      ?author rdf:type gb:Author.

      ?book gb:addedToGutenberg ?addedToCatalog.
      ?addedToCatalog rdf:type gb:AddedToGutenberg.

      ?book1 rdf:type gb:Book .
      ?book1 gb:title ?bookTitle1 .
      ?book1 gb:written_by ?author1.
      ?author1 rdf:type gb:Author.

      ?author owl:sameAs <http://dbpedia.org/resource/Franz_Kafka> .
      ?author1 owl:sameAs <http://dbpedia.org/resource/Mark_Twain> .
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext3176> owl:sameAs <http://dbpedia.org/resource/The_Innocents_Abroad>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext3177> owl:sameAs <http://dbpedia.org/resource/Roughing_It>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext245> owl:sameAs <http://dbpedia.org/resource/Life_on_the_Mississippi>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext9009> owl:sameAs <http://dbpedia.org/resource/Life_on_the_Mississippi>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext1086> owl:sameAs <http://dbpedia.org/resource/A_Horse's_Tale>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext119> owl:sameAs <http://dbpedia.org/resource/A_Tramp_Abroad>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext3174> owl:sameAs <http://dbpedia.org/resource/A_Dog's_Tale>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext3186> owl:sameAs <http://dbpedia.org/resource/The_Mysterious_Stranger>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext3190> owl:sameAs <http://dbpedia.org/resource/1610_(Mark_Twain)>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext3251> owl:sameAs <http://dbpedia.org/resource/The_Man_That_Corrupted_Hadleyburg>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext91> owl:sameAs <http://dbpedia.org/resource/Tom_Sawyer_Abroad>.
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext93> owl:sameAs <http://dbpedia.org/resource/Tom_Sawyer,_Detective>.
      <http://dbpedia.org/resource/The_Metamorphosis> owl:sameAs <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext5200> .
      <http://wifo5-04.informatik.uni-mannheim.de/gutendata/resource/etext7849> owl:sameAs <http://dbpedia.org/resource/The_Trial>.


      ?book1 gb:addedToGutenberg ?addedToCatalog1.
      ?addedToCatalog1 rdf:type gb:AddedToGutenberg

      }
      WHERE {
      ?author foaf:name "Kafka, Franz, 1883-1924".
      ?author1 foaf:name "Twain, Mark, 1835-1910".

      ?book dc:creator ?author;
      dc:title ?bookTitle;
      dc:language ?bookLanguage;
      dcterms:created ?addedToCatalog.

      ?book1 dc:creator ?author1;
      dc:title ?bookTitle1;
      dc:language ?bookLanguage1;
      dcterms:created ?addedToCatalog1

} """


sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graphGUID = 'http://bedilico.us/store/book'
graph_id=URIRef(graphGUID)
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store 
g = sparql.query().convert()

# merging results and saving the store
#g = sparql.query().convert()
g.parse("bookShelf_from_dbpedia.owl")
# the graph will be saved as full_example.owl. You can open the file with Protege to inspect it.
g.serialize("bookShelf_from_dbpedia_and_Gutenberg.owl", "xml")
print("*******************************************************************************************************************")
print("*Now you can run the SPARQL queries. Please be sure that you are in right directory...                            *")
print("*******************************************************************************************************************")