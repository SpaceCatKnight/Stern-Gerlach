# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 21:35:15 2013
This script let you do the fitting and plotting for the Stern-Gerlach-Experiment automatically.
It also saves the plot and the output-Data automatically in the path you wish.

@author: jungfranckianer & fraublauwal
modified Jan 25 2013 by sbosma@physik.uzh.ch
"""

from scipy import array
import pylab as pl
from scipy.optimize import leastsq
from numpy import ones
import functionsSG as fSG
import os.path

FUNCTION_DICT = {"NotSoIdealFunc" : fSG.NotSoIdealFunc, 
                "IdealFunc" : fSG.IdealFunc,
                "RealFunc" : fSG.RealFunc,
                "EvenMoreRealFunc": fSG.EvenMoreRealFunc}

RESIDUAL_DICT = {"NotSoIdealFunc" : fSG.NotSoIdealFuncResiduals, 
                "IdealFunc" : fSG.IdealFuncResiduals,
                "RealFunc" : fSG.RealFuncResiduals,
                "EvenMoreRealFunc": fSG.EvenMoreRealFuncResiduals}

#put your own files and locations here
file_location = '/Users/bosma/Documents/Praktikum/Stern-Gerlach/Data_2008/Michael_Christian_modif/'
filenames = ['400ma.dat','500ma.dat', '600ma.dat']

def doAll(file_location, filename, function_name="IdealFunc"):
    '''
    Fits, plots, and saves Ster-Gerlac data
    Input: file path, fit function
    Output: graph, final fit parameters, initial guess, covariance matrix, chi2. 
    '''
 
    function_in_use = FUNCTION_DICT[function_name]
    residual_in_use = RESIDUAL_DICT[function_name]

    print "\n\n -------- Processing file %s" % filename
    x, y = fSG.load_data(file_location, filename)

    #do fit
    pname = ['A','Center','q','D']
    param0 = [10, -0.0005, 4.2, 0.05] #initial params
    plsq = leastsq(residual_in_use, param0, args=(y, x), maxfev=10000, full_output=True)
    paramFinal, err = plsq[0], plsq[1]

    fit = function_in_use(paramFinal, x)
    initialGuess = function_in_use(param0, x)
    
    #show results and plot
    fig = pl.figure()
    pl.plot(x, y, 'bo', label=' data')
    pl.plot(x, fit,'r', label='fit')
    pl.plot(x, initialGuess ,'g', label='initial guess')
    pl.legend()
    pl.xlabel('Distance [mm]')
    pl.ylabel('Voltage [V]')
    pl.title('%s at %s' % (function_name,filename))
    txt_final = 'Final parameters'
    print txt_final, paramFinal
    txt_initial = 'Initial guess'
    print txt_initial, param0
    txt_cov = 'Covariance matrix'
    print txt_cov, err
    
    chi2  = sum(residual_in_use(paramFinal,y,x)**2)
    txt_chi2 = 'chi2 '
    print 'chi2 ', chi2
    
    #save graph
    graph_name="%s-%s.png" % (function_name,filename)
    output_name = os.path.join(file_location,graph_name)  
    print "Saving figure to ", output_name
    pl.savefig(output_name)
    
    #save fit info
    text_output_name = os.path.join(file_location,graph_name[:-3]+"txt")
    print "Saving fit info to ", text_output_name
    out_f = open(text_output_name,"wb")
    out_f.write(graph_name[:-4]+"\n")
    out_f.write(txt_initial + "\n")
    out_f.write(str(param0)+ "\n")
    out_f.write(txt_final + "\n")
    out_f.write(str(paramFinal) + "\n")
    out_f.write(txt_cov + "\n")
    out_f.write(str(err) + "\n") 
    out_f.write(txt_chi2+ "\n")
    out_f.write(str(chi2)+ "\n")
    out_f.write("output of least square fit"+ "\n")
    for piece in plsq:
        out_f.write(str(piece) + "\n")
    out_f.close()
    
    

if __name__ == "__main__":
    
    for file in filenames:
        for function in FUNCTION_DICT.keys():

            doAll(file_location, file, function)
