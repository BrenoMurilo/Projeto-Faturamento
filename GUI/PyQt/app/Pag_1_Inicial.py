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

class Page_Inicial(QWidget):
    def __init__(self, stacked_widget, parent):
        super().__init__()
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\breno\Downloads\Template - Página inicial.png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.layout.addWidget(label)
        label_layout = QVBoxLayout(label)
        label.setLayout(label_layout)

        self.button1 = CustomButtonClick(self,[25,195,180,50],trasnparente=True)
        self.button1.clicked.connect(self.go_to_page_Emails)

        self.button2 = CustomButtonClick(self,[25,265,180,50],trasnparente=True)
        self.button2.clicked.connect(self.go_to_page_parametros)

        self.button3 = CustomButtonClick(self,[25,340,180,50],trasnparente=True)
        self.button3.clicked.connect(self.go_to_page_Relatorios)

    def go_to_page_Emails(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_page_parametros(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_page_Relatorios(self):
        self.stacked_widget.setCurrentIndex(3)

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


