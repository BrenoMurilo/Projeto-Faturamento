
from PyQt6.QtWidgets import  QMainWindow,  QStackedWidget, QMessageBox
from GUI.PyQt.app.Pag_1_Inicial import Page_Inicial
from GUI.PyQt.app.Pag_2_Emails import Page_Emails
from GUI.PyQt.app.Pag_3_Parâmetros import Pag_Parâmetros
from GUI.PyQt.app.Pag_4_Relatorios import Page_Relatorios
from config import config, config_param, config_email
from config import Config
from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from models import Escritorios, Arquivos, Emails
from sqlalchemy import literal
from datetime import datetime
from Drivers.Documents_Drivers.Excel import Excel
import json


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = SqlAlchemy(config.dados['connections']['database_url'])
        self.planilha = False
        self.config_parametros = config_param
        self.setWindowTitle("Ferramenta de automação")
        self.setGeometry(100, 50, 1000, 600)
        self.base_geometry = self.geometry()
        #self.setFixedSize(1003, 600)
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.page_email = Page_Emails(self.stacked_widget, self)
        self.stacked_widget.addWidget(Page_Inicial(self.stacked_widget, self))
        self.stacked_widget.addWidget(self.page_email)
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
       return self.config_parametros.listar_valores_chave(tipo)
    
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

    def RegistroArquivo(self, id):
         self.db.iniciar_sessao()
         registro = self.db.ObterRegistro(Arquivos,'id',id)
         self.db.Fechar_sessao()
         return registro
    
    def RegistroEmail(self, id):
         self.db.iniciar_sessao()
         registro = self.db.ObterRegistro(Emails,'id',id)
         self.db.Fechar_sessao()
         return registro
    
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


    def atualizar_registro_tabela_emails(self, dados, id):
        email_atualizado = Emails(
            remetente = dados[0],
            destinatario =  dados[1] ,
            cc = dados[2],
            assunto = dados[3],
            corpo = dados[4],
            data_envio = None
        )
        self.db.atualizar_registro(Emails, id, email_atualizado)


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

    
    def atualizar_page_emails(self): 
        self.page_email.atualizar() 

    def abrir_planilha_faturamento(self, id):
        conteudo_binario = self.db.ObterCampo(Arquivos,'id', id, 'arquivo')
        nome_arquivo = self.db.ObterCampo(Arquivos,'id', id, 'nome_arquivo')
        self.planilha = Excel(conteudo_binario = conteudo_binario)
        self.planilha.abrir_editar_planilha_conteudo_binario(nome_arquivo)
                  
    def Salvar_planilha_faturamento(self, id):
        if self.planilha:
            conteudo_atualizado = self.planilha.obter_conteudo_binario_planilha_editada()
            if conteudo_atualizado:
                self.db.atualizar_campo(Arquivos,'id',id,'arquivo',conteudo_atualizado)

    def excluir_planilha_temporaria(self):
        if self.planilha:
            self.planilha.excluir_arquivo_temp_binario()

    def exportar_parametros(self):
        config_param.gerar_planilha("Parâmetros", "Parâmetros")

    def importar_parametros(self, caminho_arquivo):
        wb = Excel(caminho_arquivo)
        try:
            dict = wb.Gerar_Dicionario_de_Grupos_de_Colunas('Parâmetros' ,
                                                            NomeGrupoPrimeiraLinha=True, index=True)
        except:
            return "Os dados do arquivo não estão no formato esperado!" 
        diferencas = self.config_parametros.diferencas_entre_jsons(dict)
        if not diferencas:
            self.config_parametros.salvar_alteracoes(dict)
            self.config_parametros = Config('Config_Parâmetros.json')
            return None
        else:
            return diferencas
        
        

    

    


