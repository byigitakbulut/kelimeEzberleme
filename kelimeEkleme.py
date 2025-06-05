#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 25 19:33:13 2025

@author: yitik
"""

# Gerekli modüller içe aktarılır
from PyQt5 import QtWidgets
import sys
import sqlite3


# Kelime ekleme arayüzü
class KelimeEkle(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Arayüz bileşenlerini oluşturur
        self.createLink()  # Veritabanı bağlantısını kurar

    def createLink(self):
        # Veritabanı bağlantısı kurulur
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()

    def init_ui(self):
        # Arayüz bileşenleri tanımlanır
        self.setWindowTitle('Kelime Ekle')
        self.infoLabel = QtWidgets.QLabel('Eklemek istediğiniz kelime bilgilerini girin: ')
        self.engWordLabel = QtWidgets.QLabel('İngilizce:                              ')
        self.engWordTextBox = QtWidgets.QLineEdit()
        self.turWordLabel = QtWidgets.QLabel('Türkçe:                                 ')
        self.turWordTextBox = QtWidgets.QLineEdit()
        self.filePathLabel = QtWidgets.QLabel('Resmin dosya yolunu girin: ')
        self.filePathTextBox = QtWidgets.QLineEdit()
        self.addButton = QtWidgets.QPushButton('Ekle')

        # Layout ayarları (bilgileri ortalamak için HBox + VBox)
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

        # Ekle butonuna tıklanırsa kelime veritabanına kaydedilir
        self.addButton.clicked.connect(self.addWord)

        self.show()

    def addWord(self):
        # Giriş kutularından veriler alınır
        engWord = self.engWordTextBox.text()
        turWord = self.turWordTextBox.text()
        path = self.filePathTextBox.text()

        # Boş alan olup olmadığı kontrol edilir
        if len(engWord) and len(turWord) and len(path):
            # Veritabanına kelime eklenir
            self.cursor.execute('INSERT INTO Words (EngWordName, TurWordName, PicturePath) VALUES (?,?,?)',
                                (engWord, turWord, path))
            self.link.commit()
            # Başarı mesajı gösterilir
            self.infoLabel.setText(engWord + ' eklendi!\n' + 'Eklemek istediğiniz kelime bilgilerini girin: ')
        else:
            # Eksik bilgi girilmişse uyarı mesajı verilir
            self.infoLabel.setText('Gerekli bilgileri doldurmadınız. Tekrar deneyin.')


