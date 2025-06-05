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


# Kayıt olma arayüzünü tanımlayan sınıf
class KayitOl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Arayüz bileşenlerini hazırlar
        self.createLink()  # Veritabanı bağlantısını kurar

    def createLink(self):
        # SQLite veritabanına bağlantı kurulur
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()

    def init_ui(self):
        # Arayüz başlığı ve açıklama etiketi
        self.setWindowTitle("Kayıt Ol")
        self.infoTextBox = QtWidgets.QLabel("Uygulamamıza kayıt olmak için gerekli bilgileri doldurun.")
        self.infoTextBox2 = QtWidgets.QLabel()

        # Giriş alanları ve etiketleri
        self.kullaniciAdiLabel = QtWidgets.QLabel("Kullanıcı Adı:")
        self.kullaniciAdiTextBox = QtWidgets.QLineEdit()
        self.mailLabel = QtWidgets.QLabel('E-Posta:')
        self.mailTextBox = QtWidgets.QLineEdit()
        self.parolaLabel = QtWidgets.QLabel("Parola:")
        self.parolaTextBox = QtWidgets.QLineEdit()
        self.parolaTextBox.setEchoMode(QtWidgets.QLineEdit.Password)  # Şifre gizlenerek yazılır
        self.parolaLabel2 = QtWidgets.QLabel("Parola Tekrar:")
        self.parolaTextBox2 = QtWidgets.QLineEdit()
        self.parolaTextBox2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.kayitOlButton = QtWidgets.QPushButton("Kayıt Ol")  # Kayıt olma butonu

        # Dikey yerleşim düzeni
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

        # Yatay yerleşim düzeni ile ortalanır
        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()

        self.setLayout(hBox)

        # Kayıt ol butonuna tıklanınca çalışacak fonksiyon tanımlanır
        self.kayitOlButton.clicked.connect(self.kayitOl)

        self.show()  # Arayüz gösterilir

    def kayitOl(self):
        # Kullanıcıdan alınan bilgiler
        name = self.kullaniciAdiTextBox.text()
        mail = self.mailTextBox.text()
        parola = self.parolaTextBox.text()
        parola2 = self.parolaTextBox2.text()

        # Tüm alanların doldurulup doldurulmadığı kontrol edilir
        if len(name) and len(mail) and len(parola) and len(parola2):

            # Şifrelerin eşleşip eşleşmediği kontrol edilir
            if self.parolaTextBox.text() == self.parolaTextBox2.text():

                # E-posta adresinin Gmail olup olmadığı kontrol edilir
                if '@gmail.com' in mail:
                    code = createCode()  # Doğrulama kodu oluşturulur
                    sendVerificationEmail(mail, code)  # Doğrulama e-postası gönderilir
                    self.mailOnay = Verification(mail, code)  # Doğrulama arayüzü açılır
                    # Doğrulama başarılı olursa kullanıcı veritabanına eklenir
                    self.mailOnay.onay.connect(lambda: self.kullaniciEkle(name, mail, parola))
            else:
                # Şifreler uyuşmuyorsa uyarı mesajı verilir
                self.infoTextBox2.setText(self.infoTextBox2.text() + "\nGirilen paralolar eşleşmiyor, tekrar deneyin.")
        else:
            # Gerekli alanlar boşsa uyarı verilir
            self.infoTextBox2.setText("Lütfen gerekli yerleri doldurun.")

    def kullaniciEkle(self, name, mail, parola):
        # Şifre SHA256 ile hashlenir
        hashParola = hashlib.sha256(parola.encode()).hexdigest()

        # Kullanıcı veritabanına eklenir
        self.cursor.execute("""INSERT INTO Users (UserName, Password, Mail)
                                VALUES(?,?,?)""", (name, hashParola, mail))
        self.link.commit()

        # Başarılı kayıt mesajı gösterilir
        self.infoTextBox2.setText("Başarıyla kaydoldunuz!")

# Uygulama başlatılır
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = KayitOl()
    sys.exit(app.exec_())