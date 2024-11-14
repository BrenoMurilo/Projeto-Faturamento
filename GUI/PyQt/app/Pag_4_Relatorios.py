from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QMainWindow, QLabel, QComboBox, QLineEdit, QListWidget, QStackedWidget
from PyQt6.QtCore import Qt, QTimer, QEvent
import sys
from pynput.keyboard import Key, Controller
import pyautogui
import time
from PyQt6.QtGui import QColor, QFont, QBrush, QIcon, QPixmap, QKeyEvent, QKeySequence
from PyQt6.QtCore import QSize
import os
from GUI.PyQt.Objetos_Personalizados import CustomComboBox, CustomTable, CustomButtonClick
from GUI.PyQt.app.Pag_3_Parâmetros import Pag_Parâmetros

class Page_Relatorios(QWidget):
    def __init__(self, stacked_widget, parent):
        super().__init__()
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Template - Relatórios (11).png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        label_layout = QVBoxLayout(label)
        label.setLayout(label_layout)

        self.button1 = CustomButtonClick(self,[25,120,180,50],trasnparente=True)
        self.button1.clicked.connect(self.go_to_page_inicial)
        
        self.button2 = CustomButtonClick(self,[25,190,180,50],trasnparente=True)
        self.button2.clicked.connect(self.go_to_page_Emails) 

        self.button3 = CustomButtonClick(self,[25,265,180,50],trasnparente=True)
        self.button3.clicked.connect(self.go_to_page_parametros)

        self.list3=["xlsx", "csv"] 
        self.comboBox3 = CustomComboBox(parent=self, itens=self.list3, geometry=[240, 305, 310, 25],
                                        list_height = len(self.list3) * 20, search=False)

        self.list2=["escritorio 1", "escritorio 2"] 
        self.comboBox2 = CustomComboBox(parent=self, itens=self.list2, geometry=[240, 230, 310, 25],
                                        list_height = len(self.list2) * 20, search=False)

        self.list1=["Entradas", "Saidas", "Entradas e saidas"] 
        self.comboBox1 = CustomComboBox(parent=self, itens=self.list1, geometry=[240, 160, 310, 25],
                                        list_height = len(self.list1) * 20, search=False)           
    
    def go_to_page_inicial(self):
        self.stacked_widget.setCurrentIndex(0)   

    def go_to_page_Emails(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_page_parametros(self):
        self.stacked_widget.setCurrentIndex(2)

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
    
    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
            self.comboBox1.hide_list() 
            self.comboBox2.hide_list() 
            self.comboBox3.hide_list() 
            


