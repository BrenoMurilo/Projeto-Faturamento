
from PyQt6.QtWidgets import  QMainWindow,  QStackedWidget, QMessageBox
from GUI.PyQt.app.Pag_1_Inicial import Page_Inicial
from GUI.PyQt.app.Pag_2_Emails import Page_Emails
from GUI.PyQt.app.Pag_3_Parâmetros import Pag_Parâmetros
from GUI.PyQt.app.Pag_4_Relatorios import Page_Relatorios
from config import config, config_param, config_email
from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from models import Escritorios, Arquivos, Emails
from sqlalchemy import literal
from datetime import datetime


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = SqlAlchemy(config.dados['connections']['database_url'])
        self.setWindowTitle("Ferramenta de automação")
        self.setGeometry(100, 50, 1000, 600)
        self.setFixedSize(1003, 600)
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.page_email = Page_Emails(self.stacked_widget, self)
        self.stacked_widget.addWidget(Page_Inicial(self.stacked_widget, self))
        self.stacked_widget.addWidget(Page_Emails(self.stacked_widget, self))
        self.stacked_widget.addWidget(Pag_Parâmetros(self.stacked_widget, self))
        self.stacked_widget.addWidget(Page_Relatorios(self.stacked_widget, self))
    
      
    def show_message_box(self, texto):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Mensagem")
        msg_box.setText(texto)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec() 

    def tipos_parametros(self):
        return list(config_param.dados.keys())
    
    def parâmetros(self, tipo):
       return config_param.listar_valores_chave(tipo)
    
    def padrao_email(self):
        return config_email.dados['Email']
    
    def arquivos_pendentes(self):
        self.db.iniciar_sessao()
        consulta = (
        self.db.session.query(
            Arquivos.id, 
            Escritorios.nome.label("Escritório"), 
            Emails.destinatario, 
            literal(None).label("Enviar?")
        )
        .join(Escritorios, Arquivos.id_escritorio == Escritorios.id, isouter=True) 
        .join(Emails, Arquivos.id == Emails.id, isouter=True)  
        .filter(Emails.data_envio == None)
        )
        resultado = self.db.converter_consulta_list_of_list(consulta)
        self.db.Fechar_sessao()
        return resultado

    def RegistroEmail(self, id):
         print(f'o id é esse {id}')
         self.db.iniciar_sessao()
         texto = self.db.ObterRegistro(Emails,'id',id)
         self.db.Fechar_sessao()
         return texto
    
    def set_padrao_email(self, novo_padrao):
        padrao = config_email.dados['Email']
        for i, chave in enumerate(list(padrao.keys())):
            padrao[chave] = novo_padrao[i]
        config_email.salvar_alteracoes()

    def set_parametro(self, tipo_parametro, novos_dados):
        param = config_param.dados[tipo_parametro]
        for row_idx, linha in enumerate(novos_dados):
            if linha[0] != "":
                index = int(linha[0]) if not isinstance(linha[0], int) else linha[0]
                linha_param = param[index]
                for i, chave in enumerate(list(linha_param.keys())):
                    linha_param[chave] = linha[i]
        config_param.salvar_alteracoes()


    def atualizar_tabela_escritorios(self, data):
        self.db.iniciar_sessao()
        self.db.atualizar_tabela(Escritorios, data)
        self.db.Fechar_sessao()

    def atualizar_tabela_emails(self):
        consulta = (
        self.db.session.query(
            Arquivos.id, 
        )
        .join(Emails, Arquivos.id == Emails.id)  
        .filter(Emails.data_envio == None)
        )
        arquivos_pendentes = [row[0] for row in self.db.converter_consulta_list_of_list(consulta)[1:]]
        padrao = config_email.dados['Email']
        for id_arquivo in arquivos_pendentes:
            registro_arquivo = self.db.ObterRegistro(Arquivos,'id', id_arquivo)
            email_atualizado = Emails(
                remetente = padrao['remetente'],
                destinatario = self.db.ObterCampo(Escritorios, 'id', registro_arquivo['id_escritorio'],'email_destinatario') ,
                cc = padrao['cc'],
                assunto =  self.substituir_variaveis(padrao['assunto'],registro_arquivo),
                corpo =  self.substituir_variaveis(padrao['corpo'],registro_arquivo),
                data_envio = None
            )
            self.db.atualizar_registro(Emails, registro_arquivo['id'],email_atualizado)

    def substituir_variaveis(self, text, registro_arquivo):
        registro_escritorio = self.db.ObterRegistro(Escritorios,'id',registro_arquivo['id_escritorio'])
        return text.replace(
            "[escritório]", registro_escritorio['nome']
            ).replace("[data]",datetime.now().strftime("%d/%y/%Y")
            ).replace("[mês]",datetime.now().strftime("%y")
            ).replace("[ano]",datetime.now().strftime("%Y")
            ).replace("[dia]",datetime.now().strftime("%d")        
            ).replace("[sigla]", registro_escritorio['sigla']
            ).replace("[nome_arquivo]", registro_arquivo['nome_arquivo']
            )          
                  
         
        

    

    


