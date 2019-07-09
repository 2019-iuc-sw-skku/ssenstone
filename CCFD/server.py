import os.path
import pickle
import socketserver
import threading
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from keras.models import Model, load_model

warnings.filterwarnings("ignore")

HOST = 'localhost'
PORT = 1234

graph = tf.get_default_graph()

class MyTcpHandler(socketserver.StreamRequestHandler):

    def handle(self):
        global graph
        print('[%s] is connected' %self.client_address[0])
        data = self.request.recv(1024)
        nparr = pd.read_json(data.decode()).as_matrix()
        score = 0
        with graph.as_default():
            for model, name in zip(self.server.model, self.server.model_names):
                answer = model.predict(nparr)
                if name == 'Autoencoded Deep Learning':                        #keras deep learning
                    mse = np.mean(np.power(nparr - answer, 2))
                    if mse > 5:
                        score = score + 1
                    
                elif name == 'Random forest':
                    if answer[0] == 0:
                        score = score + 1
                
                if score >= self.server.pass_score:
                    break
            if score >= self.server.pass_score:
                self.request.send(bytes(str('0,%d' % score), 'utf8'))
            else:
                self.request.send(bytes(str('1,%d' % score), 'utf8'))
        
            
class ThreadedServer(socketserver.ThreadingTCPServer):
    
    def __init__(self, listen_addr):
        socketserver.ThreadingTCPServer.__init__(self, listen_addr, MyTcpHandler)
        self.model = []
        self.pass_score = 0

    def start(self):
        print("------- Server start -------")
        try:
            self.serve_forever()
        except:
            print("-------- Server end ---------")


'''
Run server using path to model(s)
model_paths: array of path to model(s)
'''
def runServer(model_paths, model_names, pass_score):
    server = ThreadedServer((HOST, PORT))
    for path in model_paths:
        if path[-3:] == '.h5':
            server.model.append(load_model(path))             # if it's keras model, use keras-load_model
        else:
            server.model.append(pickle.load(open(path, 'rb'))) # else it's pickle dumped model.

    server.pass_score = pass_score
    server.model_names = model_names
    server.start()

if __name__=='__main__':
    runServer(['./CCFD/models/model1.sav', './CCFD/models/fraud_dl.h5'], ['Random forest', 'Autoencoded Deep Learning'], 2)
