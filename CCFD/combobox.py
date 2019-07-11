import sys
import trainer
import keras
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from model_names import ModelNames

class Form(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui=uic.loadUi("combobox.ui",self)
        self.ui.show()

        self.comboBox.activated.connect(self.showA)
        self.groupBox_NN.hide()
        self.groupBox_SVM.hide()
        self.groupBox_LR.hide()
        self.cancelButton.clicked.connect(self.cancel_clicked)

        self.browse_data.clicked.connect(self.browseData_clicked)
        self.browse_sav.clicked.connect(self.browseSav_clicked)
        self.trainButton.clicked.connect(self.trainStart)

    def browseData_clicked(self):
        fname=QFileDialog.getOpenFileName(self, "Load File", ".", "sav(*.sav);;all files(*.*)")
        self.lineEdit_data.setText(fname[0])

    def browseSav_clicked(self):
        fname=QFileDialog.getOpenFileName(self, "Load File", ".", "sav(*.sav);;all files(*.*)")
        self.lineEdit_sav.setText(fname[0])

    def cancel_clicked(self):
        sys.exit(0)

    def showA(self):
        text=self.comboBox.currentText()
        if text == 'Random Forest':
            self.groupBox_RF.show()
            self.groupBox_NN.hide()
            self.groupBox_SVM.hide()
            self.groupBox_LR.hide()

        elif text == 'Neural Network':
            self.groupBox_RF.hide()
            self.groupBox_NN.show()
            self.groupBox_SVM.hide()
            self.groupBox_LR.hide()

        elif text == 'SVM':
            self.groupBox_RF.hide()
            self.groupBox_NN.hide()
            self.groupBox_SVM.show()
            self.groupBox_LR.hide()

        elif text == 'Logistic Regression':
            self.groupBox_RF.hide()
            self.groupBox_NN.hide()
            self.groupBox_SVM.hide()
            self.groupBox_LR.show()

    def trainStart(self):       #train button
        text=self.comboBox.currentText()
        FD = trainer.Trainer('./CCFD/creditcard.csv')
        if text == 'Random Forest':
            nest=self.groupBox_RF.gridLayout_RF.lineEdit1.text()
            crit=self.groupBox_RF.gridLayout_RF.lineEdit2.text()
            maxd=self.groupBox_RF.gridLayout_RF.lineEdit3.text()

            FD.training(train_pct=0.2, output_path="./model.sav",
                       model_name=ModelNames.RANDOM_FOREST, properties={'n_estimators':nest, 'criterion':crit, 'max_depth':maxd})

        elif text == 'Neural Network':
            epoch=self.groupBox_NN.gridLayout_NN.lineEdit2_1.text()
            optim=self.groupBox_NN.gridLayout_NN.lineEdit2_3.text()
            if optim == 'Adam':
                FD.training(train_pct=0.2, output_path="./model_dl.sav",
                        model_name=ModelNames.AUTOENCODED_DEEP_LEARNING,
                        properties={'epochs': epoch, 'loss': keras.losses.mean_squared_error,
                                    'optimizer': keras.optimizers.Adam()})
            elif optim == 'Eve':
                FD.training(train_pct=0.2, output_path="./model_dl.sav",
                        model_name=ModelNames.AUTOENCODED_DEEP_LEARNING,
                        properties={'epochs': epoch, 'loss': keras.losses.mean_squared_error,
                                    'optimizer': keras.optimizers.Eve()})


if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    w=Form()
    sys.exit(app.exec())