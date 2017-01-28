
clear, close all;

%% FIT CONTROL SETTINGS

%               A         Center       q            D    
ParInit =      [1          1           1            1 ]  ;  

DataSourceFolder = '/home/fkp/sbosma/SternGerlach/';
ToFitFileName = '400ma.dat' ;

%%  Loading of Data from file, 2 first columns of floats + ignore header of 3
%  first lines
fullname = [DataSourceFolder ToFitFileName];
[X, Y] = textread(fullname,'%f%f%*[^\n]','delimiter','\t','headerlines',3);
[~,sizeX] = size(X);

%%  Fitting procedure  

[FitCurveY,ParRes,kvg,iter,corp,covp,covr,stdresid,Z,r2] = leasqr(X,Y,ParInit,'RealFunc2') ;


