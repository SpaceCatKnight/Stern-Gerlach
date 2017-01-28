% observed signal at zero field

function result = zf_Func(x)

%%  These internal parameters are obtained from a two gaussian peaks fit of the zero field signal and can be modified

xc1 = 8.8563e-3 ; w1 = 0.2752 ; A1 = 1.6432 ;  
xc2 = 0.7 ; w2 = 0.2898 ; A2 = 1.6886 ;


result = (A1/(w1*sqrt(pi/2))).*exp( -2.*((x-xc1)./w1).^2  ) + (A2/(w2*sqrt(pi/2))).*exp( -2.*((x-xc2)./w2).^2  )  ;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                    2                             2
%               1/2       2 (x - xc1)         1/2       2 (x - xc2)
%           A1 2    exp(- ------------)   A2 2    exp(- ------------)
%                               2                             2
%                             w1                            w2
% zf_Func(x) = ------------------------ + ---------------------------
%                         1/2                           1/2
%                    w1 pi                         w2 pi
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

