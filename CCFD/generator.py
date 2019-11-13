import pandas as pd
import random


class Generator:
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

        return prod