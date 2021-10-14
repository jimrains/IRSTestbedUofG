%%%%% Send IRS configuration over socket to Raspberry Pi (Pi) %%%%%%
%%% The host PC must be connected to the Pi WiFi access point 'piris'
%%% Default Pi IP address is 192.168.4.1
%%%
%%% Run server code (C++) on Pi side by opening a terminal and typing:
%%% # cd ~
%%% # ./irsserver
%%%
%%% Make sure that the IRS power supply and FPGA are powered up
%%% (Power supply can be verified by observing the LED on the bottom left of the power supply) 
%%%


%%%% Example usage:
%{
IP = "192.168.4.1"    % IP address of Raspberry Pi (default 192.168.4.1)
PORT = 8888         % Port of Raspberry Pi (default 8888)
sck = tcpclient(IP, PORT, "ConnectTimeout",5)  % Set up socket with Raspberry Pi
success = sendconf(repmat([0, 1, 1], 1, 192), sck) % Send (every unit cell 011) configuration via socket
success = sendconf(repmat([1, 0, 1], 1, 192), sck) % Send (every unit cell 101) configuration via socket
success = sendconf(repmat([0, 0, 1], 1, 192), sck)
success = sendconf(repmat([0, 0, 0], 1, 192), sck)
clear sck
%}

function sent = sendconf(bitarray, sock)
     sent = 0; % Set to 1 if the send operation is unsuccessful
     
% Convert to string format
    bitstream = sprintf('%i',bitarray);

% Send configuration over TCP
    write(sock, bitstream);

% Wait for ACK from Pi in the form of character 'a'
    rec = read(sock);
    while (length(rec) == 0)
        rec = read(sock);
    end
    if rec == 97
        fprintf(" :: Received ACK \n")
        sent = 1;
    end

end



   