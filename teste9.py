from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from models import Escritorios, Arquivos, Emails
from config import config, config_param, config_email
import os

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

def obtercontedubinario(nome_arquivo):
    caminho_arquivo = os.path.join(r"C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\Planilhas de faturamento", 
                                   nome_arquivo)
    with open(caminho_arquivo, "rb") as arquivo:
        conteudo_binario = arquivo.read()
        return conteudo_binario


conteudo_arquivo = obtercontedubinario('Faturamento - LTB - 12.11.2024.xlsx')

resultado = db.converter_consulta_list_of_list(consulta2)[1:]
tabela = db.ObterTodosRegistros(Escritorios, tipo_retorno='list_of_list')
registro_escritorio = db.ObterRegistro(Escritorios,'id',2)
db.Fechar_sessao()
#db.AlterarCampo(Arquivos,'id',3,'arquivo',conteudo_arquivo)
print(F'AQUI ESTÃO OS DADOS {tabela}')