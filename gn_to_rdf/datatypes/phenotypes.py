from rdflib import Graph, Namespace, URIRef, BNode, Literal

from rdflib.namespace import DC

from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

#ZS: Define Namespaces
gn_prefix = "https://genenetwork.org/"
gn = Namespace("https://genenetwork.org/")

def convert(db_engine, out_file):
    pheno_graph = Graph()
    pheno_graph.bind("gn", gn)

    db_session = sessionmaker(bind=db_engine)()

    pheno = db_session.execute("SELECT * FROM Phenotype;").fetchall()
    pub_xref = db_session.execute("SELECT * FROM PublishXRef;").fetchall()

    for i, this_pubxref in enumerate(pub_xref):
        build_nodes(pheno_graph, this_pubxref, db_session)

    pheno_graph.serialize(destination=out_file + "phenotypes.ttl", format="turtle")

def build_nodes(pheno_graph, this_pubxref, db_session):
    group_id = this_pubxref[1]
    pheno_id = this_pubxref[2]
    this_pheno = db_session.execute(f"SELECT * FROM Phenotype where Id={ pheno_id }").fetchone()

    result = db_session.execute(f"SELECT InbredSet.Id, InbredSet.Name, InbredSet.InbredSetCode from InbredSet where InbredSet.Id ={ group_id };").fetchone()
    if result:
        group_id, group_name, group_code = result
        pheno_gn_id = URIRef(f"{ gn_prefix }phenotype/{ group_code }_{ this_pubxref[0] }")
        group_gn_id = URIRef(f"{ gn_prefix }group/{ group_id }")

        pheno_graph.add((pheno_gn_id, gn.group_id, group_gn_id))

        #ZS: Contents of Phenotype table
        if this_pheno[1]: pheno_graph.add((pheno_gn_id, gn.pre_publication_description, Literal(this_pheno[1])))
        if this_pheno[2]: pheno_graph.add((pheno_gn_id, gn.post_publication_description, Literal(this_pheno[2])))
        if this_pheno[3]: pheno_graph.add((pheno_gn_id, gn.original_description, Literal(this_pheno[3])))
        if this_pheno[4]: pheno_graph.add((pheno_gn_id, gn.units, Literal(this_pheno[4])))
        if this_pheno[5]: pheno_graph.add((pheno_gn_id, gn.pre_publication_abbreviation, Literal(this_pheno[5])))
        if this_pheno[6]: pheno_graph.add((pheno_gn_id, gn.post_publication_abbreviation, Literal(this_pheno[6])))
        if this_pheno[7]: pheno_graph.add((pheno_gn_id, gn.lab_core, Literal(this_pheno[7])))

        pheno_graph.add((pheno_gn_id, gn.publication, URIRef(gn_prefix + 'publication/' + str(this_pubxref[3]))))

        #ZS: Contents of PublishXRef table
        if this_pubxref[5]: pheno_graph.add((pheno_gn_id, gn.mean, Literal(this_pubxref[5])))
        if this_pubxref[6]: pheno_graph.add((pheno_gn_id, gn.locus, Literal(this_pubxref[6])))
        if this_pubxref[7]: pheno_graph.add((pheno_gn_id, gn.lrs, Literal(this_pubxref[7])))
        if this_pubxref[8]: pheno_graph.add((pheno_gn_id, gn.additive, Literal(this_pubxref[8])))