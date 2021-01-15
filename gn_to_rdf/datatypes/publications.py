from rdflib import Graph, Namespace, BNode, Literal

from rdflib.namespace import DC

from sqlalchemy import Table, MetaData, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

def convert(db_engine):
    pub_graph = Graph()

    #Define Namespaces
    pubmed = Namespace("https://pubmed.ncbi.nlm.nih.gov/")

    db_session = sessionmaker(bind=db_engine)()

    metadata = MetaData()
    metadata.reflect(db_engine, only=['Publication'])
    Base = automap_base(metadata=metadata)
    Base.prepare()
    publications = Base.classes.Publication
    rows = db_session.query(publications).all()

    for i, row in enumerate(rows):
        this_pub = row.__dict__

        pub_node = BNode() #ZS: This would presumably be replaced with a GN URI

        if this_pub['Abstract'] != None:
            pub_graph.add((pub_node, DC.abstract, Literal(this_pub['Abstract'])))

        if i > 10:
            break

    print(pub_graph.serialize(format="turtle").decode("utf-8"))