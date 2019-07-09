import sys
from PyQt5.QtWidgets import *

class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(800, 200, 600, 600)
        self.setWindowTitle("Server")
        
        grid = QGridLayout()

        grid.addWidget(self.numOfModel(), 0, 0)
        grid.addWidget(self.labeledData(), 1, 0)
        grid.addWidget(self.log(), 2, 0)
        self.setLayout(grid)

        self.show()

# Browse Models란을 구성하는 함수입니다.

# 해야할일
# 1. Number of Model에 따라서
# 밑에 파일경로를 입력받는 란의 개수가 조절되게 끔 만들어야 함.

    def numOfModel(self):
        groupbox = QGroupBox('Browse Models')

        grid = QGridLayout()

        cb = QComboBox(self)
        cb.addItems(['1', '3'])
        

        grid.addWidget(QLabel("Number of model", self), 0, 0)
        grid.addWidget(cb, 1, 0)

        self.le1 = QLineEdit("", self)
        self.le2 = QLineEdit("", self)
        self.le3 = QLineEdit("", self)
        
        btn1 = QPushButton("Browse..", self)
        btn2 = QPushButton("Browse..", self)
        btn3 = QPushButton("Browse..", self)
        
        for i in [0, 1, 2]:
            grid.addWidget(QLabel('Model ' + str(i + 1), self), i + 2, 0)
            
        grid.addWidget(self.le1, 2, 1)
        grid.addWidget(self.le2, 3, 1)
        grid.addWidget(self.le3, 4, 1)

        grid.addWidget(btn1, 2, 2)
        grid.addWidget(btn2, 3, 2)
        grid.addWidget(btn3, 4, 2)

        btn1.clicked.connect(self.btn1Clicked)
        btn2.clicked.connect(self.btn2Clicked)
        btn3.clicked.connect(self.btn3Clicked)

        groupbox.setLayout(grid)

        return groupbox

    def btn1Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "sav(*.sav)")
        self.le1.setText(fname[0])

    def btn2Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "sav(*.sav)")
        self.le2.setText(fname[0])

    def btn3Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "sav(*.sav)")
        self.le3.setText(fname[0])


# Saving location of sorted labeled data란을 구성하는 함수입니다.

    def labeledData(self):
        groupbox = QGroupBox('Saving location of sorted labeled data')

        grid = QGridLayout()

        self.ql = QLineEdit("", self)
        grid.addWidget(self.ql, 0, 0)
        btn = QPushButton("Browse..", self)
        grid.addWidget(btn, 0, 1)
        btn.clicked.connect(self.labeledDataButton)

        groupbox.setLayout(grid)

        return groupbox

    def labeledDataButton(self):
        fname = QFileDialog.getSaveFileName(self, "Save File", ".", "csv(*.csv)")
        self.ql.setText(fname[0])


# Server log란을 구성하는 함수입니다.

# 해야할 일
# 1. Start를 누르면 서버가 시작, Stop을 누르면 서버가 중지되게끔 
# serverHandle을 수정해야합니다.
# 2. TextBrowser에 log가 업데이트 되도록 해야합니다.

    def log(self):
        groupbox = QGroupBox('Server log')

        grid = QGridLayout()

        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.serverHandle)
        grid.addWidget(self.button, 0, 0)

        self.logtext = QTextBrowser()

        grid.addWidget(self.logtext, 1, 0)

        groupbox.setLayout(grid)
        return groupbox

    def serverHandle(self):
        if self.button.text() == 'Start':
            self.button.setText('Stop')

            # 서버 시작작업

        elif self.button.text() == 'Stop':
            self.button.setText('Start')

            # 서버 중지작업

if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = ServerGUI()
    app.exec_()