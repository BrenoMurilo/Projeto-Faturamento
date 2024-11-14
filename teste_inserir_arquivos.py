from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from config import config
from models import Escritorios, Arquivos
from datetime import datetime
import os


def obtercontedubinario(nome_arquivo):
    caminho_arquivo = os.path.join(r"C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\Planilhas de faturamento", 
                                   nome_arquivo)
    with open(caminho_arquivo, "rb") as arquivo:
        conteudo_binario = arquivo.read()
        return conteudo_binario


conteudo_arquivo1 = obtercontedubinario('Faturamento - BLA - 12.11.2024.xlsx')

novo_arquivo = Arquivos(
    id_escritorio=3,                                               
    data_geracao= datetime.now(), 
    nome_arquivo="Faturamento - BLA - 12.11.2024.xslx",  
    arquivo = obtercontedubinario('Faturamento - BLA - 12.11.2024.xlsx') 
)

novo_arquivo2 = Arquivos(
    id_escritorio=1,                                                
    data_geracao=datetime.now(), 
    nome_arquivo="Faturamento - GPA - 12.11.2024.xlsx",  
    arquivo = obtercontedubinario('Faturamento - GPA - 12.11.2024.xlsx')
)

novo_arquivo3 = Arquivos(
    id_escritorio=2,                                                    
    data_geracao=datetime.now(),    
    nome_arquivo="Faturamento - LTB - 12.11.2024.xlsx",  
    arquivo = obtercontedubinario('Faturamento - LTB - 12.11.2024.xlsx')
)


db = SqlAlchemy(config.dados['connections']['database_url'])
db.iniciar_sessao()
db.LimparDadosTabela(Arquivos)
db.AdicionarRegistro(novo_arquivo)
db.AdicionarRegistro(novo_arquivo2)
db.AdicionarRegistro(novo_arquivo3)
db.SalvarAlteracoes()
db.Fechar_sessao()
print('Arquivos inseirdos com sucesso')

db.iniciar_sessao()
registros =db.ObterTodosRegistros(Arquivos,True)
db.Fechar_sessao()
id = registros[0]['id']
print(f'aqui estão os registros: {registros}')
