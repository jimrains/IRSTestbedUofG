%% IRS phase shift model

h = 0.005
mu = 4*pi*10^-7



L1 = mu*h
L2 = 1e-9
Cn = 0.5e-12
%f = 2e9:0.1e9:5e9
f = linspace(1e9, 10e9, 91);
W = 2*pi*f;
Rn = 0;

%caps = [0.1 0.18 0.22 0.25 0.3 0.35 0.4 0.5]*1e-12 - 0.02e-12

%caps = [0.6929    0.3763    0.2995    0.2515    0.2035    0.1556    0.0596    0.0500]*1e-12
%caps = cp

figure(5)
clf
hold on
figure(6)
clf
hold on

caps = load('capsfor3p9')
caps = caps.cp
NBIT = 3
for nq = 1:NBIT
    Cn = caps(nq)
    Zn = (j*(eta/sqrt(er)).*tan(sqrt(er)*h.*W/c).*(j*W*L2 + 1./(j*W*Cn) + Rn))./(j*(eta/sqrt(er)).*tan(sqrt(er)*h.*W/c) + (j*W*L2 + 1./(j*W*Cn) + Rn));
    %Zn = (j*W.*L1.*(j*W*L2 + 1./(j*W*Cn) + Rn))./(j*W.*L1 + (j*W*L2 + 1./(j*W*Cn) + Rn));
    gamma(nq,:) = (Zn - 120*pi)./(Zn + 120*pi)
    curves(nq,:) = angle(gamma(nq,:))
    mags(nq,:) = abs(gamma(nq,:))
end
%     figure(6)
%     plot(f, 180/pi*unwrap(curves(nq,:)))
%     figure(5)
%     plot(f, mags(nq,:))
%end

figure(2)
plot(f, unwrap(curves.'))
figure(3)
plot(f, mags)
