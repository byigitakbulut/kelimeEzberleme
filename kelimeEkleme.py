#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 25 19:33:13 2025

@author: yitik
"""

from PyQt5 import QtWidgets
import sys
import sqlite3

class KelimeEkle(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.createLink()
        
    def createLink(self):
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()
        
    def init_ui(self):
        
        self.setWindowTitle('Kelime Ekle')
        self.infoLabel = QtWidgets.QLabel('Eklemek istediğiniz kelime bilgilerini girin: ')
        self.engWordLabel = QtWidgets.QLabel('İngilizce:                              ')
        self.engWordTextBox = QtWidgets.QLineEdit()
        self.turWordLabel = QtWidgets.QLabel('Türkçe:                                 ')
        self.turWordTextBox = QtWidgets.QLineEdit()
        self.filePathLabel = QtWidgets.QLabel('Resmin dosya yolunu girin: ')
        self.filePathTextBox = QtWidgets.QLineEdit()
        self.addButton = QtWidgets.QPushButton('Ekle')
        
        infoBox = QtWidgets.QHBoxLayout()
        
        infoBox.addStretch()
        infoBox.addWidget(self.infoLabel)
        infoBox.addStretch()
        
        hBox = QtWidgets.QHBoxLayout()
        
        hBox.addStretch()
        hBox.addWidget(self.engWordLabel)
        hBox.addWidget(self.engWordTextBox)
        hBox.addStretch()
        
        hBox2 = QtWidgets.QHBoxLayout()
        
        hBox2.addStretch()
        hBox2.addWidget(self.turWordLabel)
        hBox2.addWidget(self.turWordTextBox)
        hBox2.addStretch()
        
        hBox3 = QtWidgets.QHBoxLayout()
        
        hBox3.addStretch()
        hBox3.addWidget(self.filePathLabel)
        hBox3.addWidget(self.filePathTextBox)
        hBox3.addStretch()
        
        hBox4 = QtWidgets.QHBoxLayout()
        
        hBox4.addStretch()
        hBox4.addWidget(self.addButton)
        hBox4.addStretch()
        
        vBox = QtWidgets.QVBoxLayout()
        
        vBox.addStretch()
        vBox.addLayout(infoBox)
        vBox.addLayout(hBox)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox3)
        vBox.addLayout(hBox4)
        vBox.addStretch()
        
        self.setLayout(vBox)
        
        self.addButton.clicked.connect(self.addWord)
        
        self.show()
        
    def addWord(self):
        engWord = self.engWordTextBox.text()
        turWord = self.turWordTextBox.text()
        path = self.filePathTextBox.text()
        
        if len(engWord) and len(turWord) and len(path):
            self.cursor.execute('INSERT INTO Words (EngWordName, TurWordName, PicturePath) VALUES (?,?,?)', (engWord, turWord, path))
            self.link.commit()
            self.infoLabel.setText(engWord + ' eklendi!\n' + 'Eklemek istediğiniz kelime bilgilerini girin: ')
        else:
            self.infoLabel.setText('Gerekli bilgileri doldurmadınız. Tekrar deneyin.')
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = KelimeEkle()
    sys.exit(app.exec_())
        
        