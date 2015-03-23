__author__ = "bediegilmez"
import logging
import rdflib


# configuring logging
logging.basicConfig()

# creating the graph
g=rdflib.Graph()
result=g.parse("bookShelf_from_dbpedia_and_Gutenberg.owl", "xml")
print("*******************************************************************************************************************")
print("*This graph has %s statements.                                                                                  *" % len(g))
print("*******************************************************************************************************************")
# FILTER (str(?name) = str(?name1)) line is a neat trick to combine individuals that are created
# from two sources.For example individual 1236 is actually the data from linkedmdb for the movie 
# Harry Potter and the Philosopher's Stone. 1236 includes raiting information for the movie 
# which is not available from DBpedia.
query="""
PREFIX gb: <http://bedilico.us/ontologies/gutenbuch.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
SELECT ?book ?sumi ?author ?book1
WHERE { ?book rdf:type gb:Book.
        ?book gb:written_by ?author.
        ?author owl:sameAs ?author1.
        ?book owl:sameAs ?book1.
        ?book1 gb:summary ?sumi.

        FILTER (regex(str(?author),"Twain_Mark"))}
        """
# displaying results
for x,y,z,b in g.query(query):
        print("-------------------------------------------------------------------------------------------------------------------")
        print "(PG) Book URI: ",x,"\n"
        print "(DBP) Summary: ",y,"\n"
        print "(PG&DBP) Author: ",z,b,"\n"
print("*******************************************************************************************************************")
print "*Legend -> (PG): Project Gutenberg Endpoint \t (DBP): dbpedia endpoint                                          *"
print("*******************************************************************************************************************")
