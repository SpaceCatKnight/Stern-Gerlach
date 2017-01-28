from numpy import arange, exp, sqrt, array
from math import pi #and not exp ! functions take arrays as x 

# SG apparatus parameters for the realistic beam profile (in millimeters)
pSG = 0.36 
DSG = 0.48

# Zero field data path
folder0mA = '/Users/bosma/Documents/Praktikum/Stern-Gerlach/python/'#'/Users/bosma/Documents/Praktikum/Stern-Gerlach/Data_2008/Michael_Christian_modif/'
filename0mA = '0mAnr2' #'0ma.dat'

# Data taken on the [-dataBoundary, dataBoundary] interval
dataBoundary = 7 # millimeters
ConvPrecision = 0.4 # should be consistent with undersamplingRate
undersamplingRate = 523 #should be 0.4 (ConvPrecision) mm (check data)
 
# Put the double gaussian zero field data fit results here for the RealFunc calculation
# typical values are around xc1 = 0 ; w1 = 0.6 ; A1 = 1.2 ; xc2 = 0.6 ; w2 = 0.6 ; A2 = 1.15 ; B = 0.1
#fittedDoubleGaussianParam = [0, 0.6, 1.2, 0.6, 0.7, 1.15, 0.1]
#their fit result
fittedDoubleGaussianParam = [-2.69762283,  3.63440108, -2.72561122,  1.3811703,   0.97981286,  4.30870879,  1.00285366]

def IdealFuncResiduals(param, y, x):
    print "fitting - IdealFunc ..."
    return y - IdealFunc(param, x)

def NotSoIdealFuncResiduals(param, y, x):
    print "fitting - NotSoIdealFunc ..."
    return y - NotSoIdealFunc(param, x)

def RealFuncResiduals(param, y, x):
    print "fitting - RealFunc ..."
    return y - RealFunc(param, x)

def EvenMoreRealFuncResiduals(param, y, x):
    print "fitting - EvenMoreRealFunc ..."
    return y - EvenMoreRealFunc(param, x)

def zf_FuncResiduals(param, y, x):
    print "fitting - zf_Func ..."
    return y - zf_Func(param, x)


def load_data(folderPath, filename):
    """ 
    Read data from a text file. This assumes a 3 line header and a tab separated two columns x, y formatting.
    """
    f = open(folderPath+filename)
    line_number = 0
    x, y = [], []

    for line in f:
        if line_number >= 3: #ignore first 3 lines of header
            row = line.split('\t')
            assert len(row) >= 2
            x.append(float(row[0]))
            y.append(float(row[1]))
        line_number += 1

    return array(x), array(y)
    

def IdealFunc(param, x):
    """ Ideal two-peak atom distribution, as calculated in the Anleitung.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %                                        q
    %                          A exp(- --------------)
    %                                    | x - C |
    % IdealFunc([A,C,q,D], x) = ----------------------- + D
    %                                            3
    %                                   | x - C |
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    [A, C, q, D] = param
    x = abs(x-C)
    x2 = array([max(1e-10, element) for element in x]) # to avoid divisions by zero; all x values are positive
    return A*exp(-q/x2)/(x2**3) + D  
    
def NotSoIdealFunc(param, x):
    """ More realistic atom beam: a parabolic edge rectangle instead of a perfectly thin rectangle  """
    [AA, C, q, D] = param
    step = 2*DSG/50
    integral = 0
    for z in arange(-DSG, DSG, step):
        integral += IdealFunc([1,C,q,0], x-z)*I0(z)*step
    return AA*integral + D
    
def I0(z):
    """ Profile of the non-ideal atom beam"""
    if -DSG <= z <= -pSG:
        return DSG + z
    elif -pSG < z < pSG:
        return DSG - pSG/2 - z**2/(2*pSG)
    elif pSG <= z < DSG:
        return DSG - z
    else:
        return 0

def zf_Func(param, x):
    """ 
    Double gaussian approximating the atom distribution when the applied magnetic field is 0
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %                                    2                             2
    %               1/2       2 (x - xc1)         1/2       2 (x - xc2)
    %           A1 2    exp(- ------------)   A2 2    exp(- ------------)
    %                               2                             2
    %                             w1                            w2
    % zf_Func(x) = ------------------------ + --------------------------- + B
    %                         1/2                           1/2
    %                    w1 pi                         w2 pi
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    xc1, w1, A1, xc2, w2, A2, B = param
    return B + A1/(w1*sqrt(pi/2))*exp( -2*((x-xc1)/w1)**2  ) + A2/(w2*sqrt(pi/2))*exp( -2*((x-xc2)/w2)**2 )

def zf_directData(folderPath, filename):
    """ Loading an undersampled version of the measured zero-field data. """
    ampliX, ampliY = load_data(folderPath, filename)
    listOfIndexes = range(len(ampliX))
    # copy one element of ampliX/Y into ampliX/Yundersampled every undersamplingRate elements
    ampliXunderSampled = [ampliX[i] for i in listOfIndexes if i%undersamplingRate == 0]
    ampliYunderSampled = [ampliY[i] for i in listOfIndexes if i%undersamplingRate == 0]

    return array(ampliXunderSampled), array(ampliYunderSampled)


# Faster RealFunc and EvenMoreRealFunc by loading zero field data once
## using the fitted approximation 
#ampliX = arange(-dataBoundary, dataBoundary, ConvPrecision) #building a new, smaller x-axis
#ampliY = array([zf_Func(fittedDoubleGaussianParam, u) for u in ampliX])

## ~OR~ using the direct data
ampliX, ampliY = zf_directData(folder0mA, filename0mA)


def RealFunc(param, x):
    """
    Convolution of the ideal function and the zero-field distribution.
    Convolution can be calculated using the measured data (undersampled to get faster calculation) 
    ~OR~
    can be calculated using an analytical double gaussian which approximates the measured zero-field data, with parameters resulting from the fit of the zero field data.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %                                                          
    %                               -----   
    %                                \    |data(a) ~OR~                     
    % RealFunc(x, [A, C, q, D]) =     )   |zf_Func(a)    * IdealFunc(x - a, [A, C, q, 0] )  + D
    %                                /                           
    %                               -----         
    %                              a in AmpliX
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    """
    [A, C, q, D] = param  
    result = 0

    for k in range(len(ampliX) ):
        # A := ampliY[k] in IdealFunc to get one less multiplication (faster); cte in IdealFunc then needs to be 0
        # D added at the end, not in IdealFunc to get one less addition (faster)
        result += IdealFunc([ampliY[k], C, q, 0], x - ampliX[k] )

    return (A*ConvPrecision)*result + D 

def EvenMoreRealFunc(param, x):
    """ 
    Same as RealFunc, but using NotSoIdealFunc, with a more realistic beam profile.
    """
    [A, C, q, D] = param
    result = 0

    for k in range(len(ampliX) ):
        result +=  NotSoIdealFunc([ampliY[k], C, q, 0], x - ampliX[k] )

    return (A*ConvPrecision)*result + D 

    
