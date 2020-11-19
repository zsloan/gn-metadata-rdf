
import os

import click
from sqlalchemy import create_engine

from datatypes import publications

@click.command()
@click.option('--datatype')
def cli(datatype):
    if datatype == "phenotypes":
        db_engine = connect_db()
        publications.convert(db_engine)


def connect_db():
    sql_uri = os.environ("SQL_URI")
    engine = create_engine(sql_uri)
    return engine
