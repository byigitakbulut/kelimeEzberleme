# wordle_launcher.py
# Wordle oyununu bağımsız olarak başlatan kısa betik

from wordleSayfasi import WordleGame  # Wordle oyun sınıfı içe aktarılıyor

# Eğer bu dosya doğrudan çalıştırılırsa oyun başlatılır
if __name__ == '__main__':
    game = WordleGame()  # Wordle oyun nesnesi oluşturuluyor
    game.start()         # Oyun başlatılıyor
