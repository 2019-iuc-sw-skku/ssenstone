import warnings
import socket
import random
import pandas as pd
import fraud_index

warnings.filterwarnings("ignore")

HOST = 'localhost'
PORT = 1234
DATA_AMOUNT = 100

data = pd.read_csv("./creditcard.csv")
data_nolabel = data
data_nolabel = data_nolabel.drop(columns='Class')

fraud = fraud_index.fraud
random.shuffle(fraud)

def get_index(num):
    if num % 2 == 0 and num < 984:
        return fraud.pop()
    else:
        return random.randrange(0, 284807)

def throwdata(datatype, random_index):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        if datatype == 'labeled':
            data_string = data[random_index : random_index + 1].to_json()
        else:
            data_string = data_nolabel[random_index : random_index + 1].to_json()
        sock.sendall(data_string.encode())

        return sock.recv(1024)


for i in range(0, DATA_AMOUNT):
    random_index = get_index(i)
#    data_type = random.choice(['labeled','unlabeled'])
    data_type = 'unlabeled'
    
    print('transmission ' + str(i) + ' : Data no.' + str(random_index) + ', Data type : ' + data_type)
    
    ans = throwdata(data_type, random_index)
    ans = int(str(ans, 'utf8'))
    if data.iloc[random_index][30] != ans:
        print(f"Wrong answer! True = {data.iloc[random_index]['Class']}, Predicted = {ans}")
    else:
        print("Correct answer")