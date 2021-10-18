
sweep_dir = '/home/rusty/github/IRSTestbedUofG/tools/measurements/band sweep/20211016/'
%opt_dir = '/home/rusty/github/IRSTestbedUofG/PiRS/3BIT/RxSide/2021106/'


%ref = load(strcat(sweep_dir,'2021106_19509_SWEEP_0A.dat'))
ref = load(strcat(sweep_dir,'618_SWEEP_3900_0.dat'))
non = load(strcat(sweep_dir,'618_SWEEP_3900_N.dat'))

%nors = load(strcat(sweep_dir,'2021106_212323_SWEEP_1A.dat'))
%nors = load(strcat(sweep_dir,'2021106_23516_SWEEP_1B.dat'))

d1bit = load(strcat(sweep_dir,'618_SWEEP_3900_1.dat'))
d2bit = load(strcat(sweep_dir,'618_SWEEP_3900_2.dat'))
d3bit = load(strcat(sweep_dir,'618_SWEEP_3900_3.dat'))


%relmags = gip(:,3)
freq = non(:,2)

figure(1)
%clf
%plot(freq, nors(:,3), '-.')
hold on
plot(freq, ref(:,3), '--')
plot(freq, non(:,3), '-.')
plot(freq, d1bit(:,3))
plot(freq, d2bit(:,3))
plot(freq, d3bit(:,3))
axis([min(freq) max(freq) -30 max(d1bit(:,3)) + 5])
grid on
legend(["IRS off", "1 bit", "2 bit", "3 bit"])
title("Relative received power")
ylabel("Baseband power (dBFS)")
xlabel("Frequency (GHz)")

figure(3)
clf
hold on
%plot(freq, nors(:,3) - nors(:,3), 'r-.')
plot(freq, (d1bit(:,3) - ref(:,3)), 'b--')
plot(freq, (d2bit(:,3) - ref(:,3)), 'r--')
plot(freq, (d3bit(:,3) - ref(:,3)), 'bl--')
plot(freq, d1bit(:,3) - non(:,3), 'b')
plot(freq, d2bit(:,3) - non(:,3), 'r')
plot(freq, d3bit(:,3) - non(:,3), 'bl')
axis([min(freq) max(freq) -20 35])
legend(["versus IRS off", "versus no IRS"])
title("Received power improvement")
ylabel("Received power improvement (dB)")
xlabel("Frequency (GHz)")
grid on

%figure(2)
%plot(freq, nors(:,3) - nors(ref(:,3)))
%grid on
%title("Normalised received power (no IRS)")
%ylabel("Baseband received power (dBFS)")
%xlabel("Frequency (GHz)")
