import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Janela com Plano de Fundo Responsivo")
        self.setMinimumSize(600, 400)

        # Criação do widget central e layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # QLabel para exibir a imagem de fundo
        self.background_label = QLabel(self)
        pixmap = QPixmap("caminho/para/sua/imagem.jpg")
        self.background_label.setPixmap(pixmap)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # A imagem ocupa toda a janela
        
        # Adicionando outros widgets sobre o plano de fundo
        label = QLabel("Texto sobre o plano de fundo", self)
        layout.addWidget(label)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def resizeEvent(self, event):
        """Ajusta a imagem quando a janela for redimensionada"""
        # Redimensionar a imagem de fundo para cobrir toda a janela
        pixmap = QPixmap("caminho/para/sua/imagem.jpg").scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # A imagem ocupa toda a janela

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
