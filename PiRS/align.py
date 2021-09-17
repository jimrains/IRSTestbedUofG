import socket
import select
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt

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



# -25.6
c1 = "001000010010110011010110010100001001100010111011011101010100001011101010110101111011110000100000011111001010010011110100010101010010001101010010010000011100111101001011111111100001111011010110100110111001011001001111001110111110101000101101101000000110000111110101000000110100010101010110100100100000010111110001001010101110110110001000110010100010110010001011000001000111100011000111101100111001100011111010101100011101100111101001010110100010010111100111110101111000100011100100101010001100111010100001011110001101101111111011001000001101000111001001110111000110110101010110"

# -30.4
c2 = "100110000100101111100000001000000000100101010101100110001000100111001110010101000001001110001100100100110111101100101100101111000100101100011101110011100001111000111111011100110011000011000110011110000111101010100101000111011111000010110011010000010011100110010110100110010100011010110000000110000100001000001110110110000100101010110000010010000101110111101001111100001110001010011111010111001010100000101101011011000011101010010010110101000110110101101100001101111101111011101010011101000100010010011000010011111101101011110011010101011100100110110111010110000000010111010100"

# -35
c3 = "010001101001000111100111010011100001010100111001100110100000110111001100010011100110100010011001110010110100110100001010101010101011011000001111010000000001010001010010101000101100000111001010110101101100011001101000111100110100110000101111100101011000001110001001000100010101110011100101111010010101111001010111111101111010001110000000011110010010101110100010100011100001011111011000000010011101000101001100110101001110111011110011101101101000010110010111110010001000000001010111000110011110101111000111110110100100100100011101011010010010101000101011101100110001001111110111"

# -45
c4 = "000100011110010101111010001011100110001001010000000110111011101011100000010010100010110101110010011011011111001010010010110000101101000000010100010100001001111101010000110100110100010000100101101011101001010100101010110101000110101111011000010001100001010110000101001010101110001100000000011000110000010111000111110111101101001010011011111100110101110100101101111001111001110000110011000010111110101011101011010110000000110110110110110001000111001100101010011100101101111001011011000011101010010011000100110010001000001010011001001000000011101111011101001010011001100000110010"


# configs
confs = [c1,c2,c3,c4,c4,c3,c2,c1]
amps = [-25.6, -30.4, -35, -45, -45, -35, -30.4, -25.6]





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
    while True:
        if socket.poll(10) != 0:
            msg = socket.recv() # grab the message
            data = np.frombuffer(msg, dtype=np.float32, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
            with lock:
                if sample == 1:
			#PWR = np.mean(data[0:10])
                #PWR = np.mean(data[10:100])
                #msg = socket.recv() # grab the message
                #data = np.frombuffer(msg, dtype=np.float32, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
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
    x = [0,0,0,0,0,0,0,0]
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
    POWER_INIT = PWR
    print("Initial power reading:", POWER_INIT)
    count = 0
    test_sample = 0
    #while 1:
    sleeptime = 0.2
    fff = open("errors.txt", "w")
    for mm in range(0,100):
        # y = ["0"]*576
        # # for i in range(576):
        # #     y[i] = str(random.randint(0,1))
        # # Calculate config
        # sendConfig(y, s)
        # waitForAck(s)
        # Prx = rxPower()
        # count = count + 1
        # if count%100 == 0:
        #     print(count)
        #
        # y = ["1","1","0"]*192
        # sendConfig(y, s)
        # waitForAck(s)
        # Prx = rxPower()
        # count = count + 1
        # if count%100 == 0:
        #     print(count)
        # # Take power reading

        for g in range(0,8):
            strg = confs[g]
            y = list(strg)
            sendConfig(y, s)
            if waitForAck(s) == 1:
                print("Socket fail")
                sys.exit()
            time.sleep(sleeptime)
            with lock:
                sample = 1
            while sample == 1:
                time.sleep(0.0000001)
            POWERS[g] = 10*np.log10(PWR) + 30
            x[g] = abs(POWERS[g])
        print(amps)
        print(POWERS)
        plt.plot(np.array(x))
        #plt.show()
        plt.pause(0.00001)
        for i in range(0,8):
            errors = [abs(amps[i] - POWERS[i])]
        print(np.mean(errors))
        fff.write(str(np.mean(errors))+"\n")
        # for nn in range(0,576,3):
        #     k = 0
        #     while k < 8:
        #         y[nn:nn+3] = PERMS[k]
        #         sendConfig(y, s)
        #         if waitForAck(s) == 1:
        #             print("Socket fail")
        #             sys.exit()
        #         time.sleep(0.05)
        #         with lock:
        #             sample = 1
        #         while sample == 1:
        #             time.sleep(0.0000001)
        #         POWERS[k] = PWR
        #         #diff = 10*np.log10(POWERS[k]) - 10*np.log10(POWERS[k-1])
        #         # if abs(diff) < 3:
        #         if POWERS[k] > best_PWR:
        #             best_PWR = POWERS[k]
        #             print("Power: "+str(POWERS[k])+" : "+str(10*np.log10(POWERS[k]))+" dB")
        #         # #diff = 10*np.log10(POWERS[k]) - 10*np.log10(POWERS[k-1])
        #         k = k + 1
        #         #if abs(diff) > 3:
        #         #    print(diff)
        #         #    k = k - 1
        #         # if POWERS[k] > 3*prev_PWR: # if glitch occurs, try again
        #         #     print("!Glitch!")
        #         #     k = k - 1
        #         # prev_PWR = POWERS[k]
        #     #print(POWERS)
        #     y[nn:nn+3] = PERMS[POWERS.index(max(POWERS))]
            # while test_sample < max(POWERS)*0.85:
            #     print("Jumping over the glitch...")
            #     y[nn:nn+3] = PERMS[POWERS.index(max(POWERS))]
            #     with lock:
            #         sample = 1
            #     while sample == 1:
            #         time.sleep(0.0000001)
            #     test_sample = PWR
    fff.close()


if __name__ == "__main__":
    main()
