#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 12:17:05 2020
Creating files of materials struct 
@author: hardproxy
"""


import os
import csv
from pymatgen.ext.matproj import MPRester
from pymatgen.io.vasp import Poscar


with open(os.getcwd()+'/Data/ids/data.csv') as csv_file:
    '''
        Abertura de arquivo para a obtenção dos IDENTIFICADORES e FORMULAS dos
        materiais que vão ser utilizados na identificação da Figura de Mérito 
        pela técnica de Machine Learinig.
    '''
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    list_id = []
    list_formula = []
    print("Getting Formula from Data.CSV :\n")
    for row in csv_reader:
        print(row['formula'] + "\n")
        list_formula.append(row['formula'])
        
os.chdir(os.getcwd()+'/Data/structures')


with MPRester("AzDkMZ4uNfGQbovDDB79") as m:
    '''
        #Busca de dados estruturais por meio do Pymatgen         
    '''
    print("Getting Estructure from Pymatgen : \n")
    for i in list_formula :
        print(i + "\n")
        #structure = m.get_data(i,data_type = 'vasp', prop = 'structure')
        # Saving materials structure in a file in POSCAR format
   

    data = m.get_data(1234,data_type='vasp',prop='energy')
        #ids = structure[0]["material_id"]
        #g = Poscar(structure[0]['structure'])
        #g.write_file('struct_' + ids + '.dat')
