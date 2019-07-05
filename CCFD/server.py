import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import socketserver
import os

import threading

HOST = 'localhost'
PORT = 1234

class MyTcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data_transferred = 0
        print('[%s] is connected' %self.client_address[0])
        data = self.request.recv(1024)
        df = pd.read_json(data.decode())
        print(df)
        nparr = df.as_matrix()
        answer = self.server.model.predict(nparr)
        print(answer)
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