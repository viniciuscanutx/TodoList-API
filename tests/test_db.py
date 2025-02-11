from sqlalchemy import select

from fastapiproj.models.model import User


def test_create_user(session):
    user = User(
            username='kleberpereira',
            email='kleber@pereira.com',
            password='minhasenha@123',
    )
    # Adicionando as infos de User a sessão.
    session.add(user)
    # Comitando as informações para o Banco de Dados.
    session.commit()
    result = session.scalar(
            select(User).where(User.email == 'kleber@pereira.com')
    )

    assert result.id == 1
