
% returns the value of a double gaussian with param at point x

function result = DoubleGaussian(x,param)

xc1 = param(1) ; w1 = param(2) ; A1 = param(3) ;  
xc2 = param(4) ; w2 = param(5) ; A2 = param(6) ;

result = (A1/(w1*sqrt(pi/2))).*exp( -2.*((x-xc1)./w1).^2  ) + (A2/(w2*sqrt(pi/2))).*exp( -2.*((x-xc2)./w2).^2  )  ;
