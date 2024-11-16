import json
import pandas as pd
import openpyxl
from pathlib import Path
import os

class JsonDriver:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.dados = self.carregar_json()

    def carregar_json(self):
        try:
            with open(self.nome_arquivo, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            print(f"Arquivo '{self.nome_arquivo}' não encontrado.")
            return {}
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON.")
            return {}

    def listar_valores_chave(self, chave_superior):
            if chave_superior not in self.dados:
                return []
            dados = self.dados[chave_superior]
            if not isinstance(dados, list) or not all(isinstance(item, dict) for item in dados):
                return []
            nomes_colunas = list(dados[0].keys())
            tabela = [nomes_colunas]
            for item in dados:
                linha = [item.get(coluna, "") for coluna in nomes_colunas]
                tabela.append(linha)
            return tabela
    
    def salvar_alteracoes(self):
           with open(self.nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=4)

    def gerar_planilha(self, nome_planilha):
        df = pd.DataFrame()
        for i, key in enumerate(self.dados.keys()):
            dados = self.listar_valores_chave(key)
            if df.empty:
                df = pd.DataFrame(dados)
                df.columns = dados[0]
                df = df.drop(0)
                if 'index' in df.columns:
                    df = df.drop(columns='index')
            else:
                new_df = pd.DataFrame(dados).reset_index(drop=True)
                new_df.columns = dados[0]
                new_df = new_df.drop(0)
                if 'index' in new_df.columns:
                    new_df = new_df.drop(columns='index')
                df = df.join(new_df, lsuffix='_df', rsuffix=f'_new_{i}')
            vazios = " " * (i +1)
            df[vazios] = None
        downloads_folder = str(Path.home() / "Downloads")
        nome_planilha = nome_planilha + ".xlsx" if not nome_planilha.endswith(".xlsx") else nome_planilha
        caminho_planilha = os.path.join(downloads_folder, nome_planilha) 
        df.to_excel(caminho_planilha,index=False)
        os.startfile(caminho_planilha)
            
              



