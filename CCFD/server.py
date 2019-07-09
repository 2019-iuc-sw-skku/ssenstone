import os.path
import pickle
import socketserver
import threading
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

HOST = 'localhost'
PORT = 1234

class MyTcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print('[%s] is connected' %self.client_address[0])
        data = self.request.recv(1024)
        df = pd.read_json(data.decode())
        print(df)

        if 'Class' in df.columns:
            print('labeled data')
            if os.path.isfile("labeleddata.csv"):
                df.to_csv("labeleddata.csv", mode = 'a', header = False, index = False)
            else:
                df.to_csv("labeleddata.csv", mode = 'w', index = False)
        else:
            nparr = df.as_matrix()
            answer = self.server.model.predict(nparr)
            print('answer : ' + str(answer[0]))
            self.request.send(bytes(str(answer[0]), 'utf8'))
            
def runServer(path_model):
    print("------- Server start -------")

    try:
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.model = pickle.load(open(path_model, 'rb'))
        server.serve_forever()
    except KeyboardInterrupt:
        print("------- Server end -------")

if __name__=='__main__':
    runServer('model1.sav')
