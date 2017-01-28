
% two gaussian fit for data at zero field, almost same program as SGfit.m

clear, close all;

%% FIT CONTROL SETTINGS

%            xc1           w1       A1     xc2      w2      A2 
ParInit =   [ 0.008       0.2        1     0.7     0.2      1 ]  ;  
PlotAfterFit = 1 ;

DataSourceFolder = '/home/fkp/sbosma/SternGerlach/';
ToFitFileName = '0ma.dat' ;

%%  Loading of Data from file, 2 first columns of floats + ignore header of 3 first lines
fullname = [DataSourceFolder ToFitFileName];
[X, Y] = textread(fullname,'%f%f%*[^\n]','delimiter','\t','headerlines',3);

%%  Fitting procedure  

[FitCurveY,ParRes,kvg,iter,corp,covp,covr,stdresid,Z,r2] = leasqr(X,Y,ParInit,'DoubleGaussian') ;
