"""
Exemplo de setup_database_engine para PostgreSQL com SQLAlchemy.
"""

import os
import json
import logging
from time import sleep
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, JSON, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class EnvironmentalData(Base):
    """
    Classe que representa a tabela 'environmental_data'.
    """
    __tablename__ = 'environmental_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    point = Column(String, nullable=False)
    value = Column(JSON, nullable=False)  # {"value": <valor>}
    datetime = Column(Integer, nullable=False)  # Unix timestamp

    def __repr__(self):
        return json.dumps({
            "point": self.point,
            "value": self.value,
            "datetime": self.datetime
        })


def setup_database_engine(db_user, db_pass, db_host, db_port, db_name,
                          pool_size=10, max_overflow=20, echo=False):
    """
    Configura e retorna o engine do SQLAlchemy para PostgreSQL.

    :param db_user: Usuário do banco de dados.
    :param db_pass: Senha do banco de dados.
    :param db_host: Endereço do host do banco de dados.
    :param db_port: Porta do banco de dados.
    :param db_name: Nome do banco de dados.
    :param pool_size: Tamanho do pool de conexões.
    :param max_overflow: Número máximo de conexões além do pool_size.
    :param echo: Ativa/desativa logs SQL.
    :return: engine configurado.
    """
    database_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(
        database_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True
    )
    # Cria as tabelas definidas no modelo, se não existirem.
    Base.metadata.create_all(engine)
    return engine


# Configuração do Session Factory usando scoped_session para threadsafe
def get_session_factory(engine):
    SessionFactory = sessionmaker(bind=engine)
    return scoped_session(SessionFactory)


@contextmanager
def session_scope(Session):
    """
    Gerenciador de contexto para a sessão do banco de dados.
    Garante commit ou rollback e fechamento da sessão.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error("Erro na sessão: %s", e)
        session.rollback()
        raise
    finally:
        session.close()


def save_data(point, session_factory, max_retries=3):
    """
    Salva os dados no PostgreSQL de maneira robusta.

    :param point: Nome do ponto.
    :param value: Valor do ponto.
    :param dt: Timestamp (Integer).
    :param session_factory: Fábrica de sessão configurada.
    :param max_retries: Número máximo de tentativas em caso de falha temporária.
    """
    retries = 0
    while retries < max_retries:
        try:
            with session_scope(session_factory) as session:
                data = EnvironmentalData(
                    point=point.get_id(),
                    value={"value": point.get_value()},
                    datetime=point.get_last_update()  # Armazenado como inteiro (Unix timestamp)
                )
                session.add(data)
                session.commit()
                logger.info("Dados salvos: %s", data)
            break  # Sai do loop se tudo ocorrer bem
        except Exception as e:
            retries += 1
            logger.error("Tentativa %s: erro ao salvar dados: %s", retries, e)
            sleep(1)
            if retries == max_retries:
                logger.error("Número máximo de tentativas atingido. Dados não foram salvos.")


# Exemplo de uso
if __name__ == '__main__':
    # As informações de configuração podem ser obtidas de qualquer fonte.
    # Aqui, estamos usando variáveis de ambiente ou valores padrão.
    DB_USER = os.getenv("DB_USER", "seu_usuario")
    DB_PASS = os.getenv("DB_PASS", "sua_senha")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "seu_banco")

    # Configura o engine usando a função setup_database_engine
    engine = setup_database_engine(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, echo=False)

    # Obtém a fábrica de sessões
    Session = get_session_factory(engine)

    # Exemplo de inserção de dados
    point_name = "temperature_sensor_1"
    value = 25.3
    timestamp = int(datetime.now().timestamp())

    save_data(point_name, value, timestamp, Session)

    # Consulta os dados salvos para verificação
    with session_scope(Session) as session:
        records = session.query(EnvironmentalData).all()
        for record in records:
            logger.info("Registro encontrado: %s", record)
