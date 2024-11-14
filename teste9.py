from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from models import Escritorios, Arquivos, Emails
from config import config, config_param, config_email

db = SqlAlchemy(config.dados['connections']['database_url'])
db.iniciar_sessao()


#db.ExcluirTabela(Emails)
#db.CriarRecriarTabelas()
consulta = (
     db.session.query(Arquivos.id, Escritorios.nome.label("Escritório"), Emails.destinatario)
        .join(Escritorios, Arquivos.id_escritorio == Escritorios.id, isouter=True) 
        .join(Emails, Arquivos.id == Emails.id, isouter=True)  
        .filter(Emails.data_envio == None)
        )
consulta2 = (
        db.session.query(
            Arquivos.id, 
        )
        .join(Emails, Arquivos.id == Emails.id)  
        .filter(Emails.data_envio == None)
        )
resultado = db.converter_consulta_list_of_list(consulta2)[1:]
tabela = db.ObterTodosRegistros(Emails, tipo_retorno='list_of_list')
db.Fechar_sessao()
print(F'AQUI ESTÃO OS DADOS {resultado}')