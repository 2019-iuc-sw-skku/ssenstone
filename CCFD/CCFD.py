import pickle
import keras
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split

class CCFDT:
    def __init__(self, filepath, random_state=None):
        '''
        parameters:
            filepath(str): path to csv dataset file
            random_state: random seed
        '''
        self.RSEED = random_state
        self.fname = filepath
        self.model_set = 0

    def training(self, output_path, model_name, properties):
        '''
        
        '''
        df = pd.read_csv(self.fname)
        df = df.sample(frac=1)
        normal_df = df[df['Class'] == 0]
        fraud_df = df[df['Class'] == 1]

        df_norm = pd.concat([fraud_df, normal_df])

        new_df = df_norm.sample(frac=1, random_state=self.RSEED)

        x = new_df.drop('Class', axis=1)
        y = new_df['Class']

        train_x = x.values
        train_y = y.values
        print("Train start...")
        rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=self.RSEED)
        rf.fit(train_x, train_y)
        training_score = cross_val_score(rf, train_x, train_y, cv=5)

        print("Training score", training_score)

        pickle.dump(rf, open("./CCFD/models/model" + str(self.model_set) + ".sav", "wb"))

        predicted = rf.predict(test_x)
        accuracy = accuracy_score(test_y, predicted)

        print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
        print(f'Mean accuracy score: {accuracy:.3}')
   
    def show(self):
        plt.show()
     
    def set_modelnum(self,num):
        self.model_set = num

    def show_pickle(self):
        data_list = []
        with open("./CCFD/models/model" + str(self.model_set) + ".sav",'rb') as FL:
            data=[]
            while(True):
                try: 
                    data=pickle.load(FL)
                except EOFError:
                    break
                data_list.append(data)
        print(data_list)

if __name__ == '__main__':
    FD = CCFDT('creditcard.csv')
    FD.set_modelnum(1)
    FD.training()
    FD.show()
    FD.show_pickle()
