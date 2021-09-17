import socket
import select
import sys
import time
import random
import numpy as np
# Sampling from GRC:
import zmq
import threading

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


############################################################################
################## GET RX POWER FROM GNURADIO ##############################
############################################################################

sample = 0
PWR = 0
best_PWR = 0
class Thread(threading.Thread):
	def __init__(self, t, *args):
		threading.Thread.__init__(self, target=t, args=args)
		self.start()

lock = threading.Lock()

def powerGrab():
    global sample
    global PWR
    global best_PWR
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5556") # connect, not bind, the PUB will bind, only 1 can bind
    socket.setsockopt(zmq.SUBSCRIBE, b'') # subscribe to topic of all (needed or else it won't work)
    msg = socket.recv() # grab the message
    data = np.frombuffer(msg, dtype=np.float32, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
    while True:
        if socket.poll(4000) != 0:
            msg = socket.recv() # grab the message
            data = np.frombuffer(msg, dtype=np.float32, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
        with lock:
            if sample == 1:
			#PWR = np.mean(data[0:10])
                PWR = data[0]
                #print("Data length: ", len(data))
                sample = 0

t1 = Thread(powerGrab)

############################################################################
############################################################################
############################################################################

def main():
    # Globals for RX power probing
    global sample
    global PWR
    global best_PWR

    # Permutations and respective power measurements
    PERMS = [['0','0','0'],['0','0','1'],['0','1','0'],['0','1','1'],['1','0','0'],['1','0','1'],['1','1','0'],['1','1','1']]
    POWERS = [0,0,0,0,0,0,0,0]
    s = socketSetup()
    #t1 = Thread(powerGrab)
    # Initial ACK
    waitForAck(s)

    y = ["0","0","0"]*192
    sendConfig(y, s)
    waitForAck(s)
    time.sleep(0.05)
    # if waitForAck(s) == 1:
    #     printf("No ACK!")

# Take power reading
    with lock:
        sample = 1
    while sample == 1:
        time.sleep(0.0000001)
    time.sleep(0.03)
    POWERS[7] = PWR
    print("Initial power reading:", POWERS[7])
    count = 0
    test_sample = 0
    sleeptime = 0.5
    while 1:
        for nn in range(0,576,3):
            for k in range(0,8):
                y[nn:nn+3] = PERMS[k]
                print(PERMS[k])
                sendConfig(y, s)
                if waitForAck(s) == 1:
                    print("Socket fail")
                    sys.exit()
                time.sleep(sleeptime)
                with lock:
                    sample = 1
                while sample == 1:
                    time.sleep(0.0000001)
                POWERS[k] = PWR
                if POWERS[k] > best_PWR:
                    best_PWR = POWERS[k]
                    print("Power: "+str(POWERS[k])+" : "+str(10*np.log10(POWERS[k]))+" dB")
            y[nn:nn+3] = PERMS[POWERS.index(max(POWERS))]
            print(POWERS)
            print("Selected:", PERMS[POWERS.index(max(POWERS))])
            # while test_sample < max(POWERS)*0.85:
            #     print("Jumping over the glitch...")
            #     y[nn:nn+3] = PERMS[POWERS.index(max(POWERS))]
            #     with lock:
            #         sample = 1
            #     while sample == 1:
            #         time.sleep(0.0000001)
            #     test_sample = PWR



if __name__ == "__main__":
    main()
