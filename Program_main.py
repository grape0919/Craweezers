import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from view.main import Ui_MainWindow

class WindowClass(QMainWindow, Ui_MainWindow) :

    def __init__(self) :
        super(WindowClass, self).__init__()
        self.setupUi(self)
        self.comboBox.addItem("네이버>뉴스>경제>금융")
        self.comboBox.addItem("네이버>뉴스>경제>증권")
        self.comboBox.addItem("네이버>뉴스>경제>산업/재계")
        self.comboBox.addItem("네이버>뉴스>경제>중기/벤처")
        self.comboBox.addItem("네이버>뉴스>경제>부동산")
        self.comboBox.addItem("네이버>뉴스>정치>국회/정당")
        self.comboBox.addItem("네이버>뉴스>정치>행정")
        self.comboBox.addItem("네이버>뉴스>사회>사건사고")
        self.comboBox.addItem("...")

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()