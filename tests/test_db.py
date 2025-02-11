from sqlalchemy import create_engine

from fastapiproj.models.model import User, table_registry


def test_create_user():
    engine = create_engine('sqlite:///database.db')

    table_registry.metadata.create_all(engine)

    user = User(
        username='kleberpereira',
        email='kleber@pereira.com',
        password='minhasenha@123',
    )
    
    
    assert user.username == 'kleberpereira'
