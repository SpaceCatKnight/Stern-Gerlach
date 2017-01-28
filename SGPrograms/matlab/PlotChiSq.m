
% calculate and plot chi2 for values of q near the value found by fit

Range = 0.1 ; %%  10% around q from fit
NofPts = 20 ; %% Number of Points to plot

Qvect = (ParRes(3)*(1-Range)):(2*Range*ParRes(3)/NofPts):(ParRes(3)*(1 + Range)) ;
[~, NofQ] = size(Qvect) ;
ChSqVect = 0.*Qvect ;

ParValue = ParRes ;

%%  Calculation of Chi^2
for k = 1:NofQ  ;
    ParValue(3) = Qvect(k) ;
CurveY = RealFunc2(X,ParValue) ;
    ChSqVect(k) = sum((CurveY-Y).^2 ) ;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
%          Qvect = [q*(1-Range), ... q*(1-Range)*2*Range*k/NofPts, ... q*(1+Range)]
%
%                                                           
%                          -----   
%                           \                    2
%          ChSqVect(k) =     )     (yfit - ydata)
%                           /                          
%                          -----         
%                           data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%  Plotting of result
figure()
plot(Qvect,ChSqVect,'o');
xlabel('q (mm)','FontSize',12);
ylabel('chi^2 ','FontSize',12);
