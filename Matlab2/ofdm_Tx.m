close all
clear all
clc
%%
tx = comm.SDRuTransmitter(...
                    'Platform','X310', ...
                    'OutputDataType','double', ...
                    'MasterClockRate',200e6, ...
                    'DecimationFactor',400, ...
                    'Gain',35, ...
                    'CenterFrequency',3.9e9, ...
                    'SamplesPerFrame',4000)
                
spectrumScope = dsp.SpectrumAnalyzer('SampleRate',200e6/100); 
spectrumScope.ReducePlotRate = true;               

time = 0;
frameduration = (tx.SamplesPerFrame)/(200e6/100); 
%%
% Generating and coding data
% t_data= randi([0,1],9600,1)';
% x=1;
%%
while time<1000
%     data=t_data(x:x+95); %divide data into 100 pieces with each piece contains 96 numbers
%     x=x+96;
%     s1=size(data,2);  % Size of input matrix = 96
    data = randi([0,1],96,1)';
%%
% Convolutionally encoding data 
    constlen=7;
    codegen = [171 133];    % Polynomial
    trellis = poly2trellis(constlen, codegen);
    codedata = convenc(data, trellis); %1*192
    
%%
%Interleaving coded data
    s2=size(codedata,2); %192
    j=s2/4; 
    matrix=reshape(codedata,j,4);

    intlvddata = matintrlv(matrix',2,2)'; % Interleave.
    intlvddata=intlvddata'; %4*48

%%
% Binary to decimal conversion
    dec=bi2de(intlvddata','left-msb'); %48*1


%%
%16-QAM Modulation
    M=16;
    y = qammod(dec,M); 
%     scatterplot(y);

%%
% Pilot insertion
    lendata=length(y); %48
    pilt=3+3j;
    nofpits=4;
    k=1;

    for i=(1:13:52)    
        pilt_data1(i)=pilt;
        for j=(i+1:i+12)
            pilt_data1(j)=y(k);
            k=k+1;
        end
    end

    pilt_data1=pilt_data1';   % size of pilt_data =52
    pilt_data(1:52)=pilt_data1(1:52);    % upsizing to 64
    pilt_data(13:64)=pilt_data1(1:52);   % upsizing to 64
  
    for i=1:52
        pilt_data(i+6)=pilt_data1(i);
    end

%%
% IFFT
    ifft_sig=ifft(pilt_data',64); 

%%
% Adding Cyclic Extension
    cext_data=zeros(80,1);
    cext_data(1:16)=ifft_sig(49:64);
    for i=1:64    
        cext_data(i+16)=ifft_sig(i);   
    end
    tx(cext_data); 
    time = time+frameDuration; 
end % main data loop



