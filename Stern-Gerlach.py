# -*- coding: utf-8 -*-
"""
author: hp aka HanspPeter
"""


# naja nur 19 grösseordnige denäbed

import numpy as np
import matplotlib.pyplot as plt

# Konstanten
kb = 1.38064852*10**(-23) # boltzmann constant
L = 7*10**(-2) # length of the poles
a = 2.5*10**(-3) # radius of the convex pole
l1 = 0.455 # distance magnetic field entry detector??
l2 = 0.420 # distance magnetic field center detector??
ep = 0.953 # constant for magnetic field
mI = 5 # error on I in mA
ml = 1 # error on l in mm
mL = 0.1 # error on L in mm
ma = 0.1 # error on a in mm
mep = 0.0026

I = [402,600,700,800,900,1000] # current in mA
B = [0.320,0.485,0.560,0.635,0.695,0.750]
T = [184.1,186.3,186.5,186.5,186.7,187.5] # temperature in C
q = [2.2452,3.5437,4.2096,4.7810,5.3034,5.7311] 
mq = [0.0015,0.0025,0.0029,0.0032,0.0032,0.0041]

def magnetfeld(ep,a,B):
    dB = []
    for i in range(6):
        dB.append(ep*B[i]/a)
    return dB

dB = [121.984, 184.88199999999998, 213.472, 242.06199999999998, 264.93399999999997, 285.9]

def Msz(l1,L,kb,T,q,dB):
    M = []
    for i in range(6):
        M.append((q[i]*2*kb*T[i])/(l1*L*(1-L/(2*l1)*dB[i])))
    return M
    
print Msz(l1,L,kb,T,q,dB)

