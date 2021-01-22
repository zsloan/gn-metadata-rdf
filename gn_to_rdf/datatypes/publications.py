from rdflib import Graph, Namespace, URIRef, BNode, Literal

from rdflib.namespace import DC

from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

#ZS: Define Namespaces
pubmed_prefix = "https://pubmed.ncbi.nlm.nih.gov/"
gn_prefix = "https://genenetwork.org/"
gn = Namespace("https://genenetwork.org/")
schema = Namespace("https://schema.org/")

def convert(db_engine):
    pub_graph = Graph()
    pub_graph.bind("gn", gn)
    pub_graph.bind("dc", DC)
    pub_graph.bind("schema", schema)

    db_session = sessionmaker(bind=db_engine)()

    metadata = MetaData()
    metadata.reflect(db_engine, only=['Publication'])
    Base = automap_base(metadata=metadata)
    Base.prepare()
    publications = Base.classes.Publication
    rows = db_session.query(publications).all()

    for i, row in enumerate(rows):
        this_pub = row.__dict__

        build_nodes(pub_graph, this_pub)

        if i > 3:
            break

    print(pub_graph.serialize(format="turtle").decode("utf-8"))

def build_nodes(pub_graph, this_pub):
    gn_id = URIRef(gn_prefix + 'publication/' + str(this_pub['Id']))
    pm_id = URIRef(pubmed_prefix + str(this_pub['PubMed_ID']))

    pub_graph.add((gn_id, gn.published_as, pm_id))
    pub_graph.add((gn_id, gn.pmid, Literal(this_pub['PubMed_ID'])))
    pub_graph.add((gn_id, DC.title, Literal(this_pub['Title'])))
    pub_graph.add((gn_id, schema.abstract, Literal(this_pub['Abstract'])))
    issue_node = BNode()
    volume_num, issue_num = get_issue_vol(this_pub['Volume'])

    pub_graph.add((gn_id, schema.isPartOf, issue_node))
    pub_graph.add((issue_node, schema.issueNumber, Literal(issue_num)))
    date_string = get_issue_date(str(this_pub['Year']), str(this_pub['Month']))
    pub_graph.add((issue_node, schema.datePublished, Literal(date_string)))

    journal_node = BNode()
    if this_pub['Journal']:
        pub_graph.add((issue_node, schema.isPartOf, journal_node))
        pub_graph.add((journal_node, schema.name, Literal(this_pub['Journal'])))

    author_list = this_pub['Authors'].split(",")
    for author in author_list:
        pub_graph.add((gn_id, schema.contributor, Literal(author.strip())))

def get_issue_vol(volume_text):
    volume_num = "Unknown"
    issue_num = "Unknown"
    if volume_text and volume_text != "Unknown":
        if len(volume_text.split("(")) > 1:
            issue_text = volume_text.split("(")[1][:-1]
            if stringIsInt(issue_text):
                issue_num = issue_text
            volume_text = volume_text.split("(")[0]
            if stringIsInt(volume_text):
                volume_num = volume_text
        else:
            if stringIsInt(volume_text):
                volume_num = volume_text

    return volume_num, issue_num

def get_issue_date(year, month):
    date_string = "Unknown"
    if stringIsInt(year):
        date_string = year
        if stringIsInt(month):
            date_string += " - " + month

    return date_string

def stringIsInt(s):
    try:
        int(s)
        return True
    except:
        return False