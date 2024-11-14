from openpyxl import load_workbook
import pandas as pd
import json  

class Excel:

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.wb = load_workbook(caminho_arquivo)

from openpyxl import load_workbook
import pandas as pd
import json  

class Excel:

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.wb = load_workbook(caminho_arquivo)

    def Gerar_Dicionario_de_Grupos_de_Colunas(self, nome_aba, CaminhoArquivoJson=False, NomeGrupoPrimeiraLinha=False, 
                                                index =  False):
        df = pd.read_excel(self.caminho_arquivo, sheet_name=nome_aba)
        dados_grupos = {}
        grupo_numero = 1  
        colunas_grupo = {}
        nome_grupo = f'Grupo {grupo_numero}'  
        Ncol = 0
        for coluna in df.columns:
            if df[coluna].isnull().all():
                if colunas_grupo: 
                    grupo_df = pd.DataFrame(colunas_grupo).dropna(how="all").fillna("")
                    if index:
                        coluna_index = list(range(len(grupo_df)))
                        grupo_df_indexado = {'index': coluna_index}
                        grupo_df = pd.DataFrame(grupo_df_indexado).join(grupo_df.reset_index(drop=True))
                    dados_grupos[nome_grupo] = grupo_df.to_dict(orient="records")
                    grupo_numero += 1
                    nome_grupo = f'Grupo {grupo_numero}'
                    colunas_grupo = {} 
                    Ncol = 0
            else:
                if NomeGrupoPrimeiraLinha:
                    if Ncol == 0: nome_grupo = coluna
                    Ncol += 1
                    header = df[coluna].iloc[0]
                    dados = df[coluna].iloc[1:].reset_index(drop=True)  
                    colunas_grupo[header] = dados
                else:
                    colunas_grupo[coluna] = df[coluna]  
        if colunas_grupo:
            grupo_df = pd.DataFrame(colunas_grupo).dropna(how="all")
            if index:
                coluna_index = list(range(len(grupo_df)))
                grupo_df_indexado = {'index': coluna_index}
                grupo_df = pd.DataFrame(grupo_df_indexado).join(grupo_df.reset_index(drop=True))
            dados_grupos[nome_grupo] = grupo_df.to_dict(orient="records")
        if CaminhoArquivoJson:
            with open(CaminhoArquivoJson, "w", encoding="utf-8") as json_file:
                json.dump(dados_grupos, json_file, ensure_ascii=False, indent=4)
        return dados_grupos
