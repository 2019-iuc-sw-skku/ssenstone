import pandas as pd
import random


class Generator:
<<<<<<< HEAD
    df = pd.DataFrame()
    usecon = None
    uselin = None

    def __init__(self, dataframe):
        self.df = dataframe

    def update(self, dataframe):
        self.df = dataframe

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
        
        '''
=======
    data = 0
    usecon = None
    uselin = None

    def __init__(self, datapath, use_constant=True, use_linconv=True):
        self.data = datapath
        self.usecon = use_constant
        self.uselin = use_linconv

    #Not tested yet
    def generate_columns(self, col_num):
        df = pd.read_csv(self.data)
        df = df.sample(frac=1)
        df = df.drop('Class', axis=1)
        rows = df.shape()[0]
        cols = df.shape()[1]
        prod = pd.DataFrame()
        if self.usecon and self.uselin:
            for i in range(col_num/2):
                arr = [random.randrange(1, 100)]*rows
                const_col = pd.DataFrame({('c'+i): arr})
                prod.join(const_col)
            for i in range(col_num - (col_num/2)):
                linnum = random.randrange(2, 11)
                res = pd.DataFrame()
                for j in range(linnum):
                    target_col = random.randrange(0, cols)
                    tmp = df.iloc[:, target_col].copy()
                    tmp = tmp.apply(lambda x: x*random.random())
                    if j == 0:
                        res = tmp
                    else:
                        res.add(tmp)
                prod.join(res)

>>>>>>> 0132bfb6fec00f9cd6d9051c336d825e43ec5f15
        elif self.usecon:
            for i in range(col_num):
                arr = [random.randrange(1, 100)]*rows
                const_col = pd.DataFrame({('c'+i): arr})
                prod.join(const_col)

        elif self.uselin:
            for i in range(col_num):
                linnum = random.randrange(2, 11)
                res = pd.DataFrame()
                for j in range(linnum):
                    target_col = random.randrange(0, cols)
                    tmp = df.iloc[:, target_col].copy()
                    tmp = tmp.apply(lambda x: x*random.random())
                    if j == 0:
                        res = tmp
                    else:
                        res.add(tmp)
                prod.join(res)
<<<<<<< HEAD
        '''

        return prod

if __name__ == '__main__':
    df = pd.read_csv('creditcard.csv')
    gnt = Generator(df)
    prod = gnt.generate_columns(5, 5)
    print(prod.head())
    gnt.update(df.join(prod))
    prod = gnt.generate_columns(5, 5)
    print(prod.head())
=======

        return prod
>>>>>>> 0132bfb6fec00f9cd6d9051c336d825e43ec5f15
