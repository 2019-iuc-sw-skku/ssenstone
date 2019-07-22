import sys
import server
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from model_names import ModelNames

HOST = 'localhost'
PORT = 1234

class ButtonThread(threading.Thread):
    def __init__(self, btn):
        threading.Thread.__init__(self)
        self.btn = btn
    
    def run(self):
        self.btn.setDisabled(True)
        time.sleep(3)
        self.btn.setDisabled(False)

class ModelNumberError(Exception):
    '''
    If the number of model is not matched,
    this error occur.
    '''
    pass

class StdoutRedirect(QtCore.QObject):
    printOccur = QtCore.pyqtSignal(str, str, name="print")

    def __init__(self):
        QtCore.QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg: self.write(msg, color="red")

    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)

class ServerGUI(QWidget):
    def __init__(self, parent=None):
        super(ServerGUI, self).__init__(parent)

        self._stdout = StdoutRedirect()
        self._stdout.printOccur.connect(lambda x: self._append_text(x))

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
        '''
        Browse Models란을 구성하는 함수입니다.
        '''
        groupbox = QGroupBox('Browse Models')

        grid = QGridLayout()

        self.cb = QComboBox(self)
        self.cb.addItems(['1', '2', '3'])

        self.cb.currentIndexChanged.connect(self.numChanged)

        grid.addWidget(QLabel("Number of model", self), 0, 0)
        grid.addWidget(self.cb, 1, 0)

        thresholdlabel = QLabel("Threshold Score", self)
        thresholdlabel.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(thresholdlabel, 0, 1)
        radiobuttongroup = QGroupBox()
        radiobuttongrid = QGridLayout()
        
        self.rbtn1 = QRadioButton('1', self)
        self.rbtn2 = QRadioButton('2', self)
        self.rbtn3 = QRadioButton('3', self)

        self.rbtn1.setChecked(True)
        self.rbtn2.setDisabled(True)
        self.rbtn3.setDisabled(True)

        radiobuttongrid.addWidget(self.rbtn1, 0, 0)
        radiobuttongrid.addWidget(self.rbtn2, 0, 1)
        radiobuttongrid.addWidget(self.rbtn3, 0, 2)

        radiobuttongroup.setLayout(radiobuttongrid)

        grid.addWidget(radiobuttongroup, 1, 1)

        self.le1 = QLineEdit("", self)
        self.le1.setReadOnly(True)
        self.le2 = QLineEdit("", self)
        self.le2.setReadOnly(True)
        self.le3 = QLineEdit("", self)
        self.le3.setReadOnly(True)

        self.btn1 = QPushButton("Browse..", self)
        self.btn2 = QPushButton("Browse..", self)
        self.btn3 = QPushButton("Browse..", self)

        self.btn2.setDisabled(True)
        self.btn3.setDisabled(True)

        self.sbtn1 = QPushButton("Browse..", self)
        self.sbtn2 = QPushButton("Browse..", self)
        self.sbtn3 = QPushButton("Browse..", self)

        self.sbtn2.setDisabled(True)
        self.sbtn3.setDisabled(True)

        for i in [1, 2, 3]:
            grid.addWidget(QLabel('Model ' + str(i), self), 2 * i, 0)
            grid.addWidget(QLabel('Scaler ' + str(i), self), 2 * i + 1, 0)

        self.cb1 = QComboBox(self)
        self.cb1.addItems(['Random forest', 'Autoencoded Deep Learning', 'Support Vector Machine', 'Logistic Regression'])
        self.cb1.currentIndexChanged.connect(self.cb1Changed)

        self.cb2 = QComboBox(self)
        self.cb2.addItems(['Random forest', 'Autoencoded Deep Learning', 'Support Vector Machine', 'Logistic Regression'])
        self.cb2.currentIndexChanged.connect(self.cb2Changed)
        self.cb2.setDisabled(True)

        self.cb3 = QComboBox(self)
        self.cb3.addItems(['Random forest', 'Autoencoded Deep Learning', 'Support Vector Machine', 'Logistic Regression'])
        self.cb3.currentIndexChanged.connect(self.cb3Changed)
        self.cb3.setDisabled(True)

        self.sle1 = QLineEdit("", self)
        self.sle1.setReadOnly(True)
        self.sle2 = QLineEdit("", self)
        self.sle2.setReadOnly(True)
        self.sle3 = QLineEdit("", self)
        self.sle3.setReadOnly(True)

        grid.addWidget(self.cb1, 2, 1)
        grid.addWidget(self.cb2, 4, 1)
        grid.addWidget(self.cb3, 6, 1)

        grid.addWidget(self.le1, 2, 2)
        grid.addWidget(self.le2, 4, 2)
        grid.addWidget(self.le3, 6, 2)

        grid.addWidget(self.sle1, 3, 2)
        grid.addWidget(self.sle2, 5, 2)
        grid.addWidget(self.sle3, 7, 2)

        grid.addWidget(self.btn1, 2, 3)
        grid.addWidget(self.btn2, 4, 3)
        grid.addWidget(self.btn3, 6, 3)

        grid.addWidget(self.sbtn1, 3, 3)
        grid.addWidget(self.sbtn2, 5, 3)
        grid.addWidget(self.sbtn3, 7, 3)

        self.btn1.clicked.connect(self.btn1Clicked)
        self.btn2.clicked.connect(self.btn2Clicked)
        self.btn3.clicked.connect(self.btn3Clicked)

        self.sbtn1.clicked.connect(self.sbtn1Clicked)
        self.sbtn2.clicked.connect(self.sbtn2Clicked)
        self.sbtn3.clicked.connect(self.sbtn3Clicked)

        groupbox.setLayout(grid)

        return groupbox

    def numChanged(self):
        if self.cb.currentText() == '1':
            self.cb2.setDisabled(True)
            self.cb3.setDisabled(True)

            self.btn2.setDisabled(True)
            self.btn3.setDisabled(True)

            self.sbtn2.setDisabled(True)
            self.sbtn3.setDisabled(True)


            self.rbtn1.setChecked(True)
            self.rbtn2.setDisabled(True)
            self.rbtn3.setDisabled(True)

        elif self.cb.currentText() == '2':
            self.cb2.setDisabled(False)
            self.cb3.setDisabled(True)

            self.btn2.setDisabled(False)
            self.btn3.setDisabled(True)

            self.sbtn2.setDisabled(False)
            self.sbtn3.setDisabled(True)

            self.rbtn2.setChecked(True)
            self.rbtn2.setDisabled(False)
            self.rbtn3.setDisabled(True)

        elif self.cb.currentText() == '3':
            self.cb2.setDisabled(False)
            self.cb3.setDisabled(False)

            self.btn2.setDisabled(False)
            self.btn3.setDisabled(False)

            self.sbtn2.setDisabled(False)
            self.sbtn3.setDisabled(False)

            self.rbtn2.setChecked(True)
            self.rbtn2.setDisabled(False)
            self.rbtn3.setDisabled(False)

    def cb1Changed(self):
        self.le1.clear()
        self.sle1.clear()

    def cb2Changed(self):
        self.le2.clear()
        self.sle2.clear()

    def cb3Changed(self):
        self.le3.clear()
        self.sle3.clear()

    def btn1Clicked(self):
        if self.cb1.currentText() == 'Autoencoded Deep Learning':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/models", "h5(*.h5)")
        else:
            fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/models", "sav(*.sav)")
        self.le1.setText(fname[0])

    def btn2Clicked(self):
        if self.cb2.currentText() == 'Autoencoded Deep Learning':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/models", "h5(*.h5)")
        else:
            fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/models", "sav(*.sav)")
        self.le2.setText(fname[0])

    def btn3Clicked(self):
        if self.cb3.currentText() == 'Autoencoded Deep Learning':
            fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/models", "h5(*.h5)")
        else:
            fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/models", "sav(*.sav)")
        self.le3.setText(fname[0])

    def sbtn1Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/scalers", "sav(*.sav)")
        self.sle1.setText(fname[0])

    def sbtn2Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/scalers", "sav(*.sav)")
        self.sle2.setText(fname[0])

    def sbtn3Clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", "./CCFD/scalers", "sav(*.sav)")
        self.sle3.setText(fname[0])

    def log(self):
        '''
        Server log란을 구성하는 함수입니다.
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

    def getThresholdScore(self):
        if self.rbtn1.isChecked():
            return 1
        elif self.rbtn2.isChecked():
            return 2
        elif self.rbtn3.isChecked():
            return 3

    def server_handle(self):
        btnthread = ButtonThread(self.button)

        if self.button.text() == 'Start':
            try:
                pathlist = []
                scalerlist = []
                modelnamelist = []

                if self.le1.text() == '' or self.sle1.text() == '':
                    raise ModelNumberError()

                pathlist.append(self.le1.text())
                scalerlist.append(self.sle1.text())
                modelnamelist.append(ModelNames(self.cb1.currentIndex()))

                if int(self.cb.currentText()) >= 2:
                    if self.le2.text() == '' or self.sle2.text() == '':
                        raise ModelNumberError()
                    pathlist.append(self.le2.text())
                    scalerlist.append(self.sle2.text())
                    modelnamelist.append(ModelNames(self.cb2.currentIndex()))
                    
                if int(self.cb.currentText()) >= 3:
                    if self.le3.text() == '' or self.sle3.text() == '':
                        raise ModelNumberError()
                    pathlist.append(self.le3.text())
                    scalerlist.append(self.sle3.text())
                    modelnamelist.append(ModelNames(self.cb3.currentIndex()))

                score = self.getThresholdScore()
                self.button.setText('Stop')

                self.logtext.clear()
                self._stdout.start()

                btnthread.start()
                self.serverthread = server.run_server((HOST, PORT), pathlist, scalerlist, modelnamelist, score)

            except ModelNumberError:
                msgbox = QMessageBox()
                msgbox.setText('Please select models correctly')
                msgbox.exec()

        elif self.button.text() == 'Stop':

            # 서버 중지작업
            btnthread.start()
            self.serverthread.stop()
            self._stdout.stop()
            self.button.setText('Start')

    def closeEvent(self, event):
        if hasattr(self, 'serverthread') and self.serverthread.is_alive():
            '''
            reply = QMessageBox.question(self, 'Message',
                                         "Server is still alive.\nAre you sure to quit?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.serverthread.stop()
                self._stdout.stop()
                event.accept()
            else:
                event.ignore()
            '''
            self.serverthread.stop()
            self._stdout.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = ServerGUI()
    app.exec_()
