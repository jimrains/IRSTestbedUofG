rx = comm.SDRuReceiver(...
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
frameduration = (rx.SamplesPerFrame)/(200e6/100); 
while time < 1000
 [ofdm_sig,len] = step(rx); 
 %timeScope([real(NormalizedData),imag(NormalizedData)]); 
    for i=1:64    
        rxed_sig(i)=ofdm_sig(i+16);    
    end

%%
% FFT
    ff_sig=fft(rxed_sig,64);

%%
% Pilot Synch%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i=1:52    
        synched_sig1(i)=ff_sig(i+6);    
    end
    k=1;
    for i=(1:13:52)        
        for j=(i+1:i+12)
            synched_sig(k)=synched_sig1(j);
            k=k+1;
        end
    end
% scatterplot(synched_sig)
%%
% Demodulation
    dem_data= qamdemod(synched_sig,16);
%% 
% Decimal to binary conversion
    bin=de2bi(dem_data','left-msb');
    bin=bin';

%%
% De-Interleaving
    deintlvddata = matdeintrlv(bin,2,2); % De-Interleave
    deintlvddata=deintlvddata';
    deintlvddata=deintlvddata(:)';

%%
%Decoding data
    n=6;
    k=3;
    decodedata =vitdec(deintlvddata,trellis,5,'trunc','hard');  % decoding datausing veterbi decoder
    rxed_data=decodedata;
 spectrumScope(rxed_data); 
 time = time + frameduration; 
%%
% Calculating BER
%     rxed_data=rxed_data(:)';
%     errors=0;
%     c=xor(data,rxed_data);
%     errors=nnz(c); %return the number of non-zero elements
%     BER(d,1)=errors/length(data);
end % main data loop

%%
% Time averaging for optimum results
% ber=0;  
% for row=1:time    
%         ber=ber+BER(row,1);
% end
% ber=ber./100; 