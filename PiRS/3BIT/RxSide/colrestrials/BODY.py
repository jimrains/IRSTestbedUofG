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

def write_config_data(frequency, start_power, end_power, config, filename):
    datout = str(frequency) + " " + str(start_power) + " " + str(end_power)
    datout = datout + " " + ''.join(str(int(e)) for e in config)
    f = open(filename, "w")
    f.write(datout + "\n")

def generate_filename(frequency, function, position):
    DT = datetime.datetime.now()
    fn1 = str(DT.year) + str(DT.month) + str(DT.day)
    fn2 = "_" + str(DT.hour) + str(DT.minute) + str(DT.second)
    fn3 = "_" + function + "_" + position + "_"
    fn4 = str(frequency) + ".dat"
    return fn1+fn2+fn3+fn4

def mainLoop():
    #RXpower = tb.analog_probe_avg_mag_sqrd_x_0.level()
    #PERMS = [['0','0','0'],['0','0','1'],['0','1','0'],['0','1','1'],['1','0','0'],['1','0','1'],['1','1','0'],['1','1','1']]
    numbits = int(sys.argv[3])
    print(" :: Number of bits: ", numbits)
    if numbits == 1:
        PERMS = [['1','0','0'],['1','1','0']]
        NBITS = 1
    elif numbits == 2:
        PERMS = [['0','0','0'],['0','0','1'],['0','1','1'],['1','0','1']]
        NBITS = 2
    elif numbits == 3:
        PERMS = [['0','0','0'],['0','0','1'],['0','1','0'],['0','1','1'],['1','0','0'],['1','0','1'],['1','1','0'],['1','1','1']]
        NBITS = 3
    else:
        exit()
    POWERS = [0,0,0,0,0,0,0,0]
    #PDB = [0,0,0,0,0,0,0,0]
    time.sleep(3)


    cur_freq = int(sys.argv[1])
    position = sys.argv[2]

    position = position.upper()
    tb.set_freq(cur_freq*1000000)
    #rpcs = client.Server('http://192.168.4.3:8080')
    #rpcs.set_txfreq(cur_freq)
    DT = datetime.datetime.now()
    dir_name = str(DT.year) + str(DT.month) + str(DT.day) + "/"
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        print(" :: Directory exists - skipping ")

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

    start_power = PWR

    #PDB[7] = 10*np.log10(PWR)
    #sleeptime = 0.015
    sleeptime = 0.005
    AL = 1
    power_samples = [0]*AL
    count = 0
    iterations = 10
    for u in range(1, iterations):
        for nn in range(0,144,3):
            if (count%100 == 0) or count == 8:
                print(count)
                print(":: Scaled power: ", 10*np.log10(max(POWERS)), " dB")
                print(''.join(str(int(e)) for e in y))
            k = 0
            while k < 2**NBITS:
                count = count + 1
                y[nn:nn+3] = PERMS[k]
                y[(nn+143):(nn+3+143)] = PERMS[k]
                y[(nn+143*2):(nn+3+143*2)] = PERMS[k]
                y[(nn+143*3):(nn+3+143*3)] = PERMS[k]
                sendConfig(y, s)
                while waitForAck(s) == 1:
                    print("Socket fail")
                time.sleep(sleeptime)
                PWR = tb.blocks_probe_signal_x_0_0.level()
                POWERS[k] = PWR
                k = k + 1
            y[nn:nn+3] = PERMS[POWERS.index(max(POWERS))]
            y[(nn+143):(nn+3+143)] = PERMS[POWERS.index(max(POWERS))]
            y[(nn+143*2):(nn+3+143*2)] = PERMS[POWERS.index(max(POWERS))]
            y[(nn+143*3):(nn+3+143*3)] = PERMS[POWERS.index(max(POWERS))]


    config_filename = dir_name + generate_filename(cur_freq, "OPT", position)
    print(" :: Writing to: ", config_filename)
    write_config_data(cur_freq, 10*np.log10(start_power), 10*np.log10(max(POWERS)), y, config_filename)
    #input('Any key to exit')
    # except KeyboardInterrupt:
    s.close()
    print("Socket closed. Exiting.")
    os.system('play -nq -t alsa synth {} sine {}'.format(1, 400))
    input('Any key to stop')

uiThread = Thread(target=mainLoop, args=())
uiThread.start()
############################################
############################################
############################################
############################################
############################################
