import sys
import os
# sys.path.insert(0, os.path.abspath("."))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import responses
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.app import create_app

@pytest.fixture(scope='session')
def engine():
    return create_engine('postgresql://user:password@localhost:5432/test_sentiment')

@pytest.fixture(scope='function')
def db_session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    Base.metadata.drop_all(engine)
    session.close()

@pytest.fixture
def app(engine):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        with responses.RequestsMock() as rsps:
            test_client.rsps = rsps  # Attach responses to client
            yield test_client