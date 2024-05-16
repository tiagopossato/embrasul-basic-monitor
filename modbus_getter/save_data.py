"""
Save messages to the database.
"""
import os
import sys
import json
from datetime import datetime
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, JSON, DateTime, String

# path to the database
DB_PATH = "/opt/monitor/db/monitor.db"

# create the database
Base = declarative_base()
class Data(Base):
    """
    Class to represent the data table.
    """
    # nome da tabela
    __tablename__ = 'data'
    # colunas
    # Identificador único de cada linha
    id = Column(Integer, primary_key=True)
    # Ponto do modelo
    point =  Column(String)
    # Valor do ponto. 
    # Armazenado como JSON para aceitar diferentes tipos de dados
    # Manter o seguinte padrão: {"value": <valor>}
    value = Column(JSON)
    # Data e hora da leitura
    datetime = Column(Integer)  

    def __repr__(self):
        return f'{{"point":{self.point}, "value":{self.value}, "datetime":{self.datetime}}}'

def start_db_session():
    """
    Start a session with the database.
    """
    print(f"DB_PATH: {DB_PATH}")
    engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session

def save_data(point, value, datetime, session):
    """
    Save data to the database.
    """
    try:
        # create the data object
        data = Data(
            point = point,
            value = {"value": value},
            datetime = datetime)
        # save the data
        session.add(data)
        # commit the data
        session.commit()
        print(data)
    except Exception as e:
        print(f'save_data error: {e}')