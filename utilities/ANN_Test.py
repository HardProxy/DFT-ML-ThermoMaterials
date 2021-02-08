#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Código de Teste de Implementação de Rede Neural simples a partir de um banco de dados de verificação
utlizando o Standart Rescaling.
( Reescala dos valores de input para que eles fiquem entre interalos reduzidos como, por exemplo,
 -1 < input < 1 )


@author: hardproxy
'''
#import numpy as np
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import load_boston

# Loading data
X,y = load_boston(return_X_y=True)

# Splitting data ( Train vs Test )
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Starndat Rescaling data 
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train) 
X_test =  scaler.transform(X_test)

# Creating object of Neural Network
ANN  = MLPRegressor(hidden_layer_sizes=(100,100),tol=1e-3, max_iter=3000, random_state=0,verbose=True)

# Training data
ANN.fit(X_train,y_train)

# Testing fase
predictions = ANN.predict(X_test)

score = ANN.score(X_test,y_test)
print("O Score obtido pelo Rede Neural é de : " + str(score) + "\n")

