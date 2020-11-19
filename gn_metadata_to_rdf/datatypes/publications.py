from rdflib import Graph, Namespace

from sqlalchemy import Table

def convert(db_engine):
    pub_graph = Graph()

    #Define Namespaces
    pubmed = Namespace("https://pubmed.ncbi.nlm.nih.gov/")

    publications = Table("Publication", meta, autoload=True, autoload_with=db_engine)