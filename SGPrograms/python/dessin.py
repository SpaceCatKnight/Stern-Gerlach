from numpy import arange, exp, sqrt
from math import pi #and not exp ! functions take arrays as x 
from scipy import array
from scipy import array
from pylab import plot, show, figure, legend, title, xlabel, ylabel
from scipy.optimize import leastsq
from numpy import ones
from functionsSG import *


#data location
file_location = '/Users/bosma/Documents/Praktikum/Data_2008/Michael_Christian_modif/'
filename = '0mA.dat'

x, y = load_data(file_location, filename)

xu, yu = [],[]
count = 0
Nlimit = 50

for i in range(len(x)):
    if count == Nlimit:
        xu.append(x[i])
        yu.append(y[i])
        count = 0
    else:
        count += 1

yzf = map(zf_Func, xu)

plot(x,y,label='data',lw=6)
plot(xu,yu,'ro',label='undersampled data')
plot(xu,yzf,'g+',label='simulated data')
legend()
xlabel('distance in mm')
ylabel('detector signal')
title('zero field data')
show()
