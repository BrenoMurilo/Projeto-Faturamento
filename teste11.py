from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from models import Escritorios, Arquivos, Emails
from config import config, config_param, config_email
import os
from sqlalchemy import text  


db = SqlAlchemy(config.dados['connections']['database_url'])
db.iniciar_sessao()
db.session.execute(text("DROP TABLE IF EXISTS Cadastros"))
db.SalvarAlteracoes()
db.Fechar_sessao()
print('tabela excluida com sucesso')

