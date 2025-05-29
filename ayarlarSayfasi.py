#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 20:28:27 2025

@author: yitik
"""

from PyQt5 import QtWidgets, QtCore
import sys

class Setting(QtWidgets.QWidget):
    
    newNumSoru = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Ayarlar')
        self.infoLabel = QtWidgets.QLabel('Quizde çıkacak soru sayısını girin:')
        self.numSoruTextBox = QtWidgets.QLineEdit()
        self.kaydetButton = QtWidgets.QPushButton('Kaydet')
        
        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addWidget(self.infoLabel)
        vBox.addWidget(self.numSoruTextBox)
        vBox.addWidget(self.kaydetButton)
        vBox.addStretch()
        
        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()
        
        self.setLayout(hBox)
        
        self.kaydetButton.clicked.connect(self.kaydetButtonClick)
        
        self.show()
        
    def kaydetButtonClick(self):
        numSoru = int(self.numSoruTextBox.text())
        self.newNumSoru.emit(numSoru)
        self.close()       
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    setting = Setting()
    sys.exit(app.exec_())