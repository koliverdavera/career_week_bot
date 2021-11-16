from data.events import Event
from data.students import Student
from data.companies import Company
from data.database import create_db
import click
from flask.cli import with_appcontext


@click.command(name='create_tables')
@with_appcontext
def create_database():
    create_db()
