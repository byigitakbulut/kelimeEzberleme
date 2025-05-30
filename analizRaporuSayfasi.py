from PyQt5 import QtWidgets
import sqlite3

class AnalizRapor(QtWidgets.QWidget):
    def __init__(self, userName, userID):
        self.userName = userName
        self.userID = userID
        super().__init__()
        self.init_ui()
        self.createLink()
        self.loadData()

    def loadData(self):

        self.cursor.execute(
            """SELECT COUNT(*), SUM(TotalQuestions), SUM(CorrectAnswers)
               FROM Tests WHERE UserID = ? """, (self.userID,)
        )
        testCount, totQuest, totCorrect = self.cursor.fetchone()

        self.totTestLabel.setText(f"Toplam Test: {testCount or 0}")
        self.totQuestionLabel.setText(f"Toplam Soru: {totQuest or 0}")
        self.totCorrectLabel.setText(f"Toplam Doğru: {totCorrect or 0}")

        if totQuest:
            ratio = (totCorrect / totQuest) * 100
        else:
            ratio = 0

        self.sucRateLabel.setText(f"Başarı Oranı: %{ratio:.2f}")

        self.cursor.execute(
                    """SELECT TestDate, TotalQuestions, CorrectAnswers
                    FROM Tests
                    WHERE UserID = ?
                    ORDER BY TestDate DESC
                    LIMIT 5""", (self.userID,))
        recentTests = self.cursor.fetchall()
        self.testList.clear()

        for test in recentTests:
            tarih, total, correct = test
            percent = (correct / total) * 100 if total else 0
            self.testList.addItem(f"{tarih} -> {correct}/{total} (%{percent:.1f})")

    def createLink(self):
        self.link = sqlite3.connect('yazilimYapimi.db')
        self.cursor = self.link.cursor()
        self.link.commit()

    def init_ui(self):
        self.setWindowTitle('Analiz Raporu')
        self.userNameLabel = QtWidgets.QLabel("Kullanıcı Adı: " + self.userName)
        self.totTestLabel = QtWidgets.QLabel("Toplam Test: ")
        self.totQuestionLabel = QtWidgets.QLabel("Toplam Soru: ")
        self.totCorrectLabel = QtWidgets.QLabel("Toplam Doğru: ")
        self.sucRateLabel = QtWidgets.QLabel("Başarı Oranı: ")

        self.testList = QtWidgets.QListWidget()

        vBox = QtWidgets.QVBoxLayout()
        vBox.addWidget(self.userNameLabel)
        vBox.addWidget(self.totTestLabel)
        vBox.addWidget(self.totQuestionLabel)
        vBox.addWidget(self.totCorrectLabel)
        vBox.addWidget(self.sucRateLabel)
        vBox.addWidget(QtWidgets.QLabel("Son 5 Test:"))
        vBox.addWidget(self.testList)

        hBox = QtWidgets.QHBoxLayout()
        hBox.addStretch()
        hBox.addLayout(vBox)
        hBox.addStretch()

        self.setLayout(hBox)
        self.show()


