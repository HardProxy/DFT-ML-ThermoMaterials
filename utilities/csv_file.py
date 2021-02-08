#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 16:13:16 2020

@author: hardproxy
"""

import csv 
with open('Data_Base.csv', mode='w') as csv_file:
    fieldnames = ['','id','identifier','formula','temperature','energy','volume','⟨S²σ⟩p','⟨S²σ⟩n','κₑᵉ']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow(dict_info)
    