import json

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



