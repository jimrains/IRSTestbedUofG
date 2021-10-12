load phasedata28.dat
datata = phasedata28

freqs = datata(:,1)

phases = datata(:,2:end)
%phases(:,1) = 0
figure(1)
plot(freqs, phases)

% load magdata16.dat
% datata = magdata16
% 
% mags = datata(:,2:end)
% 
% mags = mags./(min(mags.').')

% figure(2)
% plot(freqs, 10*log10(mags))



