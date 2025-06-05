#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 27, 2025

@author: yitik
"""

# Gerekli modüller içe aktarılıyor
import pygame
import sqlite3
import sys

# Wordle oyunu sınıfı
class WordleGame():
    def __init__(self):
        # Oyun başlangıç ayarları
        self.font = None
        self.screen = None
        self.colorBG = (18, 18, 19)        # Arka plan rengi (siyahımsı)
        self.colorText = (255, 255, 255)   # Yazı rengi (beyaz)
        self.targetWord = ""              # Rastgele seçilecek hedef kelime
        self.guesses = []                 # Yapılan tahminler
        self.currentGuess = ""           # Anlık tahmin edilen kelime
        self.maxAttempts = 6             # Maksimum deneme hakkı

    def randWord(self):
        # Veritabanından rastgele 5 harfli kelime çekilir
        conn = sqlite3.connect('yazilimYapimi.db')
        cursor = conn.cursor()
        cursor.execute(
            """SELECT EngWordName 
               FROM Words 
               WHERE LENGTH(EngWordName) = 5 
               ORDER BY RANDOM() 
               LIMIT 1"""
        )
        word = cursor.fetchone()
        conn.close()
        return word[0].upper() if word else "APPLE"

    def initPygame(self):
        # Pygame başlatılır ve pencere oluşturulur
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("Wordle")
        self.font = pygame.font.Font(None, 60)
        self.targetWord = self.randWord()  # Rastgele hedef kelime belirlenir
        print(f"Hedef kelime (test için): {self.targetWord}")

    def drawGuesses(self):
        # Oyun ekranı çizilir
        self.screen.fill(self.colorBG)

        # Geçmiş tahminler çizilir
        for i, guess in enumerate(self.guesses):
            for j, char in enumerate(guess):
                color = (58, 58, 60)  # Varsayılan: gri
                if char == self.targetWord[j]:
                    color = (83, 141, 78)  # Doğru harf ve doğru yer: yeşil
                elif char in self.targetWord:
                    color = (181, 159, 59)  # Doğru harf ama yanlış yer: sarı

                pygame.draw.rect(self.screen, color, (50 + j * 60, 50 + i * 70, 50, 50))
                text = self.font.render(char, True, self.colorText)
                self.screen.blit(text, (65 + j * 60, 55 + i * 70))

        # Anlık tahmin kutuları
        for j, char in enumerate(self.currentGuess):
            pygame.draw.rect(self.screen, (100, 100, 100), (50 + j * 60, 50 + len(self.guesses) * 70, 50, 50), 2)
            text = self.font.render(char, True, self.colorText)
            self.screen.blit(text, (65 + j * 60, 55 + len(self.guesses) * 70))

        # Eksik harfler için boş kutular
        for j in range(len(self.currentGuess), 5):
            pygame.draw.rect(self.screen, (100, 100, 100), (50 + j * 60, 50 + len(self.guesses) * 70, 50, 50), 2)

        pygame.display.flip()

    def dispPrint(self, string_):
        # Ekrana ortalanmış şekilde bilgi mesajı gösterilir
        self.screen.fill(self.colorBG)

        fontSize = 60
        while True:
            font_ = pygame.font.Font(None, fontSize)
            textSurface = font_.render(string_, True, self.colorText)
            if textSurface.get_width() <= 380:
                break
            fontSize -= 2
            if fontSize < 20:
                break

        text_rect = textSurface.get_rect(center=(200, 300))
        self.screen.blit(textSurface, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # 3 saniye bekletilir

    def start(self):
        # Oyun döngüsü başlatılır
        self.initPygame()
        running = True

        while running:
            self.drawGuesses()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # ENTER tuşuna basıldıysa tahmin işlenir
                    if event.key == pygame.K_RETURN and len(self.currentGuess) == 5:
                        self.guesses.append(self.currentGuess.upper())

                        if self.currentGuess.upper() == self.targetWord:
                            self.dispPrint("Tebrikler! Doğru bildiniz.")
                            running = False
                        elif len(self.guesses) >= self.maxAttempts:
                            self.dispPrint(f"Bilemediniz. Kelime: {self.targetWord}")
                            running = False

                        self.currentGuess = ""

                    # BACKSPACE ile son harf silinir
                    elif event.key == pygame.K_BACKSPACE:
                        self.currentGuess = self.currentGuess[:-1]

                    # Harf girildikçe büyük harfe çevrilerek eklenir
                    elif event.unicode.isalpha() and len(self.currentGuess) < 5:
                        self.currentGuess += event.unicode.upper()

        pygame.quit()
        sys.exit()
