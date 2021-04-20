from rdflib import Graph, Namespace, URIRef, Literal

from sqlalchemy.orm import sessionmaker

#ZS: Define Namespaces
gn_prefix = "https://genenetwork.org/"
gn = Namespace("https://genenetwork.org/")

def convert(db_engine, out_file):
    the_graph = Graph()
    the_graph.bind("gn", gn)

    db_session = sessionmaker(bind=db_engine)()

    ps_xref_query = "SELECT ProbeSetXRef.ProbeSetId, ProbeSetXRef.ProbeSetFreezeId FROM ProbeSetXRef"

    results = db_session.execute(ps_xref_query).fetchall()

    for i, this_result in enumerate(results):
        build_nodes(the_graph, this_result, db_session)

    the_graph.serialize(destination=out_file + "mrna_expression.ttl", format="turtle")

def build_nodes(the_graph, this_result, db_session):
    ps_id = this_result[0]
    ps_freeze_id = this_result[1]

    this_group = db_session.execute(f"""
        SELECT InbredSet.Id, InbredSet.Name
        FROM InbredSet, ProbeFreeze, ProbeSetFreeze, ProbeSetXRef
        WHERE ProbeSetXRef.Id = { ps_id } AND
              ProbeSetFreeze.Id = ProbeSetXRef.ProbeSetFreezeId AND
              ProbeFreeze.ProbeFreezeId = ProbeSetFreeze.ProbeFreezeId AND
              InbredSet.Id = ProbeFreeze.InbredSetId
    """).fetchone()

    group_id, group_name = this_group

    group_gn_id = URIRef(f"{ gn_prefix }group/{ group_id }")