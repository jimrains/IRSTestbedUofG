############################################
############################################
############################################
############################################
############################################
############################################
############################################

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
    except socket.error:
        print('failed.')
        sys.exit()


def mainLoop():
    #RXpower = tb.analog_probe_avg_mag_sqrd_x_0.level()
    PERMS = [['0','0','0'],['0','0','1'],['0','1','0'],['0','1','1'],['1','0','0'],['1','0','1'],['1','1','0'],['1','1','1']]
    POWERS = [0,0,0,0,0,0,0,0]
    PDB = [0,0,0,0,0,0,0,0]
    time.sleep(3)

    s = socketSetup()
    waitForAck(s)
    y = ["0","0","0"]*192
    sendConfig(y, s)
    waitForAck(s)
    print("ACK received... please wait.")
    time.sleep(1)
    PWR = tb.blocks_probe_signal_x_0_0.level()
    best_PWR = PWR
    print(":: Starting power 1: ", 10*np.log10(PWR), " dB")
    time.sleep(1)
    PWR = tb.blocks_probe_signal_x_0_0.level()
    best_PWR = PWR
    print(":: Starting power 2: ", 10*np.log10(PWR), " dB")

    PDB[7] = 10*np.log10(PWR)
    #sleeptime = 0.015
    sleeptime = 0.005
    AL = 1
    power_samples = [0]*AL
    count = 0
    iterations = 5
    for u in range(1, iterations):
        for nn in range(0,576,3):
            if (count%100 == 0) or count == 8:
                print(count)
                print(":: Scaled power: ", 10*np.log10(max(POWERS)), " dB")
                print(''.join(str(int(e)) for e in y))
            k = 0
            while k < 8:
                count = count + 1
                y[nn:nn+3] = PERMS[k]
                sendConfig(y, s)
                while waitForAck(s) == 1:
                    print("Socket fail")
                time.sleep(sleeptime)
                PWR = tb.blocks_probe_signal_x_0_0.level()
                POWERS[k] = PWR
                k = k + 1
            y[nn:nn+3] = PERMS[POWERS.index(max(POWERS))]
    #input('Any key to exit')
    # except KeyboardInterrupt:
    s.close()
    print("Socket closed. Exiting.")
    input('Any key to stop')

uiThread = Thread(target=mainLoop, args=())
uiThread.start()
############################################
############################################
############################################
############################################
############################################
