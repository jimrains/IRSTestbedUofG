load phasedata28.dat
load magdata28.dat
freqs = phasedata3(:,1)
phases = phasedata3(:,2:end)



posi_phases = phases + (phases<0)*360
%posi_phases(:,6) = 0 % Invalid due to FPGA error

sorted_phases = sort(posi_phases.').'

% norm_phases = sorted_phases - sorted_phases(:,1)
% 
% clf
% hold on
% for k = 1:72 
%     plot(norm_phases(k, :))
% 
% end

%PM = norm_phases
PM = sorted_phases
norm_phases = sorted_phases - sorted_phases(:,1)
PM = norm_phases

kappa = 0
FLL = min(freqs)
FUL = max(freqs)

for s = 1:7
    kappa = kappa + (PM(:,s+1) - PM(:,s)).^3;
end

kappa = kappa + (360 - (PM(:,8) - PM(:,1))).^3;

sigma = sqrt(kappa/(12*360));
Nbit = log2(360./(sqrt(12).*sigma));
figure(1);
hold on
plot(freqs, Nbit)
grid on
xlabel('frequency (GHz)')
ylabel('phase resolution (bits)')

%axis([FLL FUL 0 3])
mags = 10*log10(magdata3(:,2:end)) - 10*log10(max(magdata3(:,2:end).').')
figure(2)
clf
plot(freqs, mags)


