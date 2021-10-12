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
        elif data.decode('utf-8') == 'b':
            print("received a fail")
            return 1
        else:
            print("received other")
            return 1
    print("Not yet ready")
    return 1

def sendConfig(config, sock):
    rstr = ''.join(str(int(e)) for e in config)
    R = rstr.encode()
    try:
        sock.send(R)
    except socket.error:
        print('failed.')
        sys.exit()


def mainLoop():
    fp = open("phasedatalime.dat", "w")
    fm = open("magdatalime.dat", "w")
    avg_length = 10
    phase = [0]*8
    phase_samples = [0]*avg_length
    mag = [0]*8
    mag_samples = [0]*avg_length

    #phase_array = [phase_samples]*int((FHI - FLO)/STEP)

    # FSTEP = 1
    # FLO = 3470
    # FHI = 3500 + FSTEP
    FSTEP = 20
    FLO = 3250
    FHI = 3750 + FSTEP

    #RXpower = tb.analog_probe_avg_mag_sqrd_x_0.level()
    #PERMS = [['0','0','0'],['0','0','1'],['0','1','0'],['0','1','1'],['1','0','0'],['1','0','1'],['1','1','0'],['1','1','1']]
    # Trying gray code for reducing transients
    PERMS = [['0','0','0'],['0','0','1'],['0','1','1'],['0','1','0'],['1','1','0'],['1','1','1'],['1','0','1'],['1','0','0']]

    s = socketSetup()
    waitForAck(s)
    y = ['0','0','0']*192
    sendConfig(y, s)
    waitForAck(s)
    print("ACK received... please wait.")


    for k in range(FLO, FHI, FSTEP):

        tb.set_freq(k*1000000)
        time.sleep(3)
        y = PERMS[0]*192
        sendConfig(y, s)
        waitForAck(s)
        #time.sleep(0.5)
        delay = 0
        tb.set_caldelay(delay)
        print(delay)
        time.sleep(0.05)
        # Get initial phase 000 state
        cal_phase = tb.blocks_probe_signal_x_0.level()
        # Loop until phase shift in line with reference at 0 degrees
        while abs(cal_phase) > 2:
            cal_phase = tb.blocks_probe_signal_x_0.level()
            if cal_phase < -10:
                delay = delay + int(abs(cal_phase))
            else:
                delay = delay + 1
            tb.set_caldelay(delay)
            #print(delay)
            time.sleep(0.1)

        print(" :: Calibration complete for", k, " MHz")
        print(" :: Delay: ", delay)
        # Loop over remaining PIN diode states
        for m in range(0,8):
            print(PERMS[m])
            y = PERMS[m]*192
            sendConfig(y, s)
            while waitForAck(s) == 1:
                time.sleep(0.1)
                print("Waiting for ack...")
                sendConfig(y, s)
            time.sleep(1)
            for l in range(0, avg_length):
                phase_samples[l] = tb.blocks_probe_signal_x_0.level()
                time.sleep(0.1)
            if m != 0:
                while abs(max(phase_samples) - min(phase_samples)) > 6:
                    print("delta phi large")
                    for l in range(0, avg_length):
                        phase_samples[l] = tb.blocks_probe_signal_x_0.level()
                        time.sleep(0.1)

            phase[m] = np.mean(phase_samples)
            mag[m] = tb.blocks_probe_signal_x_0_0.level()

        towrite = str(k) + ' ' + ' '.join(str(e) for e in phase) + '\n'
        print(towrite)
        fp.write(towrite)

        towrite = str(k) + ' ' + ' '.join(str(e) for e in mag) + '\n'
        print(towrite)
        fm.write(towrite)
        print("Round complete")

uiThread = Thread(target=mainLoop, args=())
uiThread.start()



############################################
##### \ insert_grc #########################
############################################
