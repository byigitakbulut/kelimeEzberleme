#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 13:49:54 2025

@author: yitik
"""

# Gerekli modüller içe aktarılıyor
from PyQt5 import QtWidgets
import sys
from kelimeEkleme import KelimeEkle
from quizSayfasi import Quiz
from ayarlarSayfasi import Setting
from analizRaporuSayfasi import AnalizRapor
from wordleSayfasi import WordleGame
import subprocess
import os


# Kullanıcı ana paneli sınıfı
class Kullanici(QtWidgets.QWidget):
    def __init__(self, userID, userName):
        # Kullanıcı bilgileri saklanıyor
        self.userName = userName
        self.userID = userID
        super().__init__()
        self.init_ui()  # Arayüz bileşenleri tanımlanır
        self.numSoru = 10  # Varsayılan quiz soru sayısı

    def init_ui(self):
        self.setWindowTitle('Kelime Ezberleme Oyunu')

        # Arayüz bileşenleri oluşturuluyor
        self.infoLabel = QtWidgets.QLabel(self.userName + ', hoş geldiniz!')
        self.quizButton = QtWidgets.QPushButton('Quiz Yap')
        self.playWordleButton = QtWidgets.QPushButton('Wordle Oyna')
        self.analysisButton = QtWidgets.QPushButton('Analiz Raporu Al')
        self.settingButton = QtWidgets.QPushButton('Ayarlar')
        self.addWord = QtWidgets.QPushButton('Kelime Ekle')
        self.exitButton = QtWidgets.QPushButton('Çıkış Yap')

        # Dikey kutu yerleşimi (VBox)
        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addWidget(self.infoLabel)
        vBox.addWidget(self.quizButton)
        vBox.addWidget(self.playWordleButton)
        vBox.addWidget(self.analysisButton)
        vBox.addWidget(self.settingButton)
        vBox.addWidget(self.addWord)
        vBox.addWidget(self.exitButton)
        vBox.addStretch()

        # Yatay kutu yerleşimi (merkezde durması için)
        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()

        self.setLayout(hBox)

        # Butonların tıklanma olayları tanımlanıyor
        self.addWord.clicked.connect(self.addWordClick)
        self.quizButton.clicked.connect(self.quizButtonClick)
        self.settingButton.clicked.connect(self.settingButtonClick)
        self.analysisButton.clicked.connect(self.analysisButtonClick)
        self.playWordleButton.clicked.connect(self.playWordleButtonClick)
        self.exitButton.clicked.connect(self.exitButtonClick)

        self.show()
        
    def exitButtonClick(self):
        # Giris penceresi açılır
        from girisSayfasi import GirisYap
        self.giris = GirisYap()
        self.close()

    def playWordleButtonClick(self):
        # Wordle oyununu ayrı bir süreç olarak başlat (donmayı önler)
        subprocess.Popen([sys.executable, "wordleLauncher.py"])

    def analysisButtonClick(self):
        # Analiz raporu penceresi açılır
        self.analiz = AnalizRapor(self.userName, self.userID)

    def settingButtonClick(self):
        # Ayarlar penceresi açılır
        self.setting = Setting()
        # Kullanıcının belirlediği yeni soru sayısı alınır
        self.setting.newNumSoru.connect(self.newNumSoru_)

    def newNumSoru_(self, newNum):
        # Quiz için yeni soru sayısı güncellenir
        self.numSoru = newNum

    def quizButtonClick(self):
        # Quiz ekranı başlatılır
        self.quizYap = Quiz(self.numSoru, self.userID)

    def addWordClick(self):
        # Kelime ekleme ekranı açılır
        self.kelimeEkle = KelimeEkle()

