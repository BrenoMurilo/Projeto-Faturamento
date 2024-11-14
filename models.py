
from Drivers.DataBase_Drivers.SqlAlchemy import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey, LargeBinary, DateTime


class Escritorios(Base):
    __tablename__ = 'Escritorios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    sigla = Column(String)
    email_destinatario = Column(String)

class Emails(Base):
    __tablename__ = 'Emails'
    id = Column(Integer, primary_key=True, autoincrement=True)
    remetente = Column(String)
    destinatario = Column(String)
    cc = Column(String)
    assunto = Column(String)
    corpo = Column(String)
    data_envio = Column(DateTime)

class Arquivos(Base):
    __tablename__ = 'Arquivos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_escritorio = Column(Integer, ForeignKey('Escritorios.id'))
    data_geracao = Column(DateTime)
    nome_arquivo = Column(String)
    arquivo = Column(LargeBinary)

