'''
Client program

send random rows in creditcard.csv file to server
recieve and compare answer to true value
'''
import random
import socket
import warnings

import pandas as pd

import fraud_index

warnings.filterwarnings("ignore")

HOST = 'localhost'
PORT = 1234
DATA_AMOUNT = 20

DATA = pd.read_csv("./creditcard.csv")
DATA_NOLABEL = DATA
DATA_NOLABEL = DATA_NOLABEL.drop(columns='Class')

FRAUD = fraud_index.fraud
random.shuffle(FRAUD)


def get_index(num):
    '''
    Get random index
    '''
    if num % 2 == 0 and num < 984:
        return FRAUD.pop()
    else:
        return random.randrange(0, 284807)

def throwdata(index):
    '''
    Send data to server
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        data_string = DATA_NOLABEL[index : index + 1].to_json()
        sock.sendall(data_string.encode())
        return sock.recv(1024)


for i in range(0, DATA_AMOUNT):
    random_index = get_index(i)
    print('transmission ' + str(i) +
          ' : Data no.' + str(random_index))
    ans = throwdata(random_index)

    ans = str(ans, 'utf8')
    print('recieved: %s' %ans)
    if DATA.iloc[random_index][30] != int(ans[0]):
        print(f"Wrong answer! True = {DATA.iloc[random_index]['Class']}, Predicted = {ans[0]}")
    else:
        print("Correct answer")
