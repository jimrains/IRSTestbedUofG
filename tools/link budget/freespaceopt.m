%%%% Link budget model based on Wankai Tang work

lambda = 0.3/3.9 % 3.9 GHz

N = 48
M = 48

Pt = 0.1
Gt = 10
Gr = 10
dx = 22.5e-3
dy = 15e-3

npoints = 100;
PrdB = 0;
xmin = -50;
xmax = 50;
zmin = 0;
zmax = 50;
zs = linspace(zmin, zmax, npoints);
xs = linspace(xmin, xmax, npoints);

px = -20;
py = 0;
pz = 25.6;

txcoords = [-1.3 1.2 2.83];
rxcoords = [px py pz];

xt = txcoords(1);
yt = txcoords(2);
zt = txcoords(3);

xr = rxcoords(1);
yr = rxcoords(2);
zr = rxcoords(3);


%gam = ones(N,M);
sig = 0;
d1 = sqrt(xt^2 + yt^2 + zt^2);
d2 = sqrt(xr^2 + yr^2 + zr^2);

NBIT = 3;
phi = [0 5.9 46.2 87.1 145.1 181.4 223.9 282.2];
%phi = [0 181.4]
% Iterate over columns
COLL = 12

for p = 1:M
    % Iterate over rows
    for q = 1:N/COLL
        for k = 1:(2^NBIT)
            gam(((q-1)*COLL + 1):q*COLL, p) = exp(-j*pi/180*phi(k));
            %% Find power for gamma combination
            sig = 0;
            for m = 1:M
                for n = 1:N
                    %gam(n,m) = exp(-j*pi/180*phi(mod(m, 16) + 1));
                    %gam(n,m) = 1;
                    %x element positions - m represents column
                    xnm = dx*m + dx/2 - M*dx/2;
                    %y element positions - n represents row
                    ynm = dy*n + dy/2 - N*dy/2;
                    
                    Rtx = sqrt( (xt - xnm)^2 + (yt - ynm)^2 + zt^2 );
                    Rrx = sqrt( (xr - xnm)^2 + (yr - ynm)^2 + zr^2 );
                    
                    dnm = sqrt(xnm^2 + ynm^2);
                    
                    Ftx = ( ( d1^2 + Rtx^2 - dnm^2 )/(2*d1*Rtx) )^(Gt/2 - 1);
                    Frx = ( ( d2^2 + Rrx^2 - dnm^2 )/(2*d2*Rrx) )^(Gr/2 - 1);
                    Fuct = (zt/Rtx);
                    Fucr = (zr/Rrx);
                    Fcombine = Ftx*Fuct*Fucr*Frx;
                    sig = sig + sqrt(Fcombine)*gam(n,m)*exp(-j*(2*pi/lambda*(Rtx + Rrx)))/(Rtx*Rrx);
                end
            end
            
            Pr(k) = (Pt*Gt*Gr*dx*dy*lambda^2)/(64*pi^3)*abs(sig)^2;
            
        end
        [val, ind] = max(Pr);
        gam(((q-1)*COLL+1):q*COLL, p) = exp(-j*pi/180*phi(ind));
        
    end
end

PrdB = 10*log10(Pr);
PROPT = 10*log10(Pr);

%figure(1)
%clf
%surf(zs, xs, PrdB)
%shading interp
%view(2)
%axis([-100 100 0 200])
%caxis([-100 -70])
%xlabel("Z distance from surface", 'FontSize', 14)
%ylabel("X distance from surface", 'FontSize', 14)
%colorbar
%hold on
%plot(txcoords(3), txcoords(1), 'wx', 'MarkerSize', 20, 'LineWidth', 5)

figure(1)
imagesc(angle(gam))
pbaspect([108 72 1])


% npoints = 100;
PrdB = zeros(npoints,npoints);
% xmin = -500;
% xmax = 500;
% zmin = 0;
% zmax = 1000;
% zs = linspace(zmin, zmax, npoints);
% xs = linspace(xmin, xmax, npoints);

%gam = ones(48, 48)

for zind = 1:npoints
    for xind = 1:npoints
        z = zs(zind);
        x = xs(xind);
        
%        txcoords = [90 0 50];
        rxcoords = [x 0 z];    

        xt = txcoords(1);
        yt = txcoords(2);
        zt = txcoords(3);

        xr = rxcoords(1);
        yr = rxcoords(2);
        zr = rxcoords(3);

        sig = 0;
        d1 = sqrt(xt^2 + yt^2 + zt^2);
        d2 = sqrt(xr^2 + yr^2 + zr^2);

        for m = 1:M
            for n = 1:N                
                % x element positions - m represents column
                xnm = dx*m + dx/2 - M*dx/2;
                % y element positions - n represents row
                ynm = dy*n + dy/2 - N*dy/2;

                Rtx = sqrt( (xt - xnm)^2 + (yt - ynm)^2 + zt^2 );
                Rrx = sqrt( (xr - xnm)^2 + (yr - ynm)^2 + zr^2 );

                dnm = sqrt(xnm^2 + ynm^2);

                Ftx = ( ( d1^2 + Rtx^2 - dnm^2 )/(2*d1*Rtx) )^(Gt/2 - 1);
                Frx = ( ( d2^2 + Rrx^2 - dnm^2 )/(2*d2*Rrx) )^(Gr/2 - 1);
                Fuct = (zt/Rtx);
                Fucr = (zr/Rrx);
                Fcombine = Ftx*Fuct*Fucr*Frx;
                sig = sig + sqrt(Fcombine)*gam(n,m)*exp(-j*(2*pi/lambda*(Rtx + Rrx)))/(Rtx*Rrx);
            end
        end
        Pr = ((Pt*Gt*Gr*dx*dy*lambda^2)/(64*pi^3))*abs(sig)^2;
        PrdB(xind, zind) = 10*log10(Pr);
    end
end


figure(2)
clf
surf(zs, xs, PrdB)
shading interp
view(2)

xlabel("Z distance from surface", 'FontSize', 14)
ylabel("X distance from surface", 'FontSize', 14)
colorbar
%caxis([-100 -80])
hold on
plot(txcoords(3), txcoords(1), 'wx', 'MarkerSize', 20, 'LineWidth', 5)
%plot(pz, px, 'yx', 'MarkerSize', 20, 'LineWidth', 5)

figure(3)
plot(zs, PrdB(51,:))
