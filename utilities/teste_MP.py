#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 18:00:57 2020

@author: hardproxy
"""

from pymatgen.ext.matproj import MPRester 
from mpcontribs.client import load_client
import numpy as np 
client = load_client('nmExh2lluuzGHuQKbOG8Si7kCJRY6q8V')   
contrib = client.contributions.get_entry(pk='5e5efaf25a4b4bd4eb1f1b0c', _fields=['_all']).result()

# Valores de Output
k_e = contrib['data']['κₑᵉ']['n']['value']
s_medio = contrib['data']['⟨S²σ⟩']['n']['value']


#Valores de input
temp = contrib['data']['T']['value']    
class_crystal={'tetragonal':0,'trigonal':1,'orthorhombic':2,'cubic':3,'monoclinic':4
                  ,'triclinic':5,'hexagonal': 6}
with MPRester("AzDkMZ4uNfGQbovDDB79") as m:

    structure = m.get_data('Bi3Rh',data_type = 'vasp', prop = 'structure')
    spacegroup= m.get_data('Bi3Rh',data_type='vasp',prop='spacegroup')
    
    crystal_system=[0,0,0,0,0,0,0,0]
    crystal_system[class_crystal[spacegroup[0]['spacegroup']['crystal_system']]] = 1
                    
    
    # Valores para serem testados como potencial quimico
    e_form_per_atom = m.get_data('Bi3Rh',data_type='vasp',prop='formation_energy_per_atom')[0]['formation_energy_per_atom']
    band = m.get_bandstructure_by_material_id('mp-581990')
    efermi = band.efermi
    
    species=structure[0]['structure'].types_of_specie
    ntypes=structure[0]['structure'].ntypesp
    n_sites = structure[0]['structure'].num_sites
    
    #Criação de Listas 
    period=[]
    group=[]
    atomic_mass=[]
    atomic_radius=[]
    eletronegativity=[]
    e_val=[]
    energy_level = [0,0,0,0,0,0,0]
    
    for j in range(ntypes):
        data=species[j].data
        
        # Salvando Inputs - Localização na Tabela Periodica
        period.append(species[j].row)
        group.append(species[j].group)
        
        # Calculo do numero de eletrons de valencia 
        str_ele =species[j].full_electronic_structure
        soma = 0
        for k in str_ele:
            if k[0] == 1:
                energy_level[0] += k[2]
            elif k[0] == 2:
                energy_level[1] += k[2]
            elif k[0] == 3:
                energy_level[2] += k[2]
            elif k[0] == 4:
                energy_level[3] += k[2]
            elif k[0] == 5:
                energy_level[4] += k[2]
            elif k[0] == 6:
                energy_level[5] += k[2]
            elif k[0] == 7:
                energy_level[6] += k[2]
                
            if k[0] == period[j]:
                soma += k[2]
            
        e_val.append(soma)
        # Salvando Inputs - Propriedades Fundamentais
        atomic_mass.append(data['Atomic mass'])
        atomic_radius.append(data['Atomic radius'])
        eletronegativity.append(data['X'])
                
  
# Calculo da Média e variancia da Massa, raio, eletronegatividade e eletrons de valencia
mass_mean = np.mean(atomic_mass)
mass_var = np.var(atomic_mass)

raio_mean = np.mean(atomic_radius)
raio_var = np.var(atomic_radius)

ele_mean = np.mean(eletronegativity)
ele_var = np.var(eletronegativity)

val_mean = np.mean(e_val)
val_var = np.var(e_val)