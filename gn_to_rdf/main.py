import os
import sys

import click
from sqlalchemy import create_engine

from datatypes import publications, phenotypes

module_path = os.path.dirname(os.path.realpath(__file__))

@click.command()
@click.option('-d', '--datatype', required=True)
@click.option('-o', '--out_file', default=os.path.join(module_path, "output/"))
def cli(datatype, out_file):
    db_engine = connect_db()
    if datatype == "publications":
        publications.convert(db_engine, out_file)
    elif datatype == "phenotypes":
        phenotypes.convert(db_engine, out_file)

def connect_db():
    sql_uri = os.getenv("SQL_URI")
    engine = create_engine(sql_uri)
    return engine

if __name__ == "__main__":
    cli()