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
    - Criando Banco de Dados com as informações de Input e Output (Em progresso)
    - Separação de Dataset para Treino e para Validação
    - Treino da Rede
    - Validação dos resultados 
    - Análise de Resultados e contrução de gráficos de eficiência 

@author: hardproxy
"""
import csv # Módulo de acesso a arquivos do tipo ,csv
from mpcontribs.client import load_client # Módulo de acesso a uma seção no MPContribs server
from pymatgen.ext.matproj import MPRester, MPRestError # Módulo de acesso ao MP server
from pymatgen import Structure # Acesso á classe do tipo Structure
import numpy as np  

# Inicialização  do client com a minha userkey
client = load_client('nmExh2lluuzGHuQKbOG8Si7kCJRY6q8V')

with open('/home/hardproxy/Documents/TCC-BD_ML/ML-ThermoElec/Data/ids/data.csv') as csv_file:

    csv_reader = csv.DictReader(csv_file)
    list_id = []
    list_ident = []
    list_form = []
    for row in csv_reader:
        list_id.append(row['id'])
        list_ident.append(row['identifier'])
        list_form.append(row['formula'])
csv_file.close()


with open('/home/hardproxy/Documents/TCC-BD_ML/ML-ThermoElec/Data/Materials_Data/Materials_Data.csv', mode='a') as csv_file:
    
    # Definição inicial do Arquivo de armazenamento de dados
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
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    class_crystal={'tetragonal':0,'trigonal':1,'orthorhombic':2,'cubic':3,'monoclinic':4
                  ,'triclinic':5,'hexagonal': 6}
    
    #Acesso ao servidor MP pela USER-KEY  
    with MPRester("AzDkMZ4uNfGQbovDDB79") as m:        
        for i in range(28651,len(list_id)) : 
            # Caso houver algum tipo de erro durant
            try:  
                     
                structure = m.get_data(list_ident[i],data_type = 'vasp', prop = 'structure')
                if len(structure) == 0  :             
                    structure = m.get_data(list_form[i],data_type = 'vasp', prop = 'structure')
                
                spacegroup = m.get_data(list_ident[i],data_type='vasp',prop='spacegroup')
                if len(spacegroup) == 0 :
                    spacegroup = m.get_data(list_form[i],data_type='vasp',prop='spacegroup')
                
                e_form_per_atom = m.get_data(list_ident[i],data_type='vasp',prop='formation_energy_per_atom')[0]['formation_energy_per_atom']          
           
                band = m.get_data(list_ident[i],prop='bandstructure_uniform')
                efermi = band[0]['bandstructure_uniform'].efermi
                if len(band) == 0 :      
                    band = m.get_data(list_ident[i], prop='bandstructure')
                    efermi = band[0]['bandstructure'].efermi
                    
                # Separação de diferentes Sistemas Cristalinos
                crystal_system=[0,0,0,0,0,0,0,0]
                
                crystal_system[class_crystal[spacegroup[0]['spacegroup']['crystal_system']]] = 1


                species=structure[0]['structure'].types_of_specie
                ntypes=structure[0]['structure'].ntypesp
                n_sites = structure[0]['structure'].num_sites
                
                #Criação de Listas 
                group=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                period=[0,0,0,0,0,0,0]
                atomic_mass=[]
                atomic_radius=[]
                eletronegativity=[]
                e_val=[]
                energy_level = [0,0,0,0,0,0,0]
                
                for j in range(ntypes):
                    data=species[j].data
                    
                    # Salvando Inputs - Localização na Tabela Periodica
                    if period[species[j].row - 1] == 0:
                        period[species[j].row - 1] = 1
                        
                    if group[species[j].group - 1] == 0:
                        group[species[j].group - 1] = 1
                    
                    
                    # Calculo do numero de eletrons de valencia 
                    str_ele =species[j].full_electronic_structure
                    soma = 0
                    for k in str_ele:
                        if k[0] == period[j]:
                            soma += k[2]
                        
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
                
                
                
                contrib = client.contributions.get_entry(pk=list_id[i], _fields=['_all']).result()

                temp = contrib['data']['T']['value']
                
                k_e = contrib['data']['κₑᵉ']['n']['value']
                s_medio = contrib['data']['⟨S²σ⟩']['n']['value']
        
                # Criação de um dicionário para armazenamento dos dados num arquivo .csv
                dict_info = {'':i,'id':list_id[i],'identifier':list_ident[i],
                             'formula':list_form[i],'temperature':temp,
                             'efermi':efermi,'e_per_atom':e_form_per_atom,
                             'ele_cell':n_sites,
                             'med_mass':mass_mean,'var_mass':mass_var,
                             'med_raio':raio_mean,'var_raio':raio_var,
                             'med_ele':ele_mean,'var_ele':ele_var,
                             'med_val':val_mean,'var_val':val_var,
                             'g1':group[0],'g2':group[1],'g3':group[2],
                             'g4':group[3],'g5':group[4],'g6':group[5],
                             'g7':group[6],'g8':group[7],'g9':group[8],
                             'g10':group[9],'g11':group[10],'g12':group[11],
                             'g13':group[12],'g14':group[13],'g15':group[14],
                             'g16':group[15],'g17':group[16],'g18':group[17],
                              'p1':period[0],'p2':period[1],'p3':period[2],
                              'p4':period[3],'p5':period[4],'p6':period[5],
                              'p7':period[6],
                              'e_l1':energy_level[0],'e_l2':energy_level[1],
                              'e_l3':energy_level[2],'e_l4':energy_level[3],
                              'e_l5':energy_level[4],'e_l6':energy_level[5],
                              'e_l7':energy_level[6],
                              'tetragonal':crystal_system[0],'trigonal':crystal_system[1],
                              'orthorhombic':crystal_system[2],'cubic':crystal_system[3],
                              'monoclinic':crystal_system[4],'triclinic':crystal_system[5],
                              'hexagonal':crystal_system[6],
                             '⟨S²σ⟩':s_medio,'κₑᵉ':k_e}
                print('Salvando dados do Material : ',list_form[i],'\n')
                # Escrita no arquivo .csv
                writer.writerow(dict_info)
            
            except (IndexError,MPRestError,AttributeError):
                pass
        
            print('Material processado : ' + str(i) + '\n')
