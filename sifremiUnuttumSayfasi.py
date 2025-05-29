#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 00:27:44 2025

@author: yitik
"""

from PyQt5 import QtWidgets
import sys
from MailDogrulama import Verification
import sqlite3
import hashlib
from mailBotu import createCode, sendVerificationEmail

class SifreAl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.createLink()
        
    def createLink(self):
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()
        
    def init_ui(self):
        self.setWindowTitle('Kurtarma')
        
        self.infoLabel = QtWidgets.QLabel('Yeni şifre oluşturmak için istenilen bilgileri girin.')
        self.userNameLabel = QtWidgets.QLabel('Kullanıcı Adı          : ')
        self.userNameTextBox = QtWidgets.QLineEdit()
        self.newPasswordLabel = QtWidgets.QLabel('Yeni Parola            : ')
        self.newPasswordTextBox = QtWidgets.QLineEdit()
        self.newPasswordTextBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPasswordLabel2 =  QtWidgets.QLabel('Yeni Parola Tekrar: ')
        self.newPasswordTextBox2 = QtWidgets.QLineEdit()
        self.newPasswordTextBox2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.continueButton = QtWidgets.QPushButton('Devam Et')
        
        infoBox = QtWidgets.QHBoxLayout()
        infoBox.addStretch()
        infoBox.addWidget(self.infoLabel)
        infoBox.addStretch()
        
        userBox = QtWidgets.QHBoxLayout()
        userBox.addStretch()
        userBox.addWidget(self.userNameLabel)
        userBox.addWidget(self.userNameTextBox)
        userBox.addStretch()
        
        passwordBox = QtWidgets.QHBoxLayout()
        passwordBox.addStretch()
        passwordBox.addWidget(self.newPasswordLabel)
        passwordBox.addWidget(self.newPasswordTextBox)
        passwordBox.addStretch()
        
        passwordBox2 = QtWidgets.QHBoxLayout()
        passwordBox2.addStretch()
        passwordBox2.addWidget(self.newPasswordLabel2)
        passwordBox2.addWidget(self.newPasswordTextBox2)
        passwordBox2.addStretch()
        
        buttonBox = QtWidgets.QHBoxLayout()
        buttonBox.addStretch()
        buttonBox.addWidget(self.continueButton)
        buttonBox.addStretch()
        
        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addLayout(infoBox)
        vBox.addLayout(userBox)
        vBox.addLayout(passwordBox)
        vBox.addLayout(passwordBox2)
        vBox.addLayout(buttonBox)
        vBox.addStretch()
        
        self.continueButton.clicked.connect(self.continueButtonClick)
        
        self.setLayout(vBox)
        self.show()
        
    def continueButtonClick(self):
        name = self.userNameTextBox.text()
        password = self.newPasswordTextBox.text()
        password2 = self.newPasswordTextBox2.text()
        
        if len(name) and len(password) and len(password2):
            if password == password2:
                self.cursor.execute('SELECT Mail FROM Users WHERE UserName = ?', (name,))
                data = self.cursor.fetchall()
                if len(data):
                    mail = data[0][0]
                    code = createCode()
                    sendVerificationEmail(mail, code)
                    self.mailOnay = Verification(mail, code)
                    self.mailOnay.onay.connect(lambda: self.sifreDegistir(name, password))
                else:
                    self.infoLabel.setText('Böyle bbir kullanıcı bulunamadı. Tekrar deneyin.')
                
            else:
                self.infoLabel.setText('Girilen şifreler eşleşmiyor, tekrar deneyin.')
        else:
            self.infoLabel.setText('Gerekli bilgileri doldurmadınız. Tekrar deneyin.')
    
    def sifreDegistir(self, name, password):
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('UPDATE Users SET Password = ? WHERE UserName = ?', (hashPassword, name))
        self.link.commit()
        self.infoLabel.setText('Şifre güncellendi.')
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    sifreAl = SifreAl()
    sys.exit(app.exec_())
        
        
        