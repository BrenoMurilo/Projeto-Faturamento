from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QMainWindow, QLabel, QVBoxLayout, QComboBox, QLineEdit, QListWidget, QStackedWidget
from PyQt6.QtCore import Qt, QTimer, QEvent
import sys
from pynput.keyboard import Key, Controller
import pyautogui
import time
from PyQt6.QtGui import QColor, QFont, QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QColor, QKeyEvent, QKeySequence
from PyQt6.QtCore import QSize
import os
from GUI.PyQt.Objetos_Personalizados import CustomComboBox, CustomTable, CustomButtonClick


class Pag_Parâmetros(QWidget):
    def __init__(self, stacked_widget, parent):
        super().__init__()
        self.parent = parent
        self.geometry_base =  parent.geometry()
        self.stacked_widget = stacked_widget
        self.keyboard = Controller()
        self.filtrarTabela= False
        self.last_click_time = 0
        self.double_click_simulated = False
        self.setWindowTitle("Ferramenta de automação")
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Template - Parâmetros (2).png")
        label = QLabel()
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        self.list = parent.tipos_parametros()
        self.dados = parent.parâmetros(self.list[0])

        self.table1 = CustomTable(
            parent = self, geometry = [235, 240, 737, 310],
            qtd_cols_visible = 4, rows_height = 30, data = self.dados, search_option = True, col_ocultar = 1)  
        self.table1.clicked.connect(self.teste)

        self.comboBox1 = CustomComboBox(parent=self, itens=self.list, geometry=[240, 160, 220, 25],list_height=len(self.list) * 20)  
        self.comboBox1.combo_box.setItemText(0,self.list[0])
        self.comboBox1.list_widget.itemClicked.connect(self.atualizar)

        self.button_salvar = CustomButtonClick(self,[885,126,50,61], trasnparente=True)
        self.button_salvar.clicked.connect(self.salvar)

        self.button_limpar_filtros = CustomButtonClick(self,[775,124,82,63], trasnparente=True)
        self.button_limpar_filtros.clicked.connect(self.limpar_filtros_tabela)

        self.button_atualizar = CustomButtonClick(self,[685,124,60,63], trasnparente=True)
        self.button_atualizar.clicked.connect(self.atualizar)

        self.button_exportar= CustomButtonClick(self,[585,124,60,63], trasnparente=True)
        self.button_exportar.clicked.connect(self.exportar_parametros)

        self.button_importar= CustomButtonClick(self,[485,124,60,63], trasnparente=True)
        self.button_importar.clicked.connect(self.importar)

        self.button1 = CustomButtonClick(self,[25,120,180,50],trasnparente=True)
        self.button1.clicked.connect(self.go_to_page_inicial)
        
        self.button2 = CustomButtonClick(self,[25,190,180,50],trasnparente=True)
        self.button2.clicked.connect(self.go_to_page_Emails)

        self.button3 = CustomButtonClick(self,[25,340,180,50],trasnparente=True)
        self.button3.clicked.connect(self.go_to_page_Relatorios)

        self.filtrarTabela = True
        self.setFocus()

    def go_to_page_inicial(self):
        self.stacked_widget.setCurrentIndex(0)   

    def go_to_page_Emails(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_page_Relatorios(self):
        self.stacked_widget.setCurrentIndex(3)
        
    def mousePressEvent(self, event):
        self.comboBox1.list_widget.hide() 
        if self.rect().contains(event.pos()):
            self.keyboard.press(Key.enter)
            self.table1.LimparSelecao()
            self.comboBox1.list_widget.hide() 
            self.comboBox1.search_line_edit.hide()
            self.comboBox1.icon_label.hide()
            self.comboBox1.search_line_edit.setText("")     

    def teste(self):
            self.comboBox1.list_widget.hide() 
            self.comboBox1.search_line_edit.hide()
            self.comboBox1.icon_label.hide()
            self.comboBox1.search_line_edit.setText("")

    def simulate_double_click(self):
        if not self.double_click_simulated:
            x, y = pyautogui.position()   
            pos = self.mapToGlobal(self.rect().topLeft())
            pyautogui.doubleClick(x, y) 
            self.double_click_simulated = True

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
    
    def atualizar(self, item):
        param_selecionado = self.comboBox1.combo_box.itemText(0)
        dados = self.parent.parâmetros(param_selecionado)
        filtros = self.table1.ObterLinha(0)
        geometry= self.table1.geometry().getRect()
        if self.table1 is not None:
            self.table1.clicked.disconnect()         
            self.layout().removeWidget(self.table1)  
            self.table1.deleteLater()                
            self.table1 = None                     
        self.table1 = CustomTable(
            parent=self,
            geometry=[*geometry],
            qtd_cols_visible=4,
            rows_height=30,
            data=dados,
            search_option=True,
            col_ocultar = 1
        )
        self.table1.clicked.connect(self.teste)  
        self.table1.show() 
        self.table1.stackUnder(self.comboBox1)
        if not item:
            self.table1.PrencherLinha(0,filtros)
            self.show_message_box("Dados atualizados com sucesso!")

    def salvar(self):
        tipo_param = self.comboBox1.combo_box.itemText(0)
        dados = self.table1.Dados()
        self.parent.set_parametro(tipo_param, dados[1:])
        if tipo_param == 'Dados_Escritórios':
            self.parent.atualizar_tabela_escritorios(dados[1:])
            print('tabela escritorio atualizada')
        self.table1.dados = self.parent.parâmetros(tipo_param)
        self.show_message_box("Dados salvos com sucesso!")


    def limpar_filtros_tabela(self):
        self.table1.limpar_filtros()

    def importar(self):
        caminho_arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Escolha um arquivo",
            "",
            ";Arquivos de planilha (*.xlsx)"
        )
        if caminho_arquivo:
            resultado = self.parent.importar_parametros(caminho_arquivo)
            if not resultado:
                self.show_message_box("Parâmetros importados com sucesso!")
            else:
                if isinstance(resultado, str):
                    self.show_message_box(resultado)
                    return
                if resultado["dict1"]["keys"]:
                    key = resultado["dict1"]["keys"][0]
                    self.show_message_box(f"A tabela {key} não foi localizada nos parâmetros!")
                    return
                if resultado["dict1"]["campos"]:
                    campo = resultado["dict1"]["campos"][0]
                    self.show_message_box(f"O campo {campo} não foi localizado nos parâmetros!")
                    return
                if resultado["dict2"]["keys"]:
                    key = resultado["dict2"]["keys"][0]
                    self.show_message_box(f"A tabela {key} não foi localizada na planilha!")
                    return
                if resultado["dict2"]["campos"]:
                    campo = resultado["dict2"]["campos"][0]
                    self.show_message_box(f"O campo {campo} não foi localizado na planilha!")

    def exportar_parametros(self):
        self.parent.exportar_parametros()


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
        self.resize_widget(self.button_atualizar)
        self.resize_widget(self.button_exportar)
        self.resize_widget(self.button_importar)
        self.resize_widget(self.button_salvar)
        self.resize_widget(self.button_limpar_filtros)
        self.resize_widget(self.table1)       
        self.resize_widget(self.comboBox1.combo_box)
        self.comboBox1.resize()
        self.geometry_base = self.geometry()
        


  

        
        