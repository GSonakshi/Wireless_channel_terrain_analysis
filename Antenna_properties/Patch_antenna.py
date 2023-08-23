# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:57:37 2020

@author: Sonakshi Gupta
"""



import numpy as np
import pandas as pd
from Antenna_properties.read_nsi import readNSI


def antenna_raw_data_read(name):
    data = readNSI(name)
    iFreq = 0
    p1 = data['magn'][iFreq, 0, :, :]
    p2 = data['magn'][iFreq, 1, :, :]
    pLin = np.sqrt(np.square(p1) + np.square(p2))
    pLog = 20 * np.log10(pLin)

    out = {"Theta":[], "Phi":[], "Power":[]}

    for i in range(0,len(pLog),5):

        for j in range(0,len(pLog[0]),5):

            out["Theta"].append(i)
            out["Phi"].append(j)
            out["Power"].append(pLog[i][j])

    cols = ["Theta","Phi","Power"]
    output = pd.DataFrame(out,columns=cols)
    output.to_csv("Antenna_properties/raw_data_antenna_pattern.csv",index=False)
    #print("end of function")
