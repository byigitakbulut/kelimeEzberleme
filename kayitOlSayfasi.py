#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 24 10:38:23 2025

@author: yitik
"""

from PyQt5 import QtWidgets
import sys
import sqlite3
import hashlib
from MailDogrulama import Verification
from mailBotu import createCode, sendVerificationEmail

class KayitOl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.createLink()
        
    def createLink(self):
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()
        
    def init_ui(self):
        
        self.setWindowTitle("Kayıt Ol")
        self.infoTextBox = QtWidgets.QLabel("Uygulamamıza kayıt olmak için gerekli bilgileri doldurun.")
        self.infoTextBox2 = QtWidgets.QLabel()
        self.kullaniciAdiLabel = QtWidgets.QLabel("Kullanıcı Adı:")
        self.kullaniciAdiTextBox = QtWidgets.QLineEdit()
        self.mailLabel = QtWidgets.QLabel('E-Posta:')
        self.mailTextBox = QtWidgets.QLineEdit()
        self.parolaLabel = QtWidgets.QLabel("Parola:")
        self.parolaTextBox = QtWidgets.QLineEdit()
        self.parolaTextBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.parolaLabel2 = QtWidgets.QLabel("Parola Tekrar:")
        self.parolaTextBox2 = QtWidgets.QLineEdit()
        self.parolaTextBox2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.kayitOlButton = QtWidgets.QPushButton("Kayıt Ol")
        
        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addWidget(self.infoTextBox)
        
        vBox.addStretch()
        vBox.addWidget(self.kullaniciAdiLabel)
        vBox.addWidget(self.kullaniciAdiTextBox)
        vBox.addWidget(self.mailLabel)
        vBox.addWidget(self.mailTextBox)
        vBox.addWidget(self.parolaLabel)
        vBox.addWidget(self.parolaTextBox)
        vBox.addWidget(self.parolaLabel2)
        vBox.addWidget(self.parolaTextBox2)
        vBox.addStretch()
        vBox.addWidget(self.infoTextBox2)
        vBox.addWidget(self.kayitOlButton)
        vBox.addStretch()
        
        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()
        
        self.setLayout(hBox)
        self.kayitOlButton.clicked.connect(self.kayitOl)
        
        self.show()
        
    def kayitOl(self):
        name = self.kullaniciAdiTextBox.text()
        mail = self.mailTextBox.text()
        parola = self.parolaTextBox.text()
        parola2 = self.parolaTextBox2.text()
        
        if len(name) and len(mail) and len(parola) and len(parola2):
            
            if self.parolaTextBox.text() == self.parolaTextBox2.text():
                
                if '@gmail.com' in mail:
                    code = createCode()
                    sendVerificationEmail(mail, code)
                    self.mailOnay = Verification(mail, code)
                    self.mailOnay.onay.connect(lambda: self.kullaniciEkle(name, mail, parola))
            else:
                self.infoTextBox2.setText(self.infoTextBox2.text() + "\nGirilen paralolar eşleşmiyor, tekrar deneyin.")
        else:
            self.infoTextBox2.setText("Lütfen gerekli yerleri doldurun.")
      
    def kullaniciEkle(self, name, mail, parola):
            hashParola = hashlib.sha256(parola.encode()).hexdigest()
            self.cursor.execute("""INSERT INTO Users (UserName, Password, Mail)
                                VALUES(?,?,?)""", (name, hashParola, mail))
            self.link.commit()
            self.infoTextBox2.setText("Başarıyla kaydoldunuz!")
            
            
       
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = KayitOl()
    sys.exit(app.exec_())
    