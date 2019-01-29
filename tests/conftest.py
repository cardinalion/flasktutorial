# contains setup functions called fixtures that each test will use

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__),'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # creates and opens a temporary file, returning the object and path
    db_fd, db_path = tempfile.mkstemp()

    # overrides the DATABASE path, not points to the instance folder
    # test mode
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


# tests use the client to make requests without running the server
@pytest.fixture
def client(app):
    return app.test_client()


# creates a runner that can call Click commands registered
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


# call auth.login() in a test to log in as the test user
@pytest.fixture
def auth(client):
    return AuthActions(client)

