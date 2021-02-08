#!/bin/bash
#================================================#
# Esse script faz uso do bash para que sejam executados programas 
# main.py e main_sk.py além de confeccionar gráfico de custo das 
# redes neurais
#
# Autor : Otaviano da Cruz Neto 
# 29/06/2020
#===================================================#


#Ativação do pacote pymatgen

source activate my_pymatgen

# Execução dos programas 

python main.py > out_zt.dat
python main_sk.py > out_sk.dat


#======Tratamento de dados para criação de gráfico de custo por iteração ======#

# Corte dos Outputs salvos dos programas

grep 'Iteration' out_sk.dat > out_skgrep.dat
grep 'Iteration' out_zt.dat > out_ztgrep.dat

# Organização da tabela gerada para cada um dos outputs

paste <(awk '{printf "%12.6f\n",$2}' out_ztgrep.dat) <(awk '{printf "%12.6f\n",$5}' out_ztgrep.dat) > outzt.dat
paste <(awk '{printf "%12.6f\n",$2}' out_skgrep.dat) <(awk '{printf "%12.6f\n",$5}' out_skgrep.dat) > outsk.dat

#Contrução dos gráficos

gnuplot graf.gp




