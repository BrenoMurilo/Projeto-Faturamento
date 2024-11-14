from Drivers.Documents_Drivers.JsonDriver import JsonDriver

class Config(JsonDriver):

    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.dados = self.carregar_json()
        
config = Config('Config.json')
config_param = Config('Config_Parâmetros.json')
config_email = Config('Config_Email.json')




