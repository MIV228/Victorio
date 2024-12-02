import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMessageBox, QDialog, \
    QMainWindow, QStackedWidget, QVBoxLayout, QCheckBox, QLineEdit, QTextEdit, QHBoxLayout


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main.ui", self)
        self.setWindowTitle('Victorio')

        self.logo.setPixmap(QPixmap("ui/images/logo.png"))

        self.b_create.clicked.connect(self.openCreateWindow)
        self.b_open.clicked.connect(self.openCreateOpenWindow)
        self.b_play.clicked.connect(self.openPlayWindow)
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
        file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Создать викторину", "C:/",
                                                        "Файлы викторин (*.vict)")

        if file != "":
            p_form = Create(file, self)
            p_form.show()
            # self.hide()

    def openCreateOpenWindow(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть викторину", "C:/",
                                                        "Файлы викторин (*.vict)")

        if file != "":
            p_form = CreateOpen(file, self)
            p_form.show()
            # self.hide()

    def openPlayWindow(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть викторину", "C:/",
                                                        "Файлы викторин (*.vict)")

        if file != "":
            p_form = Play(file, self)
            p_form.show()
            # self.hide()


class Create(QMainWindow):
    def __init__(self, file, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/create.ui", self)

        self.q = []  # (вопрос, несколько ответов (bool), ответы (строки с + или - в начале))
        self.file = file
        self.currAnswers = []  # ответы
        self.currAnswerCheckboxes = []
        self.currQuestion = 0

        self.b_add.clicked.connect(self.addAnswer)
        self.b_next.clicked.connect(self.openNextQuestion)
        self.b_prev.clicked.connect(self.openPrevQuestion)
        self.b_prev.hide()
        self.b_exit.clicked.connect(self.saveFile)

        self.openFileSequence()

    def openFileSequence(self):
        self.setWindowTitle(self.file + " - Victorio")
        self.f = open(self.file, mode="w", encoding="utf-8")

    def addAnswer(self):
        if not self.answer.text():
            return

        self.answer_layout: QVBoxLayout
        self.answer: QLineEdit

        check = QCheckBox(text=self.answer.text())
        self.answer_layout.addWidget(check)
        self.currAnswers.append(self.answer.text())
        self.currAnswerCheckboxes.append(check)
        self.answer.setText("")

    def saveCurrQuestion(self):
        if self.currQuestion == len(self.q) or not self.q:
            self.q.append(["", False, []])

        self.q[self.currQuestion][0] = self.question.toPlainText()
        self.q[self.currQuestion][1] = self.cb_manyanswers.isChecked()

        r = []
        for i in range(len(self.currAnswers)):
            if self.currAnswerCheckboxes[i].isChecked():
                r.append("+" + self.currAnswers[i])
            else:
                r.append("-" + self.currAnswers[i])
        self.q[self.currQuestion][2].clear()
        self.q[self.currQuestion][2].extend(r)

    def loadQuestion(self):
        if self.currQuestion == len(self.q) or not self.q:
            self.q.append(["", False, []])

        self.question: QTextEdit
        self.question.setPlainText(self.q[self.currQuestion][0])
        self.cb_manyanswers.setChecked(self.q[self.currQuestion][1])
        self.answer_layout: QVBoxLayout
        self.currAnswerCheckboxes.clear()
        self.currAnswers.clear()

        if self.q[self.currQuestion][2]:
            self.currAnswers.extend(self.q[self.currQuestion][2])

        while self.answer_layout.count() - 1 > 0:
            child = self.answer_layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()

        for i in range(len(self.currAnswers)):
            check = QCheckBox(text="")
            self.answer_layout.addWidget(check)
            self.currAnswerCheckboxes.append(check)
            if self.currAnswers[i][0] == '+':
                check.setChecked(True)
            self.currAnswers[i] = self.currAnswers[i][1:]
            check.setText(self.currAnswers[i])

        self.count.setText(f"Вопрос {self.currQuestion + 1}/{len(self.q)}")

        if self.currQuestion == 0:
            self.b_prev.hide()
        else:
            self.b_prev.show()

        if self.currQuestion == len(self.q) - 1:
            self.b_next.setText("Новый")
        else:
            self.b_next.setText("Следующий")

    def openNextQuestion(self):
        if not self.currAnswers:
            return

        self.saveCurrQuestion()
        self.currQuestion += 1
        self.loadQuestion()

    def openPrevQuestion(self):
        if self.currQuestion == 0:
            return

        self.saveCurrQuestion()
        self.currQuestion -= 1
        self.loadQuestion()

    def saveFile(self, dontopenmainmenu=False):
        self.saveCurrQuestion()
        if self.q[-1][0] == "" or not self.q[-1][2]:
            self.q.pop()
        r = []
        for q in self.q:
            answers = []
            for a in q[2]:
                answers.append(a)
            b = '0' if q[1] else '1'
            r.append(q[0] + '|' + b + '|' + '$'.join(answers))
        self.f.writelines("#".join(r))
        print(r)
        self.f.close()
        if not dontopenmainmenu:
            self.parent().show()
            self.hide()

    def closeEvent(self, e):
        self.saveFile(dontopenmainmenu=True)


class CreateOpen(QMainWindow):
    def __init__(self, file, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/create.ui", self)

        self.file = file
        self.q = []  # (вопрос, несколько ответов (bool), ответы (строки с + или - в начале))
        self.currAnswers = []  # ответы
        self.currAnswerCheckboxes = []
        self.currQuestion = 0

        self.b_add.clicked.connect(self.addAnswer)
        self.b_next.clicked.connect(self.openNextQuestion)
        self.b_prev.clicked.connect(self.openPrevQuestion)
        self.b_prev.hide()
        self.b_exit.clicked.connect(self.saveFile)

        self.openFileSequence()

        if self.oldfile != "":
            r = self.oldfile.split('#')
            for s in r:
                a = s.split('|')
                b = a[1] == '1'
                self.q.append([a[0], b, a[2].split('$')])

        self.loadQuestion()

    def openFileSequence(self):
        self.setWindowTitle(self.file + " - Victorio")
        self.f = open(self.file, mode="r+", encoding='utf-8')
        self.oldfile = self.f.readline()

    def addAnswer(self):
        if not self.answer.text():
            return

        self.answer_layout: QVBoxLayout
        self.answer: QLineEdit

        check = QCheckBox(text=self.answer.text())
        self.answer_layout.addWidget(check)
        self.currAnswers.append(self.answer.text())
        self.currAnswerCheckboxes.append(check)
        self.answer.setText("")

    def saveCurrQuestion(self):
        if self.currQuestion == len(self.q) or not self.q:
            self.q.append(["", False, []])

        self.q[self.currQuestion][0] = self.question.toPlainText()
        self.q[self.currQuestion][1] = self.cb_manyanswers.isChecked()

        r = []
        for i in range(len(self.currAnswers)):
            if self.currAnswerCheckboxes[i].isChecked():
                r.append("+" + self.currAnswers[i])
            else:
                r.append("-" + self.currAnswers[i])

        self.q[self.currQuestion][2].clear()
        self.q[self.currQuestion][2].extend(r)

    def loadQuestion(self):
        if self.currQuestion == len(self.q) or not self.q:
            self.q.append(["", False, []])

        self.question: QTextEdit
        self.question.setPlainText(self.q[self.currQuestion][0])
        self.cb_manyanswers.setChecked(self.q[self.currQuestion][1])
        self.answer_layout: QVBoxLayout
        self.currAnswerCheckboxes.clear()
        self.currAnswers.clear()

        if self.q[self.currQuestion][2]:
            self.currAnswers.extend(self.q[self.currQuestion][2])

        while self.answer_layout.count() - 1 > 0:
            child = self.answer_layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()

        for i in range(len(self.currAnswers)):
            check = QCheckBox(text="")
            self.answer_layout.addWidget(check)
            self.currAnswerCheckboxes.append(check)
            if self.currAnswers[i][0] == '+':
                check.setChecked(True)
            self.currAnswers[i] = self.currAnswers[i][1:]
            check.setText(self.currAnswers[i])

        self.count.setText(f"Вопрос {self.currQuestion + 1}/{len(self.q)}")

        if self.currQuestion == 0:
            self.b_prev.hide()
        else:
            self.b_prev.show()

        if self.currQuestion == len(self.q) - 1:
            self.b_next.setText("Новый")
        else:
            self.b_next.setText("Следующий")

    def openNextQuestion(self):
        if not self.currAnswers:
            return

        self.saveCurrQuestion()
        self.currQuestion += 1
        self.loadQuestion()

    def openPrevQuestion(self):
        if self.currQuestion == 0:
            return

        self.saveCurrQuestion()
        self.currQuestion -= 1
        self.loadQuestion()

    def saveFile(self, dontopenmainmenu=False):
        self.saveCurrQuestion()

        self.f.seek(0)
        if self.q[-1][0] == "" or not self.q[-1][2]:
            self.q.pop()

        r = []
        for q in self.q:
            answers = []
            for a in q[2]:
                answers.append(a)
            b = '0' if q[1] else '1'
            r.append(q[0] + '|' + b + '|' + '$'.join(answers))

        self.f.writelines("#".join(r))
        print(r)
        self.f.close()

        if not dontopenmainmenu:
            self.parent().show()
            self.hide()

    def closeEvent(self, e):
        self.saveFile(dontopenmainmenu=True)


class Play(QMainWindow):
    def __init__(self, file, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/play.ui", self)

        self.setWindowTitle(file.split('/')[-1][:-5] + " - Victorio")
        self._f = open(file, mode="r", encoding="utf-8")
        r = self._f.readline().split('#')
        self.q = []  # все вопросы
        for s in r:
            a = s.split('|')
            b = a[1] == '1'
            self.q.append([a[0], b, a[2].split('$')])
        print(self.q)
        self._f.close()

        self.a = []
        for i in range(len(self.q)):
            self.a.append([])
        self.currAnswers = []
        self.currAnswerCheckboxes = []
        self.currQuestion = 0

        self.b_next.clicked.connect(self.openNextQuestion)
        self.b_prev.clicked.connect(self.openPrevQuestion)

        self.loadQuestion()

    def loadQuestion(self):
        self.question: QTextEdit
        self.question.setPlainText(self.q[self.currQuestion][0])

        self.answer_layout: QVBoxLayout
        self.currAnswerCheckboxes.clear()
        self.currAnswers.clear()

        self.count: QLabel
        self.count.setText(f"Вопрос {str(self.currQuestion + 1)}/{str(len(self.q))}")

        if self.q[self.currQuestion][2]:
            self.currAnswers.extend(self.q[self.currQuestion][2])

        while self.answer_layout.count() - 1 > 0:
            child = self.answer_layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()

        for i in range(len(self.currAnswers)):
            check = QCheckBox(text="")
            self.answer_layout.addWidget(check)
            self.currAnswerCheckboxes.append(check)
            if i in self.a[self.currQuestion]:
                check.setChecked(True)
            self.currAnswers[i] = self.currAnswers[i][1:]
            check.setText(self.currAnswers[i])

        if self.q[self.currQuestion][1]:
            for cb in self.answer_layout.children():
                cb.clicked.connect(self.recheck, cb.isChecked())
            self.label_answers.setText("Выберите один правильный вариант ответа")
        else:
            self.label_answers.setText("Выберите несколько правильных вариантов ответа")

    def recheck(self, b=False):
        for cb in self.currAnswerCheckboxes:
            cb.setChecked(False)
        self.sender().setChecked(b)

    def saveCurrQuestion(self):
        s = []

        for i in range(len(self.currAnswerCheckboxes)):
            if self.currAnswerCheckboxes[i].isChecked():
                s.append(i)

        self.a[self.currQuestion].clear()
        self.a[self.currQuestion].extend(s)

    def openNextQuestion(self):
        if self.currQuestion == len(self.q) - 1:
            confirmation = QMessageBox()

            confirmation.setText("Завершить викторину?")
            confirmation.setWindowTitle("Подтверждение")
            confirmation.setIcon(QMessageBox.Icon.Question)
            confirmation.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            yes = confirmation.button(QMessageBox.StandardButton.Yes)
            yes.setText('Завершить')

            no = confirmation.button(QMessageBox.StandardButton.No)
            no.setText('Отмена')

            clickedButton = confirmation.exec()

            if clickedButton == QMessageBox.StandardButton.Yes:
                self.exitPlaying()
            else:
                self.saveCurrQuestion()
                self.loadQuestion()
        else:
            self.saveCurrQuestion()
            self.currQuestion += 1
            self.loadQuestion()

    def openPrevQuestion(self):
        if self.currQuestion == 0:
            return

        self.saveCurrQuestion()
        self.currQuestion -= 1
        self.loadQuestion()

    def exitPlaying(self):
        self.saveCurrQuestion()

        maxPoints = 0
        points = 0
        print(self.a)
        for i in range(len(self.q)):
            for s in range(len(self.q[i][2])):
                if self.q[i][2][s].startswith('+'):
                    maxPoints += 1
                    if s in self.a[i]:
                        points += 1
                    else:
                        points -= 1
                else:
                    if s in self.a[i]:
                        points -= 1

        if points < 0:
            points = 0

        dialog = QMessageBox()

        dialog.setWindowTitle("Итоги")
        if points > maxPoints / 2:
            dialog.setText(f"Поздравляем, вы прошли викторину на {points} баллов из {maxPoints}! Браво!")
        elif points == 0:
            dialog.setText(
                f"Вы прошли викторину на 0 баллов из {maxPoints}. "
                f"Напомню, выбор неправильного ответа вычитает один балл!")
        else:
            dialog.setText(
                f"Вы прошли викторину на {points} баллов из {maxPoints}. Неплохо, но можно было и постараться.")

        dialog.addButton(QMessageBox.StandardButton.Yes)
        yes = dialog.button(QMessageBox.StandardButton.Yes)
        yes.setText('Завершить викторину')

        clickedButton = dialog.exec()

        if clickedButton == QMessageBox.StandardButton.Yes:
            self.parent().show()
            self.hide()

    def closeEvent(self, e):
        exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_menu = MainMenu()
    # create = Create()
    # play = Play()
    #
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
