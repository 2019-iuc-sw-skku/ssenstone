import sys
import server
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from model_names import ModelNames

class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Server")
        
        grid = QGridLayout()

        grid.addWidget(self.numOfModel(), 0, 0)
        grid.addWidget(self.log(), 1, 0)
        self.setLayout(grid)

        self.show()


    def numOfModel(self):
        '''Browse Models란을 구성하는 함수입니다.

        해야할일
        1. Number of Model에 따라서
        밑에 파일경로를 입력받는 란의 개수가 조절되게 끔 만들어야 함.'''
        groupbox = QGroupBox('Browse Models')

        grid = QGridLayout()

        self.cb = QComboBox(self)
        self.cb.addItems(['1', '3'])
        

        grid.addWidget(QLabel("Number of model", self), 0, 0)
        grid.addWidget(self.cb, 1, 0)

        self.le1 = QLineEdit("", self)
        self.le2 = QLineEdit("", self)
        self.le3 = QLineEdit("", self)
        
        btn1 = QPushButton("Browse..", self)
        btn2 = QPushButton("Browse..", self)
        btn3 = QPushButton("Browse..", self)
        
        for i in [0, 1, 2]:
            grid.addWidget(QLabel('Model ' + str(i + 1), self), i + 2, 0)

        self.cb1 = QComboBox(self)
        self.cb1.addItems(['Random forest', 'Autoencoded Deep Learning'])
        self.cb2 = QComboBox(self)
        self.cb2.addItems(['Random forest', 'Autoencoded Deep Learning'])
        self.cb3 = QComboBox(self)
        self.cb3.addItems(['Random forest', 'Autoencoded Deep Learning'])
            
        grid.addWidget(self.cb1, 2, 1)
        grid.addWidget(self.cb2, 3, 1)
        grid.addWidget(self.cb3, 4, 1)

        grid.addWidget(self.le1, 2, 2)
        grid.addWidget(self.le2, 3, 2)
        grid.addWidget(self.le3, 4, 2)

        grid.addWidget(btn1, 2, 3)
        grid.addWidget(btn2, 3, 3)
        grid.addWidget(btn3, 4, 3)

        btn1.clicked.connect(self.btn1Clicked)
        btn2.clicked.connect(self.btn2Clicked)
        btn3.clicked.connect(self.btn3Clicked)

        groupbox.setLayout(grid)

        return groupbox

    def btn1Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", ".", "sav(*.sav);;all files(*.*)")
        self.le1.setText(fname[0])

    def btn2Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", ".", "sav(*.sav);;all files(*.*)")
        self.le2.setText(fname[0])

    def btn3Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", ".", "sav(*.sav);;all files(*.*)")
        self.le3.setText(fname[0])


    def log(self):
        '''Server log란을 구성하는 함수입니다.

        해야할 일
        1. Start를 누르면 서버가 시작, Stop을 누르면 서버가 중지되게끔 
        serverHandle을 수정해야합니다.
        2. TextBrowser에 log가 업데이트 되도록 해야합니다.'''
        groupbox = QGroupBox('Server log')

        grid = QGridLayout()

        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.server_handle)
        grid.addWidget(self.button, 0, 0)

        self.logtext = QTextBrowser()

        grid.addWidget(self.logtext, 1, 0)

        groupbox.setLayout(grid)
        return groupbox

    def server_handle(self):
        if self.button.text() == 'Start':
            self.button.setText('Stop')

            # 서버 시작작업
            pathlist = []
            pathlist.append(self.le1.text())

            modelnamelist = []
            modelnamelist.append(self.cb1.currentIndex())

            if self.cb.currentText() == '3':
                pathlist.append(self.le2.text())
                pathlist.append(self.le3.text())

                modelnamelist.append(self.cb2.currentIndex())
                modelnamelist.append(self.cb3.currentIndex())

            self.serverthread = server.run_server(('localhost', 1234), pathlist, modelnamelist, 1)

        elif self.button.text() == 'Stop':
            
            # 서버 중지작업
            self.serverthread.stop()
            self.button.setText('Start')


class Stream(QtCore.QObject):
    new_text = QtCore.pyqtSignal(str)

    def write(self, text):
        self.new_text.emit(str(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = ServerGUI()
    app.exec_()