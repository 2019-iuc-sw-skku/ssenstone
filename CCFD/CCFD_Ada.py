import pickle
from sklearn import metrics, model_selection, preprocessing, ensemble
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

class CCFDT:
    def __init__(self, RSEED, TESTP, fname ):
        self.RSEED = RSEED
        self.TESTP = TESTP
        self.fname = fname
        self.model_set = 0

    def training(self):
        df = pd.read_csv(self.fname)
        df = df.sample(frac=1)
        normal_df = df[df['Class'] == 0]
        fraud_df = df[df['Class'] == 1]

        df_norm = pd.concat([fraud_df, normal_df])

        new_df = df.sample(frac=1, random_state=self.RSEED)

        x = new_df.drop('Class', axis=1)
        y = new_df['Class']

        x_t, x_te, y_t, y_te = model_selection.train_test_split(x, y, test_size = self.TESTP, random_state = self.RSEED, stratify=y)
        x_t = x_t.values
        x_te = x_te.values
        train_y = y_t.values
        test_y = y_te.values

        #Scaling
        sc=preprocessing.StandardScaler()
        train_x=sc.fit_transform(x_t)
        test_x=sc.transform(x_te)

        print('Ada Train Start..')

        ada=ensemble.AdaBoostClassifier(n_estimators=200, random_state=0)
        ada.fit(train_x,train_y)

        pickle.dump(ada, open("./CCFD/models/model_ada" + str(self.model_set) + ".sav", "wb"))
        pickle.dump(sc, open("./CCFD/scalers/scaler_ada" + str(self.model_set) + ".sav", "wb"))

        pre=ada.predict(test_x)
        score=metrics.accuracy_score(test_y,pre)
        report=metrics.classification_report(test_y,pre)

        print(f'Mean accuracy score: {score:.3}')
        print(report)
        
        cm = pd.DataFrame(metrics.confusion_matrix(test_y, pre))
        sns.heatmap(cm, annot=True)
   
    def show(self):
        plt.show()
     
    def set_modelnum(self,num):
        self.model_set = num

    def show_pickle(self):
        data_list = []
        with open("./model_ada" + str(self.model_set) + ".sav",'rb') as FL:
            data=[]
            while(True):
                try: 
                    data=pickle.load(FL)
                except EOFError:
                    break
                data_list.append(data)
        print(data_list)

if __name__ == '__main__':
    FD = CCFDT(312,0.9,'creditcard.csv')
    FD.set_modelnum(1)
    FD.training()
    FD.show()