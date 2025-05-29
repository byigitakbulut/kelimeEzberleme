#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 25 10:52:05 2025

@author: yitik
"""

import smtplib
from email.message import EmailMessage
import random
import string


def createCode():
    return ''.join(random.choices(string.digits, k = 6))


def sendVerificationEmail(receiverEmail, code):
    senderEmail = "ezberlek@gmail.com"
    senderPassword = "gohh ksnh wjrv ewfp"

    # E-postada yazacaklar
    msg = EmailMessage()
    msg['Subject'] = "Doğrulama Kodunuz"
    msg['From'] = senderEmail
    msg['To'] = receiverEmail
    msg.set_content(f"Merhaba,\n\nKelime ezberleme uygulamasına kayıt için gerekli doğrulama kodunuz:\n{code}\n\nİyi günler!")

    # Gmail SMTPden gönder
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(senderEmail, senderPassword)
            smtp.send_message(msg)
        print("Doğrulama e-postası başarıyla gönderildi.")
    except Exception as e:
        print("Hata oluştu:", e)

