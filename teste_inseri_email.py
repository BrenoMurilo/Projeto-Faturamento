from config import config, config_param, config_email
from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from models import Escritorios, Arquivos, Emails
from datetime import datetime


def substituir_variaveis(text, linha_arquivo):
    escritorio = db.ObterCampo(Escritorios, 'id',linha_arquivo['id_escritorio'],'nome') 
    return text.replace(
        "[escritório]",escritorio).replace(
            "[data]",datetime.now().strftime("%d/%y/%Y"))

db = SqlAlchemy(config.dados['connections']['database_url'])
db.iniciar_sessao()
arquivos = db.ObterTodosRegistros(Arquivos,True)
padrao = config_email.dados['Email']
db.LimparDadosTabela(Emails)

for linha in arquivos:
    novo_email = Emails(
        remetente = padrao['remetente'],
        destinatario = db.ObterCampo(Escritorios, 'id',linha['id_escritorio'],'email_destinatario') ,
        cc = padrao['cc'],
        assunto =  substituir_variaveis(padrao['assunto'],linha),
        corpo =  substituir_variaveis(padrao['corpo'],linha),
        data_envio = None
    )
    db.AdicionarRegistro(novo_email)

#db.ExcluirTabela(Arquivos)
#db.ExcluirTabela(Emails)
#db.CriarRecriarTabelas()
emails = db.ObterTodosRegistros(Emails)
print(f'aqui estão os registros: {emails}')
db.Fechar_sessao()



