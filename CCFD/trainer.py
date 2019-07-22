'''
분류기 프로그램.
'''

import pickle

from keras import backend as K
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import threading
from keras import regularizers
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Input
from keras.models import Model
from sklearn import naive_bayes, svm
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from model_names import ModelNames


class Trainer(threading.Thread):
    def __init__(self, filepath, train_pct, output_path, output_scaler_path, model_name, properties, random_state=None):
        '''
        parameters:
            filepath(str): path to csv dataset file
            random_state: random seed

        training parameters:
            train_pct(float) : fraction of train data per overall data.
            output_path(str) : path to output model file.
            output_scaler_path(str): path to output scaler file.
            model_name(int)  : enumerated model name.
                               see model_names.py
            properties(dict) : dictionary of properties. depends on model_name.

                Random Forest:
                    Required
                        n_estimators: number of estimators.
                    Others
                        see sklearn.ensemble.RandomForestClassifier.

                example:
                    {'n_estimators': 100}

                Logistic Regression:
                    see sklearn.linear_model.LogisticRegression

                Adaboost:
                    see sklearn.ensemble.AdaBoostClassifier.

                Naive Bayes(Bernoulli):
                    see sklearn.naive_bayes.BernoulliNB

                SVM:
                    kernel = 'linear'
                    see sklearn.svm.SVC
                    
                SVM with RBF kernel:
                    kernel = 'rbf'
                    see sklearn.svm.SVC

                Deep Learning:
                    Required:
                        epochs - int: training trial number.
                        loss - keras.losses.funcname subfunction: loss function
                        optimizer - keras.optimizers.classname class: optimizer class
                    Optional:
                        batch_size: default 32. batch size in one epoch.
                        learning_rate: default 1e-7. learning rate of estimation
                        encoding_dimension: default 32. neural network layer dimension.

                example:
                    {'epochs': 100, 'loss': keras.loss.mean_squared_error, 'optimizer': keras.optimizers.Adam()}

                For an example, you can see CCFD_(algorithm).py file
        '''
        threading.Thread.__init__(self)

        self.RSEED = random_state
        self.fname = filepath
        self.model = None

        self.train_pct = train_pct
        self.output_path = output_path
        self.output_scaler_path = output_scaler_path
        self.model_name = model_name
        self.properties = properties

    def run(self):
        self.training(self.train_pct, self.output_path, self.output_scaler_path, self.model_name, self.properties)

    def training(self, train_pct, output_path, output_scaler_path, model_name, properties):
        self.graph = tf.get_default_graph()
        with self.graph.as_default():
            self.model_name = model_name
            df = pd.read_csv(self.fname)
            df = df.sample(frac=1)

            df_norm = df
    #        df_norm['Time'] = StandardScaler().fit_transform(df_norm['Time'].values.reshape(-1, 1))
    #        df_norm['Amount'] = StandardScaler().fit_transform(df_norm['Amount'].values.reshape(-1, 1))

            
            new_df = df_norm.sample(frac=1, random_state=self.RSEED)
            
            x = new_df.drop('Class', axis=1)
            y = new_df['Class']
            x, tx, y, ty = train_test_split(x, y, train_size=train_pct)

            train_x = x.values
            train_y = y.values
            test_x = tx.values

            sc = StandardScaler()
            train_x = sc.fit_transform(train_x)
            pickle.dump(sc, open(output_scaler_path, "wb"))
            
            if model_name == ModelNames.RANDOM_FOREST:
                
                rf = RandomForestClassifier(**properties, random_state=self.RSEED)
                rf.fit(train_x, train_y)

                pickle.dump(rf, open(output_path, "wb"))

                self.model = rf
            
            elif model_name == ModelNames.LOGISTIC_REGRESSION:
                lr = LogisticRegression(**properties, random_state=self.RSEED)
                lr.fit(train_x, train_y)
                pickle.dump(lr, open(output_path, "wb"))
                self.model = lr

            elif model_name == ModelNames.ADAPTIVE_BOOST:
                ada = AdaBoostClassifier(**properties, random_state=self.RSEED)
                ada.fit(train_x, train_y)
                pickle.dump(ada, open(output_path, "wb"))
                self.model = ada

            elif model_name == ModelNames.NAIVE_BAYES:
                nb = naive_bayes.BernoulliNB(**properties)
                nb.fit(train_x, train_y)
                pickle.dump(nb, open(output_path, "wb"))
                self.model = nb

            elif model_name == ModelNames.SVM:
                clf = svm.SVC(random_state=self.RSEED, **properties)
                clf.fit(train_x, train_y)
                pickle.dump(clf, open(output_path, "wb"))
                self.model = clf

    #        elif model_name == ModelNames.SVM_RBF_KERNEL:
    #            clf = svm.SVC(random_state=self.RSEED, **properties)
    #            clf.fit(train_x, train_y)
    #            pickle.dump(clf, open(output_path, "wb"))
    #            self.model = clf

            elif model_name == ModelNames.AUTOENCODED_DEEP_LEARNING:

                input_dimension = train_x.shape[1]
                learning_rate = properties.get('learning_rate')
                encoding_dimension = properties.get('encoding_dimension')
                if learning_rate is None:
                    learning_rate = 1e-7
                else:
                    del properties['learning_rate']

                if encoding_dimension is None:
                    encoding_dimension = 32
                else:
                    del properties['encoding_dimension']            

                input_layer = Input(shape=(input_dimension, ))
                    
                Encoder1 = Dense(encoding_dimension, activation="tanh", activity_regularizer=regularizers.l1(learning_rate))(input_layer)
                Encoder2 = Dense(int(encoding_dimension/2), activation="relu")(Encoder1)
                Encoder3 = Dense(int(encoding_dimension/4), activation="tanh")(Encoder2)
                Decoder1 = Dense(int(encoding_dimension/4), activation="relu")(Encoder3)
                Decoder2 = Dense(int(encoding_dimension/2), activation="tanh")(Decoder1)
                Decoder3 = Dense(input_dimension, activation="relu")(Decoder2)

                AutoEncoderModel = Model(inputs=input_layer, outputs=Decoder3)
                AutoEncoderModel.compile(metrics=['accuracy'], loss='mean_squared_error', optimizer='adam')
                # AutoEncoderModel.compile(metrics=['accuracy'], loss=properties.get('loss'), optimizer=properties.get('optimizer'))

                cp = ModelCheckpoint(filepath=output_path, save_best_only=True)
                shuffle = True
                if self.RSEED is None:
                    shuffle = False
                history = AutoEncoderModel.fit(train_x, train_x,
                                            epochs=properties.get('epochs'),
                                            batch_size=properties.get('batch_size'),
                                            shuffle=shuffle,
                                            verbose=1,
                                            callbacks=[cp], 
                                            validation_data=(test_x, test_x)).history
                
                self.model = AutoEncoderModel

    def predict_current_model(self, scaler_path):
        with self.graph.as_default():
            if self.model is None:
                print('Selected model not available')
            
            LABELS = ["Normal", "Fraud"]
            
            scaler = pickle.load(open(scaler_path, 'rb'))

            df = pd.read_csv(self.fname)
            df = df.sample(frac=1)
            normal_df = df[df['Class'] == 0]
            fraud_df = df[df['Class'] == 1]

            df_norm = df

            test_y = df_norm['Class']
            test_x = df_norm.drop(['Class'], axis=1)
            test_x = scaler.transform(test_x)
            predicted = []
            if self.model_name == ModelNames.RANDOM_FOREST:
                predicted = self.model.predict(test_x)


            elif self.model_name == ModelNames.AUTOENCODED_DEEP_LEARNING:
                threshold_fixed = 9

                test_x_predictions = self.model.predict(test_x)
                mse = np.mean(np.power(test_x - test_x_predictions, 2), axis=1)
                error_df = pd.DataFrame({'Reconstruction_error': mse, 'True_class': test_y})
                error_df['idx'] = range(1, len(error_df)+1)

                predicted = [1 if e > threshold_fixed else 0 for e in error_df.Reconstruction_error.values]


            conf_matrix = confusion_matrix(test_y, predicted)
            fig = plt.figure(figsize=(12, 12))
            '''
            sns.scatterplot(x='idx', y='Reconstruction_error', hue='True_class', data=error_df)
            plt.title('scatter plot')
            plt.ylabel('error')
            plt.xlabel('instance number')
            plt.show()
            '''
            sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d")
            plt.title("Confusion matrix")
            plt.ylabel('True class')
            plt.xlabel('Predicted class')
            plt.show()

"""
if __name__ == '__main__':
    FD = Trainer('./CCFD/creditcard.csv')
#    FD.training(train_pct=0.2, output_path="./model.sav",
#                model_name=ModelNames.RANDOM_FOREST, properties={'n_estimators':100})
    FD.training(train_pct=0.2, output_path="./model_dl.sav", output_scaler_path="./scaler_dl.sav",
                model_name=ModelNames.AUTOENCODED_DEEP_LEARNING,
                properties={'epochs': 100, 'loss': keras.losses.mean_squared_error, 'optimizer': keras.optimizers.Adam()})
    FD.predict_current_model()
"""
