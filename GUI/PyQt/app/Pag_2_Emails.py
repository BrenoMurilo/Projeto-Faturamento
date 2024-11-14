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
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Template - Emails (5).png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        label_layout = QVBoxLayout(label)
        label.setLayout(label_layout)
        self.keyboard = Controller()

        self.button1 = CustomButtonClick(self,[25,120,178,50],trasnparente=True)
        self.button1.clicked.connect(self.go_to_page_Inicial)

        self.button2 = CustomButtonClick(self,[25,265,178,50],trasnparente=True)
        self.button2.clicked.connect(self.go_to_page_parametros)

        self.button3 = CustomButtonClick(self,[25,340,180,50],trasnparente=True)
        self.button3.clicked.connect(self.go_to_page_Relatorios)

        self.button4 = CustomButtonClick(self,[267,110,80,80],trasnparente=True)
        self.button4.clicked.connect(self.abrir_janela_Emails_Geral)

        self.dados = parent.arquivos_pendentes()

        self.table1 = CustomTable(
                parent = self, geometry = [235, 240, 737, 310],
                qtd_cols_visible = 4, rows_height = 30, data = self.dados, cols_icon = True,
                path_icons_cols = r"C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\GUI\PyQt\lupa.png",
                widths_fixed_cols = [10,320,200,170,30],col_flag=3, col_ocultar = 1,
                style="""
                    QTableWidget {
                        border: none; /* Remove as bordas da tabela */
                        gridline-color: transparent; /* Remove as linhas de grade */
                    },
                    QTableWidget::item:selected {
                        background-color: red; /* Cor de fundo da seleção */
                        color: white; /* Cor do texto da seleção */
                    }
                    """
                ) 
        
        self.table1.itemClicked.connect(self.itemDetalheClicado)

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
         ConfigurarEmail(self.parent,self.table1.item(item.row(),0).text()).exec()

class ConfigurarEmailsGeral(QDialog):

    def __init__(self, parent):
        super().__init__()
        self.keyboard = Controller()
        self.parent = parent
        self.setWindowTitle("Configurar emails")
        pg = parent.geometry()
        self.setGeometry(pg.x() + 220, pg.y() + 50, pg.width() - 800, pg.height() - 500)
        self.setFixedSize(pg.width() - 421, pg.height() - 86)
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Configurar e-mails geral (2).png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        label_layout = QVBoxLayout(label)
        label.setLayout(label_layout)
        self.labels_edit = []
        em = parent.padrao_email()
        self.remetente = CustomLabel(self, [123,37,418,30],transparente=True, append_list=True, text = em['remetente'])
        self.destiny_edit = CustomLabel(self, [123,91,418,30], True ,transparente=True,append_list=True, text = em['destinatário'])
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
        self.parent.atualizar_tabela_emails()
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
        
                            
class ConfigurarEmail(QDialog):

    def __init__(self, parent, id):
        super().__init__()
        self.keyboard = Controller()
        self.setWindowTitle("Configurar email")
        pg = parent.geometry()
        self.setGeometry(pg.x() + 220, pg.y() + 50, pg.width() - 800, pg.height() - 500)
        self.setFixedSize(pg.width() - 421, pg.height() - 86)
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Configurar e-mails dos escritórios (2).png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        label_layout = QVBoxLayout(label)
        label.setLayout(label_layout)
        self.labels_edit = []
        em = parent.RegistroEmail(id)
        self.remetente = CustomLabel(self, [123,37,418,30],transparente=True, append_list=True, text = em['remetente'])
        self.destiny_edit = CustomLabel(self, [123,91,418,30], True ,transparente=True,append_list=True, text = em['destinatario'])
        self.cc_edit = CustomLabel(self, [123,145,418,30], True,transparente=True,append_list=True, text = em['cc'])
        self.assunto_edit = CustomLabel(self, [123,195,418,30], True,transparente=True,append_list=True, text = em['assunto'])
        self.corpo_edit = CustomLabel(self, [125,323,420,170], True, paragrafo=True,transparente=True,append_list=True, text = em['corpo'])

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
                self.keyboard.press(Key.enter)
                for label in self.labels_edit:
                    label.finish_editing()
                        

