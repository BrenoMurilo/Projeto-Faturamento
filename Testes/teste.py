from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from config import config

db = SqlAlchemy(config['connections']['database_url'])
db.iniciar_sessao()
db.Fechar_sessao()
print('Funcionou')


