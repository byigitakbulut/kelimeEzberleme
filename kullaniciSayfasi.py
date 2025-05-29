#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 13:49:54 2025

@author: yitik
"""

from PyQt5 import QtWidgets
import sys
from kelimeEkleme import KelimeEkle
from quizSayfasi import Quiz
from ayarlarSayfasi import Setting

class Kullanici(QtWidgets.QWidget):
    def __init__(self, userID, userName):
        self.userName = userName
        self.userID = userID
        super().__init__()
        self.init_ui()
        self.numSoru = 10
        
    def init_ui(self):
        self.setWindowTitle('Kelime Ezberleme Oyunu')
        
        self.infoLabel = QtWidgets.QLabel(self.userName + ', hoş geldiniz!')
        self.quizButton = QtWidgets.QPushButton('Quiz Yap')
        self.analysisButton = QtWidgets.QPushButton('Analiz Raporu Al')
        self.settingButton = QtWidgets.QPushButton('Ayarlar')
        self.addWord = QtWidgets.QPushButton('Kelime Ekle')
        
        vBox = QtWidgets.QVBoxLayout()
        
        vBox.addStretch()
        vBox.addWidget(self.infoLabel)
        vBox.addWidget(self.quizButton)
        vBox.addWidget(self.analysisButton)
        vBox.addWidget(self.settingButton)
        vBox.addWidget(self.addWord)
        vBox.addStretch()
        
        hBox = QtWidgets.QHBoxLayout()
        
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()
        
        self.setLayout(hBox)
        
        self.addWord.clicked.connect(self.addWordClick)
        self.quizButton.clicked.connect(self.quizButtonClick)
        self.settingButton.clicked.connect(self.settingButtonClick)
        
        self.show()
        
    def settingButtonClick(self):
        self.setting = Setting()
        self.setting.newNumSoru.connect(self.newNumSoru_)
        
    def newNumSoru_(self, newNum):
        self.numSoru = newNum
        
    def quizButtonClick(self):
        self.quizYap = Quiz(self.numSoru, self.userID)
        
    def addWordClick(self):
        self.kelimeEkle = KelimeEkle()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    kullaici = Kullanici('admin')
    sys.exit(app.exec_())