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
        link = sqlite3.connect('yazilimYapimi.db')
        cursor = link.cursor()
        cursor.execute(
            """SELECT EngWordName 
               FROM Words 
               WHERE LENGTH(EngWordName) = 5 
               ORDER BY RANDOM() 
               LIMIT 1"""
            )
        word = cursor.fetchone()
        link.close()
        return word[0].upper() if word else "HELLO"

    def initPygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400,600))
        pygame.display.set_caption("Wordle")
        self.font = pygame.font.Font(None, 60)
        self.targetWord = self.randWord()

    def drawGuesses(self):
        self.screen.fill(self.colorBG)
        for i, guess in enumerate(self.guesses):
            for j, char in enumerate(guess):
                color = (58, 58, 60)  # Gri
                if char == self.target_word[j]:
                    color = (83, 141, 78)  # Yeşil
                elif char in self.target_word:
                    color = (181, 159, 59)  # Sarı
                pygame.draw.rect(self.screen, color, (50 + j * 60, 50 + i * 70, 50, 50))
                text = self.font.render(char, True, self.colorText)
                self.screen.blit(text, (65 + j * 60, 55 + i * 70))

        for j, char in enumerate(self.currentGuess):
            pygame.draw.rect(self.screen, (100, 100, 100), (50 + j * 60, 50 + len(self.guesses) * 70, 50, 50), 2)
            text = self.FONT.render(char, True, self.colorText)
            self.screen.blit(text, (65 + j * 60, 55 + len(self.guesses) * 70))

        pygame.display.flip()

    def start(self):
        self.initPygame()
        running = True
        while running:
            self.drawGuesses()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(self.current_guess) == 5:
                        self.guesses.append(self.currentGuess.upper())
                        if self.currentGuess.upper() == self.targetWord:
                            print("Tebrikler! Doğru bildiniz.")
                            running = False
                        elif len(self.guesses) >= self.maxAttempts:
                            print(f"Bilemediniz. Kelime: {self.target_word}")
                            running = False
                        self.current_guess = ""

                    elif event.key == pygame.K_BACKSPACE:
                        self.current_guess = self.current_guess[:-1]

                    elif event.unicode.isalpha() and len(self.current_guess) < 5:
                        self.current_guess += event.unicode.upper()

        pygame.quit()
        sys.exit()
