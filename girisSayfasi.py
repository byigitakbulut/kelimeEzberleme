#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 23 20:26:30 2025

@author: yitik
"""
from PyQt5 import QtWidgets
import sys
import sqlite3
from kayitOlSayfasi import KayitOl
import hashlib
from sifremiUnuttumSayfasi import SifreAl
from kullaniciSayfasi import Kullanici

class GirisYap(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.createLink()
        
    def createLink(self):
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()
        
    def init_ui(self):
        
        self.infoLabel = QtWidgets.QLabel("Kelime Ezberleme uygulamasına hoş geldiniz!")
        self.infoLabel2 = QtWidgets.QLabel()
        self.kullaniciAdiLabel = QtWidgets.QLabel("Kullanıcı Adı:")
        self.kullaniciAdiTextBox = QtWidgets.QLineEdit()
        self.parolaLabel = QtWidgets.QLabel("Parola:")
        self.parolaTextBox = QtWidgets.QLineEdit()
        self.parolaTextBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.infoLabel3 = QtWidgets.QLabel('Henüz kayıt olmadın mı?')
        self.kayitButton = QtWidgets.QPushButton('Kaydol')
        self.girisButton = QtWidgets.QPushButton('Giriş Yap')
        self.sifreAlLabel = QtWidgets.QLabel('Giriş yapmakta zorlanıyor musun?')
        self.sifreAlButton = QtWidgets.QPushButton('Şifremi Unuttum')
        
        vBox = QtWidgets.QVBoxLayout()
        
        vBox.addStretch()
        vBox.addWidget(self.infoLabel)
        vBox.addStretch()
        vBox.addWidget(self.kullaniciAdiLabel)
        vBox.addWidget(self.kullaniciAdiTextBox)
        vBox.addWidget(self.parolaLabel)
        vBox.addWidget(self.parolaTextBox)
        vBox.addWidget(self.infoLabel2)
        
        vBox.addWidget(self.girisButton)
        vBox.addStretch()
        vBox.addWidget(self.sifreAlLabel)
        vBox.addWidget(self.sifreAlButton)
        vBox.addStretch()
        vBox.addWidget(self.infoLabel3)
        vBox.addWidget(self.kayitButton)
        vBox.addStretch()
        
        hBox = QtWidgets.QHBoxLayout()
        
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()
        
        self.setLayout(hBox)
        
        self.setWindowTitle("Giriş Yap")
        
        self.girisButton.clicked.connect(self.loginClick)
        self.kayitButton.clicked.connect(self.kayitOlClick)
        self.sifreAlButton.clicked.connect(self.sifreAlClick)
        
        self.show()
        
    def sifreAlClick(self):
        self.sifreAl = SifreAl()
        
    def kayitOlClick(self):
        self.kayitOl = KayitOl()
        
    def loginClick(self):
        
        name = self.kullaniciAdiTextBox.text()
        password = self.parolaTextBox.text()
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        
        self.cursor.execute("SELECT UserID, Username, Password FROM Users WHERE UserName = ? AND Password = ?", (name, hashPassword))
        data = self.cursor.fetchall()
        
        if len(data) == 0:
            self.infoLabel2.setText('Böyle bir kullanıcı bulunmamaktadır! Lütfen tekrar deneyin.')
            
        else:
            self.pageKullanici = Kullanici(data[0][0], data[0][1])
            self.close()
                            
                            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    kullaici = GirisYap()
    sys.exit(app.exec_())
    
    