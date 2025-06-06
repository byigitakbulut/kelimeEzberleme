#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 13:01:22 2025

@author: yitik
"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import sys
import sqlite3
import random
import datetime

# Tekrar aralıkları (gün cinsinden)
REPETITION_INTERVALS = [1, 7, 30, 90, 180, 365]


# Quiz modülü
class Quiz(QtWidgets.QWidget):
    def __init__(self, numSoru, userID):
        super().__init__()
        self.numSoru = numSoru  # Quizdeki toplam soru sayısı
        self.userID = userID  # Giriş yapan kullanıcının ID'si
        self.init_ui()  # Arayüz başlatılır
        self.createLink()  # Veritabanı bağlantısı kurulur
        self.counter = 0  # Kaç soru cevaplandığı
        self.numTrue = 0  # Doğru cevap sayısı
        self.sorulariHazirla()  # Sorulacak kelimeler hazırlanır
        self.yeniSoru()  # İlk soru ekrana getirilir
        self.testID = self.testiKaydet()  # Test veritabanına kaydedilir

    def sorulariHazirla(self):
        # Bugünün tarihi alınır
        today = datetime.date.today().isoformat()

        # Tekrar zamanı gelen kelimeler çekilir
        self.cursor.execute("""
            SELECT w.* FROM Words w
            JOIN UserWordProgress uwp ON w.WordID = uwp.WordID
            WHERE uwp.UserID = ? AND uwp.CorrectCount < 6 AND uwp.NextTestDate <= ?
            ORDER BY RANDOM()
            LIMIT ?
        """, (self.userID, today, self.numSoru))

        knownWords = self.cursor.fetchall()

        # Eğer yeterince kelime yoksa, kullanıcı için yeni kelimeler de eklenir
        if len(knownWords) < self.numSoru:
            eksik = self.numSoru - len(knownWords)
            self.cursor.execute("""
                SELECT * FROM Words
                WHERE WordID NOT IN (
                    SELECT WordID FROM UserWordProgress WHERE UserID = ?
                )
                ORDER BY RANDOM()
                LIMIT ?
            """, (self.userID, eksik))
            newWords = self.cursor.fetchall()
        else:
            newWords = []

        # Sorular oluşturulmuş olur
        self.sorular = knownWords + newWords

    def createLink(self):
        # Veritabanı bağlantısı kurulur
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()

    def init_ui(self):
        # Arayüz bileşenleri oluşturuluyor
        self.setWindowTitle('Quiz Modülü')
        self.numLabel = QtWidgets.QLabel('1.')
        self.resimLabel = QtWidgets.QLabel()
        self.resimLabel.setPixmap(QPixmap('resimler/Unknown.jpeg'))
        self.engWordLabel = QtWidgets.QLabel('EngWord')
        self.wordSampleLabel = QtWidgets.QLabel('EngWord Sample')
        self.turWordOptButton = QtWidgets.QPushButton('TurWordOpt1')
        self.turWordOptButton2 = QtWidgets.QPushButton('TurWordOpt2')
        self.turWordOptButton3 = QtWidgets.QPushButton('TurWordOpt3')

        # Arayüz yerleşim düzenleri (VBox / HBox)
        resimLabelVBox = QtWidgets.QVBoxLayout()
        resimLabelVBox.addStretch()
        resimLabelVBox.addWidget(self.numLabel)
        resimLabelVBox.addWidget(self.resimLabel)
        resimLabelVBox.addStretch()

        resimLabelHBox = QtWidgets.QHBoxLayout()
        resimLabelHBox.addStretch()
        resimLabelHBox.addLayout(resimLabelVBox)
        resimLabelHBox.addStretch()

        wordLabelVBox = QtWidgets.QVBoxLayout()
        wordLabelVBox.addWidget(self.engWordLabel)

        wordLabelHBox = QtWidgets.QHBoxLayout()
        wordLabelHBox.addStretch()
        wordLabelHBox.addLayout(wordLabelVBox)
        wordLabelHBox.addStretch()

        wordSampleVBox = QtWidgets.QVBoxLayout()
        wordSampleVBox.addWidget(self.wordSampleLabel)

        wordSampleHBox = QtWidgets.QHBoxLayout()
        wordSampleHBox.addStretch()
        wordSampleHBox.addLayout(wordSampleVBox)
        wordSampleHBox.addStretch()

        optVBox = QtWidgets.QVBoxLayout()
        optVBox.addWidget(self.turWordOptButton)
        optVBox.addWidget(self.turWordOptButton2)
        optVBox.addWidget(self.turWordOptButton3)

        optHBox = QtWidgets.QHBoxLayout()
        optHBox.addStretch()
        optHBox.addLayout(optVBox)
        optHBox.addStretch()

        vBox = QtWidgets.QVBoxLayout()
        vBox.addStretch()
        vBox.addLayout(resimLabelHBox)
        vBox.addLayout(wordLabelHBox)
        vBox.addLayout(wordSampleHBox)
        vBox.addLayout(optHBox)
        vBox.addStretch()

        self.setLayout(vBox)

        # Cevap butonlarına tıklanınca cevap kontrol edilir
        for button in [self.turWordOptButton, self.turWordOptButton2, self.turWordOptButton3]:
            button.clicked.connect(self.cevapKontrol)

        self.show()

    def cevapKontrol(self):
        # Kullanıcının seçtiği seçenek doğru mu kontrol edilir
        is_correct = 0
        if self.sender().text() == self.curSoru[2]:
            is_correct = 1
            self.numTrue += 1
            self.saveUserWordProgress(self.userID, self.curWordID)

        # Test detayları kaydedilir (doğru/yanlış)
        self.cursor.execute(
            "INSERT INTO TestDetails (TestID, WordID, IsCorrect) VALUES (?, ?, ?)",
            (self.testID, self.curWordID, is_correct)
        )
        self.link.commit()

        self.counter += 1
        self.yeniSoru()

    def yeniSoru(self):
        # Yeni soru gösterilir veya test bitirilir
        if self.counter < self.numSoru:
            self.curSoru = self.sorular[self.counter]  # Sıradaki soru
            self.curWordID = self.curSoru[0]  # Sözlükteki kelimenin ID'si
            self.numLabel.setText(f"{self.counter + 1}. Soru:")

            # Resim ve İngilizce kelime gösterilir
            self.engWordLabel.setText(self.curSoru[1])
            self.resimLabel.setPixmap(QPixmap(self.curSoru[3]))

            # Kelimenin örnek cümlesinin databaseden çekimi
            self.cursor.execute("SELECT * FROM WordSamples WHERE WordID = ?", (self.curSoru[0],))
            sampleList = self.cursor.fetchone()
            wordSample = sampleList[2]

            self.wordSampleLabel.setText(wordSample)  # İngilizce örnek cümle yazımı

            # Doğru Türkçe + 2 yanlış seçenek hazırlanır
            self.cursor.execute(
                "SELECT TurWordName FROM Words WHERE WordID != ? ORDER BY RANDOM() LIMIT 2",
                (self.curSoru[0],)
            )
            falseOpt = [row[0] for row in self.cursor.fetchall()]
            options = [self.curSoru[2]] + falseOpt
            random.shuffle(options)

            self.turWordOptButton.setText(options[0])
            self.turWordOptButton2.setText(options[1])
            self.turWordOptButton3.setText(options[2])
        else:
            self.testiBitir()

    def testiBitir(self):
        # Tüm butonlar devre dışı bırakılır ve sonuç gösterilir
        for button in [self.turWordOptButton, self.turWordOptButton2, self.turWordOptButton3]:
            button.setDisabled(True)

        self.numLabel.setText("Test Bitti")
        self.engWordLabel.setText(f"Doğru Sayısı: {self.numTrue}/{self.numSoru}")
        self.resimLabel.clear()
        self.wordSampleLabel.clear()

        # Test sonucu veritabanına yazılır
        self.cursor.execute(
            "UPDATE Tests SET CorrectAnswers = ? WHERE TestID = ?",
            (self.numTrue, self.testID)
        )
        self.link.commit()

    def testiKaydet(self):
        # Testin genel bilgisi veritabanına kaydedilir
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO Tests (UserID, TestDate, TotalQuestions, CorrectAnswers) VALUES (?, ?, ?, ?)",
            (self.userID, today, self.numSoru, 0)
        )
        self.link.commit()
        return self.cursor.lastrowid  # TestID geri döndürülür

    def saveUserWordProgress(self, userID, wordID):
        # Kullanıcının bu kelimeyle ilgili öğrenme durumu güncellenir
        today = datetime.date.today()
        self.cursor.execute("""
            SELECT CorrectCount FROM UserWordProgress
            WHERE UserID = ? AND WordID = ?
        """, (userID, wordID))
        result = self.cursor.fetchone()

        if result:
            correct_count = result[0]
            if correct_count < 6:
                correct_count += 1
                next_days = REPETITION_INTERVALS[min(correct_count, len(REPETITION_INTERVALS) - 1)]
                next_test_date = today + datetime.timedelta(days=next_days)
                self.cursor.execute("""
                    UPDATE UserWordProgress
                    SET CorrectCount = ?, LastCorrectDate = ?, NextTestDate = ?
                    WHERE UserID = ? AND WordID = ?
                """, (correct_count, today.isoformat(), next_test_date.isoformat(), userID, wordID))
        else:
            # İlk kez doğru cevaplandıysa kaydedilir
            next_test_date = today + datetime.timedelta(days=REPETITION_INTERVALS[0])
            self.cursor.execute("""
                INSERT INTO UserWordProgress (UserID, WordID, CorrectCount, LastCorrectDate, NextTestDate)
                VALUES (?, ?, ?, ?, ?)
            """, (userID, wordID, 1, today.isoformat(), next_test_date.isoformat()))

        self.link.commit()
