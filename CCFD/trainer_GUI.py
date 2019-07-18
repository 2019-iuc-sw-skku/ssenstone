'''
original data: 원래 가지고 있던 데이터
new data: 새로 들어온 데이터

original data의 끝에 new data들을 붙여서 original data를 업데이트 한 후
trainer에게 학습하는데 필요한 인자들과 같이 전달을 합니다.
'''

import sys
import csv
import trainer
import threading
import time
from model_names import ModelNames
from PyQt5.QtWidgets import *

class ProgressThread(threading.Thread):
    def __init__(self, text, fd, btn):
        threading.Thread.__init__(self)
        self.text = text
        self.fd = fd
        self.btn = btn

    def run(self):
        while self.fd.is_alive():
            time.sleep(1)

        self.text.setText('Done')
        self.fd.predict_current_model()
        self.btn.setDisabled(False)


class FilePathError(Exception):
    pass

class TrainerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.pathlist = []

        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 600, 600)
        self.setWindowTitle("Trainer")

        grid = QGridLayout()

        grid.addWidget(self.browseOriginalData(), 0, 0)
        grid.addWidget(self.browseNewData(), 1, 0)
        grid.addWidget(self.modelSetting(), 2, 0)
        grid.addWidget(self.trainStart(), 3, 0)

        self.setLayout(grid)
        self.show()

    def browseOriginalData(self):
        groupbox = QGroupBox('Browse Original Data Set')

        grid = QGridLayout()

        self.le = QLineEdit()
        self.le.setReadOnly(True)

        btn = QPushButton("Browse..", self)
        btn.clicked.connect(self.originalButton)

        grid.addWidget(self.le, 0, 0)
        grid.addWidget(btn, 0, 1)

        groupbox.setLayout(grid)

        return groupbox

    def originalButton(self):
        fname = QFileDialog.getOpenFileName(self, "Load File", ".", "csv(*.csv)")
        self.le.setText(fname[0])

    def browseNewData(self):
        groupbox = QGroupBox('Browse New Data Sets')

        grid = QGridLayout()
        buttongrid = QGridLayout()

        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.te.setReadOnly(True)

        btn = QPushButton("Browse..", self)
        btn.clicked.connect(self.buttonClicked)

        btn2 = QPushButton("Clear", self)
        btn2.clicked.connect(self.clearButton)

        buttongrid.addWidget(btn, 0, 0)
        buttongrid.addWidget(btn2, 1, 0)

        grid.addWidget(self.te, 0, 0)
        grid.addLayout(buttongrid, 0, 1)

        groupbox.setLayout(grid)

        return groupbox

    def buttonClicked(self):
        fname = QFileDialog.getOpenFileNames(self, "Load Files", ".", "csv(*.csv)")

        for i in fname[0]:
            if i not in self.pathlist:
                self.te.append(i)
                self.pathlist.append(i)

    def clearButton(self):
        self.te.clear()
        self.pathlist = []

    def modelSetting(self):
        groupbox = QGroupBox('Select Model')

        self.modelgrid = QGridLayout()
        self.selectgrid = QGridLayout()
        self.makeOptionGrid()

        self.cb = QComboBox(self)
        self.cb.addItems(['Random Forest', 'Autoencoded Deep Learning', 'Support Vector Machine', 'Logistic Regression'])
        self.cb.currentIndexChanged.connect(self.modelChanged)

        self.pcttext = QLineEdit('0.4')

        self.selectgrid.addWidget(self.cb, 0, 0)
        self.selectgrid.addWidget(QLabel('train_pct ( 0 < x < 1 )', self), 0, 1)
        self.selectgrid.addWidget(self.pcttext, 0, 2)

        self.modelgrid.addLayout(self.selectgrid, 0, 0)
        self.modelgrid.addLayout(self.optiongrid, 1, 0)

        groupbox.setLayout(self.modelgrid)

        return groupbox

    def modelChanged(self):
        if self.cb.currentText() == 'Random Forest':
            self.rfshow()
            self.dlhide()
            self.svmhide()
            self.lrhide()

        elif self.cb.currentText() == 'Autoencoded Deep Learning':
            self.rfhide()
            self.dlshow()
            self.svmhide()
            self.lrhide()

        elif self.cb.currentText() == 'Support Vector Machine':
            self.rfhide()
            self.dlhide()
            self.svmshow()
            self.lrhide()

        elif self.cb.currentText() == 'Logistic Regression':
            self.rfhide()
            self.dlhide()
            self.svmhide()
            self.lrshow()

    def rfshow(self):
        self.rfoption.show()
        self.rftext.show()

    def rfhide(self):
        self.rfoption.hide()
        self.rftext.hide()

    def dlshow(self):
        self.dloption.show()
        self.dltext.show()

    def dlhide(self):
        self.dloption.hide()
        self.dltext.hide()

    def svmshow(self):
        self.svmoption.show()
        self.svmcombo.show()
        self.svmoption1.show()
        self.svmtext1.show()

    def svmhide(self):
        self.svmoption.hide()
        self.svmcombo.hide()
        self.svmoption1.hide()
        self.svmtext1.hide()

    def lrshow(self):
        self.lroption.show()
        self.lrtext.show()
        self.lroption1.show()
        self.lrtext1.show()
        self.lroption2.show()
        self.lrcombo.show()

    def lrhide(self):
        self.lroption.hide()
        self.lrtext.hide()
        self.lroption1.hide()
        self.lrtext1.hide()
        self.lroption2.hide()
        self.lrcombo.hide()

    def makeOptionGrid(self):
        self.optiongrid = QGridLayout()

        self.rfoption = QLabel('n_estimators', self)
        self.optiongrid.addWidget(self.rfoption, 0, 0)
        self.rftext = QLineEdit('100')
        self.optiongrid.addWidget(self.rftext, 0, 1)

        self.dloption = QLabel('epochs', self)
        self.optiongrid.addWidget(self.dloption, 0, 0)
        self.dltext = QLineEdit('100')
        self.optiongrid.addWidget(self.dltext, 0, 1)

        self.svmoption = QLabel('kernel', self)
        self.optiongrid.addWidget(self.svmoption, 0, 0)
        self.svmcombo = QComboBox(self)
        self.svmcombo.addItems(['rbf', 'linear'])
        self.optiongrid.addWidget(self.svmcombo, 0, 1)
        self.svmoption1 = QLabel('C (penalty)')
        self.optiongrid.addWidget(self.svmoption1, 0, 2)
        self.svmtext1 = QLineEdit('1.0')
        self.optiongrid.addWidget(self.svmtext1, 0, 3)

        
        self.lroption = QLabel('C', self)
        self.optiongrid.addWidget(self.lroption, 0, 2)
        self.lrtext = QLineEdit('0.1')
        self.optiongrid.addWidget(self.lrtext, 0, 3)
        self.lroption1 = QLabel('max_iter', self)
        self.optiongrid.addWidget(self.lroption1, 0, 4)
        self.lrtext1 = QLineEdit('300')
        self.optiongrid.addWidget(self.lrtext1, 0, 5)
        self.lroption2 = QLabel('solver', self)
        self.optiongrid.addWidget(self.lroption2, 0, 0)
        self.lrcombo = QComboBox(self)
        self.lrcombo.addItems(['newton-cg', 'lbfgs', 'sag', 'saga'])
        self.optiongrid.addWidget(self.lrcombo, 0, 1)

        self.dlhide()
        self.svmhide()
        self.lrhide()
        
    def trainStart(self):
        groupbox = QGroupBox('Training')

        grid = QGridLayout()

        self.te1 = QLineEdit()
        self.te1.setReadOnly(True)
        self.te2 = QLineEdit()
        self.te2.setReadOnly(True)
        self.startbtn = QPushButton("start", self)
        self.startbtn.clicked.connect(self.startButton)

        btn1 = QPushButton("Browse..", self)
        btn1.clicked.connect(self.button1Clicked)
        btn2 = QPushButton("Browse..", self)
        btn2.clicked.connect(self.button2Clicked)

        self.statelabel = QLabel('Wait...', self)

        grid.addWidget(QLabel('Save File Location'), 0, 0)
        grid.addWidget(self.te1, 0, 1)
        grid.addWidget(btn1, 0, 2)
        grid.addWidget(QLabel('Save Scaler Location'), 1, 0)
        grid.addWidget(self.te2, 1, 1)
        grid.addWidget(btn2, 1, 2)
        grid.addWidget(self.startbtn, 2, 2)
        grid.addWidget(QLabel('State'), 2, 0)
        grid.addWidget(self.statelabel, 2, 1)

        groupbox.setLayout(grid)

        return groupbox
    
    def button1Clicked(self):
        if self.cb.currentText() == 'Autoencoded Deep Learning':
            fname = QFileDialog.getSaveFileName(self, "Save File", "./CCFD/models", "h5(*.h5)")
        else:
            fname = QFileDialog.getSaveFileName(self, "Save File", "./CCFD/models", "sav(*.sav)")
        self.te1.setText(fname[0])

    def button2Clicked(self):
        fname = QFileDialog.getSaveFileName(self, "Save File", "./CCFD/scalers", "sav(*.sav)")
        self.te2.setText(fname[0])

    def startButton(self):
        self.startbtn.setDisabled(True)
        try:
            pct = float(self.pcttext.text())

            if pct <= 0 or pct >= 1:
                raise ValueError

            sav = self.te1.text()
            if sav == '':
                raise FilePathError()
            
            scaler = self.te2.text()
            if scaler == '':
                raise FilePathError()

            arguments = self.getProperties()

            self.combineData()

            
            self.statelabel.setText('Training...')

            FD = trainer.Trainer(self.le.text(), train_pct=pct, output_path=sav, output_scaler_path=scaler,
                                 model_name=ModelNames(self.cb.currentIndex()), properties=arguments)
            
            progress = ProgressThread(self.statelabel, FD, self.startbtn)

            FD.start()
            progress.start()

        except FileNotFoundError:
            msgbox = QMessageBox()
            msgbox.setText('Please select data correctly')
            msgbox.exec()
        except ValueError:
            msgbox = QMessageBox()
            msgbox.setText('Please write values correctly')
            msgbox.exec()
        except FilePathError:
            msgbox = QMessageBox()
            msgbox.setText('Please select output path correctly')
            msgbox.exec()

    def combineData(self):
        with open(self.le.text(), 'a', newline='') as original_data:
            if self.pathlist != ['']:
                filewriter = csv.writer(original_data)
                for path in self.pathlist:
                    with open(path, 'r', newline='') as new_data:
                        filereader = csv.reader(new_data)
                        header = next(filereader)
                        for row in filereader:
                            filewriter.writerow(row)
    
    def getProperties(self):
        properties = dict()

        if self.cb.currentText() == 'Random Forest':
            properties[self.rfoption.text()] = int(self.rftext.text())

        elif self.cb.currentText() == 'Autoencoded Deep Learning':
            properties[self.dloption.text()] = int(self.dltext.text())

        elif self.cb.currentText() == 'Support Vector Machine':
            properties[self.svmoption.text()] = self.svmcombo.currentText()
            properties[self.svmoption1.text()] = float(self.svmtext1.text())

        elif self.cb.currentText() == 'Logistic Regression':
            properties[self.lroption.text()] = float(self.lrtext.text())
            properties[self.lroption1.text()] = int(self.lrtext1.text())
            properties[self.lroption2.text()] = self.lrcombo.currentText()

        return properties


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrainerGUI()
    sys.exit(app.exec_())
