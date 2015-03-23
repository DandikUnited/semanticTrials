__author__ = "bediegilmez"
import logging
import rdflib


logging.basicConfig()
#below you can see a simple sparql query, where the data is gathered from DBPEDIA endpoint. This query returns the
# number of pages and the work of the two authors gathered from DBPEDIA. Since Franz Kafka has some German language
# works, character encoding is a bit tricky. simple try-catch statement omits the results those couldn't be printed.

query = """
PREFIX gb: <http://bedilico.us/ontologies/gutenbuch.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?author ?pn ?name WHERE
    { ?book rdf:type gb:Book .
        ?book gb:titled_as ?name .
        ?book gb:author_name ?author .
        ?book gb:has_pagenumber ?pn.
      }GROUP BY ?pn
       ORDER BY ?pn"""


g=rdflib.Graph()
result=g.parse("bookShelf_from_dbpedia_and_Gutenberg.owl", "xml")

print("This graph has %s statements.\n" % len(g))

# displaying the results
print("-------------------------------------------------------------------------------------------------------------------")
print ('{0:45s} \t{1:10s} \t{2:10s}'.format("Author","Page Number","Book Title"))
print("-------------------------------------------------------------------------------------------------------------------")
for x,y,z in g.query(query):
    try:
        print ('{0:45s} \t {1:10s} \t{2:10s}'.format(x,y,z))
        print("-------------------------------------------------------------------------------------------------------------------")
    except UnicodeEncodeError:
        print("*******************************************************************************************************************")
        print "*INFO: Some results omitted. This is because Unicode Encoding. That's all we know.                                *"
        print("*******************************************************************************************************************")