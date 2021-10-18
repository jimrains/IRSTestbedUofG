sweep_dir = '/home/rusty/github/IRSTestbedUofG/tools/measurements/band sweep/20211016/'

%ref = load(strcat(sweep_dir,'2021106_19509_SWEEP_0A.dat'))
%ref = load(strcat(sweep_dir,'618_SWEEP_3900_0.dat'))
%non = load(strcat(sweep_dir,'618_SWEEP_3900_N.dat'))
ref = load(strcat(sweep_dir,'20211016_235030_SWEEP_1_COLREF_OFF.dat'))
%nors = load(strcat(sweep_dir,'2021106_212323_SWEEP_1A.dat'))
%nors = load(strcat(sweep_dir,'2021106_23516_SWEEP_1B.dat'))

d1bit = load(strcat(sweep_dir,'20211017_0046_SWEEP_1_1bitCOL.dat'))
d2bit = load(strcat(sweep_dir,'20211016_235554_SWEEP_2_2bitCOL.dat'))
d3bit = load(strcat(sweep_dir,'20211016_23451_SWEEP_3_3bitCOL.dat'))


%relmags = gip(:,3)
freq = ref(:,2)

figure(1)
%clf
%plot(freq, nors(:,3), '-.')
hold on
plot(freq, ref(:,3), '--')
%plot(freq, non(:,3), '-.')
plot(freq, smooth(d1bit(:,3),3))
plot(freq, smooth(d2bit(:,3),3))
plot(freq, smooth(d3bit(:,3),3))
axis([min(freq) max(freq) -30 max(d1bit(:,3)) + 5])
grid on
legend(["IRS off", "1 bit", "2 bit", "3 bit"])
title("Relative received power")
ylabel("Baseband power (dBFS)")
xlabel("Frequency (GHz)")

figure(3)
%clf
hold on
%plot(freq, nors(:,3) - nors(:,3), 'r-.')
plot(freq, smooth((d1bit(:,3) - ref(:,3)), 5), 'b-.', 'LineWidth', 2)
plot(freq, smooth((d2bit(:,3) - ref(:,3)), 5), 'r-.', 'LineWidth', 2)
plot(freq, smooth((d3bit(:,3) - ref(:,3)), 5), 'black-.', 'LineWidth', 2)
%plot(freq, d1bit(:,3) - non(:,3), 'b')
%plot(freq, d2bit(:,3) - non(:,3), 'r')
%plot(freq, d3bit(:,3) - non(:,3), 'bl')
axis([min(freq) max(freq) -20 35])
legend(["1 bit", "2 bit", "3 bit"])
title("Received Power Improvement for Optimisation at 3.9 GHz", 'FontSize', 15)
ylabel("Received Power Improvement (dB)", 'FontSize', 15)
xlabel("Frequency (GHz)", 'FontSize', 15)
grid on
axis([3800 4000 0 18])
%figure(2)
%plot(freq, nors(:,3) - nors(ref(:,3)))
%grid on
%title("Normalised received power (no IRS)")
%ylabel("Baseband received power (dBFS)")
%xlabel("Frequency (GHz)")
