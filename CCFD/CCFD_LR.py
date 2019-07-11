import pickle
import matplotlib.pyplot as plt
import mglearn
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score, train_test_split

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

        new_df = df_norm.sample(frac=1, random_state=self.RSEED)

        x = new_df.drop('Class', axis=1)
        y = new_df['Class']

        train_x, test_x, train_y, test_y = train_test_split(x, y, test_size = self.TESTP, random_state = self.RSEED, stratify=y)
        train_x = train_x.values
        test_x = test_x.values
        train_y = train_y.values
        test_y = test_y.values
        
        #Scaling
        sc=StandardScaler()
        train_x=sc.fit_transform(train_x)
        test_x=sc.transform(test_x)
        
        print("LR Train start...")
        lr=LogisticRegression(solver='newton-cg', C=0.1, max_iter=300, multi_class='multinomial')
        lr.fit(train_x, train_y)
        
        pre=lr.predict(test_x)

        pickle.dump(lr, open("./CCFD/model_Lr" + str(self.model_set) + ".sav", "wb"))

        accuracy = accuracy_score(test_y, pre)
        report=classification_report(test_y, pre)

        print(f'Mean accuracy score: {accuracy:.3}')
        print(report)

        cm = pd.DataFrame(confusion_matrix(test_y, pre))
        sns.heatmap(cm, annot=True)
   
    def show(self):
        plt.show()
     
    def set_modelnum(self,num):
        self.model_set = num

    def show_pickle(self):
        data_list = []
        with open("./CCFD/model_Lr" + str(self.model_set) + ".sav",'rb') as FL:
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
    FD.show_pickle()
