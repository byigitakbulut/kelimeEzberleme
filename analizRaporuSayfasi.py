from PyQt5 import QtWidgets
import sqlite3

# Kullanıcının test performansını gösteren analiz raporu arayüzü
class AnalizRapor(QtWidgets.QWidget):
    def __init__(self, userName, userID):
        self.userName = userName  # Kullanıcının adı
        self.userID = userID      # Kullanıcının ID'si
        super().__init__()
        self.init_ui()            # Arayüz başlatılır
        self.createLink()         # Veritabanı bağlantısı kurulur
        self.loadData()           # Veriler yüklenir

    def loadData(self):
        # Kullanıcının toplam test, soru ve doğru sayıları çekilir
        self.cursor.execute(
            """SELECT COUNT(*), SUM(TotalQuestions), SUM(CorrectAnswers)
               FROM Tests WHERE UserID = ? """, (self.userID,)
        )
        testCount, totQuest, totCorrect = self.cursor.fetchone()

        # Değerler label'lara yazdırılır
        self.totTestLabel.setText(f"Toplam Test: {testCount or 0}")
        self.totQuestionLabel.setText(f"Toplam Soru: {totQuest or 0}")
        self.totCorrectLabel.setText(f"Toplam Doğru: {totCorrect or 0}")

        # Başarı oranı hesaplanır
        if totQuest:
            ratio = (totCorrect / totQuest) * 100
        else:
            ratio = 0
        self.sucRateLabel.setText(f"Başarı Oranı: %{ratio:.2f}")

        # Son 5 testin tarih, doğru sayısı ve başarı oranı çekilir
        self.cursor.execute(
            """SELECT TestDate, TotalQuestions, CorrectAnswers
               FROM Tests
               WHERE UserID = ?
               ORDER BY TestDate DESC
               LIMIT 5""", (self.userID,))
        recentTests = self.cursor.fetchall()

        # Liste temizlenir ve son testler eklenir
        self.testList.clear()
        for test in recentTests:
            tarih, total, correct = test
            percent = (correct / total) * 100 if total else 0
            self.testList.addItem(f"{tarih} -> {correct}/{total} (%{percent:.1f})")

    def createLink(self):
        # Veritabanı bağlantısı kurulur
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()

    def init_ui(self):
        # Arayüz elemanları tanımlanır
        self.setWindowTitle('Analiz Raporu')
        self.userNameLabel = QtWidgets.QLabel("Kullanıcı Adı: " + self.userName)
        self.totTestLabel = QtWidgets.QLabel("Toplam Test: ")
        self.totQuestionLabel = QtWidgets.QLabel("Toplam Soru: ")
        self.totCorrectLabel = QtWidgets.QLabel("Toplam Doğru: ")
        self.sucRateLabel = QtWidgets.QLabel("Başarı Oranı: ")

        self.testList = QtWidgets.QListWidget()  # Son testler buraya yazılacak

        # Dikey yerleşim düzeni (VBox)
        vBox = QtWidgets.QVBoxLayout()
        vBox.addWidget(self.userNameLabel)
        vBox.addWidget(self.totTestLabel)
        vBox.addWidget(self.totQuestionLabel)
        vBox.addWidget(self.totCorrectLabel)
        vBox.addWidget(self.sucRateLabel)
        vBox.addWidget(QtWidgets.QLabel("Son 5 Test:"))
        vBox.addWidget(self.testList)

        # Ortalamak için yatay kutu yerleşimi
        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()

        self.setLayout(hBox)
        self.show()
