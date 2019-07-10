import pickle

import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from keras import regularizers
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import Dense, Input
from keras.models import Model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

from model_names import ModelNames


class Trainer:
    def __init__(self, filepath, random_state=None):
        '''
        parameters:
            filepath(str): path to csv dataset file
            random_state: random seed
        '''
        self.RSEED = random_state
        self.fname = filepath
        self.model = None

    def training(self, train_pct, output_path, model_name, properties):
        '''
        parameters:
            train_pct(float) : fraction of train data per overall data.
            output_path(str) : path to output model file.
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

        '''
        self.model_name = model_name
        df = pd.read_csv(self.fname)
        df = df.sample(frac=1)
        normal_df = df[df['Class'] == 0]
        fraud_df = df[df['Class'] == 1]

        df_norm = df
        df_norm['Time'] = StandardScaler().fit_transform(df_norm['Time'].values.reshape(-1, 1))
        df_norm['Amount'] = StandardScaler().fit_transform(df_norm['Amount'].values.reshape(-1, 1))

        
        print("Train start...")
        if model_name == ModelNames.RANDOM_FOREST:
            
            new_df = df_norm.sample(frac=1, random_state=self.RSEED)
            
            x = new_df.drop('Class', axis=1)
            y = new_df['Class']
            x, _, y, _ = train_test_split(x, y, train_size=train_pct)
            train_x = x.values
            train_y = y.values
            rf = RandomForestClassifier(**properties, random_state=self.RSEED)
            rf.fit(train_x, train_y)

            pickle.dump(rf, open(output_path, "wb"))

            self.model = rf

        elif model_name == ModelNames.AUTOENCODED_DEEP_LEARNING:

            x = df_norm[df_norm.Class == 0]
            x = x.drop(['Class'], axis=1)
            x, _ = train_test_split(x, train_size=train_pct)

            train_x = x.values

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
            AutoEncoderModel.compile(metrics=['accuracy'], loss=properties.get('loss'), optimizer=properties.get('optimizer'))

            cp = ModelCheckpoint(filepath=output_path, save_best_only=True)
            shuffle = True
            if self.RSEED is None:
                shuffle = False
            history = AutoEncoderModel.fit(train_x, train_x,
                                           epochs=properties.get('epochs'),
                                           batch_size=properties.get('batch_size'),
                                           shuffle=shuffle,
                                           verbose=1,
                                           callbacks=[cp]).history
            
            self.model = AutoEncoderModel

    def predict_current_model(self):
        if self.model is None:
            print('Selected model not available')
        
        LABELS = ["Normal","Fraud"]
        
        df = pd.read_csv(self.fname)
        df = df.sample(frac=1)
        normal_df = df[df['Class'] == 0]
        fraud_df = df[df['Class'] == 1]

        df_norm = df
        df_norm['Time'] = StandardScaler().fit_transform(df_norm['Time'].values.reshape(-1, 1))
        df_norm['Amount'] = StandardScaler().fit_transform(df_norm['Amount'].values.reshape(-1, 1))

        test_y = df_norm['Class']
        test_x = df_norm.drop(['Class'], axis=1)
        predicted = []
        if self.model_name == ModelNames.RANDOM_FOREST:
            predicted = self.model.predict(test_x)


        elif self.model_name == ModelNames.AUTOENCODED_DEEP_LEARNING:
            threshold_fixed = 5

            test_x_predictions = self.model.predict(test_x)
            mse = np.mean(np.power(test_x - test_x_predictions, 2), axis=1)
            error_df = pd.DataFrame({'Reconstruction_error': mse, 'True_class': test_y})

            predicted = [1 if e > threshold_fixed else 0 for e in error_df.Reconstruction_error.values]


        conf_matrix = confusion_matrix(test_y, predicted)

        plt.figure(figsize=(12, 12))
        sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d")
        plt.title("Confusion matrix")
        plt.ylabel('True class')
        plt.xlabel('Predicted class')
        plt.show()



if __name__ == '__main__':
    FD = Trainer('./CCFD/creditcard.csv')
#    FD.training(train_pct=0.2, output_path="./model.sav",
#                model_name=ModelNames.RANDOM_FOREST, properties={'n_estimators':100})
    FD.training(train_pct=0.2, output_path="./model_dl.sav",
                model_name=ModelNames.AUTOENCODED_DEEP_LEARNING,
                properties={'epochs': 100, 'loss': keras.losses.mean_squared_error, 'optimizer': keras.optimizers.Adam()})
    FD.predict_current_model()
