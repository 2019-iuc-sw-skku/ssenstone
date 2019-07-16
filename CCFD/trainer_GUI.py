import sys
import trainer
from PyQt5.QtWidgets import *

class TrainerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 600, 600)
        self.setWindowTitle("Classifier")

        grid = QGridLayout()

        grid.addWidget(self.browseData(), 0, 0)
        grid.addWidget(self.modelSetting(), 1, 0)
        grid.addWidget(self.trainStart(), 2, 0)

        self.setLayout(grid)
        self.show()

    def browseData(self):
        groupbox = QGroupBox('Browse Data Sets')

        grid = QGridLayout()

        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.te.setReadOnly(True)

        btn = QPushButton("Browse..", self)
        btn.clicked.connect(self.buttonClicked)

        grid.addWidget(self.te, 0, 0)
        grid.addWidget(btn, 0, 1)

        groupbox.setLayout(grid)

        return groupbox

    def buttonClicked(self):
        fname = QFileDialog.getOpenFileNames(self, "Load File", ".", "csv(*.csv)")
        for i in fname[0]:
            self.te.append(i)

    def modelSetting(self):
        groupbox = QGroupBox('Select Model')

        self.modelgrid = QGridLayout()

        self.makeOptionGrid()

        self.cb = QComboBox(self)
        self.cb.addItems(['Random Forest', 'Autoencoded Deep Learning', 'Support Vector Machine', 'Logistic Regression'])
        self.cb.currentIndexChanged.connect(self.modelChanged)

        self.modelgrid.addWidget(self.cb, 0, 0)
        self.modelgrid.addLayout(self.optiongrid, 1, 0)

        groupbox.setLayout(self.modelgrid)

        return groupbox

    def modelChanged(self):
        if self.cb.currentText() == 'Random Forest':
            self.rfoption.show()
            self.rftext.show()

            self.dloption.hide()
            self.dltext.hide()

            self.svmoption.hide()
            self.svmcombo.hide()
            self.svmoption1.hide()
            self.svmtext1.hide()

            self.lroption.hide()
            self.lrtext.hide()
            self.lroption1.hide()
            self.lrtext1.hide()
            self.lroption2.hide()
            self.lrcombo.hide()

        elif self.cb.currentText() == 'Autoencoded Deep Learning':
            self.rfoption.hide()
            self.rftext.hide()

            self.dloption.show()
            self.dltext.show()

            self.svmoption.hide()
            self.svmcombo.hide()
            self.svmoption1.hide()
            self.svmtext1.hide()

            self.lroption.hide()
            self.lrtext.hide()
            self.lroption1.hide()
            self.lrtext1.hide()
            self.lroption2.hide()
            self.lrcombo.hide()

        elif self.cb.currentText() == 'Support Vector Machine':
            self.rfoption.hide()
            self.rftext.hide()

            self.dloption.hide()
            self.dltext.hide()

            self.svmoption.show()
            self.svmcombo.show()
            self.svmoption1.show()
            self.svmtext1.show()

            self.lroption.hide()
            self.lrtext.hide()
            self.lroption1.hide()
            self.lrtext1.hide()
            self.lroption2.hide()
            self.lrcombo.hide()

        elif self.cb.currentText() == 'Logistic Regression':
            self.rfoption.hide()
            self.rftext.hide()

            self.dloption.hide()
            self.dltext.hide()

            self.svmoption.hide()
            self.svmcombo.hide()
            self.svmoption1.hide()
            self.svmtext1.hide()

            self.lroption.show()
            self.lrtext.show()
            self.lroption1.show()
            self.lrtext1.show()
            self.lroption2.show()
            self.lrcombo.show()
            

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

        self.dloption.hide()
        self.dltext.hide()
        self.svmoption.hide()
        self.svmcombo.hide()
        self.svmoption1.hide()
        self.svmtext1.hide()
        self.lroption.hide()
        self.lrtext.hide()
        self.lroption1.hide()
        self.lrtext1.hide()
        self.lroption2.hide()
        self.lrcombo.hide()
        
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

        grid.addWidget(QLabel('Save File Location'), 0, 0)
        grid.addWidget(self.te1, 0, 1)
        grid.addWidget(btn1, 0, 2)
        grid.addWidget(QLabel('Save Scaler Location'), 1, 0)
        grid.addWidget(self.te2, 1, 1)
        grid.addWidget(btn2, 1, 2)
        grid.addWidget(self.startbtn, 2, 2)

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
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrainerGUI()
    sys.exit(app.exec_())
