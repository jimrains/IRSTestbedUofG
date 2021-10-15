tx = comm.SDRuTransmitter(...
                    'Platform','X310', ...
                    'OutputDataType','double', ...
                    'MasterClockRate',200e6, ...
                    'DecimationFactor',400, ...
                    'Gain',35, ...
                    'CenterFrequency',3.9e9, ...
                    'SamplesPerFrame',4000)
%%                
sinewave = dsp.SineWave(1,30e3); %30kHz
sinewave.SampleRate = 200e6/100; 
sinewave.SamplesPerFrame = 4000; 
sinewave.OutputDataType = 'double'; 
sinewave.ComplexOutput = true;
data = step(sinewave);

%%
frameDuration = (sinewave.SamplesPerFrame)/(sinewave.SampleRate); 
time = 0;
timeScope = timescope('TimeSpanSource','Property','TimeSpan',4/30e3,...
                      'SampleRate',100e6/100);
spectrumScope = dsp.SpectrumAnalyzer('SampleRate',sinewave.SampleRate); 
disp("Transmission Started"); 
timeScope(data); 
spectrumScope(data);

%%
while time<30
    tx(data); 
    time = time+frameDuration; 
end 
disp("Transmission Stopped"); 
release(tx);
% i = 0;
%  frameduration = (tx.SamplesPerFrame)/(200e6/100);
% while i<1000
%     tx(sin(i));
%     i = i+0.01;
% end