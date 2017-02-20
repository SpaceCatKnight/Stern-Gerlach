# -*- coding: utf-8 -*-
"""
author: hp aka HanspPeter
"""


import numpy as np
import matplotlib.pyplot as plt

# Konstanten
kb = 1.38064852*10**(-23) # boltzmann constant
L = 0.07 # length of the poles
a = 2.5*10**(-3) # radius of the convex pole
l = 0.455 # distance magnetic field entry detector??
ep = 0.953 # constant for magnetic field
a0 = 1.5459*10**(-2)
a1 = 0.6113
a2= 0.5146
a3 = -0.3907
ma0 = 2.7819*10**(-3)
ma1 = 2.0927*10**(-2)
ma2 = 4.1541*10**(-2)
ma3 = 2.2721*10**(-2)
mI = 0.005 # error on I in mA IRRELEVANT!!!!
ml = 1*10**(-3) # error on l in mm 
mL = 0.1*10**(-3) # error on L in mm
ma = 0.2*10**(-3) # error on a in mm
mep = 0.0026
mq = [0.0000015,0.0000025,0.0000029,0.0000032,0.0000032,0.0000041]
mT = 0.1


I = [0.402,0.600,0.700,0.800,0.900,1.000] # current in A
T = [184.1,186.3,186.5,186.5,186.7,187.5] # temperature in C
Tc = [457.25, 459.45, 459.65, 459.65, 459.85, 460.65] # temperature in K
q = [0.0022452, 0.0035437, 0.0042096, 0.004781, 0.0053034, 0.005731099999999999] 
T = 459.4


def Bfeld(I,a0,a1,a2,a3):
    B = []
    for i in range(6):
        B.append((a0+I[i]*a1+a2*(I[i]**2)+a3*(I[i]**3)))
    return B
    
B = Bfeld(I,a,a1,a2,a3)

def FehlerBfeld(I,a1,a2,a3):
    mB = []
    for i in range(6):
        mI1 = (mI*(a1+2*a2*I[i]+3*a3*(I[i]**2)))
        ma01= ma0
        ma11= ma1*I[i]
        ma21= ma2*(I[i]**2)
        ma31= ma3*(I[i]**3)
        mB.append((mI1**2+ma01**2+ma11**2+ma21**2+ma31**2)**(0.5))
    return mB


mB = FehlerBfeld(I,a1,a2,a3)
    
def magnetfeld(ep,a,B):
    dB = []
    for i in range(6):
        dB.append(ep*B[i]/a)
    return dB


def Msz(l,L,kb,T,q,dB,ep,a,B):
    M = (2*kb*T*a)/(l*L*(1-L/(2*l))*ep*124.152)
    return M
    


   
def dq(kb,T,a,l,L,ep,B,i):
    return 2*kb*T*a/(l*L*(1-L/(2*l))*ep)
def da(kb,T,q,l,L,ep,B,i):
    return 2*kb*T*q[i]/(l*L*(1-L/(2*l))*ep*B[i])
def dT(kb,a,q,l,L,ep,B,i):
    return 2*kb*a*q[i]/(l*L*(1-L/(2*l))*ep*B[i])
def dl(kb,T,a,q,l,L,ep,B,i):
    return -8*kb*T*a*q[i]/(L*((L-2*l)**2)*ep*B[i])
def dL(kb,T,a,q,l,L,ep,B,i):
    return -8*kb*T*a*q[i]*(l-L)/((L**2)*((L-2*l)**2)*ep*B[i])   
def dep(kb,T,a,q,l,L,ep,B,i):
    return -2*kb*T*a*q[i]/(l*L*(1-L/(2*l))*(ep**2)*B[i])   
def dB(kb,T,a,q,l,L,ep,B,i):
    return -2*kb*T*a*q[i]/(l*L*(1-L/(2*l))*ep*(B[i]**2))
def dK(kb,T,a,q,l,L,ep,B,i):
    return -2*kb*T*a/(l*L*(1-L/(2*l))*ep*124.152**2)
    
def Fehler(kb,T,a,q,l,L,ep,B,mq,ma,mT,ml,mL,mep,mB):
    m = []

    for i in range(6):
        #dq1 = dq(kb,T,a,l,L,ep,B,i)
        da1 = da(kb,T,q,l,L,ep,B,i)
        dT1 = dT(kb,a,q,l,L,ep,B,i)
        dl1 = dl(kb,T,a,q,l,L,ep,B,i)
        dL1 = dL(kb,T,a,q,l,L,ep,B,i)
        dep1 = dep(kb,T,a,q,l,L,ep,B,i)
        #dB1 = dB(kb,T,a,q,l,L,ep,B,i)
        dK1 = dK(kb,T,a,q,l,L,ep,B,i)
        m.append(((da1*ma)**2+(dT1*mT)**2+(dL1*mL)**2+(dl1*ml)**2+(dep1*mep)**2+(dK1*8.17576)**2)**(0.5))
    return m
    
ML= Msz(l,L,kb,T,q,dB,ep,a,B)
FL = Fehler(kb,T,a,q,l,L,ep,B,mq,ma,mT,ml,mL,mep,mB)



print("Wert von m:",ML)
print("Mittelwert Fehler:",np.mean(FL))
"""
x = np.array([0.0022452, 0.0035437, 0.0042096, 0.004781, 0.0053034, 0.005731099999999999])
y = np.array([0.3060222679144, 0.4701447999999999, 0.5485538999999999, 0.6208455999999999, 0.6846756999999999, 0.7376999999999998])
z = np.polyfit(x, y, 1)
print(z)
"""
