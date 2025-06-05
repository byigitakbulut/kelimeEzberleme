#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 20:28:27 2025

@author: yitik
"""
from PyQt5 import QtWidgets, QtCore
import sys


# Ayarlar penceresi sınıfı
class Setting(QtWidgets.QWidget):
    # Yeni soru sayısı sinyali (diğer sayfalara aktarılır)
    newNumSoru = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()  # Arayüz hazırlanır

    def init_ui(self):
        self.setWindowTitle('Ayarlar')  # Pencere başlığı

        # Arayüz bileşenleri
        self.infoLabel = QtWidgets.QLabel('Quizde çıkacak soru sayısını girin:')
        self.numSoruTextBox = QtWidgets.QLineEdit()
        self.kaydetButton = QtWidgets.QPushButton('Kaydet')

        # Dikey yerleşim (merkezleme için VBox)
        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addWidget(self.infoLabel)
        vBox.addWidget(self.numSoruTextBox)
        vBox.addWidget(self.kaydetButton)
        vBox.addStretch()

        # Yatay kutu ile ortalanır
        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()

        self.setLayout(hBox)

        # Kaydet butonuna tıklanınca işlem yapılır
        self.kaydetButton.clicked.connect(self.kaydetButtonClick)

        self.show()

    def kaydetButtonClick(self):
        # Kullanıcının girdiği sayı alınır ve sinyal olarak yayılır
        numSoru = int(self.numSoruTextBox.text())
        self.newNumSoru.emit(numSoru)  # Diğer sayfaya gönderilir
        self.close()  # Pencere kapanır



