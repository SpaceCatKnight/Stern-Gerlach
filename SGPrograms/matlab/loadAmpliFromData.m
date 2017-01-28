%load ampliX and ampliY from data at zero field; take only one data point every N
%so that ampliX ~ -bound:ConvPrecision:bound and ampliY = corresponding
%points in data

function [ampliX, ampliY] = loadAmpliFromData(bound, ConvPrecision) 

DataSourceFolder = '/home/fkp/sbosma/SternGerlach/';
ToFitFileName = '0ma.dat' ;

%% load data 
fullname = [DataSourceFolder ToFitFileName];
[ampliXbig, ampliYbig] = textread(fullname,'%f%f%*[^\n]','delimiter','\t','headerlines',3);
[Xsizebig, ~] = size(ampliXbig) ; % size reversed: column vectors

%% initialize
count = 0 ;
index = 1 ;
Nlimit = floor(ConvPrecision/(2*bound/Xsizebig)); 
ampliX = zeros(1,2*bound/ConvPrecision-1) ;
ampliY = zeros(1,2*bound/ConvPrecision-1) ;

%% undersample data to have less points 
for i = 1:Xsizebig
    if count == Nlimit % take one data point every Nlimit points
        ampliX(index) = ampliXbig(i) ;
        ampliY(index) = ampliYbig(i) ;
        index = index + 1 ;
        count = 0 ;
    else
        count = count + 1 ;
    end
end

