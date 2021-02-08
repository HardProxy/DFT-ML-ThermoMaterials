#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esse programa utiliza de pacotes e módulos que facilitam o acesso a informações disponíveis
na Base de Dados do Materials Project e do Materials Project Contribs.

Objetivo geral : Utilizar Rede Neural para aprender como que a figura de mérito, grandeza que
determina o quão bom termoelétrico é um material, a partir de descritores como Temperatura,
Vetores Posição dos Átomos, Parâmetro de Rede.

Objetivos : 
    - Dados Estruturais : Obtenção de Informações Estruturais do VASP dos 
                          dos materiais que tiveram a análise de transporte (OK)
    - Carrier Transport : Obtenção de Informações dos Portadores de Carga
                          dos Materiais que foram análisado pelo Materials 
                          Project (OK)

    - Organização de Input para a Rede Neural (Descritores) (OK)
    - Organização de Ouput para a Rede Neural (S² sigma , Kappa elétrico) (OK)
    - Criando Banco de Dados com as informações de Input e Output (Em progresso ...)
    - Separação de Dataset para Treino e para Validação
    - Treino da Rede
    - Validação dos resultados 
    - Análise de Resultados e contrução de gráficos de eficiência 

@author: hardproxy
"""
# Importação necessário para o uso do Scikit-Learn

# Caso for necessário :  
# from sklearn.pipeline import make_pipeline
# from sklearn.datasets import load_boston - Dados de Teste da Rede Neural 

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor


import csv                                            # Módulo de acesso a arquivos do tipo .csv

#from mpcontribs.client import load_client             # Módulo de acesso a uma seção no MPContribs server
#from pymatgen.ext.matproj import MPRester             # Módulo de acesso ao MP server
#from pymatgen import Structure                        # Acesso á classe do tipo Structure    

print('Acessando Banco de Dados de Materiais ... :) \n')

with open('/home/hardproxy/Documents/TCC-BD_ML/ML-ThermoElec/Data/Materials_Data/Materials_Data.csv') as csv_file:

    csv_reader = csv.DictReader(csv_file)
    list_id = []
    list_ident = []
    list_form = []
    list_temp = []
    list_efermi = []
    list_e_per_atom = []
    list_ele_cell = []
    list_med_mass = []
    list_var_mass = []
    list_med_raio = []
    list_var_raio = []
    list_med_ele = []
    list_var_ele = []
    list_med_val = []
    list_var_val = []
    list_g1 = []
    list_g2 = []
    list_g3 = []
    list_g4 = []
    list_g5 = []
    list_g6 = []
    list_g7 = []
    list_g8 = []
    list_g9 = []
    list_g10 = []
    list_g11 = []
    list_g12 = []
    list_g13 = []
    list_g14 = []
    list_g15 = []
    list_g16 = []
    list_g17 = []
    list_g18 = []
    list_p1 = []
    list_p2 = []
    list_p3 = []
    list_p4 = []
    list_p5 = []
    list_p6 = []
    list_p7 = []
    list_e_l1 = []
    list_e_l2 = []
    list_e_l3 = []
    list_e_l4 = []
    list_e_l5 = []
    list_e_l6 = []
    list_e_l7 = []
    list_tetragonal = []
    list_trigonal = []
    list_orthorhombic = []
    list_cubic = []
    list_monoclinic = []
    list_triclinic = []
    list_hexagonal = []
    list_s = []
    list_kappa = []
    
    num_linhas =  0
    for row in csv_reader:
        if row['κₑᵉ'] == '0.0':
            pass
        else :
            list_id.append(row['id'])
            list_ident.append(row['identifier'])
            list_form.append(row['formula'])
            list_temp.append(row['temperature'])
            list_efermi.append(row['efermi'])
            list_e_per_atom.append(row['e_per_atom'])
            list_ele_cell.append(row['ele_cell'])
            list_med_mass.append(row['med_mass'])
            list_var_mass.append(row['var_mass'])
            list_med_raio.append(row['med_raio'])
            list_var_raio.append(row['var_raio'])
            list_med_ele.append(row['med_ele'])
            list_var_ele.append(row['var_ele'])
            list_med_val.append(row['med_val'])
            list_var_val.append(row['var_val'])
            list_g1.append(row['g1'])
            list_g2.append(row['g2'])
            list_g3.append(row['g3'])
            list_g4.append(row['g4'])
            list_g5.append(row['g5'])
            list_g6.append(row['g6'])
            list_g7.append(row['g7'])
            list_g8.append(row['g8'])
            list_g9.append(row['g9'])
            list_g10.append(row['g10'])
            list_g11.append(row['g11'])
            list_g12.append(row['g12'])
            list_g13.append(row['g13'])
            list_g14.append(row['g14'])
            list_g15.append(row['g15'])
            list_g16.append(row['g16'])
            list_g17.append(row['g17'])
            list_g18.append(row['g18'])
            list_p1.append(row['p1'])
            list_p2.append(row['p2'])
            list_p3.append(row['p3'])
            list_p4.append(row['p4'])
            list_p5.append(row['p5'])
            list_p6.append(row['p6'])
            list_p7.append(row['p7'])
            list_e_l1.append(row['e_l1'])
            list_e_l2.append(row['e_l2'])
            list_e_l3.append(row['e_l3'])
            list_e_l4.append(row['e_l4'])
            list_e_l5.append(row['e_l5'])
            list_e_l6.append(row['e_l6'])
            list_e_l7.append(row['e_l7'])
            list_tetragonal.append(row['tetragonal'])
            list_trigonal.append(row['trigonal'])
            list_orthorhombic.append(row['orthorhombic'])
            list_cubic.append(row['cubic'])
            list_monoclinic.append(row['monoclinic'])
            list_triclinic.append(row['triclinic'])
            list_hexagonal.append(row['hexagonal'])
            list_s.append(row['⟨S²σ⟩'])
            list_kappa.append(row['κₑᵉ'])
            num_linhas+=1
csv_file.close()



# Creating dataset
print('Criando Conjunto de Dados ... :) \n')


temp = []
for i in range(num_linhas):
    j = float(list_temp[i])
    temp.append(j)
    
temp_array = np.array(temp)

efermi = []
for i in range(num_linhas):
    j = float(list_efermi[i])
    efermi.append(j)
    
efermi_array = np.array(efermi)

e_per_atom = []

for i in range(num_linhas):
    j = float(list_e_per_atom[i])
    e_per_atom.append(j)
    
e_per_atom_array = np.array(e_per_atom)


ele_cell = []

for i in range(num_linhas):
    j = float(list_ele_cell[i])
    ele_cell.append(j)
    
ele_cell_array = np.array(ele_cell)


med_mass = []

for i in range(num_linhas):
    j = float(list_med_mass[i])
    med_mass.append(j)
    
med_mass_array = np.array(med_mass)

var_mass = []

for i in range(num_linhas):
    j = float(list_var_mass[i])
    var_mass.append(j)
    
var_mass_array = np.array(var_mass)



med_raio = []

for i in range(num_linhas):
    j = float(list_med_raio[i])
    med_raio.append(j)
    
med_raio_array = np.array(med_raio)

var_raio = []

for i in range(num_linhas):
    j = float(list_var_raio[i])
    var_raio.append(j)
    
var_raio_array = np.array(var_raio)



med_ele = []

for i in range(num_linhas):
    j = float(list_med_ele[i])
    med_ele.append(j)
    
med_ele_array = np.array(med_ele)

var_ele = []

for i in range(num_linhas):
    j = float(list_var_ele[i])
    var_ele.append(j)
    
var_ele_array = np.array(var_ele)



med_val = []

for i in range(num_linhas):
    j = float(list_med_val[i])
    med_val.append(j)
    
med_val_array = np.array(med_val)

var_val = []

for i in range(num_linhas):
    j = float(list_var_val[i])
    var_val.append(j)
    
var_val_array = np.array(var_val)



g1 = []

for i in range(num_linhas):
    j = float(list_g1[i])
    g1.append(j)
    
g1_array = np.array(g1)

g2 = []

for i in range(num_linhas):
    j = float(list_g2[i])
    g2.append(j)
    
g2_array = np.array(g2)

g3 = []

for i in range(num_linhas):
    j = float(list_g3[i])
    g3.append(j)
    
g3_array = np.array(g3)

g4 = []

for i in range(num_linhas):
    j = float(list_g4[i])
    g4.append(j)
    
g4_array = np.array(g4)


g5 = []

for i in range(num_linhas):
    j = float(list_g5[i])
    g5.append(j)
    
g5_array = np.array(g5)

g6 = []

for i in range(num_linhas):
    j = float(list_g6[i])
    g6.append(j)
    
g6_array = np.array(g6)


g7 = []

for i in range(num_linhas):
    j = float(list_g7[i])
    g7.append(j)
    
g7_array = np.array(g7)

g8 = []

for i in range(num_linhas):
    j = float(list_g8[i])
    g8.append(j)
    
g8_array = np.array(g8)

g9 = []

for i in range(len(list_g9)):
    j = float(list_g9[i])
    g9.append(j)
    
g9_array = np.array(g9)

g10 = []

for i in range(num_linhas):
    j = float(list_g10[i])
    g10.append(j)
    
g10_array = np.array(g10)

g11 = []

for i in range(num_linhas):
    j = float(list_g11[i])
    g11.append(j)
    
g11_array = np.array(g11)


g12 = []

for i in range(num_linhas):
    j = float(list_g12[i])
    g12.append(j)
    
g12_array = np.array(g12)

g13 = []

for i in range(num_linhas):
    j = float(list_g13[i])
    g13.append(j)
    
g13_array = np.array(g13)

g14 = []

for i in range(num_linhas):
    j = float(list_g14[i])
    g14.append(j)
    
g14_array = np.array(g14)

g15 = []

for i in range(num_linhas):
    j = float(list_g15[i])
    g15.append(j)
    
g15_array = np.array(g15)

g16 = []

for i in range(num_linhas):
    j = float(list_g16[i])
    g16.append(j)
    
g16_array = np.array(g16)

g17 = []

for i in range(num_linhas):
    j = float(list_g17[i])
    g17.append(j)
    
g17_array = np.array(g17)

g18 = []

for i in range(num_linhas):
    j = float(list_g18[i])
    g18.append(j)
    
g18_array = np.array(g18)


p1 = []

for i in range(num_linhas):
    j = float(list_p1[i])
    p1.append(j)
    
p1_array = np.array(p1)

p2 = []

for i in range(num_linhas):
    j = float(list_p2[i])
    p2.append(j)
    
p2_array = np.array(p2)

p3 = []

for i in range(num_linhas):
    j = float(list_p3[i])
    p3.append(j)
    
p3_array = np.array(p3)

p4 = []

for i in range(num_linhas):
    j = float(list_p4[i])
    p4.append(j)
    
p4_array = np.array(p4)

p5 = []

for i in range(num_linhas):
    j = float(list_p5[i])
    p5.append(j)
    
p5_array = np.array(p5)


p6 = []

for i in range(num_linhas):
    j = float(list_p6[i])
    p6.append(j)
    
p6_array = np.array(p6)


p7 = []

for i in range(num_linhas):
    j = float(list_p7[i])
    p7.append(j)
    
p7_array = np.array(p7)



e_l1 = []

for i in range(num_linhas):
    j = float(list_e_l1[i])
    e_l1.append(j)
    
e_l1_array = np.array(e_l1)


e_l2 = []

for i in range(num_linhas):
    j = float(list_e_l2[i])
    e_l2.append(j)
    
e_l2_array = np.array(e_l2)


e_l3 = []

for i in range(num_linhas):
    j = float(list_e_l3[i])
    e_l3.append(j)
    
e_l3_array = np.array(e_l3)


e_l4 = []

for i in range(num_linhas):
    j = float(list_e_l4[i])
    e_l4.append(j)
    
e_l4_array = np.array(e_l4)


e_l5 = []

for i in range(num_linhas):
    j = float(list_e_l5[i])
    e_l5.append(j)
    
e_l5_array = np.array(e_l5)


e_l6 = []

for i in range(num_linhas):
    j = float(list_e_l6[i])
    e_l6.append(j)
    
e_l6_array = np.array(e_l6)



e_l7 = []

for i in range(num_linhas):
    j = float(list_e_l7[i])
    e_l7.append(j)
    
e_l7_array = np.array(e_l7)


tetragonal = []

for i in range(num_linhas):
    j = float(list_tetragonal[i])
    tetragonal.append(j)
    
tetragonal_array = np.array(tetragonal)


trigonal = []

for i in range(num_linhas):
    j = float(list_trigonal[i])
    trigonal.append(j)
    
trigonal_array = np.array(trigonal)


orthorhombic = []

for i in range(num_linhas):
    j = float(list_orthorhombic[i])
    orthorhombic.append(j)
    
orthorhombic_array = np.array(orthorhombic)


cubic = []

for i in range(num_linhas):
    j = float(list_cubic[i])
    cubic.append(j)
    
cubic_array = np.array(cubic)


monoclinic = []

for i in range(num_linhas):
    j = float(list_monoclinic[i])
    monoclinic.append(j)
    
monoclinic_array = np.array(monoclinic)

triclinic = []

for i in range(num_linhas):
    j = float(list_triclinic[i])
    triclinic.append(j)
    
triclinic_array = np.array(triclinic)

hexagonal = []

for i in range(num_linhas):
    j = float(list_hexagonal[i])
    hexagonal.append(j)
    
hexagonal_array = np.array(hexagonal)



s = []

for i in range(num_linhas):
    j = float(list_s[i])
    s.append(j)
    
s_array = np.array(s)


kappa = []

for i in range(num_linhas):
    j = float(list_kappa[i])
    kappa.append(j)
    
kappa_array = np.array(kappa)

'''

    fieldnames = ['','id','identifier',
                  'formula','temperature',
                  'efermi','e_per_atom',
                  'ele_cell','med_mass',
                  'var_mass','med_raio',
                  'var_raio','med_ele',
                  'var_ele','med_val',
                  'var_val',
                  'g1','g2','g3','g4','g5','g6','g7','g8','g9','g10','g11',
                  'g12','g13','g14','g15','g16','g17','g18',
                  'p1','p2','p3','p4','p5','p6','p7',
                  'e_l1','e_l2','e_l3','e_l4','e_l5','e_l6','e_l7',
                  'tetragonal','trigonal','orthorhombic','cubic','monoclinic'
                  ,'triclinic','hexagonal',
                  '⟨S²σ⟩','κₑᵉ']

'''
#pot_quim = int(input("Escolha como maneira de caracterização de Potencial Químico \n1) Energia de Fermi \n2) Energia por Átomo \n "))
pot_quim = 1
if pot_quim == 1 :
    # Junção de Parâmetros com potencial quimico igual à energia de fermi
    X = np.c_[temp_array,efermi_array,ele_cell_array,med_mass_array,var_mass_array,med_raio_array,var_raio_array,
              med_ele_array,var_ele_array,med_val_array,var_val_array,g1_array,g2_array,g3_array,g4_array,g5_array,
              g6_array,g7_array,g8_array,g9_array,g10_array,g11_array,g12_array,g13_array,g14_array,g15_array,
              g16_array,g17_array,g18_array,p1_array,p2_array,p3_array,p4_array,p5_array,p6_array,p7_array,
              e_l1_array,e_l2_array,e_l3_array,e_l4_array,e_l5_array,e_l6_array,e_l7_array,tetragonal_array,
              trigonal_array,orthorhombic_array,cubic_array,monoclinic_array,triclinic_array,hexagonal_array]
else :
    # Junção de Parâmetros com potencial quimico igual à energia por átomo
    
    X = np.c_[temp_array,e_per_atom_array,ele_cell_array,med_mass_array,var_mass_array,med_raio_array,var_raio_array,
              med_ele_array,var_ele_array,med_val_array,var_val_array,g1_array,g2_array,g3_array,g4_array,g5_array,
              g6_array,g7_array,g8_array,g9_array,g10_array,g11_array,g12_array,g13_array,g14_array,g15_array,
              g16_array,g17_array,g18_array,p1_array,p2_array,p3_array,p4_array,p5_array,p6_array,p7_array,
              e_l1_array,e_l2_array,e_l3_array,e_l4_array,e_l5_array,e_l6_array,e_l7_array,tetragonal_array,
              trigonal_array,orthorhombic_array,cubic_array,monoclinic_array,triclinic_array,hexagonal_array]

# Otimização dos dois Parametros
#y = np.c_[s_array,kappa_array]

# Calculo da Figura de Mérito
y = s_array/kappa_array

# Splitting data ( Train vs Test )
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Starndat Rescaling data 
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train) 
X_test =  scaler.transform(X_test)

# Creating object of Neural Network
ANN  = MLPRegressor(hidden_layer_sizes=(43,20,20,15,10,5),learning_rate='adaptive',tol=1e-6, max_iter=10000,random_state=0,verbose=True)

# Training data
ANN.fit(X_train,y_train)

# Testing fase
predictions = ANN.predict(X_test)

score = ANN.score(X_test,y_test)
print("O Score obtido pelo Rede Neural é de : " + str(score) + "\n")
