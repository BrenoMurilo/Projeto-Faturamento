from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QMainWindow, QLabel, QComboBox, QLineEdit, QListWidget, QStackedWidget
from PyQt6.QtCore import Qt, QTimer, QEvent, pyqtSignal
import sys
from pynput.keyboard import Key, Controller
import pyautogui
import time
from PyQt6.QtGui import QColor, QFont, QBrush, QIcon, QPixmap, QKeyEvent, QKeySequence
from PyQt6.QtCore import QSize
import os
from GUI.PyQt.Objetos_Personalizados import CustomComboBox, CustomTable, CustomButtonClick, CustomLabel
from GUI.PyQt.app.Pag_3_Parâmetros import Pag_Parâmetros

class Page_Emails(QWidget):
    def __init__(self, stacked_widget, parent):
        super().__init__()
        self.keyboard = Controller()
        self.parent = parent
        self.geometry_base =  parent.geometry()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Template - Emails (5).png")
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.layout.addWidget(self.label)
        self.label_layout = QVBoxLayout(self.label)
        self.label.setLayout(self.label_layout)
        self.keyboard = Controller()

        self.button1 = CustomButtonClick(self,[25,120,178,50],trasnparente=True)
        self.button1.clicked.connect(self.go_to_page_Inicial)

        self.button2 = CustomButtonClick(self,[25,265,178,50],trasnparente=True)
        self.button2.clicked.connect(self.go_to_page_parametros)

        self.button3 = CustomButtonClick(self,[25,340,180,50],trasnparente=True)
        self.button3.clicked.connect(self.go_to_page_Relatorios)

        self.button4 = CustomButtonClick(self,[267,110,80,80],trasnparente=True)
        self.button4.clicked.connect(self.abrir_janela_Emails_Geral)

        self.button5 = CustomButtonClick(self,[380,110,80,80],trasnparente=True)
        self.button5.clicked.connect(self.atualizar)

        self.dados = parent.arquivos_pendentes()
        self.table_geometry_base = [235, 240, 737, 310]
        self.fixed_wdth_coluns_base = [10, 320, 200, 170, 30]
        self.table1 = CustomTable(
                parent = self, geometry = self.table_geometry_base ,
                qtd_cols_visible = 4, rows_height = 30, data = self.dados, cols_icon = True,
                path_icons_cols = r"C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\GUI\PyQt\lupa.png",
                widths_fixed_cols = [10,320,200,170,30],col_flag=3, col_ocultar = 1
                ) 
        
        self.table1.itemClicked.connect(self.itemDetalheClicado)
        self.atualizar()

    def go_to_page_Inicial(self):
        self.stacked_widget.setCurrentIndex(0)    
    
    def go_to_page_parametros(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_page_Relatorios(self):
        self.stacked_widget.setCurrentIndex(3)

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
            self.keyboard.press(Key.enter)
            self.table1.LimparSelecao() 

    def show_message_box(self, texto):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Mensagem")
        msg_box.setText(texto)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def CriarBotao(self,geometry,text=""):
        button = QPushButton(text, self)
        button.move(geometry[0], geometry[1])
        button.resize(geometry[2], geometry[3])
        return button
    
    def itemDetalheClicado(self, item):
        if item.column() == self.table1.columnCount() -1:
            self.abrir_janela_Email(item)
    
    def abrir_janela_Emails_Geral(self):
        ConfigurarEmailsGeral(self.parent).exec()

    def abrir_janela_Email(self, item):
         ConfigurarEmail(self.parent, self.table1.item(item.row(),0).text()).exec()

    def resize_widget(self, widget):
        base = self.geometry_base
        per_x = widget.geometry().x() / base.width()
        per_y = widget.geometry().y() / base.height()
        per_width = widget.geometry().width() / base.width()
        per_height = widget.geometry().height() / base.height()
        base_atual = self.parent.geometry()
        widget.setGeometry(int(base_atual.width() * per_x),int(base_atual.height() * per_y), 
                           int(base_atual.width() * per_width), int(base_atual.height() * per_height))
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_widget(self.button1)
        self.resize_widget(self.button2)
        self.resize_widget(self.button3)
        self.resize_widget(self.button4)
        self.resize_widget(self.button5)
        self.resize_widget(self.table1)
        self.geometry_base = self.geometry()

    def atualizar(self):
        self.parent.atualizar_tabela_emails()
        dados = self.parent.arquivos_pendentes()
        if dados is None:
            self.show_message_box("Nenhum dado encontrado.")
            return
        geometry = self.table1.geometry()
        new_fixed_wdth_coluns = [geometry.width() * (width / self.table_geometry_base[2]) for width in self.fixed_wdth_coluns_base]
        if self.table1 is not None:
            self.table1.itemClicked.disconnect()  
            self.table1.deleteLater()  
            self.table1 = None  
        self.table1 = CustomTable(
            parent=self,
            geometry=[*geometry.getRect()],
            qtd_cols_visible=4,
            rows_height=30,
            data=dados,
            cols_icon=True,
            path_icons_cols=r"C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\GUI\PyQt\lupa.png",
            widths_fixed_cols=new_fixed_wdth_coluns,
            col_flag=3,
            col_ocultar=1
        )
        self.table1.itemClicked.connect(self.itemDetalheClicado)
        self.table1.show() 
        if self.stacked_widget.currentIndex() == 1:
            self.show_message_box("Dados atualizados com sucesso!")
            

class ConfigurarEmailsGeral(QDialog):

    def __init__(self, parent):
        super().__init__()
        self.keyboard = Controller()
        self.parent = parent
        self.setWindowTitle("Configurar emails")
        pg = parent.geometry()
        self.geometry_base = parent.base_geometry
        per_x =  220 / self.geometry_base.width()
        per_y = 50 / self.geometry_base.height()
        per_width = (self.geometry_base.width() - 421) /  self.geometry_base.width()
        per_height = (self.geometry_base.height() - 86) / self.geometry_base.height()
        self.setGeometry(int(pg.x() + pg.width() * per_x),int(pg.y() + pg.height() * per_y), 
                           int(pg.width() * per_width), int(pg.height() * per_height))
        self.setFixedSize(int(pg.width() * per_width), int(pg.height() * per_height))
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Configurar e-mails geral (3).png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        label_layout = QVBoxLayout(label)
        label.setLayout(label_layout)
        self.labels_edit = []
        em = parent.padrao_email()
        self.remetente = CustomLabel(self, [123,37,418,30],transparente=True, append_list=True, text = em['remetente'])
        self.destiny_edit = CustomLabel(self, [123,91,418,30],transparente=True,append_list=True, text = em['destinatário'])
        self.cc_edit = CustomLabel(self, [123,145,418,30], True,transparente=True,append_list=True, text = em['cc'])
        self.assunto_edit = CustomLabel(self, [123,195,418,30], True,transparente=True,append_list=True, text = em['assunto'])
        self.corpo_edit = CustomLabel(self, [125,323,418,170], True, paragrafo=True,transparente=True,append_list=True, text = em['corpo'])
        self.button_salvar = CustomButtonClick(self, [430,257,130,50],trasnparente=True)
        self.button_salvar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_salvar.clicked.connect(self.salvar)

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
                for label in self.labels_edit:
                    label.finish_editing()

    def salvar(self):
        for label in self.labels_edit:
                label.finish_editing()
        dados = [self.remetente.text(),self.destiny_edit.text(),self.cc_edit.text(),self.assunto_edit.text(),
                self.corpo_edit.text()]
        self.parent.set_padrao_email(dados)
        self.show_message_box("Dados salvos com sucesso!")

    def show_message_box(self, texto):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Mensagem")
        msg_box.setText(texto)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec() 


    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            # Ignora o evento de Enter para evitar que execute a função salvar
            event.ignore()
        else:
            # Se não for Enter, processa normalmente os outros eventos de tecla
            super().keyPressEvent(event)

    def resize_widget(self, widget):
        base = self.geometry_base
        per_x = widget.geometry().x() / base.width()
        per_y = widget.geometry().y() / base.height()
        per_width = widget.geometry().width() / base.width()
        per_height = widget.geometry().height() / base.height()
        base_atual = self.parent.geometry()
        widget.setGeometry(int(base_atual.width() * per_x),int(base_atual.height() * per_y), 
                           int(base_atual.width() * per_width), int(base_atual.height() * per_height))
        
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_widget(self.remetente)
        self.resize_widget(self.destiny_edit)
        self.resize_widget(self.cc_edit)
        self.resize_widget(self.corpo_edit)
        self.resize_widget(self.assunto_edit)
        self.resize_widget(self.button_salvar)
        self.geometry_base = self.parent.geometry()
        
                            
class ConfigurarEmail(QDialog):

    def __init__(self, parent, id):
        super().__init__()
        self.id = id
        self.parent = parent
        self.keyboard = Controller()
        self.setWindowTitle("Configurar email")
        pg = parent.geometry()
        self.geometry_base = parent.base_geometry
        per_x =  220 / self.geometry_base.width()
        per_y = 50 / self.geometry_base.height()
        per_width = (self.geometry_base.width() - 421) /  self.geometry_base.width()
        per_height = (self.geometry_base.height() - 86) / self.geometry_base.height()
        self.setGeometry(int(pg.x() + pg.width() * per_x),int(pg.y() + pg.height() * per_y), 
                           int(pg.width() * per_width), int(pg.height() * per_height))
        self.setFixedSize(int(pg.width() * per_width), int(pg.height() * per_height))
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Configurar e-mails dos escritórios (2).png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        label_layout = QVBoxLayout(label)
        label.setLayout(label_layout)
        self.labels_edit = []
        nome_arquivo = parent.RegistroArquivo(id)['nome_arquivo']
        em = parent.RegistroEmail(id)
        self.remetente = CustomLabel(self, [123,37,418,30],transparente=True, append_list=True, text = em['remetente'])
        self.destiny_edit = CustomLabel(self, [123,91,418,30],True, transparente=True,append_list=True, text = em['destinatario'])
        self.cc_edit = CustomLabel(self, [123,145,418,30], True,transparente=True,append_list=True, text = em['cc'])
        self.assunto_edit = CustomLabel(self, [123,195,418,30], True,transparente=True,append_list=True, text = em['assunto'])
        self.corpo_edit = CustomLabel(self, [125,323,420,170], True, paragrafo=True,transparente=True,append_list=True, text = em['corpo'])
        self.nome_arquivo = CustomLabel(self, [171,250,230,30],transparente=False, append_list=True, text = nome_arquivo, font=10, negrito=True)
        self.button_salvar = CustomButtonClick(self, [430,257,130,50],trasnparente=True)
        self.button_salvar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_salvar.clicked.connect(self.salvar)
        self.button_abrir_arquivo = CustomButtonClick(self, [120,240,50,50],trasnparente=True)
        self.button_abrir_arquivo.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_abrir_arquivo.clicked.connect(self.abrir_arquivo)

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
                self.keyboard.press(Key.enter)
                for label in self.labels_edit:
                    label.finish_editing()

    def show_message_box(self, texto):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Mensagem")
        msg_box.setText(texto)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec() 

    def salvar(self):
        for label in self.labels_edit:
                label.finish_editing()
        dados = [self.remetente.text(),self.destiny_edit.text(),self.cc_edit.text(),self.assunto_edit.text(),
                self.corpo_edit.text()]
        self.parent.atualizar_registro_tabela_emails(dados, self.id)
        self.parent.Salvar_planilha_faturamento(self.id)
        self.show_message_box("Dados salvos com sucesso!")

    def abrir_arquivo(self):
        self.parent.abrir_planilha_faturamento(self.id)

    def closeEvent(self, event):
        self.exclui_arquivo_temp()
        event.accept()

    def exclui_arquivo_temp(self):
        self.parent.excluir_planilha_temporaria()

    def resize_widget(self, widget):
        base = self.geometry_base
        per_x = widget.geometry().x() / base.width()
        per_y = widget.geometry().y() / base.height()
        per_width = widget.geometry().width() / base.width()
        per_height = widget.geometry().height() / base.height()
        base_atual = self.parent.geometry()
        widget.setGeometry(int(base_atual.width() * per_x),int(base_atual.height() * per_y), 
                           int(base_atual.width() * per_width), int(base_atual.height() * per_height))
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_widget(self.remetente)
        self.resize_widget(self.destiny_edit)
        self.resize_widget(self.cc_edit)
        self.resize_widget(self.corpo_edit)
        self.resize_widget(self.assunto_edit)
        self.resize_widget(self.button_salvar)
        self.resize_widget(self.button_abrir_arquivo)
        self.resize_widget(self.nome_arquivo )
        self.geometry_base = self.parent.geometry()



                        

