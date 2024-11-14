from PyQt6.QtWidgets import  QWidget, QPushButton,  QCheckBox, QHBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QTextEdit, QComboBox, QLineEdit, QListWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap, QColor
import os
import math

class CustomLabel(QLabel):

    clicked = pyqtSignal() 

    def __init__(self, parent, geometry, edit=False, text='editar', font=12, centralizar=False, 
                 topo=False, transparente=False, paragrafo=False, append_list = False):
        super().__init__(parent)
        
        self.setGeometry(*geometry)
        self.setText(text)
        if centralizar:
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if paragrafo:
            self.setAlignment(Qt.AlignmentFlag.AlignTop) 
        if topo:
            self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setFont(QFont('Arial', font))
        if transparente:
            self.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    border: none;
                }
            """)
        if edit:
            if append_list:
                parent.labels_edit.append(self)
            if paragrafo:
                self.text_edit = QTextEdit(parent)
                self.text_edit.setGeometry(*geometry)
                self.text_edit.setFont(self.font())
                self.text_edit.hide()
                self.mousePressEvent = self.on_label_clicked
                self.text_edit.focusOutEvent = self.finish_editing
                self.text_edit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  
                self.setWordWrap(True)


                if transparente:
                    self.text_edit.setStyleSheet("""
                        QTextEdit {
                            background-color: transparent;
                            border: none;
                        }
                    """)
            else:
                self.line_edit = QLineEdit(parent)
                self.line_edit.setGeometry(*geometry)
                self.line_edit.setFont(self.font())
                self.line_edit.hide()
                self.mousePressEvent = self.on_label_clicked
                self.line_edit.editingFinished.connect(self.finish_editing)
                self.line_edit.setStyleSheet("QLineEdit { border: 1px solid #cccccc; }")  
                if transparente:
                     self.line_edit.setStyleSheet("""
                        QLineEdit {
                            background-color: transparent;
                            border: none;
                        }
                    """)
                if centralizar:
                    self.line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
       

    def parent_clicked(self, event):
            if hasattr(self, 'line_edit') and self.line_edit.isVisible():
                self.finish_editing()
            elif hasattr(self, 'text_edit') and self.text_edit.isVisible():
                self.finish_editing()
            else:
                event.accept()

    def on_label_clicked(self, event):
        if hasattr(self, 'text_edit'):
            self.text_edit.setText(self.text())
            self.text_edit.show()
            self.hide()
            self.text_edit.setFocus()
        elif hasattr(self, 'line_edit'):
            self.line_edit.setText(self.text())
            self.line_edit.show()
            self.hide()
            self.line_edit.setFocus()
    
    def finish_editing(self, event=None):
            if hasattr(self, 'text_edit'):
                if self.text_edit.hasFocus():
                    #texto = self.text_edit.toPlainText().replace('[escritório]','<span style="color: blue;">[escritório]</span>')
                    texto = self.text_edit.toPlainText()
                    self.setText(texto)
                self.text_edit.hide()
                self.text_edit.clearFocus()
            elif hasattr(self, 'line_edit'):
                if self.line_edit.hasFocus():
                    #texto = self.line_edit.text().replace('[escritório]','<span style="color: blue;">[escritório]</span>')
                    texto = self.line_edit.text()
                    self.setText(texto)
                self.line_edit.hide()
                self.line_edit.clearFocus()
            self.show()


class CustomButtonClick(QPushButton):

    def __init__(self, parent, geometry, texto=False, trasnparente = False, style = False):
        super().__init__(parent)
        if texto:
            self.setText(texto)
        self.setGeometry(*geometry)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if trasnparente:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;          
                }
                QPushButton:hover {
                    background-color: rgba(100, 150, 255, 0.5); /* Cor semi-transparente ao passar o mouse */
                }
            """)
        else:
            if style:
                self.setStyleSheet(style)


class CustomComboBox(QWidget):

    def __init__(self,parent, itens, geometry, list_height=184, PlaceholderText="Selecione os itens",
                 search = True, item_height = 20 ):
        super().__init__(parent)
        self.list=itens
        self.item_height=item_height
        self.__geometry__ = geometry
        self.list_height=list_height
        self.combo_box = QComboBox(parent)
        self.combo_box.setGeometry(*geometry)
        self.combo_box.setEditable(False)
        self.combo_box.addItem(PlaceholderText)
        self.line_edit_ofsset = 47 if search else 25
        self.search = search
        if search:
            self.search_line_edit = QLineEdit(parent)
            self.search_line_edit.setGeometry(int(geometry[0]),int(geometry[1]+25),int(geometry[2]),
                                            int(geometry[3]))
            self.search_line_edit.setPlaceholderText("Pesquise...")
            self.search_line_edit.setText('')
            self.search_line_edit.hide()
            self.search_line_edit.setStyleSheet("QLineEdit { background-color: #FDF8F8; }")

            self.icon_label = QLabel(parent)
            self.icon_label.setGeometry(int(geometry[0] + int(geometry[2]) - int(geometry[3])), int(geometry[1] + 25), int(geometry[3]-2), int(geometry[3])) 
            self.icon_label.setPixmap(QPixmap("C:/Users/breno/OneDrive/Documentos/Projeto Faturamento/GUI/PyQt/lupa-arredondada.png").scaled(20, 20))
            self.icon_label.hide()
            self.search_line_edit.textChanged.connect(self.filter_options)

        self.list_widget = QListWidget(parent)
        self.list_widget.addItems(itens)
        self.list_widget.setGeometry(int(geometry[0]),int(geometry[1]+ self.line_edit_ofsset),int(geometry[2]),
                                     list_height)
        self.list_widget.setStyleSheet("QListWidget { background-color: #FDF8F8; }")
        self.list_widget.hide()
        self.list_button = QPushButton(parent)
        self.list_button.setGeometry(*geometry)
        self.list_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.list_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 2px;
            }
        """)
    
        self.list_button.clicked.connect(self.toggle_list)
        self.list_widget.itemClicked.connect(self.itemSelect)

    def filter_options(self, text):
        current_text = text.lower()
        itens_ocultados = 0
        itens_filtrados = 0
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if current_text not in item.text().lower():
                item.setHidden(True)
                itens_ocultados += 1
            else:
                item.setHidden(False)
                itens_filtrados += 1       
        altura_padrao = self.list_height
        max_itens_visiveis = self.list_height // self.item_height
        list_height = itens_filtrados * self.item_height if itens_filtrados <= max_itens_visiveis else altura_padrao
        self.list_widget.setGeometry(int(self.__geometry__[0]), int(self.__geometry__[1] + 45),
                                    int(self.__geometry__[2]), list_height)
    def toggle_list(self):
            if self.list_widget.isVisible():
                self.list_widget.hide()
                if self.search: 
                    self.search_line_edit.hide()
                    self.icon_label.hide()
            else:
                self.list_widget.clear()
                self.list_widget.addItems(self.list)
                text_selecionado = self.combo_box.itemText(0)
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if text_selecionado == item.text():
                        item.setHidden(True)
                        self.list_widget.setGeometry(int(self.__geometry__[0]),int(self.__geometry__[1]+ self.line_edit_ofsset),
                                                        int(self.__geometry__[2]),self.list_height - self.item_height)
                self.list_widget.show()
                if self.search:
                    self.search_line_edit.show()
                    self.icon_label.show()

    def itemSelect(self, item):
        self.combo_box.setItemText(0,item.text())
        self.list_widget.hide()
        if self.search:
            self.search_line_edit.setText("")
            self.search_line_edit.hide()
            self.icon_label.hide()

    def hide_list(self):
        if self.list_widget.isVisible():
            self.list_widget.hide()
            if self.search: 
                self.search_line_edit.hide()
                self.icon_label.hide()

class CustomTable(QTableWidget):
     
    def __init__(self, parent, geometry,data, widths_fixed_cols = False, qtd_cols_visible = 4, rows_height = 30, 
                 search_option=False, scroll_offset_horizontal=3, scroll_offset_vertical=12, cols_icon = False, rows_icon = False,
                path_icon_search_option = r"C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\GUI\PyQt\lupa.png",
                path_icons_cols = "False", path_icons_rows = False, col_flag=False, col_ocultar = False  ,
                style="""
                QTableWidget {
                    border: none; /* Remove as bordas da tabela */
                    gridline-color: transparent; /* Remove as linhas de grade */
                },
                QTableWidget::item:selected {
                    background-color: red; /* Cor de fundo da seleção */
                    color: white; /* Cor do texto da seleção */
                },
                QHeaderView::section:vertical {
                    border: 1px solid #d0d0d0; /* Define as bordas do cabeçalho vertical */
                    background-color: red; /* Deixa o fundo transparente */
                }
                """):
        super().__init__(parent)
        self.app = parent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dados = data
        self.qtd_cols_visible= qtd_cols_visible
        self.cols_icon = cols_icon
        self.col_ocultar = col_ocultar
        self.widths_fixed_cols = widths_fixed_cols
        self.index_offset = 8
        self.rows_height = rows_height
        self.__width__ = geometry[2]
        self.__height__ = geometry[3]
        ln_Dados = 1 if search_option else 0
        qtd_rows = (len(data) + ln_Dados - 1) 
        self.widht_colum_icone = 15 if cols_icon else 0
        self.scroll_offset_horizontal = scroll_offset_horizontal
        self.scroll_offset_vertical = scroll_offset_vertical
        self.setGeometry(*geometry)
        self.setRowCount(qtd_rows) 
        self.setColumnCount(len(data[0])) 
        self.dimensionar_celulas(data, qtd_cols_visible, qtd_rows, cols_icon,col_ocultar, widths_fixed_cols)
        cabecalho = data[0]
        self.setHorizontalHeaderLabels(cabecalho)
        header_font = self.horizontalHeader().font()
        header_font.setBold(True)
        self.horizontalHeader().setFont(header_font)
        if search_option:
            self.inserirIconeLinha(path_icon_search_option,0)        
            self.paint_row(0, QColor(189 , 227 , 251 ))
            self.setRowHeight(0, int(rows_height / 2))
            for col in range(self.columnCount()):
                self.item(0, col).setForeground(QColor(232, 76, 61))
            self.set_bold_row(0) 
            self.itemChanged.connect(self.on_item_changed)
        if col_flag:
            self.inserirFlagColuna(col_flag)
        if cols_icon:
            col_icone = int(len(data[0])+1)
            self.setColumnCount(col_icone) 
            cabecalho.append("")
            self.setHorizontalHeaderLabels(cabecalho) 
            self.inserirIconeColuna(path_icons_cols, col_icone-1)
        for row_idx, linha in enumerate(data[1:]):  
            for col, dado in enumerate(linha):
                self.setItem(row_idx + ln_Dados, col, QTableWidgetItem(str(dado)))
                self.item(row_idx + ln_Dados, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        for row in range(self.rowCount()):
            self.setVerticalHeaderItem(row, QTableWidgetItem(""))
        if style:
            self.setStyleSheet(style)
        if col_ocultar:
            self.hideColumn(col_ocultar-1)
        self.itemClicked.connect(self.ItemClicado)                                                                                                                                       

    def ItemClicado (self, item):
        self.setCurrentItem(item)
        item.setSelected(True)
        self.editItem(item)                                                      
        self.currentItem().setSelected(True)

    def LimparSelecao(self):
        self.clearSelection()
        self.clearFocus()
        self.setCurrentItem(None)

    def keyPressEvent(self, event): 
            if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace and self.selectedItems():
                for item in self.selectedItems():
                    item.setText("")
            else:
                super().keyPressEvent(event)

    def on_item_changed(self, item):
        if item.row() == 0:
            self.LimparDados(1)
            dados = self.dados
            self.Populate(dados[1:],1,True)
            for col in range(self.columnCount()):
                header_item  = self.item(0,col)
                if header_item .text() != "" and header_item .text() != "pesquisar":
                    dados_table = self.Dados()
                    filtro = [linha for linha in dados_table if header_item.text().upper() 
                                in str(linha[col]).upper()]
                    self.LimparDados(1)
                    if filtro:
                        self.Populate(filtro[1:],1,True)

    def Dados(self):
        dados = []
        for row in range(self.rowCount()):
            linha = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                linha.append(item.text() if item else "")
            dados.append(linha)
        return dados
    
    def ObterLinha(self, row):
        linha = []
        for col in range(self.columnCount()):
            item = self.item(row, col)
            linha.append(item.text() if item else "")
        return linha
    
    def PrencherLinha(self, row, dados):
         for col, dado in enumerate(dados):
            self.item(row,col).setText(dado)

    
    def LimparDados(self, ln_Dados):
        for row in range(self.rowCount()):
            linha = []
            if row>=ln_Dados:
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    item.setText("")

    def Populate(self, data, ln_Dados, redimensionar):
        if data:
            qtd_rows = (len(data) + ln_Dados) 
            self.setRowCount(qtd_rows) 
            if redimensionar:
                self.dimensionar_celulas(data, self.qtd_cols_visible, qtd_rows, self.cols_icon, self.col_ocultar, 
                                         self.widths_fixed_cols, False)
            for row_idx, linha in enumerate(data):  
                for col, dado in enumerate(linha):
                    self.setItem(row_idx + ln_Dados, col, QTableWidgetItem(str(dado)))
                    self.item(row_idx + ln_Dados,col).setTextAlignment(Qt.AlignmentFlag.AlignCenter) 
            for row in range(self.rowCount()):
                self.setVerticalHeaderItem(row, QTableWidgetItem(""))

    def count_visible_columns(self):
        viewport_width = self.viewport().width()  
        viewport_width
        accumulated_width = 0
        visible_columns = 0
        for col in range(self.columnCount()):
            if not self.isColumnHidden(col):
                col_width = self.columnWidth(col)
                accumulated_width += col_width
                if accumulated_width > viewport_width:
                    break  
                visible_columns += 1
        return visible_columns

    def inserirIconeLinha(self, caminho_icone, row):
        if os.path.exists(caminho_icone):           
            for col in range(self.columnCount()):
                pixmap = QPixmap(caminho_icone).scaled(24, 24) 
                item_com_texto_e_icone = QTableWidgetItem("")
                item_com_texto_e_icone.setIcon(QIcon(pixmap))
                self.setItem(row, col, item_com_texto_e_icone)
        else:
            print("O arquivo do ícone não foi encontrado.")

    def inserirIconeColuna(self, caminho_icone, col):
        if os.path.exists(caminho_icone): 
            print("achou o arquivo")            
            for row in range(self.rowCount()):
                pixmap = QPixmap(caminho_icone).scaled(24, 24) 
                item_com_texto_e_icone = QTableWidgetItem("")
                item_com_texto_e_icone.setIcon(QIcon(pixmap))
                self.setItem(row, col, item_com_texto_e_icone)
                self.setColumnWidth(col, self.widht_colum_icone)
        else:
            print("O arquivo do ícone não foi encontrado.")

    def inserirFlagColuna(self, col):
        for row in range(self.rowCount()):
            checkbox = QCheckBox()
            checkbox.setFixedSize(17, 17) 
            checkbox.setChecked(True) 
            checkbox.stateChanged.connect(self.checkbox_state_changed)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
            widget.setLayout(layout)
            self.setCellWidget(row, col, widget) 
                
    def paint_row(self, row_index, color):
        for column_index in range(self.columnCount()):
            item = self.item(row_index, column_index)
            if item:
                item.setBackground(color)

    def set_bold_row(self, row_index):
        for column_index in range(self.columnCount()):
            item = self.item(row_index, column_index)
            if item:
                font = QFont()
                font.setBold(True) 
                item.setFont(font) 

    def checkbox_state_changed(self, state):
        if state == 2:
            print("Checkbox marcado")
        else:
            print("Checkbox desmarcado")


    def dimensionar_celulas(self,  data, qtd_cols_visible,  qtd_rows, cols_icon, col_ocultar, widths_fixed_cols, 
                            alterar_linhas = False):
        qtd_colunas = len(data[0]) +  1 if cols_icon else len(data[0]) - 1 if col_ocultar else len(data[0])
        qtd_colunas_visiveis = qtd_cols_visible if qtd_colunas > qtd_cols_visible else qtd_colunas
        scroll_offset_horizontal = self.scroll_offset_horizontal if qtd_colunas > qtd_colunas_visiveis else 0
        altura = self.__height__ 
        scroll_offset_vertical = self.scroll_offset_vertical if qtd_rows >= round((altura/ self.rows_height)) else 0
        largura = self.__width__ - scroll_offset_vertical - self.widht_colum_icone - self.index_offset
        divisao = largura / qtd_colunas_visiveis
        divisao_arred = math.floor(largura / qtd_colunas_visiveis)
        resto = (divisao - divisao_arred) * qtd_colunas_visiveis
        width_table_coluns = int(divisao_arred)
        rows_height = self.rows_height + scroll_offset_horizontal 
        if widths_fixed_cols:
            if isinstance(widths_fixed_cols, list):
                    for col in range(self.columnCount()):
                        self.setColumnWidth(col, widths_fixed_cols[col])
            else:
                for col in range(self.columnCount()):
                    self.setColumnWidth(col, widths_fixed_cols)
        else:
            for col in range(self.columnCount()):
                self.setColumnWidth(col, int(width_table_coluns + resto))
                resto = 0
        if alterar_linhas:
            for row in range(self.rowCount()):
                self.setRowHeight(row, rows_height)


    def limpar_filtros(self):
          for col in range(self.columnCount()):
              item = self.item(0, col)
              if item.text() != "":
                  item.setText("")

    
                

        

