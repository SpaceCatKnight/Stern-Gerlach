# -*- coding: utf-8 -*-
"""
author: hp aka HanspPeter
"""


# naja nur 19 grösseordnige denäbed

import numpy as np
import matplotlib.pyplot as plt

# Konstanten
kb = 1.38064852*10**(-23) # boltzmann constant
L = 0.07 # length of the poles
a = 2.5*10**(-3) # radius of the convex pole
l = 0.455 # distance magnetic field entry detector??
ep = 0.953 # constant for magnetic field
mI = 5 # error on I in mA IRRELEVANT!!!!
ml = 1*10**(-3) # error on l in mm 
mB = 0.01 # geschatzt aus Fehler auf I
mL = 0.1*10**(-3) # error on L in mm
ma = 0.2*10**(-3) # error on a in mm
mep = 0.0026
mq = [0.0000015,0.0000025,0.0000029,0.0000032,0.0000032,0.0000041]
mT = 0.1


I = [402,600,700,800,900,1000] # current in mA
B = [0.320,0.485,0.560,0.635,0.695,0.750] # aus Plot mithilfe von I abgelesen
TC = [184.1,186.3,186.5,186.5,186.7,187.5] # temperature in C
T = [457.25, 459.45, 459.65, 459.65, 459.85, 460.65] # temperature in K
q = [0.0022452, 0.0035437, 0.0042096, 0.004781, 0.0053034, 0.005731099999999999] 




def magnetfeld(ep,a,B):
    dB = []
    for i in range(6):
        dB.append(ep*B[i]/a)
    return dB


def Msz(l,L,kb,T,q,dB,ep,a,B):
    M = []
    for i in range(6):
        M.append((q[i]*2*kb*(T[i]))/(l*L*(1-L/(2*l))*magnetfeld(ep,a,B)[i]))
    return M
    
ML= Msz(l,L,kb,T,q,dB,ep,a,B)

   
def dq(kb,T,a,l,L,ep,B,i):
    return 2*kb*T[i]*a/(l*L*(1-L/(2*l))*ep*B[i])
def da(kb,T,q,l,L,ep,B,i):
    return 2*kb*T[i]*q[i]/(l*L*(1-L/(2*l))*ep*B[i])
def dT(kb,a,q,l,L,ep,B,i):
    return 2*kb*a*q[i]/(l*L*(1-L/(2*l))*ep*B[i])
def dl(kb,T,a,q,l,L,ep,B,i):
    return -8*kb*T[i]*a*q[i]/(L*((L-2*l)**2)*ep*B[i])
def dL(kb,T,a,q,l,L,ep,B,i):
    return -8*kb*T[i]*a*q[i]*(l-L)/((L**2)*((L-2*l)**2)*ep*B[i])   
def dep(kb,T,a,q,l,L,ep,B,i):
    return -2*kb*T[i]*a*q[i]/(l*L*(1-L/(2*l))*(ep**2)*B[i])   
def dB(kb,T,a,q,l,L,ep,B,i):
    return -2*kb*T[i]*a*q[i]/(l*L*(1-L/(2*l))*ep*(B[i]**2))

def Fehler(kb,T,a,q,l,L,ep,B,mq,ma,mT,ml,mL,mep,mB):
    m = []

    for i in range(6):
        dq1 = dq(kb,T,a,l,L,ep,B,i)
        da1 = da(kb,T,q,l,L,ep,B,i)
        dT1 = dT(kb,a,q,l,L,ep,B,i)
        dl1 = dl(kb,T,a,q,l,L,ep,B,i)
        dL1 = dL(kb,T,a,q,l,L,ep,B,i)
        dep1 = dep(kb,T,a,q,l,L,ep,B,i)
        dB1 = dB(kb,T,a,q,l,L,ep,B,i)
        m.append(((dq1*mq[i])**2+(da1*ma)**2+(dT1*mT)**2+(dL1*mL)**2+(dl1*ml)**2+(dep1*mep)**2+(dB1*mB)**2)**(0.5))
    return m
FL = Fehler(kb,T,a,q,l,L,ep,B,mq,ma,mT,ml,mL,mep,mB)



print ""      
print "Werte von m:",ML
print ""
print "Fehler auf m:",FL
print ""
print "Mittelwert m:",np.mean(ML)
print "Mittelwert Fehler:",np.mean(FL)
   
    
    
    
    
