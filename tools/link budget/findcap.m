

h = 0.003
eta = 120*pi
er = 2.2
c = 0.3e9

L2 = 0.5e-9;
Cn = 0.5e-12;
f = linspace(1e9, 6e9, 51);
W = 2*pi*f;
Rn = 0;

caps = linspace(0.01, 1, 100)*1e-12

for m = 1:length(caps)
    Cn = caps(m);
    %Zn = (j*W.*L1.*(j*W*L2 + 1./(j*W*Cn) + Rn))./(j*W.*L1 + (j*W*L2 + 1./(j*W*Cn) + Rn));
    Zn = (j*(eta/sqrt(er)).*tan(sqrt(er)*h.*W/c).*(j*W*L2 + 1./(j*W*Cn) + Rn))./(j*(eta/sqrt(er)).*tan(sqrt(er)*h.*W/c) + (j*W*L2 + 1./(j*W*Cn) + Rn));
    gamma(m,:) = (Zn - 120*pi)./(Zn + 120*pi);
    curves(m,:) = 180/pi*angle(gamma(m,:));
    mags(m,:) = abs(gamma(m,:));
end

%% Plot phase versus C for several frequencies
figure(1)
clf
hold on
%fs = [3.5 3.6 3.7 3.8 3.9 4.0]*1e9;

fs = 3e9;

for p = 1:length(fs)
    fc = fs(p);
    [val,ind] = min(abs(f - fc));
    subplot(2,1,1)
    hold on
    plot(caps, curves(:,ind) + 180, 'LineWidth', 1.5)
    axis([min(caps) max(caps) 0 360])
    
    subplot(2,1,2)
    hold on
    plot(caps, 20*log10(mags(:,ind)), 'LineWidth', 1.5)
    %axis([min(caps) max(caps) 0 1])        
end

fc = 3e9;
[val,ind] = min(abs(f - fc));
phasevcap = curves(:,ind);
%phases = [-135 -90 -45 0 45 90 135 180] - 22.5;
%phases = [-90 90] + 40;
phases = [-135 -45 45 135] - 20

for k = 1:length(phases)
    [val,ind] = min(abs(phasevcap - phases(k)));
    cp(k) = caps(ind)
end



