import sys
import server
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from model_names import ModelNames

HOST = 'localhost'
PORT = 1234

class ModelNumberError(Exception):
    pass

class StdoutRedirect(QtCore.QObject):
    printOccur = QtCore.pyqtSignal(str, str, name="print")

    def __init__(self, *param):
        QtCore.QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write =  lambda msg : self.write(msg, color="red")

    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)

class ServerGUI(QWidget):
    def __init__(self, parent = None):
        super(ServerGUI, self).__init__(parent)

        self._stdout = StdoutRedirect()
        self._stdout.printOccur.connect(lambda x : self._append_text(x))

        self.initUI()

    def _append_text(self, msg):
        self.logtext.append(msg)
        QApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)

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
        if self.cb1.currentText() == 'Random forest':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "sav(*.sav)")
        elif self.cb1.currentText() == 'Autoencoded Deep Learning':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "h5(*.h5)")
        self.le1.setText(fname[0])

    def btn2Clicked(self):
        if self.cb2.currentText() == 'Random forest':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "sav(*.sav)")
        elif self.cb2.currentText() == 'Autoencoded Deep Learning':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "h5(*.h5)")
        self.le2.setText(fname[0])

    def btn3Clicked(self):
        if self.cb3.currentText() == 'Random forest':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "sav(*.sav)")
        elif self.cb3.currentText() ==  'Autoencoded Deep Learning':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./models", "h5(*.h5)")
        self.le3.setText(fname[0])


    def log(self):
        '''
        Server log란을 구성하는 함수입니다.

        해야할 일
        log출력부분 줄간격조정을 해야합니다.
        '''
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
            try:
                pathlist = []
                modelnamelist = []

                if self.le1.text() == '':
                    raise ModelNumberError()
                
                pathlist.append(self.le1.text())
                modelnamelist.append(self.cb1.currentIndex())
                
                if int(self.cb.currentText()) >= 2:
                    if self.le2.text() == '':
                        raise ModelNumberError()
                    pathlist.append(self.le2.text())
                    modelnamelist.append(self.cb2.currentIndex())
                    
                if int(self.cb.currentText()) >= 3:
                    if self.le3.text() == '':
                        raise ModelNumberError()
                    pathlist.append(self.le3.text())
                    modelnamelist.append(self.cb3.currentIndex())

                self.button.setText('Stop')

                self.logtext.clear()
                self._stdout.start()

                self.serverthread = server.run_server((HOST, PORT), pathlist, modelnamelist, 1)
            except ModelNumberError:
                msgbox = QMessageBox()
                msgbox.setText('Please select models correctly')
                msgbox.exec()

        elif self.button.text() == 'Stop':
            
            # 서버 중지작업
            self.serverthread.stop()
            self._stdout.stop()
            self.button.setText('Start')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = ServerGUI()
    app.exec_()