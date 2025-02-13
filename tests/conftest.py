import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from fastapiproj.app import app
from fastapiproj.config.database import get_session
from fastapiproj.models.model import table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # Inicia conexão (Cria o banco)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        # o teste acontece até aqui e depois vem o tear down
        yield session  # Gerador

    # Dropa conexão (Tear Down)
    table_registry.metadata.drop_all(engine)
