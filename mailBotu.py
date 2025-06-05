#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 25 10:52:05 2025

@author: yitik
"""

import smtplib                         # E-posta gönderimi için kullanılır
from email.message import EmailMessage # E-posta mesaj nesnesi oluşturmak için
import random                          # Rastgele kod üretmek için
import string                          # Rakam karakterleri için


def createCode():
    # 6 haneli rastgele doğrulama kodu oluşturur
    return ''.join(random.choices(string.digits, k=6))


def sendVerificationEmail(receiverEmail, code):
    # Gönderen e-posta bilgileri (Gmail hesabı)
    senderEmail = "ezberlek@gmail.com"
    senderPassword = "gohh ksnh wjrv ewfp"

    # E-posta içeriği oluşturulur
    msg = EmailMessage()
    msg['Subject'] = "Doğrulama Kodunuz"
    msg['From'] = senderEmail
    msg['To'] = receiverEmail
    msg.set_content(
        f"Merhaba,\n\nKelime ezberleme uygulamasına kayıt için gerekli doğrulama kodunuz:\n{code}\n\nİyi günler!"
    )

    # SMTP üzerinden e-posta gönderilir
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(senderEmail, senderPassword)
            smtp.send_message(msg)
        print("Doğrulama e-postası başarıyla gönderildi.")
    except Exception as e:
        # Hata durumunda ekrana hata mesajı yazdırılır
        print("Hata oluştu:", e)
