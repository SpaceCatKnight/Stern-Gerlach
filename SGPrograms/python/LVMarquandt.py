# Created by S. Bosma, Jan 2013 (sbosma@physik.uzh.ch)
# Main fitting script for the Stern-Gerlach data 

from pylab import plot, show, figure, legend, title, xlabel, ylabel
from scipy.optimize import leastsq
from numpy import ones, array
from functionsSG import *

# When True, the plots also show what happens when the fitting function parameters are changed a bit.
doAllPlots = False

# When True, this will plot the chi square for values around  all the final values of the fit parameters
testChi2 = False

# Load data
file_location = '/Users/bosma/Documents/Praktikum/Stern-Gerlach/python/'
filename = '1000mA'
x, y = load_data(file_location, filename)

## Initial parameters for the non zero-field data fits
pname = ['A','C','q','D'] #parameters names
#param0 = [17, -0.001, 6, 0.1] 
param0 = [200, 1, 6, 0.1] 

## Initial parameters for the double gaussian zero field fit
# pname = ['xc1', 'w1', 'A1', 'xc2', 'w2', 'A2', 'B'] #parameters names
#param0 = [0, 0.5, 1, 0.1, 0.6, 1.1, 0] 

# Launch fit with the residuals function
plsq = leastsq(EvenMoreRealFuncResiduals, param0, args=(y, x), maxfev=10000, full_output=True)
paramFinal, err = plsq[0], plsq[1]
chi2  = sum(EvenMoreRealFuncResiduals(paramFinal,y,x)**2)

print 'Final parameters ', paramFinal
print 'Initial guess ', param0
print 'Covariance matrix ', err
print 'chi2 ', chi2

# Fit result and initial guess
fit = EvenMoreRealFunc(paramFinal, x)
initialGuess = EvenMoreRealFunc(param0, x)

# Plot results
plot(x, y, 'bo', label='data')
plot(x, fit,'r', label='fit')
plot(x, initialGuess ,'g', label='initial guess')
legend()







# Influence of parameter variation on chi2 (change the residual function as needed at *):
if testChi2: 

    nbrOfPoints = 10
    multiplier = [1, 0.005, 0.1, 0.1]
    for index in range(0,4):
        test = ones((2*nbrOfPoints,4))
        param = paramFinal.copy() 
        for i in range(-nbrOfPoints,nbrOfPoints):
            param[index] = paramFinal[index] + i*multiplier[index] 
            test[i+nbrOfPoints] = param.copy()
        errors = []
        for param in test:
            errors.append(sum(RealFuncResiduals(param,y,x)**2)) # *
        figure()
        plot(test[:,index],errors)
        ylabel('chi2' )
        xlabel('parameter nbr '+str(index)+', center value: '+str(paramFinal[index]))

# Other plots: variation of fitting curve vor parameters variations
if doAllPlots:

    figure()
    param = paramFinal.copy() #copy into param, paramFinal is an array
    plot(x, y, 'bo')
    for i in range(-10,10):
        param[0] = paramFinal[0] + i*1
        plot(x, RealFunc(param, x))
        title('A (amplitude) variating in RealFunc')

    figure()
    param = paramFinal.copy()
    plot(x, y, 'bo')
    for i in range(-10,10):
        param[1] = paramFinal[1] + i*0.05
        plot(x, RealFunc(param, x))
        title('C (Center) variating in RealFunc')

    figure()
    param = paramFinal.copy()
    plot(x, y, 'bo')
    for i in range(-10,10):
        param[2] = paramFinal[2] + i*0.1
        plot(x, RealFunc(param, x))
        title('q variating in RealFunc')

    figure()
    param = paramFinal.copy()
    plot(x, y, 'bo')
    for i in range(-10,10):
        param[3] = paramFinal[3] + i*0.1
        plot(x, RealFunc(param, x))
        title('D (vertical shift) variating in RealFunc')


show()
