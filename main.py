import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMessageBox, QDialog, \
    QMainWindow, QStackedWidget, QVBoxLayout, QCheckBox, QLineEdit
from PyQt6.uic.properties import QtGui


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main.ui", self)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Victorio')

        self.b_create.clicked.connect(self.openCreateWindow)
        self.b_open.clicked.connect(self.openPlayWindow)
        # self.b_open = QPushButton("b_open", self)
        # self.b_settings = QPushButton("b_settings", self)
        # self.b_exit = QPushButton("b_exit", self)

        self.b_exit.clicked.connect(self.exitClicked)

    def exitClicked(self):
        confirmation = QMessageBox()

        confirmation.setText("Вы точно хотите выйти?")
        confirmation.setWindowTitle("Подтверждение")
        confirmation.setIcon(QMessageBox.Icon.Question)
        confirmation.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        yes = confirmation.button(QMessageBox.StandardButton.Yes)
        yes.setText('Да')
        no = confirmation.button(QMessageBox.StandardButton.No)
        no.setText('Нет')

        clickedButton = confirmation.exec()

        if clickedButton == QMessageBox.StandardButton.Yes:
            exit()

    def openCreateWindow(self):
        create_form = Create(self)
        create_form.show()
        self.hide()

    def openPlayWindow(self):
        p_form = Play(self)
        p_form.show()
        self.hide()


class Create(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/create.ui", self)

        self.openFileSequence()

        self.q = []  # (вопрос, несколько ответов bool, ответы (строки с + или - в начале))
        self.currAnswers = [] # ответы
        self.currQuestion = 0
        self.b_add.clicked.connect(self.addAnswer)

    def openFileSequence(self):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Создать викторину", "C:/",
                                                        "Файлы викторин (*.vict)")
        self.setWindowTitle(file + " - Victorio")
        self.f = open(file, mode="w")

    def addAnswer(self):
        if not self.answer.text():
            return
        self.answer_layout: QVBoxLayout
        self.answer: QLineEdit
        check = QCheckBox(text=self.answer.text())
        self.answer_layout.addWidget(check)
        self.currAnswers.append(self.answer.text())
        self.answer.setText("")

    def saveCurrQuestion(self):
        self.q[self.currQuestion][0] = self.question.text
        self.q[self.currQuestion][1] = self.cb_manyanswers.checked
        self.q[self.currQuestion][2] = \
            ["+" if self.answer_layout.children[i].checked else "-" + self.currAnswers[i]
             for i in range(len(self.currAnswers))]

    def loadQuestion(self):
        self.answer_layout: QVBoxLayout
        self.currAnswers = self.q[self.currQuestion][2]
        self.answer_layout.children().clear()
        for i in range(len(self.currAnswers)):
            check = QCheckBox(text=self.currAnswers[i])
            self.answer_layout.addWidget(check)

    def openNextQuestion(self):
        self.saveCurrQuestion()
        self.currQuestion += 1
        if self.currQuestion == len(self.q) - 1:
            self.q.append(("", False, []))
        self.loadQuestion()

    def closeEvent(self, e):
        self.saveCurrQuestion()
        exit()


class Play(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/play.ui", self)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Координаты')

        self.lbl = QLabel(self)
        self.pixmap = QPixmap()
        self.car_index = 0
        self.cars = ["car1.png", "car2.png", "car3.png"]
        self.current_car = self.cars[self.car_index]
        self.pixmap.load(self.current_car)
        self.lbl.setPixmap(self.pixmap)

    def mouseMoveEvent(self, event):
        if event.pos().x() <= 250 and event.pos().y() <= 250:
            self.lbl.move(event.pos().x(), event.pos().y())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.car_index = (self.car_index + 1) % 3
            self.current_car = self.cars[self.car_index]
            self.pixmap.load(self.current_car)
            self.lbl.setPixmap(self.pixmap)

    def closeEvent(self, e):
        exit()


def buttonAction(w: QStackedWidget, i):
    global currScreen
    w.setCurrentIndex(i)
    currScreen = i


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    # create = Create()
    # play = Play()
    # w = QtWidgets.QStackedWidget()
    # w.addWidget(main_menu)
    # w.addWidget(create)
    # w.addWidget(play)
    #
    # main_menu.b_create.clicked.connect(lambda: buttonAction(w, 1))
    # main_menu.b_open.clicked.connect(lambda: buttonAction(w, 2))
    # main_menu.b_settings.clicked.connect(lambda: w.setCurrentIndex(3))

    main_menu.resize(640, 480)
    main_menu.show()
    sys.exit(app.exec())
