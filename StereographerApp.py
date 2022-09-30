# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 10:45:44 2022

@author: Gabriel Maccari
"""

from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QCheckBox, QColorDialog, QFileDialog, QMessageBox, QLineEdit
from PyQt6.QtGui import QIcon, QFont
from sys import argv as sys_argv
from os import getcwd as os_getcwd
import pandas
import numpy
import matplotlib.pyplot as plt
import mplstereonet
from PlotWindow import PlotWindow

class StereographerApp(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        self.setWindowTitle('Simple Stereographer')
        self.setWindowIcon(QIcon('icons/windowIcon.ico'))
        
        #Listas de opções para as combo boxes
        self.measurementType_dict = {'Planos: Strike/Dip':['Strike','Dip'],
                                   'Planos: Dip direction/Dip':['Dip direction','Dip'],
                                   'Linhas: Plunge/Trend':['Trend','Plunge'],
                                   'Rakes: Strike/Dip/Pitch':['Strike','Dip','Pitch']}
        self.cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                      'viridis', 'plasma', 'inferno', 'magma', 'cividis',
                      'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                      'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                      'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper',
                      'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
                      'twilight', 'twilight_shifted', 'hsv']
        self.projections = {'Equal area (Schmidt)':'equal_area',
                            'Equal angle (Wulff)':'equal_angle'}
        
        #variáveis gerais
        self.folder = os_getcwd()
        self.fileOpened = False
        self.file = None
        self.table = None
        self.columns_ok = False
        self.rows_ok = False
        self.fig = None
        
        #Interface
        x, y, h = 5, 5, 22
        self.file_lbl = QLabel('Selecione uma tabela contendo os dados de entrada.', self)
        self.file_lbl.setGeometry(x, y, 310, h)
        self.file_btn = QPushButton('Selecionar', self)
        self.file_btn.setGeometry(x+310, y, 80, h)
        self.file_btn.clicked.connect(self.open_file)
        
        y, h, w = y+h+5, 22, 100
        self.measurementType_lbl = QLabel('Tipo de medidas:', self)
        self.measurementType_lbl.setGeometry(x, y, w, h)
        self.measurementType_cmb = QComboBox(self)
        self.measurementType_cmb.setGeometry(x+w, y, 400-w-10, h)
        self.measurementType_cmb.addItems(self.measurementType_dict.keys())
        self.measurementType_cmb.currentTextChanged.connect(self.measurementType_selected)
        
        y, h = y+h+5, 22
        self.orientationColumn_lbl = QLabel('Strike:', self)
        self.orientationColumn_lbl.setGeometry(x, y, w, h)
        self.orientationColumn_lbl.setEnabled(False)
        self.orientationColumn_cmb = QComboBox(self)
        self.orientationColumn_cmb.setGeometry(x+w, y, 400-w-10, h)
        self.orientationColumn_cmb.currentTextChanged.connect(self.update_table)
        self.orientationColumn_cmb.setEnabled(False)
        
        y, h = y+h+5, 22
        self.dipColumn_lbl = QLabel('Dip:', self)
        self.dipColumn_lbl.setGeometry(x, y, w, h)
        self.dipColumn_lbl.setEnabled(False)
        self.dipColumn_cmb = QComboBox(self)
        self.dipColumn_cmb.setGeometry(x+w, y, 400-w-10, h)
        self.dipColumn_cmb.currentTextChanged.connect(self.update_table)
        self.dipColumn_cmb.setEnabled(False)
        
        y, h = y+h+5, 22
        self.pitchColumn_lbl = QLabel('Pitch:', self)
        self.pitchColumn_lbl.setGeometry(x, y, w, h)
        self.pitchColumn_lbl.setEnabled(False)
        self.pitchColumn_cmb = QComboBox(self)
        self.pitchColumn_cmb.setGeometry(x+w, y, 400-w-10, h)
        self.pitchColumn_cmb.currentTextChanged.connect(self.update_table)
        self.pitchColumn_cmb.setEnabled(False)
        
        y, h, w = y+h+5, 200, 355
        y2 = y-1
        self.data_tbl = QTableWidget(self)
        self.data_tbl.setGeometry(x, y, w, h)
        self.data_tbl.setColumnCount(len(self.measurementType_dict['Planos: Strike/Dip']))
        self.data_tbl.setHorizontalHeaderLabels(self.measurementType_dict['Planos: Strike/Dip'])
        self.data_tbl.itemChanged.connect(self.check_table_data)
        
        self.addRow_btn = QPushButton('', self)
        self.addRow_btn.setGeometry(w+10, y-1, 30, 30)
        self.addRow_btn.setIcon(QIcon('icons/add.png'))
        self.addRow_btn.setToolTip('Adicionar uma linha')
        self.addRow_btn.clicked.connect(self.add_row)
        
        y2+=35
        self.deleteRow_btn = QPushButton('', self)
        self.deleteRow_btn.setGeometry(w+10, y2, 30, 30)
        self.deleteRow_btn.setIcon(QIcon('icons/delete.png'))
        self.deleteRow_btn.setToolTip('Remover linha selecionada')
        self.deleteRow_btn.clicked.connect(self.delete_row)
        
        y2+=35
        self.clear_btn = QPushButton('', self)
        self.clear_btn.setGeometry(w+10, y2, 30, 30)
        self.clear_btn.setIcon(QIcon('icons/clear.png'))
        self.clear_btn.setToolTip('Remover todas as linhas')
        self.clear_btn.clicked.connect(self.clear_table)
        
        y2+=35
        self.reset_btn = QPushButton('', self)
        self.reset_btn.setGeometry(w+10, y2, 30, 30)
        self.reset_btn.setIcon(QIcon('icons/refresh.png'))
        self.reset_btn.setToolTip('Reiniciar a tabela com os dados do arquivo carregado')
        self.reset_btn.clicked.connect(self.refresh_table)
        self.reset_btn.setEnabled(False)
        
        y, h, w = y+h+5, 20, 195
        self.plotGreatCircles_chk = QCheckBox('Plotar grandes círculos', self)
        self.plotGreatCircles_chk.setGeometry(x, y, w, h)
        self.plotGreatCircles_chk.setChecked(True)
        self.plotGreatCircles_chk.stateChanged.connect(lambda: self.enable_color_selection(self.plotGreatCircles_chk))
        
        self.greatCircleColor_lbl = QLabel('Cor dos grandes círculos:', self)
        self.greatCircleColor_lbl.setGeometry(x+w, y, w, h)
        self.greatCircleColor_btn = QPushButton('#000000', self)
        self.greatCircleColor_btn.setGeometry(x+w+140, y, 55, h)
        self.greatCircleColor_btn.clicked.connect(lambda: self.select_color(self.greatCircleColor_btn))
        
        y, h = y+h+0, 20
        self.plotPoles_chk = QCheckBox('Plotar polos/linhas', self)
        self.plotPoles_chk.setGeometry(x, y, w, h)
        self.plotPoles_chk.stateChanged.connect(lambda: self.enable_color_selection(self.plotPoles_chk))
        
        self.poleColor_lbl = QLabel('Cor dos polos:', self)
        self.poleColor_lbl.setGeometry(x+w, y, w, h)
        self.poleColor_lbl.setEnabled(False)
        self.poleColor_btn = QPushButton('#000000', self)
        self.poleColor_btn.setGeometry(x+w+140, y, 55, h)
        self.poleColor_btn.clicked.connect(lambda: self.select_color(self.poleColor_btn))
        self.poleColor_btn.setEnabled(False)
        
        y, h = y+h+0, 20
        self.plotDensity_chk = QCheckBox('Plotar densidade de polos', self)
        self.plotDensity_chk.setGeometry(x, y, w, h)
        self.plotDensity_chk.stateChanged.connect(lambda: self.enable_color_selection(self.plotDensity_chk))
        
        self.densityColors_lbl = QLabel('Cores de densidade:', self)
        self.densityColors_lbl.setGeometry(x+w, y, w, h)
        self.densityColors_lbl.setEnabled(False)
        self.densityColors_cmb = QComboBox(self)
        self.densityColors_cmb.setGeometry(x+w+120, y, 75, h)
        self.densityColors_cmb.addItems(self.cmaps)
        self.densityColors_cmb.setEnabled(False)
        
        y, h = y+h+0, 20
        self.showColorbar_chk = QCheckBox('Mostrar escala das cores de densidade', self)
        self.showColorbar_chk.setGeometry(x+20, y, 390, h)
        self.showColorbar_chk.setEnabled(False)
        
        y, h = y+h+3, 20
        self.showGrid_chk = QCheckBox('Mostrar grade da projeção:', self)
        self.showGrid_chk.setGeometry(x, y, 170, h)
        self.showGrid_chk.setChecked(True)
        self.showGrid_chk.stateChanged.connect(self.enable_grid_selection)
        
        self.grid_cmb = QComboBox(self)
        self.grid_cmb.setGeometry(170, y+1, 225, h+1)
        self.grid_cmb.addItems(['Equal area (Schmidt)','Equal angle (Wulff)'])
        
        y, h = y+h+5, 18
        self.title_lbl = QLabel('Título da figura:', self)
        self.title_lbl.setGeometry(x, y, 390, h)
        y, h = y+h+0, 20
        self.title_edt = QLineEdit('', self)
        self.title_edt.setGeometry(x, y, 390, h)
        
        y, h = y+h+5, 30
        self.plotStereonet_btn = QPushButton('Gerar novo steorenet', self)
        self.plotStereonet_btn.setGeometry(x, y, 355, h)
        self.plotStereonet_btn.setEnabled(False)
        self.plotStereonet_btn.clicked.connect(lambda: self.plot_stereonet(True))
        
        self.addToStereonet_btn = QPushButton('', self)
        self.addToStereonet_btn.setGeometry(365, y, h, h)
        self.addToStereonet_btn.setIcon(QIcon('icons/add2.png'))
        self.addToStereonet_btn.setToolTip('Adicionar elementos ao stereonet atual')
        self.addToStereonet_btn.setEnabled(False)
        self.addToStereonet_btn.clicked.connect(lambda: self.plot_stereonet(False))
        
        y, h = y+h, 20
        self.copyrightLabel = QLabel('© 2022 Gabriel Maccari <gabriel.maccari@hotmail.com>', self)
        self.copyrightLabel.setGeometry(5, y, 340, h)
        self.copyrightLabel.setFont(QFont('Sans Serif', 8))
        
        y+=h
        self.setMinimumSize(400, y)
        self.setMaximumSize(400, y)
        
    
    def enable_color_selection(self, widget):
        state = widget.isChecked()
        
        if widget==self.plotGreatCircles_chk:
            self.greatCircleColor_lbl.setEnabled(state)
            self.greatCircleColor_btn.setEnabled(state)
        elif widget==self.plotPoles_chk:
            self.poleColor_lbl.setEnabled(state)
            self.poleColor_btn.setEnabled(state)
        elif widget==self.plotDensity_chk:
            self.densityColors_lbl.setEnabled(state)
            self.densityColors_cmb.setEnabled(state)
            self.showColorbar_chk.setEnabled(state)
            if state==False:
                self.showColorbar_chk.setChecked(state)
            
        
    def select_color(self, widget):
        colorObject = QColorDialog.getColor()
        color = colorObject.name()
        widget.setStyleSheet("color: %s" % (color))
        widget.setText(color)
        
    
    def enable_grid_selection(self):
        state = self.showGrid_chk.isChecked()
        self.grid_cmb.setEnabled(state)
    
        
    def open_file(self):
        """Exibe um diálogo para seleção de um arquivo (xlsx, xlsm, csv, ods) e cria um DataFrame (StereographerApp.file) para conter os dados de entrada. Elimina linhas e colunas em branco no DataFrame."""
        
        self.fileOpened = False
        #Abre um diálogo para seleção do arquivo. Os formatos suportados são xlsx, xlsm, csv e ods
        try:
            inFile = QFileDialog.getOpenFileName(self, caption='Selecione uma tabela contendo os dados de entrada.', directory=self.folder, filter='Formatos suportados (*.xlsx *.xlsm *.csv *.ods);;Pasta de Trabalho do Excel (*.xlsx);;Pasta de Trabalho Habilitada para Macro do Excel (*.xlsm);;CSV (*.csv);; OpenDocument Spreadsheet (*.ods)')
        #Se não der para abrir o arquivo, mostra uma mensagem com o erro
        except Exception as e:
            msg = QMessageBox(parent=self, text='Não foi possível abrir o arquivo selecionado.\n\nERRO: %s' % (str(e)))
            msg.setWindowTitle('Erro')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
        
        path = inFile[0]
        
        #Se algum arquivo tiver sido selecionado com sucesso
        if path != '':
            try:
                #Cria um dataframe a partir de um arquivo csv
                if path.endswith('.csv'):
                    file = pandas.read_csv(path, decimal=',', delimiter=';')
                    self.fileOpened = True
                #Cria um dataframe a partir de um arquivo xlsx, xlsm ou ods
                else:
                    #Engine odf para arquivos ods e openpyxl para arquivos do excel
                    eng=('odf' if path.endswith('.ods') else 'openpyxl')
                    wholeFile = pandas.ExcelFile(path, engine=eng)
                    sheetNames = wholeFile.sheet_names
                    #Caso o arquivo tenha mais de uma planilha, mostra um diálogo com uma comboBox para selecionar a planilha dos dados
                    if len(sheetNames) > 1:
                        sheet, ok = QInputDialog.getItem(self, 'Selecionar aba', 'Planilha:', sheetNames)
                        #Se o usuário apertar ok no diálogo, cria o dataframe a partir da planilha selecionada
                        if ok:
                            file = wholeFile.parse(sheet_name=sheet)
                        #Caso o usuário aperte em cancelar ou fechar o diálogo, cancela a leitura do arquivo
                        else:
                            return
                    #Se o arquivo tiver apenas uma planilha, cria o dataframe com ela
                    else:
                        file = pandas.read_excel(path, engine=eng)
                    
                    file.columns = file.columns.astype(str)
                    
                    #Remove colunas e linhas em branco (no caso das colunas, apenas se elas não tiverem cabeçalho)
                    remove_cols = [col for col in file.columns if 'Unnamed' in col]
                    file.drop(remove_cols, axis='columns', inplace=True)
                    file.replace(r'^\s*$', numpy.nan, inplace=True, regex=True)
                    file.dropna(how='all', axis='index', inplace=True)
                    
                    self.fileOpened = True
                    
            #Caso ocorra algum erro na leitura do arquivo, exibe uma mensagem com o erro e esvazia as combo boxes
            except Exception as e:
                self.fileOpened = False
                self.reset_btn.setEnabled(False)
                msg = QMessageBox(parent=self, text='Não foi possível abrir o arquivo.\n\n'+str(e))
                msg.setWindowTitle('Erro')
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.exec()
                self.orientationColumn_cmb.clear()
                self.dipColumn_cmb.clear()
                self.pitchColumn_cmb.clear()
                self.file_lbl.setText('Não foi possível abrir o arquivo.')
                self.file_lbl.setStyleSheet('QLabel {color: red}')
        
        #Instruções a serem seguidas quando um arquivo é aberto e o DataFrame é criado com sucesso
        if self.fileOpened:
            self.file = file
            self.update_combo_boxes() #Atualiza as comboBoxes e, consequentemente, atualiza a tabela da interface (self.update_columns())
            self.reset_btn.setEnabled(True)
            self.file_lbl.setText('Arquivo carregado com sucesso.')
            self.file_lbl.setStyleSheet('QLabel {color: green}')
    
    def update_combo_boxes(self):
        """Preenche as comboBoxes da interface com as colunas do DataFrame (StereographerApp.file) que forem apropriadas para medidas (numéricas e dentro do intervalo esperado)."""
        
        #Seleciona todas as colunas de medidas no arquivo (numéricas e dentro do intervalo 360 ou 0-90)
        combos = [self.orientationColumn_cmb, self.dipColumn_cmb, self.pitchColumn_cmb]
        msr_types = ['Strike','Dip','Pitch']
        msr_columns = [self.get_measurement_columns('Strike')]
        #Caso não tenha nenhuma coluna apropriada, exibe uma mensagem e cancela a operação
        if len(msr_columns)==0:
            msg = QMessageBox(parent=self, text='A tabela selecionada não contém nenhuma coluna válida de medidas. Verifique se as colunas desejadas possuem apenas dados numéricos e tente novamente.')
            msg.setWindowTitle('Dados inválidos')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        #Adiciona as colunas de medidas às combo boxes
        for i in range(len(combos)):
            combos[i].clear()
            items = self.get_measurement_columns(msr_types[i])
            combos[i].addItems(items)
            #Para a comboBox de pitch, usa a segunda coluna adquirida, pra não ficar igual ao dip de início
            if i==2 and len(items)>1:
                    combos[i].setCurrentIndex(1)
        #Habilita as combo boxes das colunas
        self.orientationColumn_lbl.setEnabled(True)
        self.orientationColumn_cmb.setEnabled(True)
        self.dipColumn_lbl.setEnabled(True)
        self.dipColumn_cmb.setEnabled(True)
        if self.measurementType_cmb.currentText().startswith('Rakes'):
            self.pitchColumn_lbl.setEnabled(True)
            self.pitchColumn_cmb.setEnabled(True)
            
            
    def get_measurement_columns(self, measurement) -> list:
        """Encontra e retorna uma lista com todas as colunas do DataFrame (StereographerApp.file) que possivelmente se tratam de medidas estruturais, isto é, que são numéricas e dentro do intervalo esperado (0-360 para orientação e 0-90 para mergulho e pitch).
        
        Recebe:
        - measurement (string): 'Strike', 'Dip direction', 'Trend', 'Plunge' ou 'Pitch'.
        
        Retorna:
        - msr_columns (list): Lista contendo os nomes das colunas em StereographerApp.file que contém dados adequados para as medidas em questão.
        """
        
        #Define o intervalo dos dados com base no tipo de medida recebido.
        if measurement=='Strike' or measurement=='Dip direction' or measurement=='Trend':
            max_value = 360
        else:
            max_value = 90
        
        #Armazena em uma lista todas as colunas do DataFrame que podem ser convertidas para float e estão no intervalo definido
        columns = self.file.columns.to_list()
        msr_columns = []
        for c in columns:
            try:
                self.file[c] = self.file[c].astype(float, errors='raise')
                if self.file[c].dropna().between(0, max_value).all() and not self.file[c].dropna().empty:
                    msr_columns.append(c)
            except:
                pass
        
        return msr_columns
    
    
    def update_table(self):
        """"Preenche a tabela da interface (StereographerApp.data_tbl) com os dados das colunas selecionadas nas combo boxes."""
        
        try:
            self.data_tbl.disconnect()
        except:
            pass
        
        msrType = self.measurementType_cmb.currentText()
        
        #Pega as colunas do DataFrame com base nas comboBoxes. Se alguma delas estiver vazia, cancela e retorna.
        try:
            data = pandas.DataFrame()
            data['c1'] = self.file[self.orientationColumn_cmb.currentText()]
            data['c2'] = self.file[self.dipColumn_cmb.currentText()]
            if msrType.startswith('Rakes'): 
                data['c3'] = self.file[self.pitchColumn_cmb.currentText()]
            data.dropna(how='all', axis='index', inplace=True)
        except:
            return
        
        try:
            #Define o número de linhas da tabela
            rows = max([data.c1.size, data.c2.size, data.c3.size]) if msrType.startswith('Rakes') else max([data.c1.size, data.c2.size])
            self.data_tbl.setRowCount(rows)
            
            #Preenche a tabela
            column_data = [data.c1, data.c2, data.c3] if msrType.startswith('Rakes') else [data.c1, data.c2]
            for column, c in enumerate(column_data):
                for row, i in enumerate(c):
                    value = QTableWidgetItem(str(i))
                    self.data_tbl.setItem(row, column, value)
            
            self.check_table_data()
            self.data_tbl.itemChanged.connect(self.check_table_data)
        except Exception as e:
            msg = QMessageBox(parent=self, text='Não foi possível atualizar a interface com as colunas especificadas. Verifique os dados de entrada e tente novamente.\n\n'+str(e))
            msg.setWindowTitle('Erro')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
        
                
    def measurementType_selected(self):
        """Com base no tipo de medidas selecionado, atualiza os cabeçalhos da tabela e as labels das comboBoxes e habilita ou desabilita a comboBox de pitch e os elementos de personalização do gráfico na interface."""
        
        msrType = self.measurementType_cmb.currentText()
        
        #Atualiza as labels da interface com os tipos de medida selecionados
        msr1 = self.measurementType_dict[msrType][0]+':'
        msr2 = self.measurementType_dict[msrType][1]+':'
        self.orientationColumn_lbl.setText(msr1)
        self.dipColumn_lbl.setText(msr2)
        
        #Habilita ou desabilita a comboBox de pitch conforme o tipo de medidas selecionado
        n = len(self.measurementType_dict[msrType])
        if n<3:
            self.pitchColumn_cmb.setEnabled(False)
            self.pitchColumn_lbl.setEnabled(False)
        elif n==3 and self.fileOpened:
            self.pitchColumn_cmb.setEnabled(True)
            self.pitchColumn_lbl.setEnabled(True)
            
        #Define o número de colunas e os cabeçalhos da tabela
        self.data_tbl.setColumnCount(len(self.measurementType_dict[msrType]))
        self.data_tbl.setHorizontalHeaderLabels(self.measurementType_dict[msrType])
        
        #Atualiza a tabela e checa os dados
        self.update_table()
        self.check_table_data()
        
        #Habilita ou desabilita os elementos de personalização do gráfico de acordo com o tipo de medidas selecionado
        if msrType.startswith('Planos'):
            self.plotGreatCircles_chk.setChecked(True)
            self.plotGreatCircles_chk.setEnabled(True)
            self.plotPoles_chk.setChecked(False)
            self.plotPoles_chk.setEnabled(True)
            self.plotDensity_chk.setText('Plotar densidade de polos')
            self.plotDensity_chk.setChecked(False)
            self.plotDensity_chk.setEnabled(True)
        elif msrType.startswith('Linhas'):
            self.plotGreatCircles_chk.setChecked(False)
            self.plotGreatCircles_chk.setEnabled(False)
            self.plotPoles_chk.setChecked(True)
            self.plotPoles_chk.setEnabled(True)
            self.plotDensity_chk.setText('Plotar densidade de linhas')
            self.plotDensity_chk.setChecked(False)
            self.plotDensity_chk.setEnabled(True)
        elif msrType.startswith('Rakes'):
            self.plotGreatCircles_chk.setChecked(True)
            self.plotGreatCircles_chk.setEnabled(True)
            self.plotPoles_chk.setChecked(True)
            self.plotPoles_chk.setEnabled(True)
            self.plotDensity_chk.setText('Plotar densidade de linhas')
            self.plotDensity_chk.setChecked(False)
            self.plotDensity_chk.setEnabled(True)
            
    
    def add_row(self):
        """Adiciona uma nova linha à tabela."""
        
        rows = self.data_tbl.rowCount()
        self.data_tbl.insertRow(rows)
    
        self.check_table_data()
        
    
    def delete_row(self):
        """Remove uma linha selecionada na tabela."""
        
        self.data_tbl.removeRow(self.data_tbl.currentRow())
        
        self.check_table_data()
        
    
    def clear_table(self):
        """Remove todas as linhas da tabela."""
        
        self.data_tbl.setRowCount(0)
        
        self.check_table_data()
    
    
    def refresh_table(self):
        """Reseta a tabela com os dados do arquivo"""
        
        self.clear_table()
        try:
            self.update_table()
        except:
            pass
    
    
    def check_table_data(self):
        """Verifica se os dados da tabela são válidos (todos float, mesma quantia de medidas em todas as colunas, nenhuma coluna vazia, dados dentro do intervalo aceito) e habilita ou desabilita o botão de plotagem conforme o resultado da verificação."""

        #Obtém os nomes das duas primeiras colunas de um dicionário com base no tipo de medida selecionado
        msrType = self.measurementType_cmb.currentText()
        c1_name = self.measurementType_dict[msrType][0]
        c2_name = self.measurementType_dict[msrType][1]

        #Pega os dados da tabela e armazena em um DataFrame
        data = self.get_table_data()
        self.table = pandas.DataFrame()
        self.table[c1_name] = pandas.Series(data[0]) if len(data[0])>0 else numpy.nan
        self.table[c2_name] = pandas.Series(data[1]) if len(data[1])>0 else numpy.nan
        self.table['Pitch'] = pandas.Series(data[2]) if len(data[2])>0 else numpy.nan
          
        #Substitui células em branco por NaN e exclui colunas vazias
        self.table.replace(r'^\s*$', numpy.nan, inplace=True, regex=True)
        self.table.dropna(how='all', axis='columns', inplace=True)
        
        #Armazena os headers em uma lista
        columnList = self.table.columns.to_list()
        
        #Se não houver nenhum header, isto é, nenhuma coluna, os dados são inválidos, e o botão de plotagem é desabilitado
        if len(columnList)==0:
            self.columns_ok, self.rows_ok = False, False
            self.plotStereonet_btn.setEnabled(True) if (self.columns_ok and self.rows_ok) else self.plotStereonet_btn.setEnabled(False)
            self.addToStereonet_btn.setEnabled(True) if (self.columns_ok and self.rows_ok and self.fig is not None) else self.addToStereonet_btn.setEnabled(False)
            return
        
        #Checa se os dados são float e se estão dentro do intervalo esperado (0-360° para orientação e 0-90° para ângulo de mergulho e pitch)
        self.columns_ok = True
        columns = []
        for c in columnList:
            #Intervalos de ângulos
            if c=='Strike' or c=='Dip direction' or c=='Trend':
                max_value = 360
            else:
                max_value = 90
            try:
                #Tenta converter para float
                self.table[c] = self.table[c].astype(float, errors='raise')
                #Se der certo, adiciona os dados da coluna (tirando os nulos) a uma lista e verifica se estão dentro do intervalo
                columns.append(self.table[c].dropna())
                if not (self.table[c].dropna().between(0, max_value).all() and not self.table[c].empty):
                    self.columns_ok = False
            except:
                pass
        
        #Compara o número de colunas no DataFrame com o número de colunas esperado para o tipo de medida
        columnsExpected = len(self.measurementType_dict[msrType])
        #Se forem diferentes, os dados são inválidos
        if len(columns)!=columnsExpected:
            self.columns_ok = False
        
        #Verifica se todas as colunas têm a mesma quantia de linhas não-nulas
        self.rows_ok = True
        rows = len(columns[0])
        for c in columns:
            if c.size!=rows:
                self.rows_ok = False
            rows = len(c)
        
        #Elimina linhas vazias
        self.table.dropna(how='all', axis='index', inplace=True)
        #Habilita ou desabilita o botão de plotagem conforme o resultado da verificação
        self.plotStereonet_btn.setEnabled(True) if (self.columns_ok and self.rows_ok) else self.plotStereonet_btn.setEnabled(False)
        self.addToStereonet_btn.setEnabled(True) if (self.columns_ok and self.rows_ok and self.fig is not None) else self.addToStereonet_btn.setEnabled(False)
        
    
    def get_table_data(self):
        """Obtém os dados presentes na tabela da interface.
        
        Retorna:
        - msr_list (list): Lista contendo outras três sublistas. Cada sublista contém os dados de uma coluna da tabela (strings)."""
        
        rows = self.data_tbl.rowCount()
        columns = self.data_tbl.columnCount()
        
        strikes, dips, pitches = [], [], []
        msr_list = [strikes, dips, pitches]
        
        for c in range(columns):
            for r in range(rows):
                item = self.data_tbl.item(r,c)
                try:
                    msr_list[c].append(item.text())
                except AttributeError:
                    msr_list[c].append(numpy.nan)
    
        return msr_list
        
    
    def plot_stereonet(self, newPlot=True):
        self.fig = None if newPlot else self.fig
        
        try:
            self.check_table_data()
            if self.columns_ok and self.rows_ok:
                msrType = self.measurementType_cmb.currentText()
                plotGreatCircles = self.plotGreatCircles_chk.isChecked()
                plotPoles = self.plotPoles_chk.isChecked()
                plotDensity = self.plotDensity_chk.isChecked()
                greatCircleColor = self.greatCircleColor_btn.text()
                poleColor = self.poleColor_btn.text()
                density_cmap = self.densityColors_cmb.currentText()
                title = self.title_edt.text()
                showGrid = self.showGrid_chk.isChecked()
                projection = self.projections[self.grid_cmb.currentText()]
                showColorbar = self.showColorbar_chk.isChecked()

                columns = self.table.columns.to_list()
                
                azimuths = self.table[columns[0]].values
                angles = self.table[columns[1]].values
                if msrType.startswith('Rakes'):
                    pitches = self.table[columns[2]].values
                    
                if msrType.startswith('Planos: Dip direction'):
                    azimuths = azimuths - 90
                
                if self.fig == None:
                    self.fig, self.ax = mplstereonet.subplots(figsize=[6,6], projection=projection)
                
                if msrType.startswith('Rakes'):
                    self.ax.plane(azimuths, angles, color=greatCircleColor)
                    self.ax.rake(azimuths, angles, pitches, color=poleColor)
                    if plotDensity: density = self.ax.density_contourf(azimuths, angles, pitches, measurement='rakes', cmap=density_cmap)
                elif msrType.startswith('Linhas'):
                    if plotPoles: self.ax.line(angles, azimuths, color=poleColor)
                    if plotDensity: density = self.ax.density_contourf(angles, azimuths, measurement='lines', cmap=density_cmap)
                else:
                    if plotGreatCircles: self.ax.plane(azimuths, angles, color=greatCircleColor)
                    if plotPoles: self.ax.pole(azimuths, angles, color=poleColor)
                    if plotDensity: density = self.ax.density_contourf(azimuths, angles, measurement='poles', cmap=density_cmap)

                if title!='': self.ax.set_title(title, y=1.10, fontsize=18, fontweight='bold')
                if showGrid: self.ax.grid(color='black', alpha=0.3)
                if showColorbar: self.fig.colorbar(density, pad=0.1, shrink=0.6)
                
                self.ax.set_facecolor('white')
                self.ax.set_azimuth_ticks([])

                labels = ['N','E','S','W']
                lbl_angles = numpy.arange(0,360,90)
                labx = 0.5-0.55*numpy.cos(numpy.radians(lbl_angles+90))
                laby = 0.5+0.55*numpy.sin(numpy.radians(lbl_angles+90))
                for i in range(len(labels)):
                            self.ax.text(labx[i],laby[i],labels[i], \
                                    transform=self.ax.transAxes, ha='center', va='center')
                
                plt.tight_layout()
                #plt.show()
                
                self.plotWindow = PlotWindow(plt, self)
                self.plotWindow.show()
                
                self.addToStereonet_btn.setEnabled(True)
                
            else:
                raise Exception('Columns and rows verification failed.')
        except Exception as e:
            msg = QMessageBox(parent=self, text='Não foi possível gerar o stereonet. Verifique os dados de entrada e tente novamente.\n\n'+str(e))
            msg.setWindowTitle('Erro')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()

if __name__ == '__main__':
    app = QApplication(sys_argv)
    window = StereographerApp()
    window.show()
    app.exec()