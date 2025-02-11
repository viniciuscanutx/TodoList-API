import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapiproj.app import app
from fastapiproj.models.model import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')

    # Inicia conexão (Cria o banco)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        # o teste acontece até aqui e depois vem o tear down
        yield session  # Gerador

    # Dropa conexão (Tear Down)
    table_registry.metadata.drop_all(engine)
