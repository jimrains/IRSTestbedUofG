############################################
##### added via insert_grc #################
############################################


# Enter loop to run alongside flowgraph here
# The example code takes a sample from a probe signal and prints the Rx power

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
    fp = open("phasedata3.dat", "w")
    fm = open("magdata3.dat", "w")
    avg_length = 10
    phase = [0]*8
    phase_samples = [0]*avg_length
    mag = [0]*8
    mag_samples = [0]*avg_length

    FLO = 3000
    FHI = 4500
    #RXpower = tb.analog_probe_avg_mag_sqrd_x_0.level()
    PERMS = [['0','0','0'],['0','0','1'],['0','1','0'],['0','1','1'],['1','0','0'],['1','0','1'],['1','1','0'],['1','1','1']]

    s = socketSetup()
    waitForAck(s)
    y = ['0','0','0']*192
    sendConfig(y, s)
    waitForAck(s)
    print("ACK received... please wait.")


    for k in range(FLO, FHI, 100):
        tb.set_freq(k*1000000)
        time.sleep(6)
        for m in range(0,8):
            y = PERMS[m]*192
            sendConfig(y, s)
            waitForAck(s)
            time.sleep(0.5)
            for j in range(0,avg_length):
                phase_samples[j] = tb.blocks_probe_signal_x_0.level()
                mag_samples[j] = tb.blocks_probe_signal_x_0_0.level()
                time.sleep(0.5)
            phase[m] = np.mean(phase_samples)
            mag[m] = np.mean(mag_samples)
        #phase = phase - phase[0]
        towrite = str(k) + ' ' + ' '.join(str(e) for e in phase) + '\n'
        print(towrite)
        fp.write(towrite)

        towrite = str(k) + ' ' + ' '.join(str(e) for e in mag) + '\n'
        print(towrite)
        fm.write(towrite)


uiThread = Thread(target=mainLoop, args=())
uiThread.start()



############################################
##### \ insert_grc #########################
############################################
