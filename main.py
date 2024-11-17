import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMessageBox, QDialog, QMainWindow

f = ""

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main.ui", self)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Victorio')

        #self.b_create = QPushButton("b_create", self)
        #self.b_open = QPushButton("b_open", self)
        #self.b_settings = QPushButton("b_settings", self)
        #self.b_exit = QPushButton("b_exit", self)

        self.b_exit.clicked.connect(self.exitClicked)
        self.b_create.clicked.connect(self.createClicked)

    def exitClicked(self):
        confirmation = QMessageBox()

        confirmation.setText("Вы точно хотите выйти?")
        confirmation.setWindowTitle("Подтверждение")
        confirmation.setIcon(QMessageBox.Icon.Question)
        confirmation.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        clickedButton = confirmation.exec()

        if clickedButton == QMessageBox.StandardButton.Yes:
            sys.exit(0)

    def createClicked(self):
        global f
        f, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Создать викторину", "C:/",
                                                            "Файлы викторин (*.vict)")

class Create(QMainWindow):
    def __init__(self):
        global f
        super().__init__()
        uic.loadUi("ui/create.ui", self)
        if f:
            self.f = open(f, mode="w")
            self.setWindowTitle(f)
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setWindowTitle('Координаты')


class Play(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/play.ui", self)
        self.initUI()
        self.setMouseTracking(True)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_menu = MainMenu()
    create = Create()
    play = Play()
    w = QtWidgets.QStackedWidget()
    w.addWidget(main_menu)
    w.addWidget(create)
    w.addWidget(play)

    main_menu.b_create.clicked.connect(lambda: w.setCurrentIndex(1))
    main_menu.b_open.clicked.connect(lambda: w.setCurrentIndex(2))
    #main_menu.b_settings.clicked.connect(lambda: w.setCurrentIndex(3))

    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())
