#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 25 11:54:19 2025

@author: yitik
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

import sys


# E-posta doğrulama arayüzü
class Verification(QtWidgets.QWidget):
    # Doğrulama başarılı olduğunda yayılacak sinyal
    onay = pyqtSignal()

    def __init__(self, mail, code):
        # E-posta ve doğrulama kodu parametre olarak alınır
        self.mail = mail
        self.code = code
        super().__init__()
        self.init_ui()  # Arayüz başlatılır

    def init_ui(self):
        # Pencere başlığı ayarlanır
        self.setWindowTitle('E-Mail ile Doğrulama')

        # Kullanıcıya doğrulama kodu gönderildiğini bildiren etiket
        self.infoLabel = QtWidgets.QLabel(
            self.mail + " mailinize bir doğrulama kodu gönderdik.\nLütfen kodu girin:"
        )
        self.infoLabel2 = QtWidgets.QLabel()  # Uyarı veya başarı mesajı
        self.verCodeTextBox = QtWidgets.QLineEdit()  # Kodun girileceği kutu
        self.verButton = QtWidgets.QPushButton('Doğrula')  # Doğrulama butonu

        # Arayüz yerleşimi (dikey ve yatay kutularla)
        vBox = QtWidgets.QVBoxLayout()
        hBox = QtWidgets.QHBoxLayout()

        vBox.addStretch()
        vBox.addWidget(self.infoLabel)
        vBox.addWidget(self.verCodeTextBox)
        vBox.addWidget(self.infoLabel2)
        vBox.addWidget(self.verButton)
        vBox.addStretch()

        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()

        self.setLayout(hBox)

        # Doğrula butonuna tıklanınca verification fonksiyonu çalışır
        self.verButton.clicked.connect(self.verification)

        self.show()

    def verification(self):
        # Girilen kod doğruysa onay sinyali yayılır, değilse uyarı verilir
        if self.code == self.verCodeTextBox.text():
            self.onay.emit()
            self.infoLabel2.setText('E-Mail onaylandı')
        else:
            self.infoLabel2.setText('Doğrulama kodunu yanlış girdiniz. Tekrar deneyin.')



