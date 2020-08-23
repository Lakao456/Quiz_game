from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()


def clicked():
    print("button clicked")


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200,200,300,300)
    win.setWindowTitle("First")

    label = QtWidgets.QLabel(win)
    label.setText("abc")
    label.move(50,50)

    button1 = QtWidgets.QPushButton(win)
    button1.setText("click me")
    button1.clicked.connect(clicked)


    win.show()
    sys.exit(app.exec_())

window()