import pandas as pd
import random
from sklearn.datasets import make_blobs

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
        while 'l'+str(i) in df.columns:
            i += 1
            linconv_col_num += 1
        for i in range(linconv_col_num):
            linnum = random.randrange(2, 11)
            res = pd.DataFrame()
            for j in range(linnum):
                target_col = random.randrange(0, cols)
                tmp = df.iloc[:, target_col].copy()
                rnd = random.random()
                tmp = tmp.apply(lambda x: x*rnd)
                if j == 0:
                    res = tmp
                else:
                    res.add(tmp)
            res.name = 'l'+str(i)
            if prod.empty:
                prod = res
            else:
                prod = prod.join(res)
        return prod

    '''
    generate row as center as given data and given bounds. follows gaussian.
    output = (class 1's count) * row_num
    '''
    def generate_rows(self, row_num, bounds=0.01):
        df = self.df.loc[self.df['Class'] == 1].copy()
        try:
            df = df.drop('Class', axis=1)
        except:
            ''
        (rows, cols) = df.shape
        acc = pd.DataFrame([], columns=df.columns)
        for i in range(rows):
            print('step ' + str(i+1) + ' of ' + str(rows))
            app = make_blobs(row_num, cols, 1, bounds, (-bounds, bounds))[0]
            #app = pd.DataFrame(data=app, index=range(row_num), columns=df.columns)
            for j in range(row_num):
                acc = acc.append(df.iloc[[i]].copy().add(app[j], axis='columns'), ignore_index=True)

        return acc
       


if __name__ == '__main__':
    df = pd.read_csv('creditcard.csv')
    gnt = Generator(df)
    #prod = gnt.generate_columns(5, 5)
    #print(prod.head())
    #gnt.update(df.join(prod))
    #prod = gnt.generate_columns(5, 5)
    #print(prod.head())
    rprod = gnt.generate_rows(5)
    print(rprod.shape)
    print(rprod.head())
