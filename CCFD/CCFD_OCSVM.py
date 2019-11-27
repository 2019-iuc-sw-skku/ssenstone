import pickle
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.svm import OneClassSVM
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

class CCFD_OCSVM:
    def __init__(self, RSEED, TESTP, fname):
        self.RSEED = RSEED
        self.TESTP = TESTP
        self.fname = fname

    def training(self, df=None):
        if df is None:
            df = pd.read_csv(self.fname)
        normal_df = df[df['Class'] == 0]
        fraud_df = df[df['Class'] == 1]

        sc = StandardScaler()
        df_norm = df
        df_norm['Time'] = sc.fit_transform(df_norm['Time'].values.reshape(-1, 1))
        df_norm['Amount'] = sc.fit_transform(df_norm['Amount'].values.reshape(-1, 1))

        train_x, test_x = train_test_split(df_norm, test_size=self.TESTP, random_state=self.RSEED)
        test_x = df_norm
        train_x = train_x[train_x.Class == 0]
        train_x = train_x.drop(['Class'], axis=1)
        
        test_y = test_x['Class']
        test_x = test_x.drop(['Class'], axis=1)

        train_x = train_x.values
        test_x = test_x.values

        print("Train start...")
        ocsvm = OneClassSVM(degree=4, gamma='scale', nu=0.01).fit(train_x)
        print("Train end...\ndump start...")
        pickle.dump(ocsvm, open("./models/model_OCSVM.sav", "wb"))
        pickle.dump(sc, open("./scalers/scaler_OCSVM.sav", "wb"))
        print("dump end...\npredict start...")
        
        predicted = ocsvm.predict(test_x)
        print("predict end...")
        for i in range(0, len(predicted)):
            if (predicted[i] == -1):
                predicted[i] = 1
            elif (predicted[i] == 1):
                predicted[i] = 0
        accuracy = accuracy_score(test_y, predicted)
        report=classification_report(test_y, predicted)

        print(f'Mean accuracy score: {accuracy:.3}')
        print(report)
        
        cm = pd.DataFrame(confusion_matrix(test_y, predicted))
        sns.heatmap(cm, annot=True, fmt='d')
        plt.title("Confusion matrix")
        plt.ylabel('True class')
        plt.xlabel('Predicted class')
        plt.show()

    def show_pickle(self):
        data_list = []
        with open("./models/model_OCSVM.sav",'rb') as FL:
            data=[]
            while(True):
                try:
                    data=pickle.load(FL)
                except EOFError:
                    break
                data_list.append(data)
        print(data_list)

if __name__ == '__main__':
    OCSVM = CCFD_OCSVM(312, 0.9, 'creditcard.csv')
    OCSVM.training()
    OCSVM.show_pickle()
