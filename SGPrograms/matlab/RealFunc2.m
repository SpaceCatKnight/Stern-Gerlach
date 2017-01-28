%closer to observed signal than IdealFun: convolution of zero field response and
%ideal response

function result = RealFunc2(x, param) 

A = param(1); Center = param(2); q = param(3); D = param(4);
bound = 5 ;
ConvPrecision = 0.1 ;  %  in millimeters

%% define ampliX = arbitrary support with same bounds as data, ampliY = values of zf_Func on ampliX

ampliX = -bound:ConvPrecision:bound ; 
ampliY = zf_Func(ampliX) ;

%% or define ampliX, ampliY directly from zero field data (choose one o those two methods)

[ampliX, ampliY] = loadAmpliFromData(bound, ConvPrecision) ; 

%% calculate convolution
[~,Xsize] = size(ampliX) ;  
result = 0.*x ; %  result is a vector of size same as x, full of zeros

for k = 1:Xsize
	  result = result + IdealFun2( x - ampliX(k), [ampliY(k) Center q 0 ] );
end

result = A.*result + D ;


% the above is physically equivalent to this calculation, closer to the convolution definition:
% for ...
%   result = result + zf_Func(ampliX(k)) * IdealFun2([A, C, q, D], x-ampliX(k))
% end
% 
% but quicker (less multiplications to do)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                          
%                               -----   
%                                \    |data(a) or                     
% RealFunc2(x,[A, C, q, 0]) =     )   |zf_Func(a)    * IdealFun2(x - a, [A, C, q, 0] )  + D
%                                /                           
%                               -----         
%                              a in AmpliX
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




