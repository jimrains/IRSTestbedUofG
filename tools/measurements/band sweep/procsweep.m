
sweep_dir = '/home/rusty/github/IRSTestbedUofG/tools/measurements/band sweep/2021106/'
opt_dir = '/home/rusty/github/IRSTestbedUofG/PiRS/3BIT/RxSide/2021106/'


%ref = load(strcat(sweep_dir,'2021106_19509_SWEEP_0A.dat'))
ref = load(strcat(sweep_dir,'2021106_213224_SWEEP_0B.dat'))

%nors = load(strcat(sweep_dir,'2021106_212323_SWEEP_1A.dat'))
nors = load(strcat(sweep_dir,'2021106_23516_SWEEP_1B.dat'))

gip = load(strcat(sweep_dir,'2021106_204350_SWEEP_3800.dat'))
%gip = load(strcat(sweep_dir,'2021106_20134_SWEEP_3300.dat'))
%gip = load(strcat(sweep_dir,'2021106_22409_SWEEP_4200.dat'))
gip = load(strcat(sweep_dir,'2021106_202428_SWEEP_3500.dat'))
gip = load(strcat(sweep_dir,'2021106_22143_SWEEP_3500.dat'))
gip = load(strcat(sweep_dir,'2021106_222641_SWEEP_4000.dat'))

relmags = gip(:,3)
freq = gip(:,2)

figure(1)
clf
plot(freq, nors(:,3), '-.')
hold on
plot(freq, ref(:,3), '--')
plot(freq, relmags)
axis([min(freq) max(freq) -30 max(relmags) + 5])
grid on
legend(["No IRS", "IRS off", "IRS conf"])
title("Relative received power")
ylabel("Baseband power (dBFS)")
xlabel("Frequency (GHz)")

figure(3)
clf
hold on
%plot(freq, nors(:,3) - nors(:,3), 'r-.')
plot(freq, relmags - ref(:,3), 'r--')
plot(freq, relmags - nors(:,3), 'b')
axis([min(freq) max(freq) -20 35])
legend(["versus IRS off", "versus no IRS"])
title("Received power improvement")
ylabel("Received power improvement (dB)")
xlabel("Frequency (GHz)")
grid on

% figure(2)
% plot(freq, nors(:,3) - nors(ref(:,3)))
% grid on
% title("Normalised received power (no IRS)")
% ylabel("Baseband received power (dBFS)")
% xlabel("Frequency (GHz)")
