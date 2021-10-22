%%%% Link budget model based on Wankai Tang work




%% Generate reflection profile

%caps = load('capsfor3p9')
caps = load('capsfor3p0_2bit')
caps = caps.cp

er = 2.2;
h = 0.003;
Rn = 1;
c = 0.3e9;
L2 = 0.5e-9;
f = linspace(1e9, 5e9, 41);
W = 2*pi*f;
eta = 120*pi;

NBIT = log2(length(caps));
for nq = 1:2^NBIT
    Cn = caps(nq)
    Zn = (j*(eta/sqrt(er)).*tan(sqrt(er)*h.*W/c).*(j*W*L2 + 1./(j*W*Cn) + Rn))./(j*(eta/sqrt(er)).*tan(sqrt(er)*h.*W/c) + (j*W*L2 + 1./(j*W*Cn) + Rn));
    %Zn = (j*W.*L1.*(j*W*L2 + 1./(j*W*Cn) + Rn))./(j*W.*L1 + (j*W*L2 + 1./(j*W*Cn) + Rn));
    gamma(nq,:) = (Zn - 120*pi)./(Zn + 120*pi);
    curves(nq,:) = angle(gamma(nq,:));
    mags(nq,:) = abs(gamma(nq,:));
end

gammas = gamma;

%lambda = 0.3/3.9 % 3.9 GHz

N = 48
M = 48

Pt = 0.1
Gt = 10
Gr = 10
dx = 22.5e-3
dy = 15e-3

npoints = 50;
%PrdB = 0;
xmin = -40;
xmax = 40;
zmin = 0;
zmax = 40;
zs = linspace(zmin, zmax, npoints);
xs = linspace(xmin, xmax, npoints);

px = -30;
py = 0;
pz = 20;

gam = ones(N,M);
sig = 0;
sig_ref = 0;
%gammas = load('gamma_opt3p9_wide')

% Iterate over columns
COLL = 1
g1 = [1.00,0.60,0.20];
g2 = [0.10,1.00,0.25];
g3 = [0.6, 0.6, 1];
g4 = [0.08, 0.5, 0];
freqs = f;
fstep = 1;
for a = 1:fstep:length(freqs)
    frind = a
    
    lambda = 0.3e9/freqs(a);

    figure(1)
    h4 = subplot(2,3,1);
    cla(h4);
    phasecurves = 180/pi*unwrap(curves.');
    plot(freqs/1e9, phasecurves(:,1), 'LineWidth', 2, 'Color', g1)
    hold on
    plot(freqs/1e9, phasecurves(:,2), 'LineWidth', 2, 'Color', g2)
    plot(freqs/1e9, phasecurves(:,3), 'LineWidth', 2, 'Color', g3)
    plot(freqs/1e9, phasecurves(:,4), 'LineWidth', 2, 'Color', g4)
    
    axis([1 5 -180 190])
    xline(freqs(a)/1e9, 'bl-.', 'LineWidth', 2)
    
    phi1 = phasecurves(frind,1);
    phi2 = phasecurves(frind,2);
    phi3 = phasecurves(frind,3);
    phi4 = phasecurves(frind,4);
    text(4, 160,strcat("{\phi}_{00}: ", num2str(round(phi1))),'HorizontalAlignment','left', 'FontSize', 13)
    text(4, 130,strcat("{\phi}_{01}: ", num2str(round(phi2))),'HorizontalAlignment','left', 'FontSize', 13)
    text(4, 100,strcat("{\phi}_{10}: ", num2str(round(phi3))),'HorizontalAlignment','left', 'FontSize', 13)
    text(4, 70,strcat("{\phi}_{11}: ", num2str(round(phi4))),'HorizontalAlignment','left', 'FontSize', 13)
    
    pbaspect([108 72 1])
    title("Unit cell reflection phase versus frequency")
    xlabel("Frequency (GHz)", 'FontSize', 14)
    ylabel("Phase (degrees)", 'FontSize', 14)
    yticks([-180:45:180])
    
    h1 = subplot(2,3,4)
    cla(h1)
    magcurves = mags.';        
       
    plot(freqs/1e9, magcurves(:,1), 'LineWidth', 2, 'Color', g1)   
    hold on
    plot(freqs/1e9, magcurves(:,2), 'LineWidth', 2, 'Color', g2)
    plot(freqs/1e9, magcurves(:,3), 'LineWidth', 2, 'Color', g3)   
    plot(freqs/1e9, magcurves(:,4), 'LineWidth', 2, 'Color', g4)
    
    xline(freqs(a)/1e9, 'bl-.', 'LineWidth', 2)
    
    mag1 = magcurves(frind,1);
    mag2 = magcurves(frind,2);
    mag3 = magcurves(frind,3);
    mag4 = magcurves(frind,4);
    text(4, 0.7,strcat("{|\Gamma|}_{00}: ", num2str( round((mag1),2) ) ),'HorizontalAlignment','left', 'FontSize', 13)
    text(4, 0.65,strcat("{|\Gamma|}_{01}: ", num2str(round((mag2),2) ) ),'HorizontalAlignment','left', 'FontSize', 13)
    text(4, 0.6,strcat("{|\Gamma|}_{10}: ", num2str(round((mag3),2)) ),'HorizontalAlignment','left', 'FontSize', 13)
    text(4, 0.55,strcat("{|\Gamma|}_{11}: ", num2str(round((mag4),2)) ),'HorizontalAlignment','left', 'FontSize', 13)
    
    axis([1 5 0.5 1])
    pbaspect([108 72 1])
    title("Unit cell reflection magnitude versus frequency")
    xlabel("Frequency (GHz)", 'FontSize', 14)
    ylabel("Magnitude (linear)", 'FontSize', 14)
    
    gam = ones(N,M);
    sig = 0;
    sig_ref = 0;
    
    txcoords = [-5 0 30];
    rxcoords = [px py pz];

    xt = txcoords(1);
    yt = txcoords(2);
    zt = txcoords(3);
    xr = rxcoords(1);
    yr = rxcoords(2);
    zr = rxcoords(3);
    d1 = sqrt(xt^2 + yt^2 + zt^2);
    d2 = sqrt(xr^2 + yr^2 + zr^2);

    for p = 1:M
        % Iterate over rows
        for q = 1:N/COLL
            for k = 1:(2^NBIT)    
                %% 48 relates to index of 3.9 GHz
                %gam(((q-1)*COLL + 1):q*COLL, p) = gammas.gamma(k,frind);
                gam(((q-1)*COLL + 1):q*COLL, p) = gammas(k,frind);
                %% Find power for gamma combination
                sig = 0;
                sig_ref = 0;
                for m = 1:M
                    for n = 1:N
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
            %gam(((q-1)*COLL+1):q*COLL, p) = gammas.gamma(ind,frind);
            gam(((q-1)*COLL+1):q*COLL, p) = gammas(ind,frind);
            statesmates(((q-1)*COLL+1):q*COLL, p) = ind;
        end
    end

    %% optimal gam has now been found
    
    
    PrdB = 10*log10(Pr);
    PROPT = 10*log10(Pr);

    figure(1)
    %clf
    h2 = subplot(2,3,2);
    %imagesc(angle(gam)*180/pi)
    imagesc(statesmates);
    C = [g1; g2; g3; g4];
    colormap(h2, C)
    colorbar('Ticks',[1,2,3,4],...
    'TickLabels',["00", "01", "10", "11"]);
    yticks([1:48]-0.5)
    xticks([1:48]-0.5)
    set(gca,'TickLength', [0 0])
    set(gca,'XTickLabel',[]);
    set(gca,'YTickLabel',[]);
    caxis([0.5  4.5])
    axis([0.5 48.5 0.5 48.5])
    %colorbar
    pbaspect([108 72 1])
    title("RIS configuration")

    %PrdB = zeros(npoints,npoints);
    %% Generate plot 
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
            sig_ref = 0;
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
                    sig_ref = sig_ref + sqrt(Fcombine)*(-1)*exp(-j*(2*pi/lambda*(Rtx + Rrx)))/(Rtx*Rrx);
                end
            end
            Pr = ((Pt*Gt*Gr*dx*dy*lambda^2)/(64*pi^3))*abs(sig)^2;
            Pr_ref = ((Pt*Gt*Gr*dx*dy*lambda^2)/(64*pi^3))*abs(sig_ref)^2;
            PrdB(xind, zind) = 10*log10(Pr);
            PrdB_ref(xind, zind) = 10*log10(Pr_ref);
        end
                
    end


    figure(1)
    subplot(2,3,[3,6])
    %clf
    surf(zs, xs, PrdB)
    shading interp
    view(2)
    xlabel("Z displacement (m)", 'FontSize', 14)
    ylabel("X displacement (m)", 'FontSize', 14)    
    colorbar
    caxis([-110 -60])
    hold on
    IRS_WIDTH = M*dx;
    IRS_WIDTH = 5;
    patch([0 0.5 0.5 0], [-IRS_WIDTH/2 -IRS_WIDTH/2 IRS_WIDTH/2 IRS_WIDTH/2], 'black')
    %patch([20 21 31 30], [-10 -10 -35 -35], 'gray')
    patch([20 20 40 40], [-9.5 -8 -18 -19.5], 'bl', 'FaceColor', 'white')
    plot(txcoords(3), txcoords(1), 'wx', 'MarkerSize', 20, 'LineWidth', 5)
    text(txcoords(3)-2, txcoords(1)+3, ['Tx: (', num2str(txcoords(1)), ', ' num2str(txcoords(2)), ', ' num2str(txcoords(3)), ')'])
    yline(px, 'y--', 'LineWidth', 2)
    plot(pz, px, 'yx', 'MarkerSize', 20, 'LineWidth', 5)
    text(pz-2,px+3, ['Rx: (', num2str(px), ', ' num2str(py), ', ' num2str(pz), ')'])
    title(strcat("Received power in XZ plane at f = ", num2str(freqs(a)/1e9), " GHz"))
    pbaspect([40 80 1])
    %plot(pz, px, 'yx', 'MarkerSize', 20, 'LineWidth', 5)
    subplot(2,3,5)
    %hold on
    displine = -30;
    [val, ldind] = min(abs(xs - displine));
    PrdB(ldind,1) = PrdB(ldind,2);
    PrdB_ref(ldind,1) = PrdB_ref(ldind,2);
    plot(zs(2:end), smooth(PrdB(ldind,2:end),5) - smooth(PrdB_ref(ldind,2:end), 5) )
    title({'Average received power improvement',' along x = -30 m versus metal plate'})
    axis([1 zmax -15 40])
    pbaspect([108 72 1])
    grid on
    xlabel('Z displacement (m)', 'FontSize', 14)
    ylabel('Received power improvement (dB)', 'FontSize', 14)
    print(['Frame' num2str(round(a/fstep) + 1)], '-dpng', '-r150');  
    powow(a) = max(PrdB(30,:));    
end

%figure(5)
%PWW_PLA = powow(1:fstep:100) + 20*log10(4*pi*(Rrx + Rtx)*freqs(1:fstep:100)/c)
%plot(PWW_PLA);

%% Generate animation

GifName = 'bandsweep_smoothscatter.gif';
delay = 1;
%for ii = 2:round(a/fstep)
for ii = 2:42
    [A,~] = imread(['Frame' num2str(ii) '.png']);
    [X, map] = rgb2ind(A, 256);
    if ii == 2
        imwrite(X, map, GifName, 'gif', 'LoopCount', inf, 'DelayTime', delay*3);
    else
        %if ii == round(a/fstep)
        if ii == 42 | ii == 22   
            imwrite(X, map, GifName, 'gif', 'WriteMode', 'append', 'DelayTime', delay*10);
        else
            imwrite(X, map, GifName, 'gif', 'WriteMode', 'append', 'DelayTime', delay);
        end
    end
end

