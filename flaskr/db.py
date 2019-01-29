import sqlite3

import click
from flask import current_app, g
"""
g: unique for each request, store data that might be accessed 
    by multiple functions, the connection is stored and reused
current_app: points to Flask application handling the request
"""
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # establish a connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # return rows that behave like dicts
        # allows accessing the columns by name
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    # open a file relative to the package
    # Cuz may not know the location when deploying the application
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# defines a command line command
@click.command('init_db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        pass
    pass


# registration: close_db, init_db_command with application instance
# ?
def init_app(app):
    # call the function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    # add a new command called with flask command
    app.cli.add_command(init_db_command)
    pass

# flask init_db
