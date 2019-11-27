import pandas as pd
import random
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix
from CCFD import CCFDT
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras import regularizers
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import Dense, Input

class Generator:
    df = pd.DataFrame()
    usecon = None
    uselin = None

    def __init__(self, dataframe):
        self.df = dataframe

    def update(self, dataframe):
        self.df = dataframe

    '''
    generate features from linear combination of given data or just an constant variable.
    just a random
    '''
    def generate_columns(self, const_col_num, linconv_col_num):
        try:
            df = self.df.drop('Class', axis=1)
        except:
            ''
        (rows, cols) = df.shape
        prod = pd.DataFrame()
        i = 0
        if const_col_num > 0:
            while 'c'+str(i) in df.columns:
                i += 1
                const_col_num += 1
            for i in range(const_col_num):
                arr = [random.randrange(1, 100)]*rows
                const_col = pd.DataFrame({('c'+str(i)): arr})
                if prod.empty:
                    prod = const_col
                else:
                    prod = prod.join(const_col)
            i = 0
        if linconv_col_num > 0:
            while 'l'+str(i) in df.columns:
                i += 1
                linconv_col_num += 1
            for i in range(linconv_col_num):
                linnum = random.randrange(2, 11)
                res = pd.DataFrame({('l'+str(i)): [0]*rows})
                for j in range(linnum):
                    target_col = random.randrange(0, cols)
                    tmp = df.iloc[:, target_col].copy()
                    rnd = random.random()
                    tmp = tmp.apply(lambda x: x*rnd)
                    res = res.add(pd.DataFrame({('l'+str(i)): tmp}))
                if prod.empty:
                    prod = res
                else:
                    prod = prod.join(res)
        print(prod.head())
        return prod

    '''
    generate row as center as given data and given bounds. follows gaussian.
    output = (class 1's count) * row_multiplier
    '''
    def generate_rows(self, row_multiplier, bounds=0.001):
        df = self.df.loc[self.df['Class'] == 1].copy()
        try:
            df = df.drop('Class', axis=1)
        except:
            ''
        (rows, cols) = df.shape
        acc = pd.DataFrame([], columns=df.columns)
        for i in range(rows):
            print('step ' + str(i+1) + ' of ' + str(rows))
            app = make_blobs(row_multiplier, cols, 1, bounds, (-bounds, bounds))[0]
            #app = pd.DataFrame(data=app, index=range(row_num), columns=df.columns)
            for j in range(row_multiplier):
                acc = acc.append(df.iloc[[i]].copy().add(app[j], axis='columns'), ignore_index=True)

        acc['Class'] = 1
        return acc
       


if __name__ == '__main__':
    df = pd.read_csv('./creditcard.csv')
    #gnt = Generator(df)
    #prod = gnt.generate_columns(0, 200)
    #df = df.join(prod)
    #df.to_csv('creditcard_append.csv', mode='w', index_col=False)
    #print(prod.head())
    #gnt.update(df.join(prod))
    #prod = gnt.generate_columns(5, 5)
    #print(prod.head())
    #rprod = gnt.generate_rows(100)
    #df = df.append(rprod, ignore_index=True)
    #df.to_csv('creditcard_plusfraud.csv', mode='w', index=False)
    #print(rprod.shape)
    #print(rprod.head())
    
    rf = pickle.load(open('CCFD/models/model_rf0.sav', 'rb'))
    sc = pickle.load(open('CCFD/scalers/scaler_rf0.sav', 'rb'))
    df = df.sample(frac=0.9)
    normal_df = df[df['Class'] == 0]
    fraud_df = df[df['Class'] == 1]

    df_norm = pd.concat([fraud_df, normal_df])
    #df_norm['Amount'] = sc.transform(df_norm['Amount'].values.reshape(-1, 1))
    test_x = df_norm
    test_y = test_x['Class']
    test_x = test_x.drop('Class', axis=1)
    test_x = test_x.values
    test_y = test_y.values
    test_x = sc.transform(test_x)
    predicted = rf.predict(test_x)
    print("predict end...")
    #for i in range(0, len(predicted)):
    #    if (predicted[i] == -1):
    #        predicted[i] = 1
    #    elif (predicted[i] == 1):
    #        predicted[i] = 0
    
    cm = pd.DataFrame(confusion_matrix(test_y, predicted))
    print(predicted)
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title("Confusion matrix")
    plt.ylabel('True class')
    plt.xlabel('Predicted class')
    plt.show()
    
    
    #RF = CCFDT(312, 0.9, 'creditcard.csv')
    #RF.training(df)
    #RF.show_pickle()
    