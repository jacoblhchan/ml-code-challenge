# This sys.path hack is required because of sibling directory imports. There has to be a
#  better way.
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import pytest
from sqlalchemy import event
from sqlalchemy_utils import create_database, database_exists
from src import create_app
from src.config import TestConfig
from src.models import db as _db


@pytest.fixture(scope='session')
def app(request):
    """Returns session-wide application"""
    config = TestConfig()
    database_url = config.SQLALCHEMY_DATABASE_URI

    # Ensure the test database exists
    if not database_exists(database_url):
        create_database(database_url)

    return create_app(config)


@pytest.fixture(scope='session')
def db(app, request):
    """Returns session-wide initialised database"""
    with app.app_context():
        _db.create_all()


@pytest.fixture(scope='function')
def session(app, db, request):
    """Returns function-scoped session"""
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()

        options = dict(bind=connection, binds={})
        session = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        session.begin_nested()

        @event.listens_for(session(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                session.begin_nested()

        _db.session = session
        yield session

        session.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(app, session):
    with app.test_client() as client:
        yield client
