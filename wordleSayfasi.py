# wordle_game.py
import pygame
import sqlite3
import sys


class WordleGame():
    def __init__(self):
        self.font = None
        self.screen = None
        self.colorBG = (18, 18, 19)
        self.colorText = (255, 255, 255)
        self.targetWord = ""
        self.guesses = []
        self.currentGuess = ""
        self.maxAttempts = 6

    def randWord(self):
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
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("Wordle")
        self.font = pygame.font.Font(None, 60)
        self.targetWord = self.randWord()
        print(f"Hedef kelime (test için): {self.targetWord}")

    def drawGuesses(self):
        self.screen.fill(self.colorBG)
        for i, guess in enumerate(self.guesses):
            for j, char in enumerate(guess):
                color = (58, 58, 60)  # Gri
                if char == self.targetWord[j]:
                    color = (83, 141, 78)  # Yeşil
                elif char in self.targetWord:
                    color = (181, 159, 59)  # Sarı

                pygame.draw.rect(self.screen, color, (50 + j * 60, 50 + i * 70, 50, 50))
                text = self.font.render(char, True, self.colorText)
                self.screen.blit(text, (65 + j * 60, 55 + i * 70))

        # Mevcut tahmin
        for j, char in enumerate(self.currentGuess):
            pygame.draw.rect(self.screen, (100, 100, 100), (50 + j * 60, 50 + len(self.guesses) * 70, 50, 50), 2)
            text = self.font.render(char, True, self.colorText)
            self.screen.blit(text, (65 + j * 60, 55 + len(self.guesses) * 70))

        # Eksik harfler için boş kutular
        for j in range(len(self.currentGuess), 5):
            pygame.draw.rect(self.screen, (100, 100, 100), (50 + j * 60, 50 + len(self.guesses) * 70, 50, 50), 2)

        pygame.display.flip()

    def dispPrint(self, string_):
        self.screen.fill(self.colorBG)

        #gerekiyorsa boyutu küçült
        fontSize = 60
        while True:
            font_ = pygame.font.Font(None, fontSize)
            textSurface = font_.render(string_, True, self.colorText)
            if textSurface.get_width() <= 380:  # 400 genişlikten biraz küçük olmalı
                break
            fontSize -= 2
            if fontSize < 20:  # Çok küçülmesini önle
                break

        #ortala ve göster
        text_rect = textSurface.get_rect(center=(200, 300))
        self.screen.blit(textSurface, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def start(self):
        self.initPygame()
        running = True

        while running:
            self.drawGuesses()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(
                            self.currentGuess) == 5:
                        self.guesses.append(self.currentGuess.upper())

                        if self.currentGuess.upper() == self.targetWord:
                            self.dispPrint("Tebrikler! Doğru bildiniz.")
                            running = False
                        elif len(self.guesses) >= self.maxAttempts:
                            self.dispPrint(f"Bilemediniz. Kelime: {self.targetWord}")
                            running = False

                        self.currentGuess = ""

                    elif event.key == pygame.K_BACKSPACE:
                        self.currentGuess = self.currentGuess[:-1]

                    elif event.unicode.isalpha() and len(
                            self.currentGuess) < 5:
                        self.currentGuess += event.unicode.upper()

        pygame.quit()
        sys.exit()