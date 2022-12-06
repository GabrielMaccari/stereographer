# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 13:40:59 2022

@author: Gabriel Maccari
"""

from os import getcwd, path, makedirs
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class PlotWindow(QMainWindow):
    def __init__(self, plot, parent=None):
        
        super(PlotWindow, self).__init__(parent)
        
        self.plot = plot
        self.folder = getcwd()
        
        img = self.get_plot_img()
 
        self.setWindowTitle("Plot results")
        self.setWindowIcon(QIcon('icons/windowIcon.ico'))
 
        image_icn = QIcon(img)
        self.plot_canvas = QPushButton(self)
        self.plot_canvas.setGeometry(0,0,450,400)
        self.plot_canvas.setIcon(image_icn)
        self.plot_canvas.setIconSize(QSize(450, 400))
        self.plot_canvas.setFlat(True)
        
        self.save_btn = QPushButton(self)
        self.save_btn.setGeometry(395, 345, 50, 50)
        self.save_btn.setIcon(QIcon('icons/save.png'))
        self.save_btn.setIconSize(QSize(50, 50))
        self.save_btn.clicked.connect(self.save_plot)
        
        self.setMinimumWidth(450)
        self.setMaximumWidth(450)
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)
    
    def get_plot_img(self):
        try:
            plot_folder = self.folder + '/plots'
            if not path.exists(plot_folder):
                makedirs(plot_folder)
    
            i=0
            while True:
                fig_name = 'plots/plot'+str(i)+'.png'
                if not path.exists(fig_name):
                    break
                i+=1
            
            plt.savefig(fig_name, dpi=150, transparent=True, format='png')
            return fig_name
        except:
            plt.savefig(
                'C:/Users/Public/Pictures/plot.png',
                dpi=150,
                transparent=True,
                format='png'
            )
            return 'C:/Users/Public/Pictures/plot.png'
    
    def save_plot(self):
        try:
            outFile = QFileDialog.getSaveFileName(
                self,
                caption='Salvar arquivo',
                directory=getcwd(),
                filter='PNG (*.png);;JPEG (*.jpg);; SVG (*.svg)'
            )
            filePath = outFile[0]
            if filePath!='':
                output_format = filePath[-3:]
                self.plot.savefig(
                    filePath,
                    dpi=300,
                    transparent=True,
                    format=output_format
                )
                msg = QMessageBox(
                    parent=self,
                    text='Arquivo salvo com sucesso!'
                )
                msg.setWindowTitle('Sucesso')
                msg.exec()
        except Exception as e:
            msg = QMessageBox(
                parent=self,
                text='Não foi possível salvar o stereonet no caminho '
                     'especificado.\n\n'+str(e)
            )
            msg.setWindowTitle('Erro')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()