import socket
import select
import sys
import time
import random

host = '192.168.4.1'
port = 8080
verbose = 0

def socketSetup():
    print('Creating socket...')
    # SOCK_STREAM is TCP
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
      print('failed.')
      sys.exit()

    print('Getting remote IP address')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved')
        sys.exit()

    # Test to remove stalling

    print('Connecting to server ' + host + ' (' + str(port) + ')')
    sock.connect((remote_ip, port))
    return sock

def waitForAck(sock):
    ready = select.select([sock], [], [], 1)
    if ready[0]:
        data = sock.recv(4096)
        if data.decode('utf-8') == 'a':
            return 0;
        else:
            return 1;

def sendConfig(config, sock):
    rstr = ''.join(str(int(e)) for e in config)
    R = rstr.encode()
    try:
        sock.send(R)
        if verbose == 1:
            print(rstr)
    except socket.error:
        print('failed.')
        sys.exit()

def rxPower():
    #print("Taking power sample")
    # with lock:
    #     sample = 1
    # while sample == 1:
    #     time.sleep(0.0000001)
    # RPOWER = PWR
    # return RPOWER
    return 0

def main():
    s = socketSetup()
    # Initial ACK
    waitForAck(s)

    y = ["1","1","1"]*192
    sendConfig(y, s)
    if waitForAck(s) == 1:
        printf("No ACK!")
    # Take power reading
    Prx = rxPower()
    count = 0
    while 1:
        y = ["0"]*576
        # for i in range(576):
        #     y[i] = str(random.randint(0,1))
        # Calculate config
        sendConfig(y, s)
        #time.sleep(0.0000001)
        waitForAck(s)
        Prx = rxPower()
        count = count + 1
        if count%100 == 0:
            print(count)

        y = ["1","1","0"]*192
        sendConfig(y, s)
        #time.sleep(0.0000001)
        waitForAck(s)
        Prx = rxPower()
        count = count + 1
        if count%100 == 0:
            print(count)
        # Take power reading

if __name__ == "__main__":
    main()
